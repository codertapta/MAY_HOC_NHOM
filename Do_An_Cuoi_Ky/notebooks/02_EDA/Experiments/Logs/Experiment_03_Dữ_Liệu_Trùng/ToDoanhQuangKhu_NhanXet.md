**Ngày chạy:** 20/11/2026  
**Người chạy:** Tô Doanh Quang Khu

**Mục tiêu:** Kiểm tra số dòng trùng trong tập dữ liệu.

**Kết quả chạy:** Được lưu tại các file Excel trong `Experiment_03`.

**Nhận xét:**

Qua thống kê, tập dữ liệu xuất hiện 23.899 bản ghi trùng lặp, chiếm khoảng 9,42% tổng dữ liệu. Khi phân tích theo biến mục tiêu, nhận thấy sự chênh lệch rất lớn giữa các lớp: lớp 0 chiếm 23.648 dòng trùng, lớp 2 có 249 dòng và lớp 1 có 2 dòng. Như vậy, hiện tượng trùng lặp không phân bố đồng đều giữa các nhóm. Cần cân nhắc việc loại bỏ các bản ghi trùng trước khi xây dựng mô hình để hạn chế việc một số quan sát bị lặp lại quá nhiều.
