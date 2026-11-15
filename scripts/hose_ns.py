"""Nạp không gian tên của notebook v4 trong script: chạy lại đúng các ô mã (chỉ ô định nghĩa/dữ liệu) của notebook.
Dùng: ns = load_ns("EW_RIE_HOSE_v4.ipynb", cells=[...]) ; cells = chỉ số ô hoặc tên thẻ 'defs'."""
import os, sys, json, nbformat, linecache
os.environ.setdefault("MPLBACKEND", "Agg"); os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
NB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "notebooks")

def load_ns(nb="EW_RIE_HOSE_v4.ipynb", cells=None, tag="defs", ns=None):
    os.chdir(NB_DIR); nbk = nbformat.read(nb, 4); ns = ns if ns is not None else {"__name__": "__main__"}
    for i, c in enumerate(nbk.cells):
        if c.cell_type != "code": continue
        if (cells is not None and i in cells) or (cells is None and tag in c.metadata.get("tags", [])):
            fn = f"<cell {i}>"; src = c.source if c.source.endswith("\n") else c.source + "\n"
            linecache.cache[fn] = (len(src), None, src.splitlines(True), fn)      # để inspect.getsource hoạt động
            exec(compile(src, fn, "exec"), ns)
    return ns
