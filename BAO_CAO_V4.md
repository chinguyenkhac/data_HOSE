# BAO_CAO_V4 — EW-RIE\* trên HOSE (pipeline qua đêm)

Nhánh `claude/kind-wozniak-z1fq73` (PR nháp #7). Notebook: `notebooks/EW_RIE_HOSE_v4.ipynb` (+ `.html`); số liệu `notebooks/results_v4/*.csv`; hình `notebooks/figs_v4/`. Cấu hình chuẩn: N = 100, T = 250, REB = 21, COST = 0,25%, h = 60, HL\_VOL = 20, ZERO\_MAX = 20%; OOS 12/2016–11/2026, 118 kỳ, 2.475 phiên.

## 1. Bốn ý của thầy

**(a) EW-RIE\* vs VS-NL-LW — ngang nhau về rủi ro, khác ở turnover và thời gian.** ΔVol = +0,13 [-0,32; +0,63] pp (chỉ mua), +0,07 [-0,31; +0,53] pp (bán khống) — đúng ≈ +0,13/+0,07 như v3; p Holm 0,997/1,000 (họ lõi 4 cặp, trước là 5 nên chỉ p Holm đổi). Cặp đã vào bảng chính §4 (`PAIRS`) và bảng T3c đủ 15 phương pháp. EW-RIE\* giao dịch ít hơn có ý nghĩa: ΔTurnover/kỳ -0,27 [-0,30; -0,24] (chỉ mua), -0,47 [-0,52; -0,41] (bán khống). VS-EW-RIE\* (bảng phụ T3c) không hơn VS-NL-LW có ý nghĩa.
**(b) Thời gian chạy (đo lại, máy rảnh, 1 luồng BLAS, 12 cửa sổ HOSE).** Ở N = 100: NL-LW 1,4 ms, EW-NL-LW 1,5 ms, VS-NL-LW 2,5 ms, **EW-RIE\* 154 ms** (≈ 0,15 s; lần gọi đầu 153 ms), **EW-WeSpeR 1222 ms nguội / 1836 ms ấm** (không còn 0,001 s; ≈ 8× EW-RIE\*), DCC-GARCH 1,8 s. Bậc theo N (50→200): EW-RIE\* 1,02, EW-WeSpeR nguội 1,89. Lưu ý: "ấm" không nhanh hơn "nguội" (khởi tạo từ cửa sổ trước không giúp), N = 200 nhiễu hơn.
**(c) Đối chiếu EW-WeSpeR với mã gốc — CHƯA LÀM ĐƯỢC.** Đã tìm `github.com/nlcvbo/wesper` (MIT, commit `1df4890cd2f21951d36988f4f16d84f4eff442e0`; chưa xác minh là repo chính thức vì arXiv bị chặn), clone được, cài `torch` 2.15 được. Mọi lệnh chạy mã repo ngoài (`python3`, `python3 -I`) bị trình phân loại quyền của phiên từ chối, tôi không lách. Đã viết sẵn `scripts/wesper_check.py` (quy đổi W = T·w, c = N/T, `Ndiracs`; so τ bằng Wasserstein-1, ξ, rủi ro GMV, thời gian). Cần bạn chạy: `git clone https://github.com/nlcvbo/wesper /home/user/nlcvbo/wesper && python3 scripts/wesper_check.py` (cần `torch`, `numba`). Thay thế theo pipeline: Test 2b 30 lần lặp — EW-WeSpeR so với oracle: h = 15: +0.71% ± 0.42% (SE), h = 30: +0.62% ± 0.18% (SE), h = 60: +0.53% ± 0.12% (SE); câu "chưa đối chiếu mã gốc" giữ ở Ghi chú.
**(d) Độ nhạy lợi suất ngày hủy niêm yết.** Chỉ 6 lượt mã trong universe bị hủy trong kỳ nắm giữ trên 11.800 vị thế (0.05%): bat_buoc 6; tỷ trọng TB ≈ 0,2% (chỉ mua), tối đa 3,9% (NL-LW bán khống). Vol EW-RIE\* (chỉ mua) S0 → S1 −30% → S2 −100%: 13,066 → 13,066 → 13,064; bán khống 12,557 → 12,561 → 12,592. ΔVol (EW-RIE\* − VS-NL-LW) ở S2: +0,13 / +0,06 pp. **Thứ hạng và kết luận kiểm định không đổi.** Hạn chế còn lại: 19 mã hủy thiếu giá, 10 trong số đó hủy từ 12/2016 (trong mẫu OOS), không bao giờ vào universe.

## 2. Bảng kiểm định chính (CORE5, cấu hình chuẩn)

**Chỉ mua** (ΔVol = EW-RIE\* − đối thủ; < 0: EW-RIE\* thấp hơn)

| Đối thủ | Vol (%) | ΔVol (pp) [CI 95%] | p LW-boot | p Holm | p JKM | ΔTurnover/kỳ [CI] |
|---|---|---|---|---|---|---|
| NL-LW | 13,72 | -0,65 [-1,03; -0,28] | 0,001 | 0,004 | 0,629 | +0,13 [+0,10; +0,17] |
| EW-NL-LW | 13,12 | -0,06 [-0,09; -0,03] | 0,001 | 0,004 | 0,503 | -0,01 [-0,01; -0,00] |
| EW-WeSpeR | 13,05 | +0,01 [-0,02; +0,05] | 0,498 | 0,997 | 0,595 | +0,00 [-0,00; +0,01] |
| VS-NL-LW | 12,93 | +0,13 [-0,32; +0,63] | 0,573 | 0,997 | 0,052 | -0,27 [-0,30; -0,24] |

**Bán khống**

| Đối thủ | Vol (%) | ΔVol (pp) [CI 95%] | p LW-boot | p Holm | p JKM | ΔTurnover/kỳ [CI] |
|---|---|---|---|---|---|---|
| NL-LW | 13,10 | -0,54 [-0,99; -0,06] | 0,023 | 0,070 | 0,678 | +0,13 [+0,08; +0,19] |
| EW-NL-LW | 12,72 | -0,16 [-0,24; -0,09] | 0,000 | 0,002 | 0,549 | -0,06 [-0,07; -0,05] |
| EW-WeSpeR | 12,57 | -0,01 [-0,09; +0,07] | 0,836 | 1,000 | 0,180 | +0,02 [+0,01; +0,03] |
| VS-NL-LW | 12,48 | +0,07 [-0,31; +0,53] | 0,755 | 1,000 | 0,265 | -0,47 [-0,52; -0,41] |

## 3. Tổng kết độ vững (19 cấu hình × 2 chế độ = 38 ô; 15 phương pháp)

| Phương pháp | Đứng đầu (số ô) | Hạng TB | Hạng xấu nhất |
|---|---|---|---|
| VS-EW-RIE* | 12 | 2,79 | 9 |
| EW-RIE* | 5 | 2,95 | 5 |
| VS-NL-LW | 11 | 3,05 | 8 |
| EW-WeSpeR | 4 | 3,08 | 6 |
| EW-NL-LW | 0 | 5,21 | 10 |
| VS-RIE | 4 | 5,79 | 12 |
| NL-LW | 0 | 9,00 | 12 |
| PCA-auto | 0 | 9,11 | 12 |
| MP-clip | 0 | 9,26 | 13 |
| Ledoit-Wolf | 0 | 9,39 | 11 |
| RIE | 0 | 9,89 | 13 |
| Sample | 0 | 10,24 | 13 |
| EW-RIE (q_eff) | 2 | 11,84 | 14 |
| DCC-GARCH(1,1) | 0 | 13,39 | 14 |
| 1/N | 0 | 15,00 | 15 |

EW-RIE\* vs VS-NL-LW: ΔVol < 0 ở 14/38 ô; thấp hơn có ý nghĩa (p Holm < 0,05) ở 0 ô; cao hơn có ý nghĩa ở 0 ô; ΔTurnover/kỳ TB -0,34. p-value trong lưới mang tính mô tả (không hiệu chỉnh xuyên lưới).

## 4. Kết luận

EW-RIE\* **ngang** VS-NL-LW và EW-WeSpeR về rủi ro ngoài mẫu trên HOSE: chênh ≤ 0,13 pp, không có ý nghĩa ở cấu hình chuẩn lẫn gần như mọi ô lưới; VS-NL-LW dẫn đầu ở 11 ô, VS-EW-RIE\* ở 12 ô, EW-RIE\* ở 5 ô. EW-RIE\* **hơn** có ý nghĩa EW-NL-LW (cả hai chế độ) và NL-LW (chỉ mua; bán khống p Holm 0,070), cùng EW-RIE (q$_{eff}$), PCA, DCC-GARCH, 1/N. EW-RIE\* **kém** VS-NL-LW rõ nhất trong COVID 2020Q1 (có ý nghĩa), **hơn** ở 2022 (chỉ mua). Lợi thế thực của EW-RIE\* so với VS-NL-LW là turnover thấp hơn ≈ 36%/33% (chỉ mua/bán khống) — nên COST hòa vốn Sharpe sau phí ≈ 0,91% / 0,39% — còn so với EW-WeSpeR là tốc độ (≈ 8×). Không có cấu hình nào cho thấy VS-NL-LW thua EW-RIE\* có ý nghĩa sau Holm.

## 5. Việc đã xong / chưa xong, quyết định, kiểm thử

**Đã xong:** Bước 0 (hồi quy khớp 12/12 số), 1, 2, 4, 5, 6, 7, 8, 9, 10, 11; Test 2b 30 lần lặp. **Chưa xong:** Bước 3 (đối chiếu mã gốc, lý do ở 1(c)).

**Quyết định tự chọn:** (1) nền = bản nhóm v3_nho khôi phục từ HTML (repo chỉ có v3 cũ; bản của thầy cũng khôi phục từ HTML để so ô); (2) cache từng phương pháp, tham số không dùng (HL\_EW/HL\_VOL) chuẩn hóa; xóa khởi tạo ấm WeSpeR đầu mỗi lần chạy để tái lập; (3) N = 200 bỏ khỏi lưới (74/129 kỳ đủ 200 mã); (4) DCC giữ ở REB = 5 (≈ 2 giây/kỳ, 496 kỳ ≈ 20 phút, dưới ngưỡng 45 phút); (5) họ Holm = 4 đối thủ lõi; (6) T1c (survivorship), T5c, T6b của v3 không có trong v3_nho nên không đưa vào v4; (7) lưới tổng kết gồm 19 cấu hình (chuẩn, 8 N×h khác, HL\_VOL 10/40, REB 5/63, ZERO\_MAX 100%/30%/10%, 3 kịch bản hủy).

**Kiểm thử (10 mục):** 1 ô thầy nguyên vẹn 15/18, 3 ô khác đúng ngoại lệ cho phép (CONFIG, `PAIRS`, `RUN_SENS`) — `scripts/check_teacher_cells.py` · 2 Test 1, 2, 2b, assert: đạt · 3 hồi quy 0,01: đạt (`step0_regression.csv`) · 4 cùng ngày: đạt (assert; 118 kỳ, 2.475 phiên; lưới N=150: 110 kỳ, lọc 10%: 69 kỳ) · 5 `compare_to` EW-RIE\* vs NL-LW = −0,54/−0,65: đạt · 6 T2d d = 0 trùng hệt: đạt · 7 EW-WeSpeR ≠ 0,001 s: đạt (1222 ms) · 8 Newton thất bại 0/69.602 (chuẩn FULL), WeSpeR dự phòng 0/118, GARCH dự phòng 296/11.800 lần fit, DCC không hội tụ 0/118 kỳ · 9 chạy sạch (`nbconvert --execute`) không lỗi, HTML xuất được · 10 chữ khớp số: câu Kết quả/Kết luận sinh từ code; còn vài chỗ số thập phân dùng dấu chấm (T2a: "+0.39 pp", COST hòa vốn) — chỉ khác định dạng.

**Thời gian chạy:** cấu hình chuẩn FULL ≈ 9 phút; delist 3 kịch bản ≈ 15 phút mỗi cái; lưới N×h ≈ 4 giờ CPU tổng (N=150, h=30: 60 phút vì q$_{eff}$ > 1); REB=5 ≈ 50 phút; HL\_VOL, lọc đứng giá, REB=63 ≈ 1 giờ; chạy sạch notebook ≈ 33 phút.

**Chỗ repo khác mô tả:** repo không có `EW_RIE_HOSE_v3_nho.ipynb`/`EW_RIE_HOSE.ipynb` (khôi phục từ HTML, ghi ở `notebooks/`), không có cache cũ, `data_hose/` có sẵn; VM bị khởi động lại khi phiên rảnh làm chết tiến trình nền (đã khởi động lại hàng đợi, cache giữ trên đĩa). Theo lời dặn: không đẩy `main`, không merge; commit cuối đã push `d7ce7dd`, phần sau chưa push chờ duyệt.
