"""v6 Bước 5: ô mở đầu = ô 0 của thầy chép nguyên văn, chỉ thay đoạn từ '**Kết quả hiện có' đến hết dòng 'Hạn chế: ...'. Số lấy từ CSV của notebook v6 đã chạy.
Ghi scripts/cells/m6_intro0.md; nếu có --patch thì thay luôn ô 0 của notebooks/EW_RIE_HOSE_v6.ipynb (đã thực thi)."""
import os, sys, nbformat, pandas as pd, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); NB = f"{H}/../notebooks"; R = f"{NB}/results_v6"
t = nbformat.read(f"{NB}/EW_RIE_HOSE.ipynb", 4); c0 = t.cells[0].source
B = pd.read_csv(f"{R}/T3b_benchmark.csv").set_index(["Chế độ", "Phương pháp"]); PT = pd.read_csv(f"{R}/T3c_pair_table.csv").set_index(["mode", "Cặp"])
f = lambda x, d=2: f"{x:.{d}f}".replace(".", ","); s = lambda x, d=2: ("+" if x > 0 else "−" if x < 0 else "") + f(abs(x), d)
pH = lambda p: "< 0,01" if p < .01 else f"= {f(p)}"
vol = lambda k, m: B.loc[(m, k), "Vol %"]; pr = lambda m, p: PT.loc[(m, p)]
rows = [("NL-LW", "NL-LW"), ("EW-NL-LW", "EW-NL-LW"), ("EW-RIE ($q\\_{\\text{eff}}$)", "EW-RIE (q_eff)"), ("EW-WeSpeR", "EW-WeSpeR"), ("VS-NL-LW", "VS-NL-LW"), ("**EW-RIE\\***", "EW-RIE*")]
tab = "|  | Bán khống | Chỉ mua |\n| --- | --- | --- |\n" + "\n".join(
    f"| {lab} | " + " | ".join((f"**{f(vol(k, m))}%**" if k == "EW-RIE*" else f"{f(vol(k, m))}%") for m in ("Bán khống", "Chỉ mua")) + " |" for lab, k in rows)
# CI của EW-RIE* − NL-LW: bảng CI của thầy (Bảng 8, 11) lưu ở rmt_work? tính lại từ ΔVol của bảng benchmark + CI trong T3c không có ⇒ dùng ΔVol của Bảng 25 và CI của ô thầy (CSV ci_*.csv nếu có)
a, e_, w_ = ("short_ok", "long_only"), "EW-RIE* − VS-NL-LW", "EW-RIE* − EW-WeSpeR"
n_ = {m: vol("EW-RIE*", mm) - vol("NL-LW", mm) for m, mm in zip(a, ("Bán khống", "Chỉ mua"))}
CI = {m: pd.read_excel(f"{NB}/rmt_work/results_N100_T250_h60.xlsx", sheet_name=f"{m}_CI", index_col=0).loc["EW-RIE* vs NL-LW"] for m in a}   # bảng CI của ô thầy (Bảng 8, 11)
nsig = {m: bool(CI[m]["CI 97.5%"] < 0) for m in a}
ew = {m: pr(m, "EW-RIE* − EW-NL-LW") for m in a}; vs = {m: pr(m, e_) for m in a}; ws = {m: pr(m, w_) for m in a}
sent = (f"EW-RIE\\* có rủi ro thấp hơn EW-NL-LW có ý nghĩa (ΔVol {s(ew['short_ok']['ΔVol (pp)'])} / {s(ew['long_only']['ΔVol (pp)'])} điểm %, bán khống / chỉ mua; p Holm {pH(ew['short_ok']['p Holm'])} / {pH(ew['long_only']['p Holm'])}) "
        f"và thấp hơn NL-LW ({s(n_['short_ok'])} / {s(n_['long_only'])} điểm %; CI 95% bootstrap khối của thầy {'không chứa 0 ở cả hai chế độ' if all(nsig.values()) else 'chứa 0 ở ít nhất một chế độ'}). "
        f"So với VS-NL-LW và EW-WeSpeR, chênh lệch rủi ro không có ý nghĩa (ΔVol {s(vs['short_ok']['ΔVol (pp)'])} / {s(vs['long_only']['ΔVol (pp)'])} và {s(ws['short_ok']['ΔVol (pp)'])} / {s(ws['long_only']['ΔVol (pp)'])} điểm %; p Holm {pH(vs['short_ok']['p Holm'])} / {pH(vs['long_only']['p Holm'])} và {pH(ws['short_ok']['p Holm'])} / {pH(ws['long_only']['p Holm'])}). "
        f"Turnover mỗi kỳ của EW-RIE\\* thấp hơn VS-NL-LW ({s(vs['short_ok']['ΔTurnover'])} / {s(vs['long_only']['ΔTurnover'])}; CI 95% {'không chứa 0' if (vs['short_ok']['Turn CI hi'] < 0 and vs['long_only']['Turn CI hi'] < 0) else 'chứa 0 ở ít nhất một chế độ'}).")
lim = ("Hạn chế: 19 mã hủy niêm yết thiếu giá; chưa có VN30/HNX; EW-RIE\\* kém ổn định khi N > T\\_eff; EW-WeSpeR khớp mã gốc về rủi ro GMV nhưng trị riêng sau co lệch ~10% ở h = 15–30 (repo gốc chưa xác minh).")
new = "**Kết quả hiện có (HOSE 12/2016–11/2026, N=100, T=250, h=60):**\n\n" + tab + "\n\n" + sent + "\n" + lim
i, j = c0.index("**Kết quả hiện có"), c0.index("\n\n**Tài liệu chính"); out0 = c0[:i] + new + c0[j:]
assert out0[:i] == c0[:i] and out0.endswith(c0[j:])
open(f"{H}/cells/m6_intro0.md", "w", encoding="utf-8").write(out0); print(new)
if "--patch" in sys.argv:
    p = f"{NB}/EW_RIE_HOSE_v6.ipynb"; nb = nbformat.read(p, 4); assert nb.cells[0].cell_type == "markdown" and nb.cells[0].source.startswith("# EW-RIE"); nb.cells[0].source = out0; nbformat.write(nb, p); print("đã thay ô 0")
