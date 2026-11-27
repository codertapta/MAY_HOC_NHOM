# Nhật ký thí nghiệm — Naive Bayes (GaussianNB)

- **Bài toán:** phân loại 3 lớp `Diabetes_012` (0 = không tiểu đường, 1 = tiền tiểu đường, 2 = tiểu đường) trên BRFSS 2015.
- **Nguồn:** `naive_bayes.ipynb` (output đã lưu, 68 cell). Log này được ghi lại từ output đã lưu, **không chạy lại notebook**. Ngày chạy thực tế và phiên bản thư viện không được ghi trong notebook.
- **Ngày lập log:** 2026-11-27
- **Tệp kết quả:** `result_summary.csv` (mỗi thí nghiệm một dòng, mã `E00`–`E04`).

## 1. Thiết lập chung

| Mục                  | Giá trị                                                                                                         |
| -------------------- | --------------------------------------------------------------------------------------------------------------- |
| Dữ liệu              | 253,680 dòng × 22 cột (21 đặc trưng + target)                                                                   |
| Dòng trùng           | 23,899, **không loại bỏ**                                                                                       |
| Phân bố lớp          | lớp 0: 213,703 (84.24%); lớp 1: 4,631 (1.83%); lớp 2: 35,346 (13.93%)                                           |
| Tiền xử lý           | Không có bước nào trong notebook (ghi chú "dựa vào preprocessing của mô hình trước")                            |
| Chia dữ liệu         | `train_test_split`, `stratify=y`, `random_state=42`: train 177,576 / validation 38,052 / test 38,052 (70/15/15) |
| Quy tắc chọn mô hình | Chọn tham số theo **Macro F1 trên validation**; test chỉ dùng một lần ở cuối                                    |
| Metric chính         | Macro F1, balanced accuracy, recall từng lớp (đặc biệt lớp 1). Accuracy chỉ tham khảo                           |

## 2. Các thí nghiệm

### E00 — Baseline đa số (tính toán, không có trong notebook)

- **Mục đích:** có mốc so sánh cho accuracy.
- **Cấu hình:** luôn dự đoán lớp 0.
- **Kết quả (validation):** accuracy 0.8424; balanced accuracy 0.3333; Macro F1 ≈ 0.3048.
- **Nhận xét:** accuracy của mọi mô hình Naive Bayes bên dưới (≈ 0.758) **thấp hơn** baseline này, nên không dùng accuracy làm bằng chứng mô hình tốt.

### E01 — GaussianNB mặc định

- **Cấu hình:** `GaussianNB()` (`var_smoothing=1e-9`), prior học từ train (≈ 0.8424 / 0.0183 / 0.1393), fit trên train.
- **Kết quả (validation):** accuracy 0.7576; balanced accuracy 0.4636; Macro F1 0.4284; recall lớp 0/1/2 = 0.8041 / 0.0130 / 0.5737.
- **Train vs validation:** accuracy 0.7565 vs 0.7576, không có dấu hiệu overfit về accuracy tổng thể.
- **Lớp 1 (694 mẫu):** đoán đúng 9, bị đoán thành lớp 0 là 358, thành lớp 2 là 327.
- **Precision/F1 lớp 1:** 0.03 / 0.02.
- **Quan sát đặc trưng:** trung bình BMI, HighBP, HighChol, Age, GenHlth của lớp 1 nằm gần lớp 2 hơn lớp 0; boxplot BMI/Age/GenHlth chồng lấp. Đây chỉ là mô tả, chưa chứng minh nguyên nhân.

### E02 — Prior bằng nhau

- **Cấu hình:** prior 1/3 cho mỗi lớp, các tham số khác như E01.
- **Kết quả (validation, số làm tròn từ classification report):** accuracy 0.68; macro-average recall ≈ 0.49; Macro F1 0.42; recall lớp 0/1/2 = 0.70 / 0.12 / 0.65; precision lớp 1 = 0.03.
- **Nhận xét:** recall lớp 1 tăng từ 1.3% lên 12% nhưng precision vẫn rất thấp, accuracy giảm 7.8 điểm phần trăm, Macro F1 không tăng. Đổi prior không giải quyết được vấn đề.

### E03 — Quét `var_smoothing` (7 giá trị: 1e-12 … 1e-6)

