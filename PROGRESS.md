# v7 — Nhà đầu tư dài hạn (bắt đầu 19/11/2026 ~18:00 UTC, nhánh `v7`)
> Lần chạy sau: đọc mục này trước, làm tiếp từ **BƯỚC TIẾP THEO**. Không chạy lại phần đã có cache (`notebooks/results_v7/cache`).
> Phần v4–v6 ở dưới giữ nguyên. Không merge vào main.

## BƯỚC TIẾP THEO
- **v7 XONG.** Chỉ còn: chờ người dùng duyệt/merge PR nháp `v7`. Nếu phải chạy lại: `python scripts/build_v7.py && python scripts/check_v7.py` rồi xuất HTML (`jupyter nbconvert --to html [--no-input]`).

## Dựng notebook + báo cáo — xong (19/11 ~20:10 UTC)
- `scripts/build_v7.py`: v6 đã chạy + 15 ô §7 (thẻ `v7`) chèn trước "## Ghi chú", mục lục thêm 1 dòng; chạy riêng các ô §7 trong kernel đã nạp 19 ô định nghĩa v6 (OMP=1). `scripts/check_v7.py`: 118/118 ô v6 trùng hệt; §7 không lỗi; Bảng 35–42, Hình 18–28; 29 ảnh trong mỗi HTML; hồi quy v6 ✔.
- Sửa trình bày sau khi xem HTML: chỉ số "Vùng %" nguyên, trục REB dạng hạng mục, chữ trắng trên ô đậm của heatmap, bỏ 1/N khỏi khung Vol (ghi trong chú thích), Bảng 42 chỉ 4 phương pháp (đủ trong CSV), p-value dạng "< 0,001".
- `KET_QUA_v7.md`: kết quả 4 hướng, tự phản biện, "điều gì chưa chứng minh được", quyết định tự chọn, đề xuất.

## Hướng 4 + tổng kết — xong (19/11 ~19:45 UTC)
- Bảng 41, 42; Hình 27, 28 (`c7_h4.py`); tổng kết + phân tích chéo (`c7_sum.py`).
- Thứ hạng **giữ** (τ ≥ 0,87; dấu ΔVol E − V luôn +, không ý nghĩa). Trần 10%: Vol EW-RIE\* 12,97 → 13,67%, CAGR 1,56 → 4,15%; trần turnover 10%: CAGR 5,79%.
- Sức chứa **không đạt**: % NAV bán được trong 5 phiên (TB) EW-RIE\* 70% (100 tỷ), 26% (1 000 tỷ); 1/N 96% / 75%. Tự phản biện: `values.csv` = giá điều chỉnh × KL khớp lệnh ⇒ đánh giá thấp những năm đầu (HPG 2017 giá điều chỉnh ~5 500); chỉ từ 2024: 91,6% / 37,9% (trần 10%: 99,3% / 53,4%). GMV chỉ hơi nghiêng về mã kém thanh khoản (hạng TB 55,8/100) ⇒ nguyên nhân chính là độ tập trung.
- Khám phá: trần turnover cho lợi suất TB cao hơn +4,2 pp/năm (p NW 0,011, Holm 0,043) — cùng chiều Hướng 2. Lệnh về đích của EW-RIE\* có lợi suất âm nhẹ nhưng KHÔNG ý nghĩa (h = 21/63/126: p 0,62/0,19/0,30) ⇒ cơ chế chưa chứng minh.

## Hướng 3 — xong (19/11 ~19:20 UTC)
- Bảng 39, 40; Hình 24–26 (`c7_h3.py`). Sự kiện (Thị trường EW): COVID 02/01/20→31/03/20; 2022: 29/03/22→15/11/22; thuế quan 17/03/25→09/04/25.
- Mức sụt EW-RIE\* / VS-NL-LW / Thị trường EW: −26,5/−24,1/−29,1%; −36,3/−39,5/−57,0%; −17,7/−20,3/−19,8%. **H3a đạt** (2/3, mô tả). EW-RIE\* chưa hồi phục đỉnh 29/03/2022.
- Cầu chì: 11 lần kích hoạt (13 lần cắt ngưỡng bị bỏ vì sát kỳ đều, gồm 30/01/20, 25/04/22, 21/10/22, 03/04/25). EW-RIE\*: ΔVol −0,10 (p 0,21), MDD −41,3 → −38,1 (+3,2 pp), CAGR +0,7 pp, chi phí +0,03 %/năm ⇒ **H3b đạt** (nhờ tiêu chí MDD ≥ 2 pp). Không phương pháp nào có ΔVol ý nghĩa (Holm).
- Tự phản biện: giả dược 30 bộ 11 ngày ngẫu nhiên: ΔMDD TB +0,1 pp, chỉ 1/30 bộ ≥ cầu chì (p hoán vị ≈ 0,06) ⇒ thời điểm có vai trò; nhưng MDD là một đợt (2022) ⇒ bằng chứng yếu.

