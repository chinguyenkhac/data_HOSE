"""Bước 2 (chạy riêng, nên chạy khi máy rảnh): thực thi đúng ô §4.3 của notebook trong một tiến trình, ghi CSV vào results_v5/ (T43_*.csv)."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hose_ns import load_ns
ns = load_ns("EW_RIE_HOSE_v5.ipynb")
import nbformat
nb = nbformat.read("EW_RIE_HOSE_v5.ipynb", 4)
src = next(c.source for c in nb.cells if c.cell_type == "code" and c.source.startswith("# ---- 4.3 Thời gian chạy"))
t0 = time.time(); exec(compile(src, "<timing>", "exec"), ns); print(f"xong {time.time() - t0:.0f}s"); print(ns["TT"].round(2)); print(ns["PROF"].round(1)); print(ns["HW"])
