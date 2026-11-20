## Mục lục

| Mục | Nội dung | Đầu ra |
|---|---|---|
| **0. Cài đặt & cấu hình** | Thư viện; cấu hình chuẩn: N = 100, T = 250, h = 60, HL\_VOL = 20, REB = 21, phí 0,25%, lọc mã đứng giá 20% | — |
| **1. Thư viện** | 1.1 Mười bộ ước lượng của thầy · 1.2 Bổ sung: EW-NL-LW khi N > T\_eff, EW-WeSpeR (Oriol 2024), VS-EW-RIE\* | — |
| **1b. Kiểm thử** (giả lập) | Test 1, Test 2 của thầy · Test 2b (20 lần lặp, kiểm bản sửa EW-NL-LW và EW-WeSpeR) · Đối chiếu EW-WeSpeR với mã gốc của Oriol | Bảng 1–2 |
| **2. Dữ liệu** (T1) | HOSE 2015–11/2026, gồm mã hủy niêm yết: nạp và lọc khoảng niêm yết, chất lượng dữ liệu, lịch sử niêm yết/hủy, chọn ngưỡng lọc đứng giá | Bảng 3–5, Hình 1–3 |
| **3. Danh mục & backtest** | `run_backtest` của thầy · lọc mã đứng giá (không sửa ô thầy) · tiện ích chung: 12 phương pháp, 12 cặp so sánh định trước (cụm A–E), kiểm định Ledoit–Wolf (2011) + Holm, heatmap cặp | — |
| **4. Chạy chính** | 4.1 Bảng kết quả của thầy (thêm cặp EW-RIE\* vs VS-NL-LW và vs EW-WeSpeR) · 4.2 Hình của thầy · 4.3 Thời gian chạy · 4.4 Phổ trị riêng trước/sau làm sạch | Bảng 6–12, Hình 4–5 |
| **5. Độ nhạy** (T6) | 5.1 Half-life (ô thầy) + lưới N × h · 5.2 Vol 12 phương pháp theo N, h, HL\_VOL · 5.3 Heatmap 12 cặp · 5.3b h × HL\_VOL cho VS-EW-RIE\* · 5.4 Cửa sổ T (sửa lỗi bộ VS khi T nhỏ) · 5.5 Tham số tự chọn từ quá khứ | Bảng 13–18, Hình 6–9 |
| **6. Việc của nhóm** | **T2 Độ vững:** tái cân bằng và phí, lọc đứng giá, phí thực tế, lợi suất ngày hủy niêm yết · **T3 Đối chứng & kiểm định:** 1/N, PCA, DCC-GARCH, kiểm định 12 cặp · **T5 Vì sao VS giúp:** theo giai đoạn, dự báo biến động, cặp chính theo thời gian, phần chung hay phần riêng · **Tổng kết** 12 cặp trên mọi cấu hình | Bảng 19–34, Hình 10–17 |
| **Ghi chú** | Ghi chú của thầy; hạn chế và trạng thái các việc T của nhóm | — |

**Cách đọc:** ΔVol = Vol(bộ trước) − Vol(bộ sau), %/năm; âm là bộ trước rủi ro thấp hơn. Mỗi mục: Câu hỏi → Bảng/Hình → Kết quả → Kết luận. Kết luận chính dựa vào kiểm định ở cấu hình chuẩn (T3c); heatmap và số theo giai đoạn chỉ mang tính mô tả.