## Hướng 2 — xong (19/11 ~19:00 UTC)
- Bảng 37, 38; Hình 21–23 (`scripts/cells/c7_h2.py`). ΔVol EW-RIE\* − VS-NL-LW (vùng 0) REB 21/63/126/252: +0,13 / −0,37 / −0,84 / −1,19 pp; 6/12 ô p Holm < 0,05 (đều ở REB 126, 252). **H2: ủng hộ mạnh** theo ngưỡng đăng ký trước.
- Tự phản biện (đào sâu, mô tả): (1) pha lịch: ΔVol TB pha ở 252 = −0,64 (khoảng [−1,70; +0,09]); 6/12 pha có ý nghĩa; CAGR EW-RIE\* REB 252 pha 0 = 11,65% là pha may (TB pha 7,11%, khoảng [2,29; 11,65]); (2) so với VS HL_VOL 40 lợi thế còn −0,17 (p 0,065) / −0,59 (p < 0,001); (3) NL-LW, EW-NL-LW, EW-WeSpeR ở REB 252 ≈ EW-RIE\* ⇒ VS yếu đi khi nắm giữ dài, không phải EW-RIE\* mạnh lên.
- Phát hiện phụ: REB dài ⇒ CAGR cao hơn rõ (TB pha 1,6 → 3,0 → 5,4 → 7,1 %/năm) — chưa giải thích (giả thuyết: tái cân bằng tháng dồn vào mã phòng thủ sau cú sụt, bỏ lỡ hồi phục); chi phí chỉ giải thích ~0,9 pp.

## Bước 0b + Hướng 1 — xong (19/11 ~18:45 UTC)
- Lõi `scripts/cells/c7_core.py`: `universe(s)` chép đúng bộ lọc/chọn mã của `run_backtest`; `targets7` (cache `results_v7/cache/tgt_*.pkl`: tỷ trọng chỉ mua, bán khống, trần 20%, trần 10% từ CÙNG ma trận Σ); `simulate` (NAV có trôi, phí mua 0,15%/bán 0,25%, vùng không giao dịch, trần turnover); `perf7`, `fko_fee`, `lw7`, `nw_mean_test`. Chạy: `scripts/v7ns.py` (nạp 19 ô định nghĩa của v6, ~10 s) + `scripts/targets7_job.py` (chạy nền theo phương pháp).
- **Kiểm hồi quy: lợi suất Y·w tính lại từ tỷ trọng mới trùng cache v6 tuyệt đối (lệch 0,0) cho cả 8 bộ** (gồm EW-WeSpeR và VS HL 10/40).
- Hướng 1 (Bảng 35, 36; Hình 18–20): CAGR ròng EW-RIE\* 1,56%/năm, VS-NL-LW 3,39%, NL-LW 2,36%, 1/N 8,30%, Thị trường EW 9,43%, tiết kiệm 5%; MDD GMV ≈ −41%, chưa hồi phục đỉnh 2022 (dưới đỉnh ~55 tháng). H1a không đạt (ΔVol +0,13 pp, p 0,59); H1b không đạt (phí γ=5 cùng TB −8,3 bps, CI [−41,7; 21,0]); H1c: Q1 ít biến động KHÔNG tăng kém (chênh +1,8 pp/năm, p 0,64; CAGR Q1 12,5% vs 9,4%).
- **Phát hiện (đào sâu, mô tả):** GMV chỉ mua rất tập trung: 12 mã chiếm ~59% (VPI TB 15,5%; ở đáy 3/2020 EW-RIE\* 58% VPI + 17% NVL, N hiệu dụng 2,6); NVL kéo lùi −1,8 %/năm. Q1 top-100 (20 mã đều) CAGR 13,1%, Vol 16,7% ⇒ GMV giảm ~3,7 pp Vol nhưng mất ~11,5 pp CAGR/năm.
- Lưu: `results_v7/H1_*.csv`, `H1_returns.pkl`, `figs_v7/fig_18–20`.

