# Nhật ký thí nghiệm – 04_feature_engineering

| Mục | Giá trị |
|---|---|
| Người chạy | Tô Doanh Quang Khu |
| Ngày chạy | 12/11/2026 |
| Giờ bắt đầu – kết thúc | 10:43:45 – 10:44:48 (62.6 giây) |
| Notebook | `04_Feature_Engineering.ipynb` |
| Mục tiêu | Tạo đặc trưng mới (artist freq, tên bài hát, đặc trưng kết hợp) và đánh giá bằng GroupKFold macro-F1 |
| Môi trường | Python 3.13.9 · Windows 11 |

## Các bước & kết quả

1. **Nạp dữ liệu**
   - train_shape: [14396, 37]
   - test_shape: [3600, 35]
   - n_base_features: 32
2. **Tạo đặc trưng mới**
   - artist: [artist_freq, artist_unknown]
   - track: [track_len, track_words, track_paren, track_feat]
   - combo: [energy_x_loud, energy_minus_acoust, loud_minus_acoust, dance_x_valence, speech_x_instr, acoust_x_instr, tempo_x_energy, dance_x_energy]
3. **So sánh GroupKFold (RF, 5 fold)**
   - results: [{'thí nghiệm': '0. Gốc (32 đặc trưng)', 'n_features': 32, 'macro_F1': 0.5745, 'std': 0.0043, 'accuracy': 0.5499}, {'thí nghiệm': '1. Gốc + Artist', 'n_features': 34, 'macro_F1': 0.6005, 'std': 0.0071, 'accuracy': 0.5699}, {'thí nghiệm': '2. Gốc + Tên bài hát', 'n_features': 36, 'macro_F1': 0.5855, 'std': 0.0048, 'accuracy': 0.5565}, {'thí nghiệm': '3. Gốc + Kết hợp', 'n_features': 40, 'macro_F1': 0.5681, 'std': 0.0084, 'accuracy': 0.5467}, {'thí nghiệm': '4. Gốc + Tất cả', 'n_features': 46, 'macro_F1': 0.5907, 'std': 0.008, 'accuracy': 0.564}]
4. **Feature importance (RF 500 cây)**
   - top5: {'dur_was_minutes': 0.0928, 'acousticness': 0.0547, 'Popularity': 0.053, 'energy_minus_acoust': 0.0519, 'speechiness': 0.0514}
5. **Lưu kết quả**
   - chosen: 1. Gốc + Artist
   - n_features: 34
   - train_fe: [14396, 37]
   - test_fe: [3600, 35]

## Nhận xét

Bộ đặc trưng chọn: 1. Gốc + Artist (34 cột). Frequency encoding Artist đếm trên train+test (không dùng nhãn). Cột liên tục mới (track_len, track_words, artist_freq) chuẩn hoá bằng thống kê của train. Đã lưu processed/train_fe.csv, test_fe.csv, feature_cols_fe.csv.
