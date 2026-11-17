# data_vn30 – VN30: chỉ số, thành phần theo kỳ (point-in-time), OHLCV từng mã

| File | Nội dung |
|---|---|
| `vn30_index.csv` | OHLCV chỉ số VN30, 2015-01-05 → 2026-11-16 (VCI). `value_raw_vci` là số thô, đơn vị không nhất quán giữa các năm – chưa dùng. |
| `vn30_periods.csv` | Các kỳ có hiệu lực (`effective_from/to`), nhãn `quality`, ghi chú nguồn |
| `vn30_membership.csv` | Dạng dài: mỗi kỳ × 30 mã (`effective_from, effective_to, ticker, quality`) |
| `ohlcv/<MÃ>.csv` | OHLCV ngày **đã điều chỉnh** (VCI) của 62 mã từng nằm trong rổ. Khớp `data_hose/prices.csv` (chênh ≤0,2%; VNM lệch hằng số do điều chỉnh sau ngày cào của `data_hose`) |

## Độ tin cậy (`quality`)
- `official`: danh sách 30 mã đọc từ file PDF công bố của HOSE.
- `derived_official`: suy ra từ mục "cổ phiếu thêm vào / loại ra" ghi trong chính file HOSE kỳ sau.
- `news_inferred`: suy ra từ báo chí (7/2017, 7/2018, 8/2022); 7/2017 khớp với danh sách HOSE 1/2018.
- `official_assumed_unchanged`: 8/2021–7/2022, giả định kỳ 1/2022 không đổi (chưa tìm được file HOSE).
- `inferred_date_uncertain`: KDH→BCM, xảy ra giữa 8/2022 và 8/2023, ngày đúng chưa rõ (đặt 2023-02-06).
- `vci_current_list`: từ 2026-08-03, lấy từ danh sách VN30 hiện tại của VCI (chưa có file HOSE kỳ 7/2026); ngày hiệu lực là giả định.

## Khoảng trống (CHƯA có thành phần rổ – cần bổ sung/soát)
1. **2015-01-05 → 2016-07-24**: chưa tìm được file HOSE các kỳ 1/2015, 7/2015, 1/2016, 7/2016. Báo chí cho biết kỳ 1/2015 (hiệu lực 26/1/2015) thêm KBC, HVG, loại EIB, CTG.
2. **2020-02-03 → 2021-01-31**: chưa có file kỳ 1/2020 và 7/2020. Các thay đổi giữa danh sách 7/2019 và 1/2021: vào KDH, PDR, PLX, POW, TCH, TPB; ra CTD, DPM, EIB, GMD, ROS, SAB.
3. Một số `ohlcv/` có dữ liệu trước ngày niêm yết (VCI trả lịch sử cổ phiếu tiền thân, ví dụ VHM từ 2015) → khi dùng, cắt theo `data_hose/security_master.csv`.

Code: `scrape/` (`build_vn30_membership.py` tải và đọc PDF HOSE; `fetch_vn30_ohlcv.py`, `fetch_vn30_index.py` cào VCI).