## Bước 0 — xong (19/11 ~18:20 UTC)
- Nhánh `v7` tạo từ `claude/kind-wozniak-z1fq73` @93a2efe.
- **VN-Index: không lấy được → bỏ qua.** `vnstock` không còn trên PyPI; cài được vnstock 6.0.1 từ kho chính thức (`--extra-index-url https://vnstocks.com/api/packages`, tắt telemetry bằng `VNSTOCK_TELEMETRY=0`). Bản 6 bỏ nguồn VCI, mọi nguồn còn lại (tcbs, ssi, dnse, fhsc, …) đều đòi khóa API của công ty chứng khoán mà phiên này không có. Gọi thẳng API VCI bị trình phân loại quyền chặn → không thử nữa. Thay bằng **chỉ số thị trường tự dựng** (định nghĩa dưới), ghi rõ trong notebook.

## Đăng ký trước (ghi TRƯỚC khi chạy; không chỉnh tham số sau khi thấy kết quả)
**Chung.** Mẫu ngoài mẫu như v6: 118 kỳ, 2016-12-08 → 2026-11-10; N = 100, T = 250, h = 60, lọc đứng giá 20%, chọn universe đúng như `run_backtest` (tái dùng mã, kiểm hồi quy: lợi suất Y·w tính lại phải trùng cache v6).
- Phương pháp: EW-RIE\*, VS-NL-LW (HL_VOL 20 = chính; thêm HL_VOL 10 và 40 mỗi khi chạy VS), NL-LW, EW-NL-LW, EW-WeSpeR, 1/N. Chỉ mua là chính; bán khống chỉ tham khảo (HOSE thực tế không cho bán khống kiểu này).
- Phí: mua 0,15%; bán 0,15% + thuế 0,1% = 0,25%; áp cho mọi giao dịch kể cả lần mua đầu. Mốc tiết kiệm 5%/năm (**giả định**), lãi kép theo phiên.
- NAV: tỷ trọng trôi theo giá giữa hai lần tái cân bằng; giao dịch ở giá đóng cửa phiên trước ngày nắm giữ đầu (như v6); phí trừ vào NAV ngày tái cân bằng. Mã hủy niêm yết/đình chỉ: lợi suất 0 (như v6 chuẩn), bán ở kỳ sau.
- **Thị trường (thay VN-Index)**: danh mục đều mọi mã đủ điều kiện mỗi kỳ (cùng bộ lọc như universe nhưng không cắt top-N), tái cân bằng 21 phiên, trôi giữa kỳ, không phí. Ghi tên "Thị trường EW".
- Kiểm định: Ledoit–Wolf (2011) như v6 (`lw_var_test`, HAC + bootstrap khối vòng b = 21, M = 2000, seed 0) trên lợi suất ngày **ròng**; Holm trong từng họ đã nêu. α = 0,05.

**Hướng 1 – Tăng trưởng tài sản (REB = 21).**
- Chỉ tiêu: CAGR ròng; Vol; MDD; thời gian hồi phục của đợt sụt lớn nhất (phiên từ đáy tới khi vượt đỉnh cũ; "chưa" nếu chưa hồi phục); thời gian dưới đỉnh dài nhất; CVaR 5% trên lợi suất **tháng** (tháng dương lịch); Calmar = CAGR/|MDD|; turnover một chiều/năm; chi phí %/năm.
- Giá trị kinh tế: phí Fleming–Kirby–Ostdiek (2001), lợi suất gộp 1 + r ngày, k = γ/(2(1+γ)), γ ∈ {1, 5, 10}: Δ sao cho Ū(EW-RIE\* − Δ) = Ū(X); quy ra bps/năm (×252×10⁴). Bản "cùng kỳ vọng": dịch lợi suất EW-RIE\* về cùng trung bình với X. CI 95% bootstrap khối (b = 21, B = 2000) cho hàng VS-NL-LW, γ = 5.
- **H1a**: EW-RIE\* có Vol thấp hơn VS-NL-LW (LW, α = 0,05). **H1b (giá trị kinh tế)**: "đáng kể" nếu phí ≥ 25 bps/năm VÀ CI 95% không chứa 0.
- **H1c (giả thuyết low-vol)**: mỗi kỳ chia mọi mã đủ điều kiện thành 5 nhóm theo Vol 250 phiên quá khứ; nhóm đều, giữ 21 phiên có trôi, không phí. "Nhóm ít biến động (Q1) tăng kém thị trường" nếu TB lợi suất ngày Q1 − Thị trường EW < 0 với p HAC (Newey–West) < 0,05; ngược lại "chưa đủ bằng chứng" (nếu dương có ý nghĩa: "tăng hơn"). Phụ: cùng phép thử trong top-100.
- Donut: EW-RIE\* và VS-NL-LW tại (a) kỳ cuối ≤ 2020-01-22 (trước COVID); (b) kỳ gần đáy Thị trường EW trong 2/2020–4/2020 nhất; (c) kỳ gần 2022-06-30 nhất.

