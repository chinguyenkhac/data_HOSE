### 4.4 So sánh mọi cặp trong nhóm dẫn đầu (mới, v5)

**Câu hỏi.** Trong nhóm dẫn đầu, có bộ nào thật sự tốt hơn bộ khác không, hay tất cả ngang nhau?

**Làm gì.** `TOP` = 6 bộ có hạng trung bình tốt nhất ở bảng tổng kết độ vững của v4: EW-RIE\*, VS-NL-LW, VS-EW-RIE\*, EW-WeSpeR, EW-NL-LW, VS-RIE. Hàm `pairwise_top` (§3.3) so mọi 15 cặp trên cùng ngày OOS: ΔVol, kiểm định phương sai Ledoit–Wolf (2011) bằng bootstrap khối (b = 21), Jobson–Korkie–Memmel, ΔTurnover, **Holm trên cả 15 cặp** (rộng hơn họ lõi 4 đối thủ của §4.1/T3c nên p Holm ở đây lớn hơn). Cùng cấu hình chuẩn: N = 100, T = 250, h = 60, REB = 21.
