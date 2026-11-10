# data_hose – HOSE 2015-01-05 → nay, không survivorship bias

Gồm cả mã đã hủy niêm yết/chuyển sàn, chỉ giữ giai đoạn mã giao dịch trên HOSE (xem `security_master.csv`).
Hàng = ngày, cột = mã. Ngày không giao dịch/đình chỉ = trống (NaN), không nội suy.

| File | Nội dung | Nguồn |
|---|---|---|
| prices.csv | giá đóng cửa ĐÃ điều chỉnh (đồng) | vnstock 5.2.2, VCI |
| volumes.csv | khối lượng khớp lệnh | vnstock, VCI |
| values.csv | **xấp xỉ** giá trị GD = prices × volumes (quyết định (a), 10/11/2026) | tính từ 2 file trên |
| security_master.csv | mỗi dòng = 1 giai đoạn niêm yết trên HOSE: ngày niêm yết/hủy, sàn trước/sau, lý do, nguồn | HSX + Vietstock + VCI |
| missing_tickers.csv | mã trong master không lấy được giá điều chỉnh | |
| QA.md | báo cáo kiểm tra chất lượng | |
| ENV.json | nguồn, thời điểm cào, phiên bản thư viện | |

Code: repo `ew-rie-hose`, thư mục `scrape/`.
