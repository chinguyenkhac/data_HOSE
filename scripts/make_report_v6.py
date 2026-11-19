"""v6 Bước 8: BAO_CAO_V6.md (thư mục gốc repo), mọi số đọc từ notebooks/results_v6/*.csv và check_v6.json."""
import pandas as pd, numpy as np, json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); R = f"{ROOT}/notebooks/results_v6"
f = lambda x, d=2: "–" if pd.isna(x) else f"{x:.{d}f}".replace(".", ","); s = lambda x, d=2: "–" if pd.isna(x) else ("+" if x > 0 else "−" if x < 0 else "") + f(abs(x), d)
PT = pd.read_csv(f"{R}/T3c_pair_table.csv").set_index(["mode", "Cặp"]); B = pd.read_csv(f"{R}/T3b_benchmark.csv").set_index(["Chế độ", "Phương pháp"])
TT = pd.read_csv(f"{R}/T43_timing.csv", index_col=0)
O = pd.read_csv(f"{R}/T1b_oriol_summary.csv", index_col=0).set_index("index"); EP = pd.read_csv(f"{R}/T1b_oriol_epochs.csv", index_col=0)
S34 = pd.read_csv(f"{R}/T_summary_clusters.csv").set_index(["Cụm", "Cặp"]); P32 = pd.read_csv(f"{R}/T5c_periods_DE.csv", index_col=0)
T24 = pd.read_csv(f"{R}/T2d_tableA_scenarios.csv", header=[0, 1], index_col=0); HOLD = pd.read_csv(f"{R}/T2d_events.csv", index_col=0)
C = json.load(open(f"{R}/check_v6.json")); M = ("short_ok", "long_only"); VN = {"short_ok": "Bán khống", "long_only": "Chỉ mua"}
E_ = {m: PT.loc[(m, "EW-RIE* − VS-NL-LW")] for m in M}
b = lambda m, k, c: B.loc[(VN[m], k), c]; e34 = S34.xs("EW-RIE* − VS-NL-LW", level=1).iloc[0]; ms = lambda k: TT.loc[k, "100"]
CR, CXI, CNAN = "chênh rủi ro GMV (gốc/nhóm − 1), TB %", "ξ lệch, trung vị (50 epoch)", "mã gốc không hội tụ (NaN)"
two = lambda fn: f"{fn('short_ok')} / {fn('long_only')}"
L = ["# BAO_CAO_V6 — EW-RIE\\* trên HOSE (bản gọn theo khuôn của thầy)", "",
     "Notebook `notebooks/EW_RIE_HOSE_v6.ipynb` (+ `EW_RIE_HOSE_v6.html` đủ code, `EW_RIE_HOSE_v6_gon.html` không code). HOSE 12/2016–11/2026, 118 kỳ, 2 475 phiên ngoài mẫu; N = 100, T = 250, h = 60, HL_VOL = 20, REB = 21, COST = 0,25%. "
     "Mọi số lấy từ `notebooks/results_v6/*.csv`. ΔVol = Vol(bộ trước) − Vol(bộ sau), pp/năm; hai số = bán khống / chỉ mua.", "",
     "## 1. Bốn ý trả lời thầy", ""]
