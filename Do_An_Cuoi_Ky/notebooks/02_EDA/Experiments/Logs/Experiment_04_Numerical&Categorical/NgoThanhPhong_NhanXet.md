**Ngày chạy:** 20/11/2026  
**Người chạy:** Ngô Thanh Phong

**Mục tiêu:** Phân loại và xác định các thuộc tính thuộc Numerical hay Categorical.

**Kết quả chạy:** Được lưu tại các file Excel trong `Experiment_04`.

**Nhận xét:**

Qua quá trình kiểm tra và phân loại, tôi nhận thấy 21 thuộc tính được chia thành ba nhóm có đặc điểm khác nhau. Cụ thể, nhóm Numerical gồm 3 biến, nhóm Categorical Nominal gồm 14 biến và nhóm Categorical Ordinal gồm 4 biến. Trong đó, các biến phân loại không có thứ tự chiếm tỷ lệ lớn nhất.

Việc tất cả thuộc tính cùng có kiểu lưu trữ `float64` có thể gây nhầm lẫn nếu chỉ kiểm tra bằng phương thức `dtypes`. Vì vậy, cần xem xét ý nghĩa của từng biến để xác định đúng loại dữ liệu. Theo tôi, kết quả này đặc biệt hữu ích cho bước EDA tiếp theo vì mỗi nhóm biến sẽ cần cách biểu diễn trực quan và phương pháp phân tích riêng.
