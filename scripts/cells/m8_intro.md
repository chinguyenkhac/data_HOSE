## 8. Lưới siêu tham số (v8)

**Câu hỏi.** Kết luận "EW-RIE\* ngang VS-NL-LW" ở cấu hình chuẩn có còn đúng khi đổi siêu tham số không? Ở điều kiện nào EW-RIE\* đáng dùng? Khi phản ứng "gấp và nhanh" (half-life ngắn, tái cân bằng dày) thì EW-RIE\*, VS-EW-RIE\* và VS-NL-LW ra sao?

**Cách làm.** Dùng đúng universe, bộ ước lượng và GMV của §1–§3. Lợi suất theo quy ước kiểm định v6: tỷ trọng cố định trong kỳ, chưa phí. Ô 8.0 kiểm hồi quy: ở cấu hình chuẩn trùng hệt cache v6. Mọi cấu hình đều có **EW-RIE\*, VS-EW-RIE\*, VS-NL-LW** (+ NL-LW, EW-NL-LW, EW-RIE (q_eff), RIE, VS-RIE). Hai chế độ: bán khống và chỉ mua.

**Các cặp kiểm định** (như v6, đặt tên theo cụm): A1 EW-RIE\* − EW-NL-LW · A2 EW-RIE\* − EW-RIE (q_eff) · B1 EW-NL-LW − NL-LW · B2 EW-RIE\* − RIE · C1 VS-NL-LW − NL-LW · C2 VS-RIE − RIE · **C3 VS-EW-RIE\* − EW-RIE\*** (cùng h: VS có giúp?) · **D1 VS-EW-RIE\* − VS-NL-LW** (cùng HL_VOL: chỉ khác bộ làm sạch) · D2 VS-EW-RIE\* − VS-RIE · D3 VS-RIE − VS-NL-LW · **E1 EW-RIE\* − VS-NL-LW** (cặp chính). A3 (EW-WeSpeR) chỉ có ở cấu hình chuẩn (Bảng 26–27) vì EW-WeSpeR ~1,2 s/kỳ.

| Tầng | Lưới | Đầu ra |
|---|---|---|
| 8.1 Quét từng tham số | HL_VOL {5, 10, 20, 30, 40, 60}; h {15, 30, 45, 60, 90, 120, 250}; T {120, 180, 250, 375, 500, 750}; REB {5, 10, 21, 42, 63, 126, 252}; N {50, 75, 100, 150}; lọc đứng giá {không, 10, 15, 20, 30%} | mỗi tham số 1 bảng Vol + 1 heatmap 11 cặp |
| 8.2 "Gấp và nhanh" | h {15, 30, 60, 120} × HL_VOL {5, 10, 20, 30, 40, 60}, REB 5 và 21 | heatmap E1, D1, C3 + bảng tham số tốt nhất |
| 8.3 Dài hạn | T {120, 250, 500, 750} × REB {5, 21, 63, 252} | heatmap E1, D1, C3 + bảng Vol |
| 8.4 Kiểm định chung, kết luận | TB ΔVol và max\|t\| qua mỗi lần quét | bảng + kết luận theo ngưỡng đăng ký trước |

Giả thuyết H8a–H8c ghi trong `PROGRESS.md` trước khi chạy. Holm: tầng 1 trên 11 cặp mỗi cột; tầng 2–3 trên các ô của lưới cho mỗi cặp × chế độ.
