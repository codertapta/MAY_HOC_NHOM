# Nhật ký thí nghiệm – 03_Data_Preprocessing

| Mục | Giá trị |
|---|---|
| Người chạy | Tô Doanh Quang Khu |
| Ngày chạy | 12/11/2026 |
| Giờ bắt đầu – kết thúc | 10:28:38 – 10:29:26 (47.8 giây) |
| Notebook | `03_Data_Preprocessing.ipynb` |
| Mục tiêu | Tiền xử lý: missing, duplicates, outliers, encoding, scaling; lưu dữ liệu đã xử lý |
| Môi trường | Python 3.13.9 · Windows 11 |

## Các bước & kết quả

1. **Dữ liệu vào**
   - train_rows: 14396
   - test_rows: 3600
   - n_raw_features: 16
2. **Duration**
   - train_rows_in_minutes: 2075
   - action: quy đổi về phút
3. **Missing**
   - medians: {'Popularity': 44.0, 'instrumentalness': 0.00392}
   - action: cờ *_isna + median (Popularity, instrumentalness), key NaN→0
4. **Duplicates**
   - dup_groups: 979
   - exact_dup_incl_class: 0
   - strategy: keep_all
   - rows_used: 14396
5. **Outliers**
   - method: winsorize p1-p99 (fit trên train)
   - columns: [loudness, speechiness, liveness, duration_min, tempo]
6. **Encoding**
   - key: one-hot (12 cột, key_0 = không rõ)
   - time_signature: one-hot (4 cột)
   - dropped: Artist Name, Track Name, Id
7. **Scaling**
   - method: StandardScaler (fit trên train)
   - n_scaled: 11
8. **CV: Duplicates | RF | giữ tất cả**
   - macro_F1: 0.5734
   - std: 0.0034
   - accuracy: 0.5504
9. **CV: Duplicates | RF | bỏ bản trùng (giữ dòng đầu)**
   - macro_F1: 0.572
   - std: 0.0041
   - accuracy: 0.5492
10. **CV: Outliers | LR | winsorize 1%-99% (mặc định)**
   - macro_F1: 0.5252
   - std: 0.011
   - accuracy: 0.5059
11. **CV: Outliers | LR | KHÔNG cắt outlier**
   - macro_F1: 0.5232
   - std: 0.0105
   - accuracy: 0.5039
12. **CV: Scaling | LR | StandardScaler (mặc định)**
   - macro_F1: 0.5252
   - std: 0.011
   - accuracy: 0.5059
13. **CV: Scaling | LR | KHÔNG scale**
   - macro_F1: 0.4824
   - std: 0.0113
   - accuracy: 0.4818
14. **Đầu ra**
   - X_train: [14396, 32]
   - X_test: [3600, 32]
   - n_features: 32
   - files: train_processed.csv, test_processed.csv, preprocessor.joblib

## Nhận xét

Điền nhận xét của bạn ở đây (vd: quyết định xử lý, điểm cần lưu ý cho bước 04/05).
