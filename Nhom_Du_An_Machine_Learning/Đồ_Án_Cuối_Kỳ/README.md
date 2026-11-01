# Dự đoán tiểu đường từ chỉ số sức khỏe (BRFSS2015)

Đồ án: dự đoán nguy cơ tiểu đường từ 21 chỉ số sức khỏe và lối sống.

## Dữ liệu
- CDC Diabetes Health Indicators, UCI ID 891: https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators
- 253.680 mẫu, 21 thuộc tính, nhãn nhị phân `Diabetes_binary` (86,1% / 13,9%).
- Giấy phép: ghi theo trang UCI ở link trên (nhóm kiểm tra và điền vào đây).

## Cấu trúc
```
data/raw/        dữ liệu gốc (không sửa, không đưa lên git)
data/processed/  dữ liệu sau xử lý
notebooks/       EDA, thí nghiệm mô hình
src/             preprocessing.py, download_data.py
figures/         hình EDA và kết quả
logs/            experiment_log.csv
```

## Cách chạy
```bash
pip install -r requirements.txt
python src/download_data.py        # tải dữ liệu về data/raw/diabetes.csv
python src/preprocessing.py        # chạy thử tiền xử lý (từ thư mục gốc repo)
jupyter notebook notebooks/02_EDA.ipynb
```
Trong notebook mô hình, dùng tiền xử lý bằng:
```python
import sys; sys.path.append("../src")
from preprocessing import load_and_split, make_pipeline
```
Lưu ý: `load_and_split()` dùng đường dẫn `data/raw/diabetes.csv`, nên trong notebook truyền `path="../data/raw/diabetes.csv"`.

## Quy trình làm việc
- Nhánh: `main` (bản chạy được) ← `dev` ← `feature/*`. Không push thẳng vào `main`.
- Mỗi người ghi thí nghiệm vào `logs/experiment_log.csv` (thêm dòng vào cuối file).