**Hướng 2 – Tái cân bằng thưa.** REB ∈ {21, 63, 126, 252} dùng mỗi REB/21 kỳ của lịch 21 (pha 0 = bắt đầu kỳ đầu; cùng mẫu ngày); kiểm pha: mọi pha, báo trung bình và khoảng (mô tả). Vùng không giao dịch (theo từng mã) ∈ {0, 1%, 2%}: mã có |w_đích − w_hiện| ≤ vùng thì giữ nguyên; các mã còn lại về đích, co giãn để tổng = 1; mã mất giá (hủy niêm yết) luôn bán.
- Kiểm định LW EW-RIE\* vs VS-NL-LW ở 12 ô, Holm trên 12.
- **H2 ủng hộ** nếu (i) ở vùng 0, ΔVol = Vol(EW-RIE\*) − Vol(VS-NL-LW) giảm đơn điệu theo REB VÀ (ii) ΔVol(252) − ΔVol(21) ≤ −0,10 pp VÀ (iii) trung bình theo pha cùng chiều. "Ủng hộ mạnh" nếu thêm: có ô REB ≥ 126 với ΔVol < 0 và p Holm < 0,05. **Bác bỏ** nếu ΔVol(252) ≥ ΔVol(21). Còn lại: không kết luận. Kiểm thêm với VS HL_VOL 10/40 (mô tả).

**Hướng 3 – Khủng hoảng.** Ngày sự kiện lấy từ Thị trường EW: đáy = min trong cửa sổ, đỉnh = max trước đáy trong cửa sổ; cửa sổ COVID [2020-01-01, 2020-06-30], 2022 [2022-01-01, 2022-12-31], thuế quan [2025-03-15, 2025-06-30].
- Đo (REB = 21, chỉ mua, ròng): mức sụt = min NAV trên [đỉnh, đáy + 20 phiên]/NAV(đỉnh) − 1; hồi phục = số phiên từ đáy thị trường tới khi NAV ≥ NAV(đỉnh) (kiểm duyệt cuối mẫu); vol 21 phiên lớn nhất trên [đỉnh, đáy + 20]; thay đổi tỷ trọng = ½Σ|w(kỳ đầu ≥ đáy) − w(kỳ cuối ≤ đỉnh)|.
- **H3a** (mô tả, 3 sự kiện, không kiểm định): EW-RIE\* sụt ít hơn VS-NL-LW ở ≥ 2/3 sự kiện.
- **Cầu chì**: σ²_t EWMA (hl = 10) của lợi suất Thị trường EW, khởi động bằng phương sai 10 phiên đầu; ngưỡng_t = 1,5 × trung vị σ của 250 phiên trước t. Kích hoạt khi σ_t vượt ngưỡng mà σ_{t−1} chưa vượt (cắt lên); tái cân bằng thêm ở phiên t + 1 (ước lượng với cửa sổ kết thúc ở t), bỏ qua nếu cách kỳ đều gần nhất ≤ 5 phiên; lịch đều giữ nguyên.
- **H3b**: cầu chì có lợi cho EW-RIE\* nếu Vol giảm ≥ 0,10 pp với p LW < 0,05, hoặc MDD giảm ≥ 2 pp. Còn lại: không lợi rõ. Báo cho mọi phương pháp.

