"""Không gian tên cho phần 7: chạy lại các ô ĐỊNH NGHĨA/DỮ LIỆU của notebook v6 (không chạy ô tính toán nặng),
rồi chạy các ô của phần 7 (scripts/cells/c7_*.py). Dùng: python scripts/v7ns.py c7_core.py c7_h1a.py ...
Các ô v6 nạp: §0 cấu hình, §1 bộ ước lượng, §2.1 dữ liệu, §3 run_backtest + lọc, §3.3 tiện ích, §4 STD (đọc cache run_full)."""
import os, sys, time, linecache, traceback
for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(k, "1")   # như khi tạo cache v6
os.environ.setdefault("MPLBACKEND", "Agg")
import nbformat
H = os.path.dirname(os.path.abspath(__file__)); NB = os.path.join(H, "..", "notebooks")
BOOT = [4, 5, 6, 9, 10, 11, 12, 14, 15, 27, 28, 29, 45, 47, 49, 50, 51, 52, 62]

def _exec(src, fn, ns):
    src = src if src.endswith("\n") else src + "\n"; linecache.cache[fn] = (len(src), None, src.splitlines(True), fn)
    exec(compile(src, fn, "exec"), ns)

def boot(quiet=True):
    os.chdir(NB); nb = nbformat.read("EW_RIE_HOSE_v6.ipynb", 4); ns = {"__name__": "__main__"}
    import io, contextlib
    t0 = time.time()
    for i in BOOT:
        assert nb.cells[i].cell_type == "code"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): _exec(nb.cells[i].source, f"<v6 cell {i}>", ns)
    from IPython.display import Markdown
    def display(*o, **k):
        for x in o:
            if type(x).__name__ == "Styler": print(x.data.to_string())
            elif isinstance(x, Markdown): print(x.data)
            elif hasattr(x, "to_string"): print(x.to_string())
            else: print(x)
    ns["display"] = display; ns["md"] = lambda s: print(s)
    print(f"[boot v6: {time.time() - t0:.0f}s]", flush=True)
    return ns

def run(ns, files):
    for f in files:
        t0 = time.time(); print(f"\n===== {f} =====", flush=True)
        _exec(open(os.path.join(H, "cells", f), encoding="utf-8").read(), f"<{f}>", ns)
        print(f"[{f}: {time.time() - t0:.0f}s]", flush=True)

if __name__ == "__main__":
    ns = boot(); run(ns, sys.argv[1:])
