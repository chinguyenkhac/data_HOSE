# data_s&p500 – S&P 500, 2015-01-02 → 2026-11-13

Mọi mã **từng** thuộc S&P 500 trong kỳ (kể cả mã đã bị loại / hủy niêm yết).
Bảng rộng: hàng = ngày giao dịch NYSE, cột = mã. Ô trống = không có dữ liệu (không nội suy).
Giá bao phủ toàn kỳ khi Yahoo có dữ liệu, không bị cắt theo giai đoạn thuộc chỉ số –
dùng `membership_daily.csv` để lọc.

| File | Nội dung |
|---|---|
| `prices.csv` | giá đóng cửa **đã điều chỉnh** (Adj Close: chia tách + cổ tức), USD |
| `prices_close_unadjusted.csv` | giá đóng cửa Close của Yahoo (chỉ điều chỉnh chia tách), USD |
| `volumes.csv` | khối lượng (cổ phiếu) |
| `membership_daily.csv` | 1 = mã thuộc S&P 500 ngày đó, 0 = không (mọi danh tính, kể cả không có giá) |
| `security_master.csv` | mỗi dòng = 1 giai đoạn thuộc chỉ số: `member_from`, `member_to`, ngày thêm/loại, lý do loại, GICS (với mã hiện tại), `price_status` |
| `index_changes.csv` | lịch sử thay đổi thành phần từ 2015 (thêm/loại, lý do); cột `*_hist` là mã gốc trên Wikipedia, cột không hậu tố là danh tính đã chuẩn hoá |
| `delisted.csv` | các mã đã bị loại khỏi chỉ số, phân loại `removal_type` (acquired_or_merged / index_rebalance / spin_off_related / bankruptcy) và có/không có giá |
| `constituents_current.csv` | danh sách hiện tại (503 mã) |
| `download_report.csv` | trạng thái tải từng mã trên Yahoo |
| `QA.md` | báo cáo kiểm tra |
| `ENV.json` | nguồn, thời điểm cào, phiên bản |
| `raw/` | bản lưu HTML Wikipedia đã dùng (14/11/2026) |

## Nguồn
- Thành phần & lịch sử thay đổi: Wikipedia *List of S&P 500 companies* và *Historical components of the S&P 500* (bản 14/11/2026). Dựng ngược từ danh sách hiện tại.
- Giá/khối lượng: Yahoo Finance qua `yfinance`.

## Hạn chế quan trọng
- **Survivorship bias còn lại**: Yahoo không lưu lịch sử của mã đã hủy niêm yết (bị mua lại, phá sản…). 153/751 danh tính không có giá – chủ yếu các mã bị mua lại. Tỷ lệ thành phần có giá: ~77% (2015) → ~99% (2026). Xem `QA.md`.
- Mã bị công ty khác dùng lại (vd. FB, ADT, APC, BBBY…) được phát hiện và loại bỏ (dữ liệu Yahoo bắt đầu sau ngày vào chỉ số).
- Danh tính hậu tố `.OLD` / `.21CF`: công ty cũ có mã đã bị dùng lại (AGN.OLD, CB.OLD, DOW.OLD, SNDK.OLD, FOXA.21CF, FOX.21CF).
- Lịch sử thay đổi của Wikipedia có thể thiếu một vài sự kiện nhỏ; số thành phần dựng lại 502–507/ngày, khớp kỳ vọng (~503–505 do nhiều lớp cổ phiếu).

Code: `scripts/sp500/01_membership.py` → `02_prices.py` → `03_reports.py`.
