"""
Tiền xử lý dữ liệu cho Challenge 2 (phân loại bài hát theo `Class`).

`MusicPreprocessor` tương thích scikit-learn (fit / transform) nên dùng được trực tiếp
trong `Pipeline` + cross-validation ở bước 05 mà KHÔNG bị rò rỉ dữ liệu:
mọi thống kê (median, ngưỡng cắt outlier, mean/std) chỉ học từ dữ liệu truyền vào `fit`.

Các bước (có thể gọi riêng từng bước để minh hoạ trong notebook):
    1. fix_duration   : chuẩn hoá cột duration (phút / mili-giây lẫn lộn) về phút
    2. impute         : tạo cờ missing + điền Popularity, instrumentalness (median), key (NaN -> 0 = "không rõ")
    3. clip_outliers  : winsorize các cột lệch/nhiều outlier theo phân vị học từ train
    4. encode         : one-hot key, time_signature; giữ mode; bỏ cột text/Id
    5. scale          : StandardScaler cho các cột liên tục
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler

ID, TARGET = "Id", "Class"
DUR = "duration_in min/ms"
TEXT_COLS = ["Artist Name", "Track Name"]

MINUTES_THRESHOLD = 1000          # duration < 1000  -> đơn vị phút ; >= 1000 -> mili-giây
KEY_VALUES = list(range(12))      # 0 = không rõ (NaN), 1..11 = nốt nhạc
TS_VALUES = [1, 3, 4, 5]          # các time_signature xuất hiện trong train

CONT_COLS = ["Popularity", "danceability", "energy", "loudness", "speechiness",
             "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_min"]
FLAG_COLS = ["pop_isna", "key_isna", "instr_isna", "dur_was_minutes"]
KEY_COLS = [f"key_{k}" for k in KEY_VALUES]
TS_COLS = [f"ts_{v}" for v in TS_VALUES]
FEATURE_COLS = CONT_COLS + ["mode"] + FLAG_COLS + KEY_COLS + TS_COLS


class MusicPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, clip_quantiles=(0.01, 0.99),
                 clip_cols=("loudness", "speechiness", "liveness", "duration_min", "tempo"),
                 scale=True):
        self.clip_quantiles = clip_quantiles
        self.clip_cols = clip_cols
        self.scale = scale

    # ------------------------------------------------------------------ các bước riêng lẻ
    def fix_duration(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()
        is_min = df[DUR] < MINUTES_THRESHOLD
        df["dur_was_minutes"] = is_min.astype(int)
        df["duration_min"] = np.where(is_min, df[DUR], df[DUR] / 60000.0)
        return df

    def impute(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["pop_isna"] = df["Popularity"].isna().astype(int)
        df["key_isna"] = df["key"].isna().astype(int)
        df["instr_isna"] = df["instrumentalness"].isna().astype(int)
        for c, med in self.medians_.items():
            df[c] = df[c].fillna(med)
        df["key"] = df["key"].fillna(0).astype(int)
        return df

    def clip_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for c, (lo, hi) in self.clip_bounds_.items():
            df[c] = df[c].clip(lo, hi)
        return df

    def encode(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for k in KEY_VALUES:
            df[f"key_{k}"] = (df["key"] == k).astype(int)
        for v in TS_VALUES:
            df[f"ts_{v}"] = (df["time_signature"] == v).astype(int)
        return df

    def scale_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df[CONT_COLS] = self.scaler_.transform(df[CONT_COLS])
        return df

    # ------------------------------------------------------------------ sklearn API
    def fit(self, X: pd.DataFrame, y=None):
        df = self.fix_duration(X)
        self.medians_ = df[["Popularity", "instrumentalness"]].median().to_dict()
        df = self.impute(df)
        lo_q, hi_q = self.clip_quantiles
        self.clip_bounds_ = {c: (float(df[c].quantile(lo_q)), float(df[c].quantile(hi_q)))
                             for c in self.clip_cols}
        df = self.clip_outliers(df)
        self.scaler_ = StandardScaler().fit(df[CONT_COLS])
        self.feature_names_ = list(FEATURE_COLS)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = self.clip_outliers(self.impute(self.fix_duration(X)))
        df = self.encode(df)
        if self.scale:
            df = self.scale_features(df)
        return df[FEATURE_COLS]

    def get_feature_names_out(self, input_features=None):
        return np.array(FEATURE_COLS)