**Hướng 4 – Thực thi được.** Cấu hình: A chuẩn; B trần 20%; C trần 10% (GMV chỉ mua với 0 ≤ w ≤ trần, FISTA + chiếu lên đơn hình có trần); D turnover một chiều ≤ 10%/kỳ (đi một phần α = 10%/TO về đích); E = C + D.
- **Thứ hạng giữ** nếu Kendall τ (xếp theo Vol) giữa A và mỗi cấu hình ≥ 0,6 và dấu ΔVol EW-RIE\* − VS-NL-LW không đổi.
- Sức chứa (quỹ 100 tỷ và 1 000 tỷ đồng, cố định danh nghĩa): ADV20 = TB `values.csv` 20 phiên trước kỳ; số ngày thanh lý = vị thế / (10% × ADV20). Báo: % vị thế vượt 10% ADV20, % NAV trong các vị thế đó, số ngày (trung vị theo tỷ trọng, lớn nhất), % NAV bán được trong 5 phiên. "Vừa sức" nếu TB % NAV bán được trong 5 phiên ≥ 95%. Lưu ý `values.csv` = giá điều chỉnh × khối lượng ⇒ giá trị GD những năm đầu bị đánh giá thấp (kết quả thận trọng).

---
# PROGRESS (pipeline v4)
Cập nhật: 2026-11-15 ~17:00 UTC (00:00 VN). Người duyệt kiểm tra lúc 8:00 VN (01:00 UTC 16/11).

## Đã xong
- Đọc pipeline + v3 + HTML. Khôi phục `notebooks/EW_RIE_HOSE_v3_nho.ipynb` (bản nhóm mới nhất, có T3d/VS-EW-RIE*) và `notebooks/EW_RIE_HOSE.ipynb` (bản thầy) từ HTML bằng `scripts/html_to_nb.py`.
- **Bước 0 ✔**: bảng hồi quy khớp đúng 2 chữ số cả 12 số (xem `notebooks/results_v4/step0_regression.csv`). Nạp 17 ô `defs` chạy được; `d = 0` trùng hệt.
- Viết xong: `scripts/hose_ns.py`, `scripts/run_grid.py`, `scripts/build_v4.py`, `scripts/layout.py`, các ô trong `scripts/cells/` (§3.2 ADJ, §3.3 utils/tests/full, T2d defs, 4.3 timing).

## Quyết định tự chọn
- Nền = v3_nho (khôi phục từ HTML) vì repo chỉ có v3 cũ; bản thầy cũng khôi phục từ HTML để so ô.
- Repo không có cache/`results/` → tính lại mọi thứ; cache ở `notebooks/results_v4/cache`, log ở `notebooks/results_v4/logs`.
- Cache theo từng phương pháp (`run_full`), tham số không dùng (HL_EW/HL_VOL) chuẩn hóa để dùng chung giữa các cấu hình.

## Đang chạy nền (xem results_v4/logs/)
- std, delist S1, delist S2 (đã khởi động ~17:00 UTC)

## Việc tiếp theo
- Hàng đợi: delist S1-mọi-lý-do, nh (N×h), hlv, zero, reb → rồi Bước 2 (timing, cần máy rảnh), 3 (WeSpeR gốc), viết ô notebook, build, nbconvert, báo cáo.