- **Cấu hình:** `GaussianNB(var_smoothing=v)`, `v = np.logspace(-12, -6, 7)`, fit trên train, đánh giá trên validation.
- **Kết quả:**
  - 1e-12 → 1e-9: kết quả giống hệt nhau (Macro F1 0.428353).
  - 1e-8: 0.428369.
  - **1e-7: 0.428400 (cao nhất, được chọn)**.
  - 1e-6: 0.427802 (giảm nhẹ; recall lớp 1 = 0.0115).
- **Nhận xét:** chênh lệch Macro F1 giữa giá trị tốt nhất và mặc định chỉ khoảng 0.00005, nằm trong mức nhiễu; việc tinh chỉnh gần như không có tác dụng. Lưới hẹp quanh giá trị mặc định 1e-9, chưa thử các giá trị lớn hơn (ví dụ tới 1).

### E04 — Đánh giá cuối trên test

- **Cấu hình:** `GaussianNB(var_smoothing=1e-7)`, fit trên train + validation (215,628 mẫu), dự đoán test một lần.
- **Kết quả (test):** accuracy 0.7575; balanced accuracy 0.4636; Macro F1 0.4313; recall lớp 0/1/2 = 0.8058 / 0.0230 / 0.5619.
- **Precision lớp 1:** 0.04.
- **Confusion matrix (hàng = thật, cột = dự đoán):**

  |        | Dự đoán 0 | Dự đoán 1 | Dự đoán 2 |
  | ------ | --------- | --------- | --------- |
  | Thật 0 | 25,829    | 290       | 5,936     |
  | Thật 1 | 387       | 16        | 292       |
  | Thật 2 | 2,251     | 72        | 2,979     |

- **Nhận xét:** chỉ 16/695 mẫu lớp 1 được nhận diện đúng. Kết quả test gần với validation. Recall lớp 1 khác nhau (1.30% = 9/694 trên validation; 2.30% = 16/695 trên test) là dao động do số mẫu rất nhỏ, không phải xu hướng.

## 3. Kết luận từ các thí nghiệm

1. GaussianNB đạt accuracy ≈ 75.7% nhưng thấp hơn baseline đa số (84.24%); balanced accuracy chỉ ≈ 46.4%, Macro F1 ≈ 0.43.
2. Hiệu quả không đều giữa các lớp: lớp 0 tốt, lớp 2 trung bình, lớp 1 gần như không nhận diện được.
3. Prior bằng nhau và quét `var_smoothing` không cải thiện đáng kể Macro F1.
4. Kết luận chỉ áp dụng cho các cấu hình GaussianNB đã thử, không suy ra mọi biến thể Naive Bayes đều không phù hợp.

## 4. Vấn đề và hạn chế đã biết

- Dòng trùng (23,899) chưa xử lý, có thể gây rò rỉ nhẹ giữa train và validation/test, làm số liệu hơi lạc quan.
- Dữ liệu chủ yếu là biến nhị phân/thứ tự nhưng dùng GaussianNB (giả định phân phối chuẩn).
- Chưa thử BernoulliNB/CategoricalNB, chỉnh ngưỡng quyết định bằng `predict_proba`, hay các kỹ thuật xử lý mất cân bằng khác.
- Lưới `var_smoothing` hẹp.
- Lớp 1 chỉ có khoảng 700 mẫu ở validation/test nên các chỉ số của lớp này có độ bất định cao.
- Đường dẫn CSV trong cell 2 là đường dẫn máy cá nhân, notebook không tự chạy lại được ở môi trường khác.
- Số liệu của E02 chỉ có dạng làm tròn (2 chữ số) vì notebook chỉ in classification report.

## 5. Việc tiếp theo (đề xuất, chưa thực hiện)

| Mã  | Việc                                                               | Mục đích                                       |
| --- | ------------------------------------------------------------------ | ---------------------------------------------- |
| E05 | Loại dòng trùng trước khi chia, chạy lại E01–E04                   | Loại rủi ro rò rỉ dữ liệu                      |
| E06 | CategoricalNB / BernoulliNB                                        | Kiểm tra ảnh hưởng của giả định Gaussian       |
| E07 | Chỉnh ngưỡng bằng `predict_proba` (trọng số lớp 1) trên validation | Tăng recall lớp 1 có kiểm soát                 |
| E08 | Mở rộng lưới `var_smoothing` (ví dụ 1e-9 … 1)                      | Xác nhận việc tinh chỉnh có tác dụng hay không |
