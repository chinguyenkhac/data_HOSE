## Ghi chú v5

- **Phiên bản:** v5 = v4 + (Bước 1) phần mở đầu chép nguyên văn của thầy, chỉ đổi đoạn Kết quả/Hạn chế; (2) đối chiếu mã gốc WeSpeR; (3) cửa sổ T §5.4; (4) so sánh mọi cặp §4.4; (5) bảng/hình bổ sung; (6) khôi phục và nhúng đủ hình.
- **Nguồn nền:** bản nhóm `EW_RIE_HOSE_v3_nho` (khôi phục từ HTML đã gửi; repo chỉ có `EW_RIE_HOSE_v3` cũ hơn) và bản của thầy `EW_RIE_HOSE` (cũng khôi phục từ HTML để so ô). Ô của thầy giữ nguyên; ngoại lệ: ô CONFIG, cờ `RUN_SENS`, ba cặp thêm vào `PAIRS` (§4).
- **Phần nặng** chạy bằng `scripts/run_grid.py` (cache từng phương pháp ở `results_v5/cache`, log ở `results_v5/logs`); notebook đọc cache nên chạy sạch nhanh. Cache không đưa lên repo (kích thước), chạy lại bằng `scripts/queue.sh` (xem `PROGRESS.md`).
- **Đối chiếu EW-WeSpeR với mã gốc (v5):** đã chạy `scripts/wesper_check.py` với mã `nlcvbo/wesper` (repo chính thức chưa xác minh được vì arXiv bị chặn); kết quả và tiêu chí đạt/không đạt ở §1b. Lần chạy đầu dùng sai khởi tạo τ, đã bỏ và chạy lại (xem §1b).
- **N = 200** không đưa vào lưới N × h: chỉ 74/129 kỳ tái cân bằng còn đủ 200 mã sau lọc đứng giá 20%. N = 150 có 110 kỳ (không so Vol tuyệt đối giữa các N).
- **Hủy niêm yết:** 19 mã hủy thiếu giá (VCI không còn mã) không bao giờ vào universe; cú sốc −30%/−100% ở T2d là kịch bản quy ước, không phải đo thực nghiệm.
- **p-value trong lưới** (N × h, HL\_VOL, REB, lọc đứng giá, hủy niêm yết) mang tính mô tả, không hiệu chỉnh xuyên lưới; kết luận chính dựa vào cấu hình chuẩn và xu hướng nhất quán.
- **EW-NL-LW (v3)** dùng nhánh p > n của Ledoit–Wolf (2020) khi N > T\_eff (T\_eff = 1/Σw² không nguyên); đây là phép mở rộng hợp lý, không phải kết quả lý thuyết của LW cho trọng số mũ. EW-RIE\* kém ổn định khi q\_eff > 2 (h = 15).
- **Tái lập:** seed cố định; EW-WeSpeR khởi tạo ấm từ kỳ trước nên kết quả phụ thuộc thứ tự chạy ở mức sai số tối ưu (`run_full` xóa khởi tạo ấm đầu mỗi lần chạy). Phiên bản thư viện ở `results_v5/ENV_CONFIG.json`.
- **Chưa làm (để sau):** T4 (lý thuyết), VN30/HNX của T6 (cửa sổ T đã làm ở §5.4), T7. Dữ liệu không mở rộng (chỉ `data_hose/`); 19 mã hủy thiếu giá.
