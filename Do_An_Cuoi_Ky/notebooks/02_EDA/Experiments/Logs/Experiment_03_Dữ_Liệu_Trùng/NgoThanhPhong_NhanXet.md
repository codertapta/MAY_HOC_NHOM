**Ngày chạy:** 20/11/2026  
**Người chạy:** Ngô Thanh Phong

**Mục tiêu:** Kiểm tra số dòng trùng trong tập dữ liệu.

**Kết quả chạy:** Được lưu tại các file Excel trong `Experiment_03`.

**Nhận xét:**

Kết quả cho thấy có một lượng bản ghi trùng lặp tương đối đáng kể trong bộ dữ liệu, cụ thể là 23.899 dòng, chiếm 9,42%. Phân tích sâu hơn cho thấy 23.648 dòng thuộc nhóm không mắc bệnh, trong khi nhóm tiền tiểu đường có 249 dòng và nhóm mắc tiểu đường chỉ có 2 dòng trùng. Theo tôi, đây là vấn đề cần quan tâm vì các bản ghi trùng có thể khiến mô hình học quá nhiều từ những trường hợp giống nhau. Tuy nhiên, cần xem xét việc loại bỏ trùng lặp trên dữ liệu huấn luyện và tránh làm mất thông tin khi đánh giá mô hình.