L += [f"**(1) Cặp EW-RIE\\* vs VS-NL-LW** (T3c: Bảng 26–27, 29, Hình 14; Tổng kết: Bảng 34). ΔVol {two(lambda m: s(E_[m]['ΔVol (pp)']))} pp, p bootstrap {two(lambda m: f(E_[m]['p LW-boot'], 3))}, p Holm (12 cặp) {two(lambda m: f(E_[m]['p Holm']))}: **ngang về rủi ro**. "
      f"Trên {int(e34['Số ô'])} ô độ nhạy/độ vững (N, h, HL_VOL, T, REB, lọc đứng giá), cặp này có ý nghĩa ở {int(e34['Âm có ý nghĩa'] + e34['Dương có ý nghĩa'])} ô (ΔVol < 0 ở {int(e34['ΔVol < 0'])} ô, trung vị {s(e34['ΔVol trung vị (pp)'])}). "
      f"EW-RIE\\* giao dịch ít hơn có ý nghĩa: ΔTurnover {two(lambda m: s(E_[m]['ΔTurnover']))} mỗi kỳ (CI {two(lambda m: '[' + s(E_[m]['Turn CI lo']) + '; ' + s(E_[m]['Turn CI hi']) + ']')}).", "",
      f"**(2) Thời gian chạy** (§4.3, Bảng 12; N = 100, ms mỗi lần ước lượng, trung vị 12 cửa sổ HOSE, 1 luồng BLAS). NL-LW {f(ms('NL-LW'), 1)}, EW-NL-LW {f(ms('EW-NL-LW'), 1)}, VS-NL-LW {f(ms('VS-NL-LW'), 1)}, "
      f"**EW-RIE\\* {f(ms('EW-RIE*'), 0)}**, **EW-WeSpeR {f(ms('EW-WeSpeR'), 0)}** (gọi thẳng, khởi tạo lại mỗi lần, không qua cache), DCC-GARCH {f(ms('DCC-GARCH(1,1)'), 0)}. EW-RIE\\* nhanh hơn EW-WeSpeR {f(ms('EW-WeSpeR') / ms('EW-RIE*'), 1)} lần, chậm hơn NL-LW {f(ms('EW-RIE*') / ms('NL-LW'), 0)} lần.", "",
      f"**(3) Lợi suất ngày hủy niêm yết** (T2d: Bảng 23–24). {len(HOLD)} lượt mã trong universe bị hủy trong kỳ nắm giữ. Cú sốc 0% / −30% / −100% (và −30% mọi lý do) làm Vol đổi tối đa "
      f"{f(max((T24[(VN[m], c)] - T24[(VN[m], 'S0')]).abs().max() for m in M for c in T24[VN[m]].columns), 3)} pp; thứ hạng 12 bộ "
      f"{'không đổi' if all((T24[(VN[m], c)].rank() == T24[(VN[m], 'S0')].rank()).all() for m in M for c in T24[VN[m]].columns) else 'có đổi'}. Hạn chế: 19 mã hủy thiếu giá không bao giờ vào universe.", ""]
ep = lambda h, e: EP[(EP.h == h) & (EP.epoch == e) & EP.loss_finite.astype(bool)].xi_med.median() * 100
L += [f"**(4) Đối chiếu EW-WeSpeR với mã gốc** (§1b, Bảng 2). Repo `nlcvbo/wesper` **chưa xác minh được là repo chính thức** (người giao việc tự kiểm). Rủi ro GMV khớp: chênh trung bình "
      + ", ".join(f"{i}: {s(O.loc[i, CR])}%" for i in O.index if not i.startswith("HOSE")) + f". Trị riêng sau co ξ lệch trung vị (50 epoch): " + ", ".join(f"{i}: {f(O.loc[i, CXI], 1)}%" for i in O.index)
      + f". Chạy tiếp 3 mẫu đến 200 epoch: h = 15: {f(ep(15, 50), 1)}% → {f(ep(15, 100), 1)}% → {f(ep(15, 200), 1)}%; h = 30: {f(ep(30, 50), 1)}% → {f(ep(30, 100), 1)}% → {f(ep(30, 200), 1)}% (một phần độ lệch do mã gốc chưa hội tụ ở 50 epoch). "
      f"Mã gốc không hội tụ (NaN) ở {int(O.loc['HOSE (h = 60)', CNAN])}/{int(O.loc['HOSE (h = 60)', 'số mẫu'])} cửa sổ HOSE.", ""]
