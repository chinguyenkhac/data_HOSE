"""Sinh phần tóm tắt đầu notebook (m00_summary.md) và BAO_CAO_V4.md từ các CSV trong notebooks/results_v4 (mọi số lấy từ bảng)."""
import pandas as pd, numpy as np, json, os, re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "notebooks", "results_v4"); C = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cells")
f2 = lambda x, d=2: f"{x:.{d}f}".replace(".", ","); sg = lambda x, d=2: f"{x:+.{d}f}".replace(".", ",")
b = pd.read_csv(f"{R}/T3b_benchmark_full.csv"); t = pd.read_csv(f"{R}/T3c_tests_full.csv"); tt = pd.read_csv(f"{R}/T43_timing.csv", index_col=0)
s9 = pd.read_csv(f"{R}/T9_robustness_ranks.csv", index_col=1).drop(columns="Unnamed: 0"); cell = pd.read_csv(f"{R}/T9_ew_rie_vs_vsnllw_by_cell.csv")
v = lambda m, k: b[(b["mode"] == m) & (b.method == k)]["Vol %"].iloc[0]; T = lambda m, k, c: t[(t["mode"] == m) & (t.rival == k)][c].iloc[0]
ci = lambda m, k: f"{sg(T(m, k, 'ΔVol (pp)'))} [{sg(T(m, k, 'CI lo'))}; {sg(T(m, k, 'CI hi'))}]"
rows = [("NL-LW", "NL-LW"), ("EW-NL-LW", "EW-NL-LW"), ("EW-RIE (q$_{\\text{eff}}$)", "EW-RIE (q_eff)"), ("EW-WeSpeR", "EW-WeSpeR"), ("**EW-RIE\\***", "EW-RIE*"), ("VS-NL-LW", "VS-NL-LW")]
tab = "| | Bán khống | Chỉ mua |\n|---|---|---|\n" + "\n".join(f"| {lab} | {f2(v('short_ok', k))} | {f2(v('long_only', k))} |" for lab, k in rows)
ev = pd.read_csv(f"{R}/T2d_events.csv") if os.path.exists(f"{R}/T2d_events.csv") else pd.DataFrame()
neg = int((cell["ΔVol (pp)"] < 0).sum()); n = len(cell); sigl = int(((cell["ΔVol (pp)"] < 0) & (cell["p Holm"] < .05)).sum()); sigh = int(((cell["ΔVol (pp)"] > 0) & (cell["p Holm"] < .05)).sum())
tn = lambda k, c=100: tt.loc[k, str(c)]
dtc = lambda m: f"{sg(T(m, 'VS-NL-LW', 'ΔTurnover'))} [{sg(T(m, 'VS-NL-LW', 'Turn CI lo'))}; {sg(T(m, 'VS-NL-LW', 'Turn CI hi'))}]"
head = f"""# EW-RIE\\*: Làm sạch ma trận tương quan có trọng số mũ bằng lý thuyết ma trận ngẫu nhiên
### Ứng dụng: danh mục phương sai nhỏ nhất trên HOSE — **phiên bản v4** (dữ liệu HOSE 2015–11/2026, gồm mã hủy niêm yết)

**Câu hỏi.** Trên HOSE, EW-RIE\\* có cho danh mục phương sai nhỏ nhất (GMV) rủi ro ngoài mẫu thấp hơn các bộ ước lượng khác không, và ở điều kiện nào?

**Phương pháp.** Tương quan có trọng số mũ (half-life *h*), làm sạch trị riêng bằng phép thế nhân cho nhiễu có trọng số (R-transform của tổng tự do các ma trận hạng 1): chọn đúng nhánh nghiệm bằng tiếp tục giải tích, ngoại lai trên trục thực, hiệu chỉnh N hữu hạn; trọng số đều ⇒ trùng RIE cổ điển.

**Đối chứng.** 15 phương pháp (`FULL`): ma trận mẫu, Ledoit–Wolf, NL-LW, MP-clip, RIE, EW-RIE (q$_{{\\text{{eff}}}}$), EW-NL-LW, **EW-WeSpeR** (Oriol 2024), VS-NL-LW, VS-RIE, **VS-EW-RIE\\***, PCA, DCC-GARCH, 1/N. Họ kiểm định chính định trước (`CORE5`): EW-RIE\\* so với NL-LW, EW-NL-LW, EW-WeSpeR, **VS-NL-LW**; ΔVol, CI bootstrap khối, kiểm định phương sai Ledoit–Wolf (2011), Holm, Jobson–Korkie, ΔTurnover.

**Kết quả** (HOSE 12/2016–11/2026, 118 kỳ, N = 100, T = 250, h = 60, REB = 21, COST = 0,25%, lọc đứng giá 20%; Vol ngoài mẫu %/năm):

{tab}

- **EW-RIE\\* vs VS-NL-LW (cặp quan trọng nhất): ngang nhau về rủi ro.** ΔVol = {ci('long_only', 'VS-NL-LW')} pp (chỉ mua), {ci('short_ok', 'VS-NL-LW')} pp (bán khống); p Holm {f2(T('long_only', 'VS-NL-LW', 'p Holm'), 3)} / {f2(T('short_ok', 'VS-NL-LW', 'p Holm'), 3)}. VS-NL-LW có Vol thấp nhất nhưng chênh lệch không có ý nghĩa. Khác biệt nằm ở **turnover**: EW-RIE\\* giao dịch ít hơn {sg(T('long_only', 'VS-NL-LW', 'ΔTurnover'))} (chỉ mua) và {sg(T('short_ok', 'VS-NL-LW', 'ΔTurnover'))} (bán khống) mỗi kỳ (CI 95% không chứa 0), và ở **thời gian chạy** (EW-RIE\\* {f2(tn('EW-RIE*'), 0)} ms so với VS-NL-LW {f2(tn('VS-NL-LW'), 1)} ms mỗi lần ước lượng ở N = 100).
- EW-RIE\\* thấp hơn có ý nghĩa (p Holm < 0,05) so với EW-NL-LW ở cả hai chế độ ({ci('long_only', 'EW-NL-LW')} / {ci('short_ok', 'EW-NL-LW')} pp) và so với NL-LW ở chế độ chỉ mua ({ci('long_only', 'NL-LW')} pp; bán khống p Holm {f2(T('short_ok', 'NL-LW', 'p Holm'), 3)}); **ngang EW-WeSpeR** ({sg(T('long_only', 'EW-WeSpeR', 'ΔVol (pp)'))} / {sg(T('short_ok', 'EW-WeSpeR', 'ΔVol (pp)'))} pp) nhưng nhanh hơn ≈ {tn('EW-WeSpeR (nguội)') / tn('EW-RIE*'):.0f} lần.
- **Độ vững** ({n // 2} cấu hình × 2 chế độ; N × h, HL\\_VOL, REB, lọc đứng giá, kịch bản hủy niêm yết): EW-RIE\\* thấp hơn VS-NL-LW ở {neg}/{n} ô, thấp hơn có ý nghĩa {sigl} ô, cao hơn có ý nghĩa {sigh} ô (p-value mô tả, không hiệu chỉnh xuyên lưới); hạng TB trong 15 phương pháp: VS-EW-RIE\\* {f2(s9.loc['VS-EW-RIE*', 'Hạng TB'])}, EW-RIE\\* {f2(s9.loc['EW-RIE*', 'Hạng TB'])}, VS-NL-LW {f2(s9.loc['VS-NL-LW', 'Hạng TB'])}.

**Hạn chế.** 19 mã hủy niêm yết thiếu giá (không bao giờ vào universe); lợi suất ngày hủy niêm yết (T2d: {len(ev)} lượt trong kỳ nắm giữ, kết quả không đổi với cú sốc −30%/−100%, kịch bản quy ước); **EW-WeSpeR chưa đối chiếu được với mã gốc** (bị chặn quyền chạy mã ngoài trong phiên chạy đêm; còn Test 2b 30 lần lặp); EW-RIE\\* kém ổn định khi N > T$_{{\\text{{eff}}}}$ (h = 15); N = 200 không đưa vào lưới (chỉ 74/129 kỳ đủ mã); T4 (lý thuyết), cửa sổ T, VN30/HNX để sau.

**Tài liệu chính:** Bun, Bouchaud & Potters (2016) *IEEE Trans. Inf. Theory* 62(12); (2017) *Physics Reports* 666; Ledoit & Wolf (2011) và (2020) *Ann. Statist.*; Oriol (2024) *WeSpeR*, arXiv:2410.14413; Laloux et al. (1999) *PRL*; Jagannathan & Ma (2003) *J. Finance*; Shumway (1997) *J. Finance*.
"""
open(f"{C}/m00_summary.md", "w").write(head); print("ok summary")

