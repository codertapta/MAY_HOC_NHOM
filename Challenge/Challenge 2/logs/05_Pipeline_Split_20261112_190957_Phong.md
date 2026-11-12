# Nhật ký thí nghiệm – 05_Pipeline_Split

| Mục                    | Giá trị                                                   |
| ---------------------- | --------------------------------------------------------- |
| Người chạy             | Ngô Thanh Phong                                           |
| Ngày chạy              | 12/11/2026                                                |
| Giờ bắt đầu – kết thúc | 19:09:47 – 19:09:57 (9.9 giây)                            |
| Notebook               | `05_Pipeline_Split.ipynb`                                 |
| Mục tiêu               | Stratified group split và pipeline tiền xử lý không rò rỉ |
| Môi trường             | Python 3.14.3 · Windows-11-10.0.26300-SP0                 |

## Các bước & kết quả

- raw train=(14396, 18)
- raw test=(3600, 17)
- groups=13166
- StratifiedGroupKFold 5 folds
- holdout macro-F1=0.522346
- accuracy=0.453819
- fold 1: 11516 train / 2880 validation rows, 11 lớp, group-disjoint
- fold 2: 11516 train / 2880 validation rows, 11 lớp, group-disjoint
- fold 3: 11517 train / 2879 validation rows, 11 lớp, group-disjoint
- fold 4: 11517 train / 2879 validation rows, 11 lớp, group-disjoint
- fold 5: 11518 train / 2878 validation rows, 11 lớp, group-disjoint

## Nhận xét

MusicPreprocessor được fit riêng trong pipeline trên từng fold; test không dùng để chọn mô hình
