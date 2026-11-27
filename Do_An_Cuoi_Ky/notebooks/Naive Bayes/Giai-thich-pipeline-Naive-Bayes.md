# Pipeline, mục đích từng cell và kết luận — Naive Bayes

Nguồn đối chiếu: `sources/naive bayes.ipynb`. Notebook có 68 cell (đánh số từ 1), tất cả cell code có execution count và các kết quả được tóm tắt dưới đây là output đã lưu trong notebook. Notebook không được sửa và không chạy lại trong quá trình ghi chép.

## 1. Pipeline thực tế

1. Import thư viện, đọc CSV BRFSS 2015 từ đường dẫn cục bộ trong mã.
2. Kiểm tra kích thước dữ liệu, số dòng trùng và phân bố target `Diabetes_012`; vẽ phân bố nhãn.
3. Tách X (21 biến) và y; ghi chú dựa vào preprocessing của mô hình trước, không thực hiện bước làm sạch/loại dòng trùng trong notebook này.
4. Chia dữ liệu có stratify, `random_state=42`: 70% train (177,576), 15% validation (38,052), 15% test (38,052).
5. Fit GaussianNB mặc định trên train. Khảo sát prior, trung bình/phương sai đã học; lấy dự đoán và xác suất trên validation.
6. Đánh giá validation: accuracy, train/validation accuracy, confusion matrix, classification report, balanced accuracy; lọc lỗi và xem riêng lớp 1 cùng một số đặc trưng.
7. Thử GaussianNB với prior ba lớp bằng nhau; xem báo cáo, log-likelihood theo đặc trưng và so sánh trung bình một số biến của các nhóm mẫu.
8. Thử 7 giá trị `var_smoothing` từ `1e-12` đến `1e-6`, chọn giá trị theo Macro F1 validation.
9. Gộp train + validation, fit mô hình cuối với `var_smoothing=1e-7`, rồi đánh giá đúng một lần trên test theo các metric và confusion matrix.

## 2. Mục đích từng cell

