# data_vn30 – VN30: chỉ số, thành phần theo kỳ (point-in-time), OHLCV từng mã

| File | Nội dung |
|---|---|
| `vn30_index.csv` | OHLCV chỉ số VN30, 2015-01-05 → 2026-11-16 (VCI). `value_raw_vci` là số thô, đơn vị không nhất quán giữa các năm – chưa dùng. |
| `vn30_periods.csv` | Các kỳ có hiệu lực (`effective_from/to`), nhãn `quality`, ghi chú nguồn |
| `vn30_membership.csv` | Dạng dài: mỗi kỳ × 30 mã (`effective_from, effective_to, ticker, quality`) |
| `ohlcv/<MÃ>.csv` | OHLCV ngày **đã điều chỉnh** (VCI) của 67 mã từng nằm trong rổ. Khớp `data_hose/prices.csv` (chênh ≤0,2%; VNM lệch hằng số do điều chỉnh sau ngày cào của `data_hose`) |

## Độ tin cậy (`quality`)
- `official`: danh sách 30 mã đọc từ file PDF công bố của HOSE (2/2016, 1/2017, 1/2018, 1/2019, 7/2019, 1/2021, 7/2021, 1/2022, 7/2023, 1/2024, 7/2024, 1/2025, 10/2025, 1/2026).
- `news_inferred`: suy ra từ danh sách HOSE kỳ gần nhất cộng/trừ các thay đổi do báo chí đưa tin (1/2016, 2/2016, 7/2017, 7/2018, 1/2020, 7/2020, 8/2022). Đã kiểm: chuỗi 7/2019 → 1/2020 → 7/2020 khớp đúng danh sách HOSE 1/2021; 7/2017 khớp 1/2018; danh sách HOSE 2/2016 khớp 1/2017 đảo theo ghi chú chính thức.
- `inferred_date_uncertain`: KDH→BCM, xảy ra giữa 8/2022 và 8/2023, ngày đúng chưa rõ (đặt 2023-02-06).
- `vci_current_list`: từ 2026-08-03, lấy từ danh sách VN30 hiện tại của VCI (chưa có file HOSE kỳ 7/2026); ngày hiệu lực là giả định.
- Ngày hiệu lực kỳ 1/2021, 1/2022 là giả định (thứ Hai đầu tháng 2).

## Khoảng trống còn lại (CHƯA có thành phần rổ)
- **2015-01-05 → 2015-07-26**: thiếu danh sách kỳ 1/2015 và các thay đổi kỳ 7/2015. Biết kỳ 1/2015 (hiệu lực 26/1/2015) thêm KBC, HVG, loại EIB, CTG; chưa tìm được thay đổi kỳ 7/2015 (HHS, EIB vào rổ vào khoảng kỳ này).

## Lưu ý
- Một số `ohlcv/` có dữ liệu trước ngày niêm yết (VCI trả lịch sử mã tiền thân, ví dụ VHM từ 2015) → cắt theo `data_hose/security_master.csv` khi dùng.

Code: `scrape/` (`build_vn30_membership.py` tải và đọc PDF HOSE; `fetch_vn30_ohlcv.py`, `fetch_vn30_index.py` cào VCI).
