**Ngày chạy:** 20/11/2026  
**Người chạy:** Tô Doanh Quang Khu

**Mục tiêu:** Phân loại và xác định các thuộc tính thuộc Numerical hay Categorical.

**Kết quả chạy:** Được lưu tại các file Excel trong `Experiment_04`.

**Nhận xét:**

Kết quả phân loại cho thấy tập dữ liệu có 21 đặc trưng, trong đó 3 biến thuộc nhóm Numerical, 14 biến thuộc nhóm Categorical Nominal và 4 biến thuộc nhóm Categorical Ordinal. Có thể thấy dữ liệu chủ yếu chứa các biến phân loại thay vì các biến định lượng liên tục.

Một điểm đáng chú ý là toàn bộ thuộc tính đều được lưu dưới kiểu `float64`, tuy nhiên điều này không có nghĩa tất cả đều là biến số. Ví dụ, các biến nhị phân hoặc biến được mã hóa theo cấp độ vẫn mang bản chất phân loại. Do đó, cần sử dụng kết quả phân nhóm này để tránh áp dụng sai các phương pháp thống kê và xử lý dữ liệu.
