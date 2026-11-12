# Nhật ký thí nghiệm – 02_EDA

| Mục | Giá trị |
|---|---|
| Người chạy | Tô Doanh Quang Khu |
| Ngày chạy | 12/11/2026 |
| Giờ bắt đầu – kết thúc | 09:48:41 – 09:48:56 (15.5 giây) |
| Notebook | `02_EDA.ipynb` |
| Mục tiêu | EDA: khám phá dữ liệu train/test, missing, duplicates, phân phối, tương quan, target |
| Môi trường | Python 3.13.9 · Windows 11 |

## Các bước & kết quả

1. **Tải dữ liệu**
   - files: [sample_submission (2).csv, test (2).csv, train (1).csv]
   - train_rows: 14396
   - test_rows: 3600
   - n_columns_train_raw: 18
   - n_classes: 11
2. **Missing values**
   - Popularity_%: 2.3
   - key_%: 11.2
   - instrumentalness_%: 24.6
3. **Duplicates**
   - dup_rows_same_features: 1081
   - dup_groups: 979
   - groups_conflicting_label: 979
   - test_tracks_already_in_train: 607
4. **Bất thường duration (phút/ms lẫn lộn)**
   - train_rows_in_minutes: 2075
   - test_rows_in_minutes: 505
5. **Tương quan mạnh nhất**
   - pair: loudness - energy
   - pearson_r: 0.77
6. **Biến mục tiêu**
   - imbalance_ratio: 12.8
   - majority_baseline_accuracy: 0.275
   - top5_features_by_eta2: [acousticness, speechiness, energy, loudness, danceability]

## Nhận xét

Điền nhận xét của bạn ở đây (vd: phát hiện gì, quyết định xử lý gì ở bước sau).
