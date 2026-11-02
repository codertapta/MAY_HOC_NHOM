# Dự án ML: dự đoán tiểu đường

README này hướng dẫn chạy phần tạo đặc trưng, pipeline và đánh giá tái lập được cho bộ dữ liệu CDC Diabetes Health Indicators.

## Cách chạy

Yêu cầu Python 3.10 trở lên. Từ thư mục gốc dự án, chạy:

```powershell
python src/feature_pipeline.py
python src/feature_pipeline.py --run-cv
```

Lệnh đầu đọc dữ liệu và ghi thông tin kiểm tra vào log. Lệnh thứ hai chạy so sánh 5-fold CV giữa hai phiên bản đặc trưng, chỉ trên tập train. Kết quả được ghi vào `logs/experiment_log.json` và `logs/experiment_log.csv`.

## Dữ liệu và nhãn

Mã đọc `sources/diabetes.csv` và không sửa đổi tệp này. Dữ liệu được cung cấp có nhãn **nhị phân** `Diabetes_binary` (0/1), trong khi một số phần của đề cương mô tả bài toán ba lớp `Diabetes_012`. Nhóm cần thống nhất loại nhãn sẽ dùng trong báo cáo và các thực nghiệm tiếp theo.

Tệp có 253.680 dòng, 21 đặc trưng đầu vào và không có ô dữ liệu thiếu. Thống kê nhãn, tỷ lệ trùng lặp và phiên bản thư viện được ghi trong JSON log.

## Đặc trưng được tạo

- Nhóm BMI theo ngưỡng WHO: thiếu cân (<18,5), bình thường (18,5 đến dưới 25), thừa cân (25 đến dưới 30), béo phì (từ 30 trở lên).
- Tổng số bệnh đồng mắc: `HighBP`, `HighChol`, `Stroke`, `HeartDiseaseorAttack`.
- Điểm lối sống lành mạnh: tổng `PhysActivity`, `Fruits`, `Veggies` (từ 0 đến 3).
- Tương tác tùy chọn `Age × HighBP`.

## Chia dữ liệu và pipeline

Dữ liệu được chia phân tầng 80/20 với `random_state=42`. Tập train dùng Stratified 5-fold CV có xáo trộn, cùng `random_state=42`, để so sánh hai bộ đặc trưng. Cả hai dùng Logistic Regression với `class_weight="balanced"`.

Bộ điền giá trị thiếu và `StandardScaler` nằm trong sklearn Pipeline, nên chỉ được học trên phần huấn luyện của từng fold. Tùy chọn `--run-cv` không đánh giá tập test. Chỉ dùng tập test một lần sau khi đã chọn xong mô hình và đặc trưng.

## Quyết định về dòng trùng lặp

Các dòng trùng lặp được giữ lại vì những tổ hợp câu trả lời giống nhau có thể xuất hiện hợp lệ trong dữ liệu khảo sát; xóa tất cả có thể làm thay đổi phân bố lớp và quần thể dữ liệu. Số dòng trùng và tỷ lệ được ghi trong log. Vì vậy, các bản ghi trùng có thể xuất hiện ở cả train và test. Nếu nhóm muốn đảm bảo các mẫu có cùng tổ hợp đặc trưng không nằm ở hai tập, cần thống nhất cách xử lý trước khi chia dữ liệu và ghi rõ ảnh hưởng đến kết quả.

## Kết quả so sánh hiện tại

Một lần chạy 5-fold CV trên tập train cho kết quả:

| Phiên bản            | Macro F1 trung bình ± độ lệch chuẩn | Accuracy trung bình |
| -------------------- | ----------------------------------: | ------------------: |
| Không thêm đặc trưng |                 0,633365 ± 0,001411 |            0,731951 |
| Có thêm đặc trưng    |                 0,632064 ± 0,001505 |            0,728994 |

Trong lần chạy này, các đặc trưng mới không làm tăng Macro F1. Đây là kết quả CV, chưa phải kết quả đánh giá cuối trên tập test.

## Thư viện cần cài

Các thư viện được liệt kê trong `requirements.txt`: NumPy, pandas, scikit-learn và matplotlib (matplotlib dùng để tạo sơ đồ pipeline).

Sơ đồ pipeline: `figures/pipeline.png`.