| Cell | Mục đích |
|---|---|
| 1 | Import numpy, pandas, matplotlib, seaborn và `Path`. |
| 2 | Đọc CSV vào DataFrame bằng đường dẫn cục bộ được ghi trong notebook. |
| 3 | In số dòng và cột. |
| 4 | Đếm dòng trùng; không xóa chúng. |
| 5 | Đếm và tính tỷ lệ từng lớp target. |
| 6 | Vẽ count plot phân bố target. |
| 7 | Tách đặc trưng X và nhãn y. |
| 8 | Ghi chú bỏ qua preprocessing vì dựa vào mô hình trước; đây là ghi chú, không phải kiểm tra dữ liệu. |
| 9 | Import `train_test_split`. |
| 10 | Tạo train 70% và temp 30%, stratify theo nhãn, random state 42. |
| 11 | Giải thích temp sẽ chia thành validation và test. |
| 12 | Chia temp làm đôi thành validation và test, có stratify. |
| 13 | Ghi chú validation và test có kích thước bằng nhau. |
| 14 | Ghi chú không kiểm tra thêm do dùng cùng dataset với mô hình trước. |
| 15 | Import và khởi tạo GaussianNB mặc định. |
| 16 | Fit mô hình trên train. |
| 17 | In class prior, mean (`theta_`) và variance (`var_`) học được. |
| 18 | In danh sách lớp và hình dạng ma trận mean/variance. |
| 19 | Dự đoán lớp và xác suất từng lớp cho toàn bộ validation. |
| 20 | Minh họa xác suất trên một mẫu validation đầu tiên. |
| 21 | Tạo bảng nhãn thực tế, dự đoán và cờ đúng/sai. |
| 22 | Đếm số dự đoán đúng và sai validation. |
| 23 | Tính accuracy validation. |
| 24 | Nhắc accuracy riêng lẻ chưa đủ kết luận chất lượng. |
| 25 | Thêm xác suất dự đoán từng lớp vào bảng và in 10 dòng đầu. |
| 26 | So sánh accuracy train với validation. |
| 27 | Ghi chú hai accuracy gần nhau; đây là quan sát, chưa đủ tự nó khẳng định tổng quát hóa tốt trên mọi mặt. |
| 28 | Import công cụ confusion matrix và hiển thị. |
| 29 | Tính confusion matrix validation chuẩn hóa theo hàng (tỷ lệ trong từng lớp thật). |
| 30 | Vẽ confusion matrix chuẩn hóa. |
| 31 | Nhận xét lớp 1 có tỷ lệ nhận diện đúng thấp nhất. |
| 32 | Import `classification_report`. |
| 33 | In precision, recall, F1 và support từng lớp trên validation. |
| 34 | Nhận xét metric lớp 1 thấp nhất. |
| 35 | Import balanced accuracy. |
| 36 | Tính balanced accuracy validation. |
| 37 | In accuracy và balanced accuracy cạnh nhau. |
| 38 | Nhận xét balanced accuracy thấp hơn nhiều accuracy, thể hiện hiệu quả không đều giữa các lớp. |
| 39 | Lập bảng và lọc các dự đoán sai validation. |
| 40 | Ghi chú về lỗi lớp 1; output định lượng chi tiết hơn nằm ở cell 41. |
| 41 | Đếm lớp được dự đoán cho các mẫu thật thuộc lớp 1. |
| 42 | Tính trung bình BMI, HighBP, HighChol, PhysActivity, Age, GenHlth theo lớp thật. |
| 43 | Nhận xét một số trung bình lớp 1 gần lớp 2; đây là mô tả, chưa chứng minh quan hệ nhân quả hoặc khả năng phân biệt tổng thể. |
| 44 | Vẽ boxplot BMI theo lớp thật. |
| 45 | Ghi nhận xét về phân bố BMI. |
| 46 | Vẽ boxplot Age theo lớp thật. |
| 47 | Ghi nhận xét về phân bố Age. |
| 48 | Vẽ boxplot GenHlth theo lớp thật. |
| 49 | Ghi nhận xét về độ chồng lấp GenHlth. |
| 50 | Tổng hợp diễn giải từ ba biểu đồ đặc trưng. |
| 51 | Tạo bảng prior của mô hình. |
| 52 | Nhận xét prior lớp 1 thấp. |
| 53 | Tính phân bố lớp của train để đối chiếu. |
| 54 | Nhận xét lớp 1 chiếm tỷ lệ nhỏ trong train. |
| 55 | Tạo, fit GaussianNB với prior bằng nhau và dự đoán validation (`model_equal`). |
| 56 | In classification report của dự đoán từ mô hình prior đều. |
| 57 | Nhận xét recall lớp 1 vẫn thấp và đặt giả thuyết cần xem khả năng phân biệt qua likelihood. |
| 58 | Tính bảng log-likelihood Gaussian trung bình theo từng feature cho các mẫu validation thật thuộc lớp 1, dưới tham số của từng lớp trong `model_equal`. |
| 59 | So sánh trung bình một số feature giữa mẫu lớp 1 bị mô hình gốc dự đoán thành lớp 2 và mẫu lớp 2 được dự đoán đúng. |
| 60 | Tổng kết giả thuyết trong notebook: prior thấp và đặc trưng tương đồng có thể góp phần gây nhầm; đây là diễn giải, không phải kết luận nhân quả. |
| 61 | Tiêu đề phần cải thiện mô hình. |
| 62 | Thử 7 giá trị `var_smoothing`; ghi accuracy, balanced accuracy, Macro F1 và recall từng lớp trên validation. |
| 63 | Lấy dòng có Macro F1 validation cao nhất. |
| 64 | Ghép train và validation làm tập huấn luyện cuối. |
| 65 | Khởi tạo GaussianNB `var_smoothing=1e-7` và fit trên train + validation. |
| 66 | Tạo dự đoán trên test. |
| 67 | In các metric, báo cáo phân lớp và confusion matrix trên test. |
| 68 | Kết luận của notebook: sau tinh chỉnh, nhận diện lớp 1 vẫn yếu; tác giả đánh giá GaussianNB không phù hợp với dataset. |

## 3. Kết quả quan sát được trong notebook

