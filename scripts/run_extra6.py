"""v6: chạy các bộ mới (VS "đủ T", T5d) bằng hàm của notebook v6 (cache results_v6/cache). Dùng: python run_extra6.py WINDOW M1,M2,..."""
import sys, os, time; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hose_ns import load_ns
ns = load_ns("EW_RIE_HOSE_v6.ipynb"); T = int(sys.argv[1]); ms = sys.argv[2].split(",")
for lo in (True, False):
    t0 = time.time(); ns["PRE_SHORT"].clear(); d = ns["run_full"](dict(ns["CONFIG"], WINDOW=T), lo, ms)
    print(f"T={T} {'long_only' if lo else 'short_ok'}: {len(d['ulog'])} kỳ, {time.time()-t0:.0f}s, thiếu phiên trước cửa sổ: {len(ns['PRE_SHORT'])} lần, "
          f"Vol: { {k: round(o['m']['Vol %'], 2) for k, o in d['out'].items()} }", flush=True)
