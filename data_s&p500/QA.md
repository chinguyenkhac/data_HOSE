# QA – data_s&p500

- Kỳ: 2015-01-02 → 2026-11-13, 2985 phiên giao dịch.
- Số danh tính từng thuộc S&P 500 trong kỳ: 751; có giá: 598, không có trên Yahoo: 131, bị loại vì mã đã bị tái sử dụng / chỉ có 1 phiên: 22.
- Số thành phần mỗi ngày (tính cả nhiều lớp cổ phiếu): 502–507.
- Thành phần hiện tại thiếu giá: không có.
- Giá ≤ 0: 0 ô.

## Tỷ lệ thành phần có giá (trung bình theo năm)

Thiếu chủ yếu là các công ty đã bị mua lại / phá sản – Yahoo xoá lịch sử của mã đã hủy niêm yết,
nên dữ liệu những năm đầu vẫn còn **survivorship bias** (xem `delisted.csv`, cột `price_status`).

| Năm | Tỷ lệ |
|---|---|
| 2015 | 77.3% |
| 2016 | 80.9% |
| 2017 | 83.9% |
| 2018 | 86.1% |
| 2019 | 88.5% |
| 2020 | 90.7% |
| 2021 | 92.2% |
| 2022 | 94.0% |
| 2023 | 95.8% |
| 2024 | 96.5% |
| 2025 | 97.7% |
| 2026 | 99.2% |

## Biến động 1 phiên > 50% (cần lưu ý)

Phần lớn là biến động thật (GME 2021, OXY/TRGP 3/2020...). Ngoại lệ đã biết: DHR 2016-07-05
(Yahoo điều chỉnh sai sự kiện tách Fortive). Yahoo không điều chỉnh spin-off một cách nhất quán.

| Mã | Ngày | |ret| |
|---|---|---|
| AAP | 2025-05-22 | 0.57 |
| AMD | 2016-04-22 | 0.523 |
| APA | 2020-03-09 | 0.539 |
| BE | 2024-11-15 | 0.592 |
| BLDR | 2015-04-13 | 0.677 |
| CPRI | 2023-08-10 | 0.557 |
| CVNA | 2023-06-08 | 0.56 |
| DHR | 2016-07-05 | 0.612 |
| ECHO | 2025-08-26 | 0.702 |
| FLR | 2020-03-19 | 0.762 |
| FOSL | 2018-02-14 | 0.877 |
| GL | 2024-04-11 | 0.531 |
| GME | 2021-01-27 | 1.348 |
| HOOD | 2021-08-04 | 0.504 |
| LUMN | 2024-08-06 | 0.931 |
| MRNA | 2026-08-19 | 1.77 |
| NBR | 2020-06-05 | 0.511 |
| NKTR | 2025-06-24 | 1.563 |
| OXY | 2020-03-09 | 0.52 |
| PBI | 2021-01-26 | 0.81 |
| PCG | 2019-01-24 | 0.746 |
| RIG | 2020-06-05 | 0.506 |
| TRGP | 2020-03-09 | 0.529 |

## Xử lý danh tính (mã đổi / mã tái sử dụng)

Xem `scripts/sp500/01_membership.py` (ALIAS, fix) và `ENV.json` → `identity_splits`.
Các danh tính hậu tố `.OLD`/`.21CF` là công ty cũ có mã đã bị công ty khác dùng lại;
chúng có trong `security_master.csv`, `membership_daily.csv` nhưng không có giá.