# 2. bảng hơn / ngang / kém
p_ = P32[P32["Cặp"] == "EW-RIE* − VS-NL-LW"]; sig = p_[(p_["Giai đoạn"] != "Toàn mẫu") & ((p_["CI lo"] > 0) | (p_["CI hi"] < 0))]
better = "; ".join(f"{r['Giai đoạn']} ({r['Chế độ'].lower()}, {s(r['ΔVol (pp)'])})" for _, r in sig[sig["ΔVol (pp)"] < 0].iterrows())
worse = "; ".join(f"{r['Giai đoạn']} ({r['Chế độ'].lower()}, {s(r['ΔVol (pp)'])})" for _, r in sig[sig["ΔVol (pp)"] > 0].iterrows())
turn_better = all(E_[m]["Turn CI hi"] < 0 for m in M); jk = {m: E_[m]["p JKM"] for m in M}
rows = [("Rủi ro, cấu hình chuẩn", "", f"ΔVol {two(lambda m: s(E_[m]['ΔVol (pp)']))} pp, p Holm {two(lambda m: f(E_[m]['p Holm']))}", "", "Bảng 26–27"),
        ("Rủi ro theo N, h, HL_VOL, T, REB, lọc đứng giá", "", f"có ý nghĩa ở {int(e34['Âm có ý nghĩa'] + e34['Dương có ý nghĩa'])}/{int(e34['Số ô'])} ô; ΔVol < 0 ở {int(e34['ΔVol < 0'])} ô; trung vị {s(e34['ΔVol trung vị (pp)'])} pp (mô tả)", "", "Hình 8, 9, 11, 13; Bảng 34"),
        ("Rủi ro theo giai đoạn", better or "", "các giai đoạn còn lại (CI chứa 0)", worse or "", "Bảng 32, Hình 17 (CI bootstrap, mô tả)"),
        ("Turnover và chi phí giao dịch", (f"ΔTurnover {two(lambda m: s(E_[m]['ΔTurnover']))}/kỳ (CI không chứa 0); chi phí GD {two(lambda m: f(b(m, 'EW-RIE*', 'Chi phí GD %/năm')))} so với {two(lambda m: f(b(m, 'VS-NL-LW', 'Chi phí GD %/năm')))} %/năm") if turn_better else "",
         "" if turn_better else "CI chứa 0", "", "Bảng 25–27"),
        ("Mức tập trung danh mục", "", f"số mã hiệu dụng {two(lambda m: f(b(m, 'EW-RIE*', 'Số mã hiệu dụng'), 1))} so với {two(lambda m: f(b(m, 'VS-NL-LW', 'Số mã hiệu dụng'), 1))}; tỷ trọng max {two(lambda m: f(b(m, 'EW-RIE*', 'Tỷ trọng max %'), 1))}% so với {two(lambda m: f(b(m, 'VS-NL-LW', 'Tỷ trọng max %'), 1))}% (chưa kiểm định)", "", "Bảng 25"),
        ("Thời gian chạy", "", "", f"{f(ms('EW-RIE*'), 0)} ms so với {f(ms('VS-NL-LW'), 1)} ms mỗi lần (N = 100; đo trực tiếp, chênh ~{f(ms('EW-RIE*') / ms('VS-NL-LW'), 0)} lần, không cần kiểm định)", "Bảng 12"),
        ("Lợi nhuận và Sharpe", "", f"Sharpe gộp {two(lambda m: f(b(m, 'EW-RIE*', 'Sharpe')))} so với {two(lambda m: f(b(m, 'VS-NL-LW', 'Sharpe')))}; sau phí {two(lambda m: f(b(m, 'EW-RIE*', 'Sharpe sau phí')))} so với {two(lambda m: f(b(m, 'VS-NL-LW', 'Sharpe sau phí')))}; p JKM {two(lambda m: f(jk[m], 3))} (không có ý nghĩa)" if all(v >= .05 for v in jk.values()) else "", "" if all(v >= .05 for v in jk.values()) else "Sharpe thấp hơn, p JKM < 0,05", "Bảng 22, 25–27")]
L += ["## 2. EW-RIE\\* so với VS-NL-LW: hơn / ngang / kém", "", "Chỉ ghi \"hơn\" hoặc \"kém\" khi có kiểm định hoặc CI ủng hộ (riêng thời gian chạy: đo trực tiếp).", "",
      "| Tiêu chí | Hơn | Ngang | Kém | Nguồn |", "|---|---|---|---|---|"] + [f"| {a} | {b_} | {c} | {d} | {e} |" for a, b_, c, d, e in rows] + [""]
