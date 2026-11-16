"""Chạy thử các ô mã của notebook v4 trong MỘT tiến trình (không cần kernel): dev_exec.py [--from I] [--to J] [--skip a,b] [--tag T]
Ô §4 (RESULTS) được lưu/nạp từ /tmp/RESULTS6.pkl để khỏi chạy lại 5 phút."""
import sys, os, re, pickle, argparse, traceback, linecache, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hose_ns, nbformat
ap = argparse.ArgumentParser(); ap.add_argument("--nb", default="EW_RIE_HOSE_v5.ipynb"); ap.add_argument("--frm", type=int, default=0); ap.add_argument("--to", type=int, default=10**6)
ap.add_argument("--skip", default=""); ap.add_argument("--stop-on-error", action="store_true"); a = ap.parse_args()
os.chdir(hose_ns.NB_DIR); nb = nbformat.read(a.nb, 4); ns = {"__name__": "__main__"}; skip = {int(x) for x in a.skip.split(",") if x}
import matplotlib; matplotlib.use("Agg")
from IPython.display import display as _d, Markdown
def display(*o, **k):
    for x in o:
        if hasattr(x, "data") and hasattr(x, "export") is False and type(x).__name__ == "Styler": pass
        if type(x).__name__ == "Styler": print(x.data.round(3).to_string()); continue
        if hasattr(x, "data") and hasattr(x, "_repr_markdown_") is False: print(x)
        elif isinstance(x, Markdown): print(x.data)
        elif hasattr(x, "to_string"): print(x.to_string())
        elif hasattr(x, "data") and hasattr(x, "export"): print(x.data.to_string())
        else: print(x)
ns["display"] = display
for i, c in enumerate(nb.cells):
    if c.cell_type != "code" or i < a.frm or i > a.to or i in skip: continue
    src = c.source if c.source.endswith("\n") else c.source + "\n"; fn = f"<cell {i}>"; linecache.cache[fn] = (len(src), None, src.splitlines(True), fn)
    if "RESULTS = {}" in src and os.path.exists("/tmp/RESULTS6.pkl"):
        ns["ESTIMATORS"] = ns["build_estimators"](ns["CONFIG"]); ns["RESULTS"] = pickle.load(open("/tmp/RESULTS6.pkl", "rb")); ns["PAIRS"] = None; print(f"[cell {i}] RESULTS nạp từ pkl"); continue
    if "N_GRID, K_WIN, REPS" in src and os.path.exists("results_v5/T43_timing_long.csv"):
        head = src.split("hl = CONFIG")[0]; post = "TIMING = pd.read_csv('results_v5/T43_timing_long.csv')\n" + src.split("TIMING = pd.DataFrame(rows);")[1].lstrip().replace('save(TIMING, "T43_timing_long")', "pass")
        post = post.replace("def profile_ew_rie", "def profile_ew_rie_unused").split("_s0 = dict(_STATS)")[0] + "PROF = pd.read_csv('results_v5/T43_ew_rie_profile.csv', index_col=0); HW = 'CPU (dev)'"
        post = post.replace('save(TT, "T43_timing")', "pass")
        post = "\n".join(l.lstrip() if l.startswith(" ") and not l.startswith("    ") else l for l in post.split("\n"))
        exec(compile(head + "\nhl = CONFIG['HL_EW']\n" + post, fn, "exec"), ns); print(f"[cell {i}] timing nạp từ CSV"); continue
    t0 = time.time(); print(f"\n===== cell {i} =====", flush=True)
    try:
        exec(compile(src, fn, "exec"), ns); ns["display"] = display
    except Exception:
        traceback.print_exc(); print(f"!!! cell {i} lỗi"); 
        if a.stop_on_error: break
    if "RESULTS = {}" in src: pickle.dump(ns["RESULTS"], open("/tmp/RESULTS6.pkl", "wb"))
    print(f"[{time.time() - t0:.0f}s]")
