## Ghi chú của nhóm

- **Hạn chế:** 19 mã hủy niêm yết thiếu giá (VCI không còn mã) không bao giờ vào universe; chưa có VN30/HNX; vế "VS không giúp trong GARCH" của T5 chưa mô phỏng; đối chiếu EW-WeSpeR với mã gốc khớp về rủi ro GMV nhưng trị riêng sau co lệch ~10% ở h = 15–30, mã gốc không hội tụ ở 7/12 cửa sổ HOSE, repo `nlcvbo/wesper` chưa xác minh được là repo chính thức (§1b); EW-RIE\* kém ổn định khi N > T\_eff; bộ VS của thầy dùng T − HL\_VOL phiên (§5.4 thêm bản "đủ T"); T5d là cách nhóm hiểu gợi ý (a), cần thầy xác nhận; tham số tự chọn (5.5) chưa tính phí do đổi tham số.
- **Mã hủy niêm yết:** lợi suất các ngày sau ngày giao dịch cuối = 0 (đúng quy ước của thầy); độ nhạy ở T2d.
- **EW-NL-LW** dùng nhánh p > n của Ledoit–Wolf (2020) khi N > T\_eff; T\_eff = 1/Σw² không nguyên.
- **Phần nặng** chạy bằng script nền (`scripts/run_grid.py`, `scripts/run_extra6.py`, `scripts/wesper_check.py`, `scripts/wesper_epochs.py`), cache từng phương pháp ở `results_v6/cache`; notebook đọc cache. p-value ở heatmap và theo giai đoạn mang tính mô tả.
- **Trạng thái các việc T:** T1 (dữ liệu) xong; T2 (REB, phí, lọc đứng giá, hủy niêm yết) xong; T3 (đối chứng, kiểm định 12 cặp) xong; T4 (lý thuyết) chưa làm; T5 (a)–(c) xong, (a) theo cách hiểu của nhóm; T6: N, h, HL\_VOL, cửa sổ T xong, VN30/HNX chưa làm; T7 (viết bài) chưa làm.
