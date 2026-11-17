## Ghi chú v4

- **Nguồn nền:** bản nhóm `EW_RIE_HOSE_v3_nho` (khôi phục từ HTML đã gửi; repo chỉ có `EW_RIE_HOSE_v3` cũ hơn) và bản của thầy `EW_RIE_HOSE` (cũng khôi phục từ HTML để so ô). Ô của thầy giữ nguyên; ngoại lệ: ô CONFIG, cờ `RUN_SENS`, ba cặp thêm vào `PAIRS` (§4).
- **Phần nặng** chạy bằng `scripts/run_grid.py` (cache từng phương pháp ở `results_v4/cache`, log ở `results_v4/logs`); notebook đọc cache nên chạy sạch nhanh. Cache không đưa lên repo (kích thước), chạy lại bằng `scripts/queue.sh` (xem `PROGRESS.md`).
- **Đối chiếu EW-WeSpeR với mã gốc:** chưa làm được trong phiên chạy đêm (xem §1b); EW-WeSpeR của nhóm vẫn là bản tự cài từ các phương trình của bài, **chưa đối chiếu số với mã gốc**. Cần chạy `scripts/wesper_check.py` trước khi công bố.
- **N = 200** không đưa vào lưới N × h: chỉ 74/129 kỳ tái cân bằng còn đủ 200 mã sau lọc đứng giá 20%. N = 150 có 110 kỳ (không so Vol tuyệt đối giữa các N).
- **Hủy niêm yết:** 19 mã hủy thiếu giá (VCI không còn mã) không bao giờ vào universe; cú sốc −30%/−100% ở T2d là kịch bản quy ước, không phải đo thực nghiệm.
- **p-value trong lưới** (N × h, HL\_VOL, REB, lọc đứng giá, hủy niêm yết) mang tính mô tả, không hiệu chỉnh xuyên lưới; kết luận chính dựa vào cấu hình chuẩn và xu hướng nhất quán.
- **EW-NL-LW (v3)** dùng nhánh p > n của Ledoit–Wolf (2020) khi N > T\_eff (T\_eff = 1/Σw² không nguyên); đây là phép mở rộng hợp lý, không phải kết quả lý thuyết của LW cho trọng số mũ. EW-RIE\* kém ổn định khi q\_eff > 2 (h = 15).
- **Tái lập:** seed cố định; EW-WeSpeR khởi tạo ấm từ kỳ trước nên kết quả phụ thuộc thứ tự chạy ở mức sai số tối ưu (`run_full` xóa khởi tạo ấm đầu mỗi lần chạy). Phiên bản thư viện ở `results_v4/ENV_CONFIG.json`.
- **Chưa làm (để sau):** T4 (lý thuyết), cửa sổ T và VN30/HNX của T6, T7.