# 3. tự kiểm
L += ["## 3. Tự kiểm (Bước 7)", "",
      f"1. Ô code của thầy: {C['teacher_code_cells']} nguyên vẹn; khác (đúng 3 ngoại lệ cho phép: CONFIG, `RUN_SENS = True`, `PAIRS`): {C['teacher_code_cells_diff']}. Ô mở đầu chỉ khác ở đoạn Kết quả/Hạn chế: **{'đạt' if C['intro0_only_result_block_differs'] else 'không đạt'}**; ô Phân công nhóm nguyên văn: **{'đạt' if C['intro1_verbatim'] else 'không đạt'}**.",
      f"2. Test 1, 2, 2b và mọi assert: lỗi thực thi {len(C['cell_errors'])} → **{'đạt' if not C['cell_errors'] else 'không đạt'}**.",
      f"3. Hồi quy Bước 0: " + "; ".join(l for l in C["selfcheck"] if "Hồi quy" in l) + ".",
      f"4. Số bảng {len(C['bang'])}/34, số hình {len(C['hinh'])}/17 (**{'đạt' if C['bang_ok'] and C['hinh_ok'] else 'không đạt'}**); ảnh nhúng: notebook {C['images_nb']}, HTML đủ code {C['images_EW_RIE_HOSE_v6.html']}, HTML gọn {C['images_EW_RIE_HOSE_v6_gon.html']}.",
      f"5. " + "; ".join(l for l in C["selfcheck"] if "Bảng A" in l or "heatmap" in l) + ".",
      "6. Số trong chữ: mọi câu Kết quả/Kết luận sinh từ code bằng số của bảng ngay trên (không gõ tay); ô mở đầu sinh từ CSV của T3c/T3b sau khi chạy (`scripts/make_intro6.py`).",
      f"7. {'; '.join(C['counts'])}.", "", "Các dòng tự kiểm trong notebook:", ""] + [f"- {l}" for l in C["selfcheck"]] + [""]
L += ["## 4. Việc chưa xong, quyết định đã tự chọn, đề xuất", "",
      "- **Chưa xong:** xác minh repo gốc của EW-WeSpeR (arXiv bị chặn từ phiên chạy); T4 (lý thuyết), VN30/HNX, vế \"không giúp trong GARCH\" của T5; 19 mã hủy thiếu giá.",
      "- **Tự chọn:** (i) bộ VS \"đủ T\": mã không có đủ HL_VOL phiên trước cửa sổ (chưa niêm yết hoặc toàn 0) khởi động EWMA trên đầu cửa sổ như `make_vs` (số lượt ghi ở §5.4); lần cài đầu không xử lý điều này và cho VS-NL-LW 18% ở T = 250, đã sửa. "
      "(ii) Xóa trạng thái khởi tạo ấm của EW-WeSpeR sau Test 2b, vì Test 2b 20 lần lặp làm EW-WeSpeR bán khống ở §4 thành 13,33% (thay vì 12,57%) — EW-WeSpeR nhạy với khởi tạo. "
      "(iii) Lọc đứng giá 5%: không kỳ nào đủ 100 mã ⇒ báo riêng. (iv) Bảng 21 xếp hai chế độ theo hàng để giữ một số bảng. (v) Tổng kết (Bảng 34) bỏ các cột trùng cấu hình chuẩn (h = 60, HL_VOL = 20, REB = 21, T = 250). (vi) Test 2b dùng 20 lần lặp (v3: 6).",
      "- **Đề xuất (không thêm vào notebook):** kiểm định chênh lệch số mã hiệu dụng/tỷ trọng max (bootstrap theo kỳ) để biến dòng \"mức tập trung\" ở mục 2 thành hơn/kém có căn cứ; đo thời gian kèm khoảng tứ phân vị; thử EW-WeSpeR với khởi tạo nguội ở mọi kỳ để đo độ nhạy khởi tạo.", ""]
open(f"{ROOT}/BAO_CAO_V6.md", "w", encoding="utf-8").write("\n".join(L)); print("BAO_CAO_V6.md:", len(L), "dòng")
