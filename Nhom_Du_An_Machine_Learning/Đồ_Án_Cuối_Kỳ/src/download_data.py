"""Tải CDC Diabetes Health Indicators (UCI ID 891) về data/raw/diabetes.csv.

Chạy từ thư mục gốc repo:  python src/download_data.py
"""
import os
import pandas as pd
from ucimlrepo import fetch_ucirepo

OUT = "data/raw/diabetes.csv"

ds = fetch_ucirepo(id=891)
df = pd.concat([ds.data.features, ds.data.targets], axis=1)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
df.to_csv(OUT, index=False)
print("Đã lưu:", OUT, "| Kích thước:", df.shape)
