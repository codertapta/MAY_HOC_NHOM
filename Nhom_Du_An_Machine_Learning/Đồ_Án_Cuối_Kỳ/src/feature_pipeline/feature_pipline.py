"""Reproducible CDC Diabetes Binary baseline and feature comparison."""

from pathlib import Path
import argparse
import json
import platform
from datetime import date

import numpy as np
import pandas as pd
import sklearn
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, f1_score
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "sources" / "diabetes.csv"
TARGET = "Diabetes_binary"
RANDOM_STATE = 42
TEST_SIZE = 0.20


class HealthFeatureEngineer(BaseEstimator, TransformerMixin):
    """Derive WHO BMI group, comorbidity count, healthy lifestyle score, and optional interaction."""

    def __init__(self, interaction=True):
        self.interaction = interaction

    def fit(self, X, y=None):
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        return self

    def transform(self, X):
        out = X.copy()
        bmi = out["BMI"]
        out["BMI_WHO_Group"] = pd.cut(
            bmi, [-np.inf, 18.5, 25, 30, np.inf], labels=False, right=False
        ).astype(float)
        morbidity = ["HighBP", "HighChol", "Stroke", "HeartDiseaseorAttack"]
        out["Comorbidity_Count"] = out[morbidity].sum(axis=1)
        habits = ["PhysActivity", "Fruits", "Veggies"]
        out["Healthy_Lifestyle_Score"] = out[habits].sum(axis=1)
        if self.interaction:
            out["Age_x_HighBP"] = out["Age"] * out["HighBP"]
        return out

    def get_feature_names_out(self, input_features=None):
        names = list(self.feature_names_in_) + [
            "BMI_WHO_Group",
            "Comorbidity_Count",
            "Healthy_Lifestyle_Score",
        ]
        if self.interaction:
            names.append("Age_x_HighBP")
        return np.asarray(names, dtype=object)


def make_pipeline(use_engineered=True):
    # Preserve dataframe column names so feature creation follows fold-local imputation.
    imputer = SimpleImputer(strategy="median").set_output(transform="pandas")
    return Pipeline(
        [
            ("imputer", imputer),
            (
                "feature_engineering",
                HealthFeatureEngineer() if use_engineered else "passthrough",
            ),
            ("scaler", StandardScaler()),
            (
                "model",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=500,
                    solver="liblinear",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )


def main(run_cv=False):
    df = pd.read_csv(DATA)
    if TARGET not in df:
        raise ValueError(f"Expected target column {TARGET}; found {list(df.columns)}")
    duplicates = int(df.duplicated().sum())
    # Keep duplicate rows: the requested split isolates copies in expectation imperfectly; grouped duplicate
    # splitting is intentionally avoided because it can materially alter the sampled population. Document this choice.
    X, y = df.drop(columns=TARGET), df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    summary = {
        "date": date.today().isoformat(),
        "runner": "src/feature_pipeline.py",
        "dataset": "sources/diabetes.csv",
        "rows": len(df),
        "features": X.shape[1],
        "target": TARGET,
        "class_counts": {
            str(k): int(v) for k, v in y.value_counts().sort_index().items()
        },
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows_retained": duplicates,
        "duplicate_fraction": duplicates / len(df),
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
        "cv": "StratifiedKFold(5, shuffle=True, random_state=42)",
        "model": "LogisticRegression(class_weight=balanced, solver=liblinear, max_iter=500)",
        "versions": {
            "python": platform.python_version(),
            "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "status": "CV pending" if not run_cv else "CV complete",
    }
    if run_cv:
        scoring = {
            "macro_f1": make_scorer(f1_score, average="macro"),
            "accuracy": "accuracy",
        }
        for engineered in (False, True):
            result = cross_validate(
                make_pipeline(engineered),
                X_train,
                y_train,
                cv=cv,
                scoring=scoring,
                n_jobs=-1,
                return_train_score=False,
            )
            summary["engineered" if engineered else "original"] = {
                "macro_f1_mean": float(result["test_macro_f1"].mean()),
                "macro_f1_std": float(result["test_macro_f1"].std()),
                "accuracy_mean": float(result["test_accuracy"].mean()),
            }
        summary["status"] = "CV complete; holdout test not evaluated"
    out = ROOT / "logs" / "experiment_log.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-cv",
        action="store_true",
        help="Run the shared 5-fold CV feature ablation on train only",
    )
    main(parser.parse_args().run_cv)
