"""Bước 1 (v5): sinh hai ô mở đầu = chép nguyên văn ô 0 và 1 của EW_RIE_HOSE.ipynb (thầy), chỉ thay đoạn từ dòng
'**Kết quả hiện có' đến hết dòng 'Hạn chế: ...' bằng bảng/câu sinh từ CSV. Ghi scripts/cells/m00_intro.md, m01_intro.md."""
import os, re, nbformat, pandas as pd, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); NB = f"{H}/../notebooks"
res = f"{NB}/results_v5" if os.path.exists(f"{NB}/results_v5/T3c_tests_full.csv") else f"{NB}/results_v4"
t = nbformat.read(f"{NB}/EW_RIE_HOSE.ipynb", 4); c0, c1 = t.cells[0].source, t.cells[1].source
B = pd.read_csv(f"{res}/T3b_benchmark_full.csv").set_index(["method", "mode"]); T3 = pd.read_csv(f"{res}/T3c_tests_full.csv")
def f(x, d=2): return f"{x:.{d}f}".replace(".", ",")
def s(x, d=2): return ("+" if x > 0 else "−" if x < 0 else "") + f(abs(x), d)
def pH(p): return "< 0,01" if p < .01 else f"= {f(p)}"
def vol(m, mode): return B.loc[(m, mode), "Vol %"]
def T(r, mode): return T3[(T3["rival"] == r) & (T3["mode"] == mode)].iloc[0]
rows = [("NL-LW", "NL-LW"), ("EW-NL-LW", "EW-NL-LW"), ("EW-RIE ($q\\_{\\text{eff}}$)", "EW-RIE (q_eff)"), ("**EW-RIE\\***", "EW-RIE*"), ("EW-WeSpeR", "EW-WeSpeR"), ("VS-NL-LW", "VS-NL-LW")]
tab = "|  | Bán khống | Chỉ mua |\n| --- | --- | --- |\n" + "\n".join(
    f"| {lab} | " + " | ".join((f"**{f(vol(k, md))}%**" if k == "EW-RIE*" else f"{f(vol(k, md))}%") for md in ("short_ok", "long_only")) + " |" for lab, k in rows)
sk, lo = "short_ok", "long_only"
v, w, e, n = (lambda r: (T(r, sk), T(r, lo)))("VS-NL-LW"), (lambda r: (T(r, sk), T(r, lo)))("EW-WeSpeR"), (lambda r: (T(r, sk), T(r, lo)))("EW-NL-LW"), (lambda r: (T(r, sk), T(r, lo)))("NL-LW")
sec_r, sec_w = B.loc[("EW-RIE*", sk), "Giây/lần ước lượng"], B.loc[("EW-WeSpeR", sk), "Giây/lần ước lượng"]
ST = f"{res}/wesper_status.txt"; status = open(ST, encoding="utf-8").read().strip() if os.path.exists(ST) else "EW-WeSpeR là bản nhóm tự cài, chưa đối chiếu với mã gốc"
PW = f"{res}/pairwise_sentence.txt"; pw = (" " + open(PW, encoding="utf-8").read().strip()) if os.path.exists(PW) else ""
sent = (f"EW-RIE\\* ngang VS-NL-LW và EW-WeSpeR về rủi ro (ΔVol so với VS-NL-LW {s(v[0]['ΔVol (pp)'])} / {s(v[1]['ΔVol (pp)'])} điểm %, p Holm {pH(v[0]['p Holm'])} / {pH(v[1]['p Holm'])}; so với EW-WeSpeR {s(w[0]['ΔVol (pp)'])} / {s(w[1]['ΔVol (pp)'])}, p Holm {pH(w[0]['p Holm'])} / {pH(w[1]['p Holm'])}), "
        f"và thấp hơn có ý nghĩa so với EW-NL-LW ({s(e[0]['ΔVol (pp)'])} / {s(e[1]['ΔVol (pp)'])}, p Holm {pH(e[0]['p Holm'])} / {pH(e[1]['p Holm'])}); so với NL-LW chỉ có ý nghĩa ở chế độ chỉ mua ({s(n[1]['ΔVol (pp)'])}, p Holm {pH(n[1]['p Holm'])}; bán khống {s(n[0]['ΔVol (pp)'])}, p Holm {pH(n[0]['p Holm'])}). "
        f"Turnover mỗi kỳ thấp hơn VS-NL-LW có ý nghĩa ({s(v[0]['ΔTurnover'])} bán khống, {s(v[1]['ΔTurnover'])} chỉ mua; CI 95% không chứa 0) và mỗi lần ước lượng nhanh hơn EW-WeSpeR khoảng {sec_w/sec_r:.0f} lần ({f(sec_r)} s so với {f(sec_w)} s).{pw}")
lim = f"Hạn chế: 19 mã hủy niêm yết không có giá (VCI không còn mã) nên không vào universe; {status}; EW-RIE\\* kém ổn định khi N > T\\_eff (ví dụ h = 15)."
new = ("**Kết quả hiện có (HOSE 12/2016–11/2026, N=100, T=250, h=60):**\n\n" + tab + "\n\n" + sent + "\n" + lim)
i, j = c0.index("**Kết quả hiện có"), c0.index("\n\n**Tài liệu chính")
assert c0[j:].startswith("\n\n**Tài liệu chính")
out0 = c0[:i] + new + c0[j:]
open(f"{H}/cells/m00_intro.md", "w", encoding="utf-8").write(out0); open(f"{H}/cells/m01_intro.md", "w", encoding="utf-8").write(c1)
# kiểm: ngoài đoạn thay, chuỗi trùng ô thầy
assert out0[:i] == c0[:i] and out0.endswith(c0[j:]); print(new)