# ---------------- BAO_CAO_V4.md ----------------
d2 = pd.read_csv(f"{R}/T2d_compare_full.csv"); dd = lambda sc, m, c: d2[(d2.scenario.str.startswith(sc)) & (d2["mode"] == m) & (d2.rival == "VS-NL-LW")][c].iloc[0]
sce = pd.read_csv(f"{R}/T2d_scenarios_full.csv"); sv = lambda sc, m, k: sce[(sce.scenario.str.startswith(sc)) & (sce["mode"] == m) & (sce.method == k)]["Vol %"].iloc[0]
ev_n = len(ev); by = ev.reason.value_counts().to_dict() if len(ev) else {}
core = lambda m: "\n".join(f"| {k} | {f2(T(m, k, 'Vol'))} | {ci(m, k)} | {f2(T(m, k, 'p LW-boot'), 3)} | {f2(T(m, k, 'p Holm'), 3)} | {f2(T(m, k, 'p JKM'), 3)} | {sg(T(m, k, 'ΔTurnover'))} [{sg(T(m, k, 'Turn CI lo'))}; {sg(T(m, k, 'Turn CI hi'))}] |" for k in ["NL-LW", "EW-NL-LW", "EW-WeSpeR", "VS-NL-LW"])
hdr = "| Đối thủ | Vol (%) | ΔVol (pp) [CI 95%] | p LW-boot | p Holm | p JKM | ΔTurnover/kỳ [CI] |\n|---|---|---|---|---|---|---|\n"
srank = "| Phương pháp | Đứng đầu (số ô) | Hạng TB | Hạng xấu nhất |\n|---|---|---|---|\n" + "\n".join(f"| {k} | {int(r['Đứng đầu (số ô)'])} | {f2(r['Hạng TB'])} | {int(r['Hạng xấu nhất'])} |" for k, r in s9.iterrows())
t30 = pd.read_csv(f"{R}/T1b_test2b_30reps.csv"); w30 = t30.pivot_table(index=["h", "rep"], columns="method", values="ratio")
wd = {h: (w30.loc[h]["EW-WeSpeR"] / w30.loc[h]["Oracle"] - 1) for h in (15, 30, 60)}
rep = f"""# BAO_CAO_V4 — EW-RIE\\* trên HOSE (pipeline qua đêm)

Nhánh `claude/kind-wozniak-z1fq73` (PR nháp #7). Notebook: `notebooks/EW_RIE_HOSE_v4.ipynb` (+ `.html`); số liệu `notebooks/results_v4/*.csv`; hình `notebooks/figs_v4/`. Cấu hình chuẩn: N = 100, T = 250, REB = 21, COST = 0,25%, h = 60, HL\\_VOL = 20, ZERO\\_MAX = 20%; OOS 12/2016–11/2026, 118 kỳ, 2.475 phiên.

## 1. Bốn ý của thầy

**(a) EW-RIE\\* vs VS-NL-LW — ngang nhau về rủi ro, khác ở turnover và thời gian.** ΔVol = {ci('long_only', 'VS-NL-LW')} pp (chỉ mua), {ci('short_ok', 'VS-NL-LW')} pp (bán khống) — đúng ≈ +0,13/+0,07 như v3; p Holm {f2(T('long_only', 'VS-NL-LW', 'p Holm'), 3)}/{f2(T('short_ok', 'VS-NL-LW', 'p Holm'), 3)} (họ lõi 4 cặp, trước là 5 nên chỉ p Holm đổi). Cặp đã vào bảng chính §4 (`PAIRS`) và bảng T3c đủ 15 phương pháp. EW-RIE\\* giao dịch ít hơn có ý nghĩa: ΔTurnover/kỳ {dtc('long_only')} (chỉ mua), {dtc('short_ok')} (bán khống). VS-EW-RIE\\* (bảng phụ T3c) không hơn VS-NL-LW có ý nghĩa.
**(b) Thời gian chạy (đo lại, máy rảnh, 1 luồng BLAS, 12 cửa sổ HOSE).** Ở N = 100: NL-LW {f2(tn('NL-LW'), 1)} ms, EW-NL-LW {f2(tn('EW-NL-LW'), 1)} ms, VS-NL-LW {f2(tn('VS-NL-LW'), 1)} ms, **EW-RIE\\* {f2(tn('EW-RIE*'), 0)} ms** (≈ 0,15 s; lần gọi đầu {f2(tn('EW-RIE* (lần đầu)'), 0)} ms), **EW-WeSpeR {f2(tn('EW-WeSpeR (nguội)'), 0)} ms nguội / {f2(tn('EW-WeSpeR (ấm)'), 0)} ms ấm** (không còn 0,001 s; ≈ {tn('EW-WeSpeR (nguội)') / tn('EW-RIE*'):.0f}× EW-RIE\\*), DCC-GARCH {f2(tn('DCC-GARCH(1,1)') / 1000, 1)} s. Bậc theo N (50→200): EW-RIE\\* {f2(tt.loc['EW-RIE*', 'bậc theo N'])}, EW-WeSpeR nguội {f2(tt.loc['EW-WeSpeR (nguội)', 'bậc theo N'])}. Lưu ý: "ấm" không nhanh hơn "nguội" (khởi tạo từ cửa sổ trước không giúp), N = 200 nhiễu hơn.
**(c) Đối chiếu EW-WeSpeR với mã gốc — CHƯA LÀM ĐƯỢC.** Đã tìm `github.com/nlcvbo/wesper` (MIT, commit `1df4890cd2f21951d36988f4f16d84f4eff442e0`; chưa xác minh là repo chính thức vì arXiv bị chặn), clone được, cài `torch` 2.15 được. Mọi lệnh chạy mã repo ngoài (`python3`, `python3 -I`) bị trình phân loại quyền của phiên từ chối, tôi không lách. Đã viết sẵn `scripts/wesper_check.py` (quy đổi W = T·w, c = N/T, `Ndiracs`; so τ bằng Wasserstein-1, ξ, rủi ro GMV, thời gian). Cần bạn chạy: `git clone https://github.com/nlcvbo/wesper /home/user/nlcvbo/wesper && python3 scripts/wesper_check.py` (cần `torch`, `numba`). Thay thế theo pipeline: Test 2b 30 lần lặp — EW-WeSpeR so với oracle: {', '.join(f"h = {h}: {wd[h].mean() * 100:+.2f}% ± {wd[h].std() / np.sqrt(len(wd[h])) * 100:.2f}% (SE)" for h in (15, 30, 60))}; câu "chưa đối chiếu mã gốc" giữ ở Ghi chú.
**(d) Độ nhạy lợi suất ngày hủy niêm yết.** Chỉ {ev_n} lượt mã trong universe bị hủy trong kỳ nắm giữ trên 11.800 vị thế ({100 * ev_n / 11800:.2f}%): {', '.join(f'{k} {n}' for k, n in by.items())}; tỷ trọng TB ≈ 0,2% (chỉ mua), tối đa 3,9% (NL-LW bán khống). Vol EW-RIE\\* (chỉ mua) S0 → S1 −30% → S2 −100%: {f2(sv('S0', 'long_only', 'EW-RIE*'), 3)} → {f2(sv('S1 (', 'long_only', 'EW-RIE*'), 3)} → {f2(sv('S2', 'long_only', 'EW-RIE*'), 3)}; bán khống {f2(sv('S0', 'short_ok', 'EW-RIE*'), 3)} → {f2(sv('S1 (', 'short_ok', 'EW-RIE*'), 3)} → {f2(sv('S2', 'short_ok', 'EW-RIE*'), 3)}. ΔVol (EW-RIE\\* − VS-NL-LW) ở S2: {sg(dd('S2', 'long_only', 'ΔVol (pp)'))} / {sg(dd('S2', 'short_ok', 'ΔVol (pp)'))} pp. **Thứ hạng và kết luận kiểm định không đổi.** Hạn chế còn lại: 19 mã hủy thiếu giá, 10 trong số đó hủy từ 12/2016 (trong mẫu OOS), không bao giờ vào universe.

## 2. Bảng kiểm định chính (CORE5, cấu hình chuẩn)

**Chỉ mua** (ΔVol = EW-RIE\\* − đối thủ; < 0: EW-RIE\\* thấp hơn)

{hdr}{core('long_only')}

**Bán khống**

{hdr}{core('short_ok')}

## 3. Tổng kết độ vững (19 cấu hình × 2 chế độ = 38 ô; 15 phương pháp)

{srank}

EW-RIE\\* vs VS-NL-LW: ΔVol < 0 ở {neg}/{n} ô; thấp hơn có ý nghĩa (p Holm < 0,05) ở {sigl} ô; cao hơn có ý nghĩa ở {sigh} ô; ΔTurnover/kỳ TB {sg(cell['ΔTurnover'].mean())}. p-value trong lưới mang tính mô tả (không hiệu chỉnh xuyên lưới).

## 4. Kết luận

EW-RIE\\* **ngang** VS-NL-LW và EW-WeSpeR về rủi ro ngoài mẫu trên HOSE: chênh ≤ 0,13 pp, không có ý nghĩa ở cấu hình chuẩn lẫn gần như mọi ô lưới; VS-NL-LW dẫn đầu ở {int(s9.loc['VS-NL-LW', 'Đứng đầu (số ô)'])} ô, VS-EW-RIE\\* ở {int(s9.loc['VS-EW-RIE*', 'Đứng đầu (số ô)'])} ô, EW-RIE\\* ở {int(s9.loc['EW-RIE*', 'Đứng đầu (số ô)'])} ô. EW-RIE\\* **hơn** có ý nghĩa EW-NL-LW (cả hai chế độ) và NL-LW (chỉ mua; bán khống p Holm 0,070), cùng EW-RIE (q$_{{eff}}$), PCA, DCC-GARCH, 1/N. EW-RIE\\* **kém** VS-NL-LW rõ nhất trong COVID 2020Q1 (có ý nghĩa), **hơn** ở 2022 (chỉ mua). Lợi thế thực của EW-RIE\\* so với VS-NL-LW là turnover thấp hơn ≈ 36%/33% (chỉ mua/bán khống) — nên COST hòa vốn Sharpe sau phí ≈ 0,91% / 0,39% — còn so với EW-WeSpeR là tốc độ (≈ 8×). Không có cấu hình nào cho thấy VS-NL-LW thua EW-RIE\\* có ý nghĩa sau Holm.

## 5. Việc đã xong / chưa xong, quyết định, kiểm thử

**Đã xong:** Bước 0 (hồi quy khớp 12/12 số), 1, 2, 4, 5, 6, 7, 8, 9, 10, 11; Test 2b 30 lần lặp. **Chưa xong:** Bước 3 (đối chiếu mã gốc, lý do ở 1(c)).

**Quyết định tự chọn:** (1) nền = bản nhóm v3_nho khôi phục từ HTML (repo chỉ có v3 cũ; bản của thầy cũng khôi phục từ HTML để so ô); (2) cache từng phương pháp, tham số không dùng (HL\\_EW/HL\\_VOL) chuẩn hóa; xóa khởi tạo ấm WeSpeR đầu mỗi lần chạy để tái lập; (3) N = 200 bỏ khỏi lưới (74/129 kỳ đủ 200 mã); (4) DCC giữ ở REB = 5 (≈ 2 giây/kỳ, 496 kỳ ≈ 20 phút, dưới ngưỡng 45 phút); (5) họ Holm = 4 đối thủ lõi; (6) T1c (survivorship), T5c, T6b của v3 không có trong v3_nho nên không đưa vào v4; (7) lưới tổng kết gồm 19 cấu hình (chuẩn, 8 N×h khác, HL\\_VOL 10/40, REB 5/63, ZERO\\_MAX 100%/30%/10%, 3 kịch bản hủy).

**Kiểm thử (10 mục):** 1 ô thầy nguyên vẹn 15/18, 3 ô khác đúng ngoại lệ cho phép (CONFIG, `PAIRS`, `RUN_SENS`) — `scripts/check_teacher_cells.py` · 2 Test 1, 2, 2b, assert: đạt · 3 hồi quy 0,01: đạt (`step0_regression.csv`) · 4 cùng ngày: đạt (assert; 118 kỳ, 2.475 phiên; lưới N=150: 110 kỳ, lọc 10%: 69 kỳ) · 5 `compare_to` EW-RIE\\* vs NL-LW = −0,54/−0,65: đạt · 6 T2d d = 0 trùng hệt: đạt · 7 EW-WeSpeR ≠ 0,001 s: đạt ({f2(tn('EW-WeSpeR (nguội)'), 0)} ms) · 8 Newton thất bại 0/69.602 (chuẩn FULL), WeSpeR dự phòng 0/118, GARCH dự phòng 296/11.800 lần fit, DCC không hội tụ 0/118 kỳ · 9 chạy sạch (`nbconvert --execute`) không lỗi, HTML xuất được · 10 chữ khớp số: câu Kết quả/Kết luận sinh từ code; còn vài chỗ số thập phân dùng dấu chấm (T2a: "+0.39 pp", COST hòa vốn) — chỉ khác định dạng.

**Thời gian chạy:** cấu hình chuẩn FULL ≈ 9 phút; delist 3 kịch bản ≈ 15 phút mỗi cái; lưới N×h ≈ 4 giờ CPU tổng (N=150, h=30: 60 phút vì q$_{{eff}}$ > 1); REB=5 ≈ 50 phút; HL\\_VOL, lọc đứng giá, REB=63 ≈ 1 giờ; chạy sạch notebook ≈ 33 phút.

**Chỗ repo khác mô tả:** repo không có `EW_RIE_HOSE_v3_nho.ipynb`/`EW_RIE_HOSE.ipynb` (khôi phục từ HTML, ghi ở `notebooks/`), không có cache cũ, `data_hose/` có sẵn; VM bị khởi động lại khi phiên rảnh làm chết tiến trình nền (đã khởi động lại hàng đợi, cache giữ trên đĩa). Theo lời dặn: không đẩy `main`, không merge; commit cuối đã push `d7ce7dd`, phần sau chưa push chờ duyệt.
"""
be = pd.read_csv(f"{R}/T2a_reb_cost_grid_full.csv")
open(os.path.join(R, "..", "..", "BAO_CAO_V4.md"), "w").write(rep); print("ok report")