- Dữ liệu có **253,680 dòng, 22 cột**; đếm được **23,899 dòng trùng**. Notebook không xóa hoặc xử lý các dòng trùng trong pipeline này.
- Target: lớp 0 có **213,703 (84.24%)**, lớp 1 **4,631 (1.83%)**, lớp 2 **35,346 (13.93%)**. Đây là mất cân bằng lớp rõ rệt.
- Validation của GaussianNB mặc định: accuracy **75.76%**, balanced accuracy **46.36%**, Macro F1 **0.43**. Recall theo lớp 0/1/2 lần lượt **80.41% / 1.30% / 57.37%**. Trong 694 mẫu lớp 1 validation, mô hình đoán đúng 9, đoán thành lớp 0 là 358 và lớp 2 là 327.
- Train accuracy **75.65%**, validation accuracy **75.76%**. Sự gần nhau này chỉ nói accuracy tổng thể tương tự; không đồng nghĩa hiệu quả tốt cho từng lớp.
- Thử prior đều: validation accuracy **68%**; recall lớp 1 tăng lên **12%**, nhưng vẫn thấp. Kết quả cho thấy thay prior trong thử nghiệm này không đưa recall lớp 1 lên mức cao, đồng thời accuracy giảm.
- Quét `var_smoothing`: Macro F1 cao nhất được lưu tại **`1e-7`**, nhưng chỉ khoảng **0.4284**; recall lớp 1 là **1.30%**. Các khác biệt giữa các giá trị rất nhỏ.
- Mô hình cuối trên test: accuracy **75.75%**, balanced accuracy **46.36%**, Macro F1 **0.4313**. Recall lớp 0/1/2 là **80.58% / 2.30% / 56.19%**. Với lớp 1, report cho thấy precision **0.04**, recall **0.02**, F1 **0.03**; confusion matrix cho biết chỉ **16/695** mẫu lớp 1 được nhận diện đúng.

## 4. Kết luận và phân biệt dữ kiện với suy luận

**Kết luận được hỗ trợ trực tiếp bởi output:** mô hình có accuracy tổng thể khoảng 75.7%, nhưng hiệu quả giữa các lớp không đồng đều. Khả năng nhận diện lớp 1 rất thấp ở cả validation mặc định và test cuối. Quét `var_smoothing` không cải thiện đáng kể Macro F1/recall lớp 1. Prior đều làm recall lớp 1 tăng trong validation nhưng vẫn chỉ 12% và accuracy giảm. Vì vậy, theo mục tiêu nhận diện tốt cả ba lớp, kết quả notebook cho thấy mô hình GaussianNB hiện tại chưa đáp ứng tốt, đặc biệt với lớp Prediabetes (class 1).

**Suy luận/giả thuyết, không được thí nghiệm chứng minh nhân quả:** mất cân bằng nhãn và sự giống nhau/chồng lấp của đặc trưng có thể góp phần khiến lớp 1 khó phân biệt. Các bảng trung bình và biểu đồ một vài đặc trưng chỉ gợi ý điều này; chúng không chứng minh rằng đó là nguyên nhân duy nhất. Notebook cũng không so sánh với mô hình khác, nên câu “không phù hợp với dataset” nên hiểu trong phạm vi mô hình và mục tiêu/đánh giá đã thử, không phải kết luận rằng mọi biến thể GaussianNB đều không thể dùng.

## Ghi chú về phạm vi và độ tin cậy

- Notebook dựa vào preprocessing từ “model trước” nhưng trong các cell được xem không có mô tả đủ để xác nhận cụ thể những bước làm sạch nào đã thực hiện. Cell 4 cho thấy dữ liệu hiện tại vẫn có 23,899 bản ghi trùng; không nên gọi dataset này là “sạch” chỉ dựa trên ghi chú ở cell 8.
- Đường dẫn CSV trong cell 2 là đường dẫn máy cá nhân; bản notebook tự nó không đảm bảo có thể chạy lại ở môi trường khác. Bản tổng kết này dựa trên mã và output đã lưu, không chạy lại pipeline.
- Chia train/validation/test có `stratify` và random state cố định. Việc test chỉ được dùng sau khi chọn `var_smoothing` trên validation phù hợp với trình tự thể hiện trong notebook.
