# Nhật ký thí nghiệm – Random Forest (Diabetes_012)

Nguồn: `random_forest.ipynb`. Số liệu chi tiết từng thí nghiệm xem thêm ở `result_summary.csv`.

## 0. Thông tin chung

| Mục                | Nội dung                                                                    |
| ------------------ | --------------------------------------------------------------------------- |
| Bài toán           | Phân loại 3 lớp: 0 = No Diabetes, 1 = Prediabetes, 2 = Diabetes             |
| Dữ liệu            | 253,680 mẫu, 22 cột (21 đặc trưng + `Diabetes_012`)                         |
| Phân phối nhãn gốc | Lớp 0: 84.24% (213,703) · Lớp 2: 13.93% (35,346) · Lớp 1: 1.83% (4,631)     |
| Cách chia          | 70/15/15, `stratify` theo nhãn, `random_state=42`                           |
| Kích thước         | Train 177,576 · Validation 38,052 · Test 38,052                             |
| Chỉ số chính       | Macro-F1 (accuracy chỉ tham khảo vì đoán toàn lớp 0 đã đạt ≈ 0.842)         |
| Quy tắc dùng tập   | Train để học và CV · Validation để chọn mô hình · Test chỉ dùng 1 lần ở E04 |
| Môi trường         | Python: [điền] · scikit-learn: [điền] · ngày chạy: [điền]                   |

Kiểm chứng chia dữ liệu: tỷ lệ 3 lớp ở train/validation/test khớp tập gốc (sai lệch dưới 0.01 điểm phần trăm).

---

## E01 – Baseline Random Forest

**Mục tiêu:** có mốc so sánh ban đầu với tham số mặc định.

**Cấu hình:** `RandomForestClassifier(n_jobs=-1, random_state=42)`, tức `n_estimators=100`, `max_depth=None`, `max_features="sqrt"`, `min_samples_split=2`, `min_samples_leaf=1`, `class_weight=None`.

**Kết quả (Validation):**

| Accuracy | Macro-P | Macro-R | Macro-F1 |
| -------- | ------- | ------- | -------- |
| 0.8435   | 0.4547  | 0.3874  | 0.3974   |

| Lớp         | Precision | Recall | F1   | Support |
| ----------- | --------- | ------ | ---- | ------- |
| No Diabetes | 0.86      | 0.97   | 0.91 | 32,056  |
| Prediabetes | 0.00      | 0.00   | 0.00 | 694     |
| Diabetes    | 0.50      | 0.19   | 0.28 | 5,302   |

**Chẩn đoán overfitting:**

| Chỉ số   | Train  | Validation | Gap    |
| -------- | ------ | ---------- | ------ |
| Accuracy | 0.9936 | 0.8435     | 0.1501 |
| Macro-F1 | 0.9820 | 0.3974     | 0.5846 |

**Nhận xét:**

- Overfit nặng: cây không giới hạn độ sâu gần như học thuộc dữ liệu train (Macro-F1 train 0.98 so với validation 0.40).
- Mô hình bỏ sót hoàn toàn lớp Prediabetes (precision, recall, F1 đều 0) và chỉ bắt được 19% ca Diabetes.
- Accuracy 0.8435 chỉ cao hơn mức đoán toàn lớp đa số (≈ 0.842) rất ít, nên không phản ánh chất lượng thật.

**Quyết định:** tối ưu siêu tham số để giảm overfit (E02).

**Hình:** `figures/E01_confusion_matrix.png`, `figures/E01_train_vs_val.png`

---

## E02 – Tối ưu siêu tham số (RandomizedSearchCV)

**Mục tiêu:** giảm overfit và tăng Macro-F1.

**Cấu hình:** `RandomizedSearchCV`, `n_iter=12`, `StratifiedKFold(3, shuffle=True, random_state=42)`, `scoring="f1_macro"`, 36 lần fit, chỉ chạy trên tập train.

