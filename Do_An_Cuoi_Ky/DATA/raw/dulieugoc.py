from ucimlrepo import fetch_ucirepo

# Tải dataset
cdc_diabetes_health_indicators = fetch_ucirepo(id=891)

# Lấy dữ liệu
X = cdc_diabetes_health_indicators.data.features
y = cdc_diabetes_health_indicators.data.targets

# Kiểm tra metadata
print(cdc_diabetes_health_indicators.metadata)

# Kiểm tra các biến
print(cdc_diabetes_health_indicators.variables)
import pandas as pd

df = pd.concat([X, y], axis=1)

df.to_csv("diabetes.csv", index=False)

print("Đã lưu dữ liệu thành công!")
print("Kích thước dữ liệu:", df.shape)