# Kết quả v8 — Lưới siêu tham số

Notebook: `EW_RIE_HOSE_v8.ipynb` (+ `EW_RIE_HOSE_v8.html`, `EW_RIE_HOSE_v8_gon.html`) = v7 giữ nguyên (133/133 ô trùng hệt) + **phần 8**. Nhánh `v8`, không merge.

## Đã làm
- 99 cấu hình × 2 chế độ (chỉ mua, bán khống), 211 bộ tỷ trọng, **1 154 kiểm định** Ledoit–Wolf (bootstrap khối b = 21, M = 2 000). Mọi cấu hình đều có **EW-RIE\*, VS-EW-RIE\*, VS-NL-LW** (+ NL-LW, EW-NL-LW, EW-RIE (q_eff), RIE, VS-RIE). Lợi suất theo quy ước kiểm định của v6 (tỷ trọng cố định trong kỳ, chưa phí). Ở cấu hình chuẩn, kết quả trùng hệt cache v6 cho 8 bộ × 2 chế độ.
- Các cặp: A1 EW-RIE\*−EW-NL-LW, A2 EW-RIE\*−EW-RIE(q_eff), B1, B2 EW-RIE\*−RIE, C1, C2, **C3 VS-EW-RIE\*−EW-RIE\*** (cùng h), **D1 VS-EW-RIE\*−VS-NL-LW** (cùng HL_VOL: chỉ khác bộ làm sạch), D2, D3, **E1 EW-RIE\*−VS-NL-LW**. Riêng A3 (EW-WeSpeR) chỉ có ở cấu hình chuẩn, vì bộ này mất khoảng 1,2 giây mỗi kỳ.
- Tầng 1: quét từng tham số — HL_VOL {5, 10, 20, 30, 40, 60}; h {15, 30, 45, 60, 90, 120, 250}; T {120, 180, 250, 375, 500, 750}; REB {5, 10, 21, 42, 63, 126, 252}; N {50, 75, 100, 150}; lọc đứng giá {không, 10, 15, 20, 30%}. Tầng 2 "gấp và nhanh": h × HL_VOL ở REB 5 và 21. Tầng 3: T × REB. Kiểm định chung cho mỗi lần quét: trung bình ΔVol và max|t|.
- Notebook có 9 bảng (Bảng 43–51), 9 hình (Hình 29–37) và 18 đoạn nhận xét ngay dưới bảng/hình. Giả thuyết H8a–c được ghi trước khi chạy.
- **Sửa một lỗi đã biết:** ở T nhỏ, bộ VS bản gốc bỏ mất HL_VOL phiên ⇒ T = 120 cho kết quả vô lý (D1 bán khống +60 pp). Các ô có thay đổi T dùng bản VS "đủ T" của §5.4 (quyết định ghi trong PROGRESS.md).

## Kết quả chính (ΔVol tính bằng pp/năm; âm = bộ đứng trước rủi ro thấp hơn)
1. **EW-RIE\* luôn thắng các bản xấp xỉ cùng họ** (A1, A2, B2): có ý nghĩa ở 70–85% số ô của mọi lần quét, trung bình −0,75 đến −1,0 pp. Kết luận này vững nhất.
2. **E1 (EW-RIE\* − VS-NL-LW) không phân biệt được ở 174/198 ô.** Các ô có ý nghĩa (Holm):
   - EW-RIE\* **thấp hơn** (12 ô): REB = 126 và 252 (cả hai chế độ, −0,9 đến −1,25), T = 750, và lưới T × REB ở REB 252 (T 250, 500, 750; tới −1,78 ở T = 500).
   - EW-RIE\* **cao hơn** (12 ô): chỉ khi **h = 15 và cho bán khống** (+2,0 đến +2,9). Với 100 mã, trọng số mũ quá ngắn làm T_eff ≈ 43 < N.
   - Các tham số HL_VOL, N và lọc đứng giá: không ô nào có ý nghĩa; kiểm định chung cũng không có ý nghĩa.
3. **Kiểm định chung** (không chọn ô đẹp): E1 có ý nghĩa ở quét REB (trung bình −0,37 / −0,27, p 0,008 / 0,034), quét T (bán khống: p max|t| 0,017), và quét h (bán khống: trung bình +0,48, do h = 15).
4. **"Gấp và nhanh"** (REB 5–21, h và HL_VOL ngắn): chỉ mua không ô E1 nào có ý nghĩa. Nếu chỉnh mỗi bộ về tham số tốt nhất (nhìn trước nên lạc quan), Vol chỉ giảm ≤ 0,15 pp, và **VS-EW-RIE\* cho Vol thấp nhất ở cả 4 tổ hợp REB × chế độ**.
5. **D1 (bộ làm sạch, khi đã VS):** gần 0 ở cấu hình nhanh; có ý nghĩa **âm** (RIE\* tốt hơn NL-LW) ở T dài hoặc REB dài.
6. **C3 (thêm VS vào EW-RIE\*):** gần 0 hoặc hơi âm khi nhanh; **dương có ý nghĩa** (VS làm hại) khi REB ≥ 63, lên tới +1,5 ở T = 500, REB = 252.

**Theo ngưỡng đăng ký trước:**
- **H8a đạt.** Spearman giữa ΔVol E1 và T là −0,49, với REB là −1,00.
- **H8b không đạt.** D1 có ý nghĩa ở 11/96 ô, nên bộ làm sạch có tạo khác biệt ở một số cấu hình.
- **H8c không đạt.** Ở vùng "gấp và nhanh", E1 > 0 ở 75% ô (chỉ mua) và 50% ô (bán khống), nhưng không ô chỉ mua nào có ý nghĩa.

## Khi nào nên dùng EW-RIE\*
- **Nên dùng:** khi nắm giữ dài (REB ≥ 126, hoặc T ≥ 500 kết hợp REB ≥ 63). Khi đó EW-RIE\* thấp hơn VS-NL-LW khoảng 1–1,8 pp và có ý nghĩa; thêm VS vào lại làm hại. Ngoài ra EW-RIE\* luôn giao dịch ít hơn và luôn hơn các bản xấp xỉ cùng họ.
- **Không có lợi thế:** khi tái cân bằng dày (REB 5–21) với T = 250. Ở vùng này EW-RIE\*, VS-EW-RIE\* và VS-NL-LW ngang nhau; nếu phải chọn thì VS-EW-RIE\* nhỉnh nhất.
- **Tránh:** h quá ngắn (15) ở chế độ bán khống.

## Tự phản biện / chưa chứng minh được
- Lợi suất chưa trừ phí và giữ tỷ trọng cố định trong kỳ. Hướng 2 của v7 (có phí, có trôi tỷ trọng) cho cùng chiều ở REB dài, nhưng kết quả nhạy với pha của lịch tái cân bằng; ở v8 chưa kiểm pha.
- Mỗi T có mẫu ngoài mẫu riêng: T = 750 bắt đầu muộn hơn và bỏ qua giai đoạn 2016–2017.
- Bảng "tham số tốt nhất" chọn sau khi nhìn kết quả nên lạc quan. Muốn công bằng hơn cần chọn tham số theo quá khứ (walk-forward) cho cả h lẫn HL_VOL; việc này chưa làm.
- EW-WeSpeR (A3) chưa có trên lưới.
- Chưa có kiểm định tương đương (TOST) cho các ô E1 không phân biệt được.