| Siêu tham số      | Không gian tìm kiếm  |
| ----------------- | -------------------- |
| n_estimators      | 100, 200, 300        |
| max_depth         | None, 10, 15, 20, 30 |
| min_samples_split | 2, 5, 10, 20         |
| min_samples_leaf  | 1, 2, 4, 8           |
| max_features      | sqrt, log2, None     |

Không gian tìm kiếm **không có** `class_weight`.

**Bộ tham số tốt nhất:** `max_depth=15`, `min_samples_split=10`, `min_samples_leaf=1`, `max_features=None`, `n_estimators=100`.

**Kết quả (Validation) so với baseline:**

| Chỉ số          | Baseline | Tuned  | Chênh lệch |
| --------------- | -------- | ------ | ---------- |
| Accuracy        | 0.8435   | 0.8495 | +0.0060    |
| Macro-Precision | 0.4547   | 0.4729 | +0.0182    |
| Macro-Recall    | 0.3874   | 0.3876 | +0.0001    |
| Macro-F1        | 0.3974   | 0.3982 | +0.0009    |

Generalization gap (Macro-F1): train 0.4857 so với validation 0.3982, gap = 0.0875 (baseline là 0.5846).

**Nhận xét:**

- Tuning **giảm overfit rõ rệt** (gap từ 0.585 xuống 0.087).
- Macro-F1 gần như không đổi (+0.0009, nằm trong mức nhiễu) và Macro-Recall không đổi, nên khả năng nhận diện lớp thiểu số **không cải thiện**. Phần tăng chủ yếu đến từ precision.
- Không nên viết rằng tuned “cân bằng precision và recall tốt hơn”, vì số liệu không ủng hộ.
- Nguyên nhân hợp lý (chưa kiểm chứng): search không có `class_weight` nên không có cơ chế nào giúp lớp thiểu số.

**Quyết định:** dùng bản tuned làm mô hình ứng viên; thử xử lý mất cân bằng ở E05.

**Việc còn thiếu:** notebook chưa in classification report theo lớp cho bản tuned trên validation, nên cần chạy thêm để điền vào `result_summary.csv`.

---

## E03 – Phân tích mức độ quan trọng của đặc trưng

**Mục tiêu:** xác định các đặc trưng ảnh hưởng nhiều nhất tới dự đoán.

**Cấu hình:** mô hình tuned; (a) impurity-based importance; (b) permutation importance trên validation, 5 lần lặp, đo mức giảm Macro-F1.

**Kết quả (top 5):**

| Hạng | Impurity-based | Permutation (mean ± std) |
| ---- | -------------- | ------------------------ |
| 1    | HighBP 0.1674  | BMI 0.0407 ± 0.0016      |
| 2    | BMI 0.1460     | HighBP 0.0275 ± 0.0014   |
| 3    | GenHlth 0.1423 | GenHlth 0.0235 ± 0.0009  |
| 4    | Age 0.0879     | HighChol 0.0193 ± 0.0007 |
| 5    | Income 0.0696  | Age 0.0127 ± 0.0008      |

**Nhận xét:**

- Hai phương pháp thống nhất ở nhóm HighBP, BMI, GenHlth, Age; nên kết luận theo nhóm, không khẳng định một biến duy nhất đứng đầu.
- Thứ hạng khác nhau vì impurity-based có xu hướng thiên về biến liên tục như BMI.
- Importance chỉ phản ánh đóng góp vào dự đoán, không chứng minh quan hệ nhân quả.
- Cần đối chiếu với kết quả EDA đã làm trước đó.

**Hình:** `figures/E03_impurity_importance.png`, `figures/E03_permutation_importance.png`

---

## E04 – Mô hình cuối cùng, đánh giá trên Test

**Mục tiêu:** đo hiệu năng tổng quát của mô hình đã chọn.

**Cấu hình:** tham số của E02, fit lại trên train + validation (215,628 mẫu), đánh giá trên test đúng một lần.

**Kết quả (Test):**

| Accuracy | Macro-P | Macro-R | Macro-F1 |
| -------- | ------- | ------- | -------- |
| 0.8481   | 0.4675  | 0.3896  | 0.4005   |

