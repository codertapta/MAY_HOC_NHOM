# Nhật ký thí nghiệm – 05_Pipeline_Split

| Mục                    | Giá trị                                                                           |
| ---------------------- | --------------------------------------------------------------------------------- |
| Người chạy             | Ngô Thanh Phong                                                                   |
| Ngày chạy              | 12/11/2026                                                                        |
| Giờ bắt đầu – kết thúc | 18:49:55 – 18:49:56 (0.6 giây)                                                    |
| Notebook               | `05_Pipeline_Split.ipynb`                                                         |
| Mục tiêu               | Kiểm tra GroupKFold theo group_id và xác nhận hai bộ processed/feature-engineered |
| Môi trường             | Python 3.14.3 · Windows-11-10.0.26300-SP0                                         |

## Các bước & kết quả

- base train=(14396, 35), test=(3600, 33), n_features=32
- FE train=(14396, 37), test=(3600, 35), n_features=34
- 5 folds
- mỗi fold có 11 lớp

## Nhận xét

Fold assignment is group-disjoint; chỉ dùng train để đánh giá; test chưa đánh giá
