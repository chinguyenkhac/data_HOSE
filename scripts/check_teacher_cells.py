"""Kiểm thử 1: so từng ô mã của bản thầy với v4. In ô khác (diff) và kết luận."""
import nbformat, difflib, sys, os
NB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "notebooks")
th = nbformat.read(f"{NB}/EW_RIE_HOSE.ipynb", 4); v4 = nbformat.read(f"{NB}/EW_RIE_HOSE_v4.ipynb", 4)
norm = lambda s: "\n".join(l.rstrip() for l in s.strip().split("\n"))
src4 = [norm(c.source) for c in v4.cells if c.cell_type == "code"]
nbad = 0; lines = []
for i, c in enumerate([c for c in th.cells if c.cell_type == "code"]):
    s = norm(c.source)
    if s in src4: lines.append(f"ô thầy #{i}: NGUYÊN VẸN | {s.splitlines()[0][:60]}"); continue
    best = max(src4, key=lambda t: difflib.SequenceMatcher(None, s, t).quick_ratio()); d = list(difflib.unified_diff(s.splitlines(), best.splitlines(), "thầy", "v4", lineterm="", n=0))
    nbad += 1; lines.append(f"ô thầy #{i}: KHÁC | {s.splitlines()[0][:60]}\n" + "\n".join("    " + x for x in d[2:12]))
print("\n".join(lines)); print(f"\nTổng: {len(lines) - nbad}/{len(lines)} ô nguyên vẹn, {nbad} ô khác (xem lý do ở báo cáo)")