| Lớp         | Precision | Recall | F1   | Support |
| ----------- | --------- | ------ | ---- | ------- |
| No Diabetes | 0.86      | 0.97   | 0.92 | 32,055  |
| Prediabetes | 0.00      | 0.00   | 0.00 | 695     |
| Diabetes    | 0.54      | 0.19   | 0.29 | 5,302   |

**Nhận xét:**

- Macro-F1 test (0.4005) gần như bằng validation của E02 (0.3982), nên mô hình ổn định và không có dấu hiệu overfit vào validation.
- Hạn chế vẫn như các thí nghiệm trước: Prediabetes bằng 0, Diabetes recall chỉ 0.19. Với bài toán sàng lọc bệnh, bỏ sót ca bệnh là rủi ro lớn.
- Accuracy test 0.8481 chỉ nhỉnh hơn mức đoán toàn lớp đa số (≈ 0.842).

**Hình:** `figures/E04_confusion_matrix_test.png`

**Lưu ý lỗi (xem mục Vấn đề bên dưới):** bảng “Validation vs Test” ở cell 68 không hợp lệ vì validation đã nằm trong dữ liệu huấn luyện của mô hình cuối.

---

## E05 – class_weight để xử lý mất cân bằng (kế hoạch, chưa chạy)

**Giả thuyết:** `class_weight="balanced"` hoặc `"balanced_subsample"` làm tăng recall lớp Prediabetes và Diabetes, đổi lại có thể giảm precision và accuracy.

**Cấu hình dự kiến:** thêm `class_weight: [None, "balanced", "balanced_subsample"]` vào không gian tìm kiếm của E02, giữ nguyên các thiết lập khác; so sánh trên validation, chạy test một lần nếu chọn mô hình mới.

**Kết quả:** [điền sau khi chạy]

**Nhận xét:** [điền sau khi chạy]

**Quyết định:** [điền sau khi chạy]

---

## Vấn đề và lỗi đã phát hiện khi rà soát notebook

| #   | Vị trí      | Vấn đề                                                                                                                                   | Mức độ       | Trạng thái          |
| --- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------ | ------------------- |
| 1   | Cell 68     | So sánh Validation vs Test bị rò rỉ: mô hình cuối đã fit trên validation (Acc 0.884, F1 0.482 không có giá trị so sánh)                  | Nghiêm trọng | Cần bỏ khỏi báo cáo |
| 2   | Cell 36     | Không gian tìm kiếm thiếu `class_weight`; mất cân bằng lớp chưa được xử lý                                                               | Nghiêm trọng | Xử lý ở E05         |
| 3   | Cell 30, 60 | Nhận định sai/quá mức: “chưa thể kết luận overfitting” (thực tế overfit nặng); “cân bằng precision và recall tốt hơn” (recall không đổi) | Quan trọng   | Cần viết lại        |
| 4   | Cell 32     | Biểu đồ Train vs Validation: hai nhóm cột cùng dùng `x - width/2` nên bị đè                                                              | Trung bình   | Cần sửa             |
| 5   | Cell 24     | `yticklabels` thiếu dấu phẩy, hai nhãn bị dính thành một                                                                                 | Trung bình   | Cần sửa             |
| 6   | Cell 29     | Dòng in “F1-score gap” in nhầm giá trị `val_f1` (0.3974) thay vì gap (0.5846)                                                            | Nhỏ          | Cần sửa             |
| 7   | Cell 1      | Output còn lưu `FileNotFoundError` do đường dẫn cục bộ                                                                                   | Nhỏ          | Restart & Run All   |

---

## Ghi chú tái lập

- `random_state=42` được dùng cho cả chia dữ liệu, mô hình và CV.
- Số liệu per-class ở E01 và E04 lấy từ classification report đã làm tròn 2 chữ số.
- Cần lưu thêm: `models/rf_final.joblib`, `best_params.json`, các hình vào `figures/` đúng tên đã ghi ở từng thí nghiệm.
