Người chạy Ngô Thanh Phong
Ngày chạy: 20/11/2026
Mục đích: Chạy thử nghiệm mô hình đơn giản trên tập dữ liệu với một lớp nhất định và lớp được chọn ở đây là lớp 0 trong toàn bộ tập từ đó xác định được dự đoán của một phương pháp đơn giản có thể cho ra kết quả như thế nào trên dataset
Kết quả: Accuracy đạt mức 84.2412% điều này vẫn chưa thực sự có ý nghĩa thực tiễn do đó ta có Precision và Recall lần lượt đạt 0 và 100% điều này cho thấy phương pháp đơn giản chỉ cho ra kết quả của các dự đoán được cho là đúng trên tổng thể và bỏ qua toàn bộ các dự đoán khác được cho là sai
Tổng kết: Phương pháp đơn giản chỉ cho ra kết quả đã biết trước và không thể tự dự đoán kết quả từ những mẫu chưa có kết quả
Phương pháp cải thiện: Tạo các tập train, validation và test trên dataset sau đó sử dụng 2 mô hình phù hợp với dữ liệu ở đây là (Classification) phân lớp để thử nghiệm và so sánh sự thể hiện của 2 mô hình qua các lần cập nhật trọng số và bias để xác định mô hình có sự chính xác cao hơn để có thể áp dụng vào các dataset tương tự
