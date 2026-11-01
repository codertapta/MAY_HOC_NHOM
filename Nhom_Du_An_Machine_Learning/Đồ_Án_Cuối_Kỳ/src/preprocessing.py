"""3. Tiền xử lý dữ liệu – BRFSS2015 (diabetes.csv, nhãn nhị phân)"""
import pandas as pd, numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

TARGET = "Diabetes_binary"
RANDOM_STATE = 42

# Biến thứ tự (Age, Education, Income, GenHlth) giữ nguyên dạng số.
NUMERIC = ["BMI", "MentHlth", "PhysHlth", "Age", "Education", "Income", "GenHlth"]


class Winsorizer(BaseEstimator, TransformerMixin):
    """Cắt giá trị về [p1, p99]; ngưỡng chỉ học từ tập train (không rò rỉ)."""
    def __init__(self, lower=0.01, upper=0.99):
        self.lower, self.upper = lower, upper

    def fit(self, X, y=None):
        X = np.asarray(X, dtype=float)
        self.lo_ = np.quantile(X, self.lower, axis=0)
        self.hi_ = np.quantile(X, self.upper, axis=0)
        return self

    def transform(self, X):
        return np.clip(np.asarray(X, dtype=float), self.lo_, self.hi_)


def load_and_split(path="data/raw/diabetes.csv"):
    df = pd.read_csv(path)
    n0 = len(df)

    # 1) Bỏ dòng trùng TRƯỚC khi chia, để cùng một bản ghi không rơi vào cả train lẫn test.
    #    Dữ liệu chỉ gồm các biến rời rạc nên nhiều người khác nhau có thể trùng hồ sơ;
    #    giữ lại sẽ làm điểm test bị thổi phồng. Tác động in ở dưới.
    before = df[TARGET].value_counts(normalize=True).sort_index()
    df = df.drop_duplicates().reset_index(drop=True)
    after = df[TARGET].value_counts(normalize=True).sort_index()
    print(f"Bỏ {n0 - len(df)} dòng trùng ({(n0 - len(df)) / n0:.2%}): {n0} -> {len(df)}")
    print("Tỷ lệ lớp trước:", (before * 100).round(2).to_dict())
    print("Tỷ lệ lớp sau  :", (after * 100).round(2).to_dict())

    X, y = df.drop(columns=TARGET), df[TARGET].astype(int)
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE)


def build_preprocessor(X):
    """Winsorize BMI (p1–p99) rồi StandardScaler cho biến số; biến nhị phân giữ nguyên.

    BMI: cắt ngoại lệ vì có 281 mẫu >= 80 (khó xảy ra thực tế) và BMI lệch phải
    làm lệch hệ số của mô hình tuyến tính. MentHlth/PhysHlth không cắt vì giá trị 30
    là người bệnh thật.
    """
    binary = [c for c in X.columns if c not in NUMERIC]
    bmi = Pipeline([("win", Winsorizer()), ("scale", StandardScaler())])
    return ColumnTransformer(
        [("bmi", bmi, ["BMI"]),
         ("num", StandardScaler(), [c for c in NUMERIC if c != "BMI"]),
         ("bin", "passthrough", binary)]
    )


def make_pipeline(model, X):
    """Scaler nằm trong Pipeline nên chỉ được fit trên train (kể cả khi CV)."""
    return Pipeline([("prep", build_preprocessor(X)), ("model", model)])


if __name__ == "__main__":
    from sklearn.linear_model import LogisticRegression
    X_train, X_test, y_train, y_test = load_and_split()
    print("Train:", X_train.shape, "| Test:", X_test.shape)
    pipe = make_pipeline(LogisticRegression(max_iter=1000), X_train).fit(X_train, y_train)
    prep = pipe.named_steps["prep"]
    print("BMI cắt về [%.1f, %.1f]" % (prep.named_transformers_["bmi"]["win"].lo_[0],
                                       prep.named_transformers_["bmi"]["win"].hi_[0]))
    print("Chạy pipeline OK, accuracy test = %.3f" % pipe.score(X_test, y_test))