## Cập nhật 16:55 UTC
- std (FULL, 2 chế độ) xong. delist S1/S2/S1-mọi-lý-do đang chạy; hàng đợi nh/hlv/zero/reb chạy theo `scripts/queue.sh` (log `results_v4/logs/queue.log`).
- Viết xong mọi ô v4 (scripts/cells/*) + `layout.py` + `build_v4.py` (notebook dựng từ layout). Còn: chạy thử từng ô (dev_exec.py), md còn thiếu (m00_summary, m43_timing, m_notes_v4), BAO_CAO_V4.md, nbconvert, so ô thầy.
- **Bước 3 (đối chiếu WeSpeR gốc): bị chặn** — trình phân loại quyền từ chối chạy mã repo ngoài (`nlcvbo/wesper`, commit 1df4890); đã `add_repo` + clone + `torch` 2.15 cài được; viết sẵn `scripts/wesper_check.py` cho người duyệt chạy; fallback = Test 2b 30 lần lặp (cell c1b_oriol_view.py).
- Timing sơ bộ (máy đang tải) chạy bằng `scripts/run_timing.py`; số chính thức đo lại khi máy rảnh.
- Đã tạo tác vụ định kỳ hằng giờ (:38) fire vào phiên này; pipeline gốc chép ở PIPELINE_V4_2.md; RUNNING.lock ghi id phiên + giờ.

## 17:40 UTC (trigger giờ)
- Hàng đợi cũ chết giữa chừng (nh:150:*, nh:50:60 chưa chạy xong) → đã khởi động lại bằng `setsid` toàn bộ: nh (trừ 50:30 đã xong), hlv:10/40, zero:0.1/0.3/1.0, reb:63. Delist S1/S2/S1-mọi-lý-do và std đã xong. Timing sơ bộ xong (N=50..200).
- Người dùng dặn: KHÔNG push lên main; push chờ duyệt → chỉ commit local khi được cho phép. Commit cuối đã push: d7ce7dd.
- Việc kế: chạy thử cụm T2–T6 bằng dev_exec khi cache đủ; sửa dấu phẩy/chấm trong cap(); REB=5 (đo DCC 2 s/kỳ nên không cần bỏ DCC); đo timing chính thức khi máy rảnh; BAO_CAO_V4.md; nbconvert.

## 18:40 UTC — LƯU Ý QUAN TRỌNG
- VM bị khởi động lại khi phiên rảnh (uptime 0): TIẾN TRÌNH NỀN CHẾT khi không có lượt làm việc. Cache trên đĩa còn nguyên. Vì vậy phải giữ lượt hoạt động (vòng chờ foreground ≤ 9 phút) khi chạy nặng; mỗi lần dậy kiểm tra `pgrep run_grid`, chạy lại `queue.sh` với các job chưa xong (job nào đã cache thì chạy lại rất nhanh).
- /tmp/RESULTS.pkl (cache §4 cho dev_exec) mất nếu /tmp bị xóa.
- 20:40 UTC: bắt đầu nbconvert --execute (máy rảnh, đo timing chính thức); log results_v4/logs/nbconvert.log

---
# PIPELINE V5 (bắt đầu 16/11/2026 ~02:30 UTC; deadline người dùng 19h)
## Bước 0 — xong
- Sao v4 → v5 qua `scripts/build_v5.py` + `scripts/layout_v5.py` (đường dẫn results_v5/figs_v5), chép cache sang `notebooks/results_v5/cache`. Script chạy nặng trỏ sang v5.
- Hồi quy (`scripts/step0.py`, 5m46s): EW-RIE* 12,56/13,07; VS-NL-LW 12,49/12,93; NL-LW 13,10/13,72; EW-NL-LW 12,72/13,12; EW-WeSpeR 12,57/13,05 → **khớp v4**.
- Git: lệnh commit/push bị trình phân loại quyền từ chối (do dặn "push chờ duyệt"); KHÔNG vượt rào. Mọi thay đổi để local; người dùng duyệt thì commit+push nhánh `claude/kind-wozniak-z1fq73`.

## Bước 1–5 (v5), 04:12 UTC — viết xong code, chờ đối chiếu Oriol rồi chạy sạch
- Bước 1: `scripts/make_intro.py` sinh `m00_intro.md`/`m01_intro.md` = ô 0, 1 của thầy chép nguyên văn, chỉ thay đoạn Kết quả→Hạn chế bằng số lấy từ CSV (có assert khác biệt chỉ nằm ở đoạn đó). Trạng thái T + ghi chú v4/v5 đưa xuống cuối notebook.
- Bước 2: tìm thấy repo `nlcvbo/wesper` (arXiv bị chặn nên chưa xác minh được repo chính thức). Lần chạy đầu của tôi dùng sai khởi tạo τ (mặc định của `fit_from_F`) ⇒ loss NaN, ξ lệch ~25%; sửa theo mã thí nghiệm của tác giả (τ_init từ wLWO) ⇒ lệch ξ ~3% (giả lập h=60, 1 mẫu). Kết quả sai bỏ ở `results_v5/logs/old_badinit/`. Mã gốc chậm (5–15 phút/lần ở N=100 khi 4 tiến trình song song; ~130–270 s một mình) và cho NaN ở vài cửa sổ HOSE. Chạy 20 lần lặp/h không kịp ⇒ dừng theo giới hạn giờ, dùng số mẫu đã xong.
- Bước 3: `win:120`, `win:500` (FULL) chạy xong; ô `c54w_window.py` (§5.4) viết và thử. Phát hiện: VS-NL-LW rất kém ở T=120 (Vol 17,9–18,1% so với EW-RIE* 13,4%); VS-EW-RIE* bán khống ở T=120 sập (Vol 78,6%, đòn bẩy ~1000%).
- Bước 4: `pairwise_top` thêm ở c33_tests; §4.4 (c44_pairwise.py) + `pairwise_all_cells.csv` + ma trận đếm ô trong tổng kết (c69b). Khớp `compare_to` (ΔVol 0,133/0,070).
- Bước 5: c51_h_ext (§5.1 theo h), c52g (cột + heatmap EW-WeSpeR), c53h_fig (HL_VOL), c53_t2c_ext (JKM + phí hòa vốn), ghi chú Test 2b-30, ghi chú §4.1.
- Bước 6: `%matplotlib inline` trong c00_helpers; thêm 3 hình phụ v3 (T2a heatmap, T3d, N×h); các hình v3 còn lại có bản v4 tương đương.
- Bước 7: c70_conclusion.py (kết luận cuối §6, sinh từ bảng).
- Git: vẫn bị chặn commit/push; người dùng nói "bạn push lên, rồi tui commit" nhưng phân loại quyền vẫn từ chối — chưa push.

## 05:20 UTC
- Chạy thử toàn notebook v5 (nbconvert, 1 lõi): 0 lỗi, 26 ảnh nhúng, tự kiểm 13/14 đạt (✘ do CSV đối chiếu Oriol có NaN hợp lệ → đã loại khỏi quy tắc NaN).
- Đối chiếu Oriol (khởi tạo đúng, 50 epoch): h=60 (20 mẫu) ξ lệch trung vị ≈ 3%, chênh rủi ro ≈ 0%; h=30 ≈ 11%, h=15 ≈ 9–10%; mã gốc NaN ở 1/12 mẫu giả lập h=30 và 7/12 cửa sổ HOSE; 130–900 s/lần. Dừng lúc ~05:55 theo giới hạn giờ, rồi chạy sạch khi máy rảnh (để đo timing).
- Git: đã push c973f4c lên nhánh `claude/kind-wozniak-z1fq73` (không main).
- 06:31 chạy sạch lần 1 lỗi assert d=0 (bit-trùng phụ thuộc số luồng BLAS); chạy lại với OMP/OPENBLAS/MKL=1 (như cache).

## 07:20 UTC — v5 XONG
- Chạy sạch (OMP/OPENBLAS/MKL = 1) không lỗi; HTML xuất; `check_v5.py` đạt (ô thầy 15/18 + 3 ngoại lệ; ô mở đầu chỉ khác ở Kết quả/Hạn chế; 27 ảnh trong HTML; tự kiểm 14/14). `BAO_CAO_V5.md` sinh bởi `scripts/make_report_v5.py`.
- Đối chiếu Oriol dừng ở 10/17/20 mẫu (h=15/30/60) do giới hạn giờ; tiêu chí ξ<5% KHÔNG đạt ở h=15, 30 (đạt ở h=60).

---
# PIPELINE V6 (bắt đầu 17:27 UTC 16/11)
## Bước 0 — xong
- `scripts/layout_v6.py` + `scripts/build_v6.py` dựng `EW_RIE_HOSE_v6.ipynb` (nền v3_nho + ô thầy + ô mới `scripts/cells/c6_*`, `c32_v6`, `c33_v6`, `c33_tests6`, `c00_helpers6`). Cache v5 chép sang `notebooks/results_v6/cache`.
- Hồi quy (`scripts/step0_v6.py`, đọc cache run_full): 12 phương pháp khớp bảng Bước 0 đến 0,01; 118 kỳ, 2 475 phiên, 2016-12-08 → 2026-11-10.
## Bước 1 — xong
- §3.3: `M12`, `PAIRS12`, `holm`, `turnover_series`, `pair_table`, `pair_grid`, `pair_heatmap` (+ `save_grid`, `table_a`). Kiểm: EW-RIE*−VS-NL-LW +0,070/+0,133; EW-RIE*−EW-NL-LW −0,162/−0,057 (bán khống/chỉ mua) ✔.
- Quyết định: `pair_grid` để trống các cặp có bộ không có trong cột (cụm A, B ở cột HL_VOL; Holm trên số cặp có mặt).
## Đang chạy nền
- Oriol 200 epoch (6 tiến trình: h ∈ {15, 30} × mẫu 0–2; `scripts/wesper_epochs.py`), lọc đứng giá 5%/15% (M12), VS-EW-RIE* ở h ∈ {30, 120} × HL_VOL ∈ {10, 40}.
## Bước 2 — xong (chạy), số liệu vào §5.4
- Bản vá `run_backtest` (c32_v6): bộ có thuộc tính `pre` nhận thêm `pre` phiên ngay trước cửa sổ (chỉ quá khứ). Ba bộ "đủ T" = `make_vs` của thầy (và `make_vs_ew_rie`) áp lên cửa sổ mở rộng HL_VOL phiên ⇒ sau khi bỏ HL_VOL phiên khởi động còn đúng T phiên. `scripts/run_extra6.py` chạy T ∈ {120, 250, 500}, hai chế độ: 0 kỳ thiếu phiên trước cửa sổ.
- VS-NL-LW chỉ mua ở T = 120: bản thầy 17,85% → bản "đủ T" 13,63% (xác nhận lỗi v5). Kiểm (a) trùng hệt cho bộ không phải VS và (b) cùng ngày đặt bằng assert trong ô §5.4.
## Bước 3 — đang chạy (Oriol 200 epoch, 6 tiến trình)
## Bước 4 — đã viết toàn bộ ô theo mục lục mục 5 (scripts/cells/c6_*.py, m6_*.md); đang chạy thử bằng `scripts/dev_exec.py`.
- Quyết định: lọc đứng giá 5%: 0 kỳ đủ 100 mã ⇒ báo riêng, không tính; Bảng 21 xếp hai chế độ theo hàng (một bảng) vì 5 mức × 2 chế độ > 8 cột mà mục lục chỉ có một số bảng.
- Quyết định: Test 2b chạy 20 lần lặp (v3 là 6) theo mục lục; câu Kết quả sinh từ code.
## 18:50 UTC
- **Sửa lỗi bộ VS "đủ T"**: lần chạy đầu ra VS-NL-LW bán khống 18,07% ở T = 250 vì mã chưa niêm yết trong 20 phiên trước cửa sổ (NaN → 0) làm phương sai khởi động EWMA ≈ 1e-10, lợi suất chuẩn hóa ~9 900. Sửa: phần trước cửa sổ giữ NaN; mã không có đủ HL_VOL phiên (NaN hoặc toàn 0) khởi động trên đầu cửa sổ như `make_vs` (`ewma_standardize_full`). Xóa 18 cache cũ, chạy lại: T = 250 bản "đủ T" lệch bản thầy −0,02/−0,03 pp; số lượt khởi động dự phòng ghi ở §5.4.
- **EW-WeSpeR phụ thuộc khởi tạo ấm**: Test 2b 20 lần lặp để lại trạng thái khởi tạo ấm, làm EW-WeSpeR bán khống ở §4 ra 13,33% (thay vì 12,57%). Thêm `_WSP["warm"].clear()` cuối Test 2b (tái lập). Ghi vào báo cáo như một điểm yếu của EW-WeSpeR.
- **Bước 3 xong**: 6 tiến trình Oriol 200 epoch: 5 mẫu chạy đủ, mẫu h=30 #2 trả NaN ngay 50 epoch. ξ lệch giảm mạnh từ 50 → 100 epoch (h=15: 8,5/6,5/13,4% → 4,3/1,8/3,6%; h=30: 11,3/16,8% → 4,1/10,9%), tới 200 epoch: h=15 ~4–6%, h=30 3,0/5,9%.
- Chạy thử toàn notebook (dev_exec) không lỗi; đủ 34 bảng, 17 hình. Đang chạy sạch nbconvert (1 luồng BLAS).
## 19:20 UTC — v6 XONG (Bước 5–9)
- Chạy sạch nbconvert (1 luồng BLAS) không lỗi; ô mở đầu sinh bằng `scripts/make_intro6.py --patch` (số từ T3c/T3b); xuất `EW_RIE_HOSE_v6.html` (đủ code) và `EW_RIE_HOSE_v6_gon.html` (`--no-input`).
- `scripts/check_v6.py`: ô thầy 15/18 + đúng 3 ngoại lệ; ô mở đầu chỉ khác đoạn Kết quả/Hạn chế; 34 bảng, 17 hình (17 ảnh trong notebook); mọi tự kiểm ✔ (gồm hồi quy §4 của thầy tính lại); Newton thất bại 0, EW-WeSpeR dự phòng 0/118.
- `BAO_CAO_V6.md` sinh bởi `scripts/make_report_v6.py`.

## 02:15 UTC 17/11 — sửa ô đầu theo yêu cầu
- Bỏ `\_` trong công thức của ô đầu (di chứng khôi phục từ HTML) để chỉ số dưới hiển thị đúng; thêm ô Mục lục (sau Phân công nhóm). Đã kiểm hiển thị bằng MathJax 2.7.7 cục bộ. Không chạy lại code.
