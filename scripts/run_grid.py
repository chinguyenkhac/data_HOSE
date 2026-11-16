"""Chạy nặng: điền cache `results_v5/cache` bằng đúng các hàm của notebook v4. Dùng:  python scripts/run_grid.py JOB [JOB ...]
JOB: std | win:T | nh:N:h | hlv:HV | reb:R[:skipDCC] | zero:Z | delist:TÊN_KỊCH_BẢN   (mỗi job chạy cả hai chế độ, FULL)."""
import sys, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hose_ns import load_ns
ns = load_ns("EW_RIE_HOSE_v5.ipynb"); CONFIG = ns["CONFIG"]; FULL = ns["FULL"]
def one(job):
    p = job.split(":"); kind = p[0]; cfg = dict(CONFIG); methods = None; skip = []
    if kind == "nh": cfg.update(N=int(p[1]), HL_EW=int(p[2]))
    elif kind == "win": cfg.update(WINDOW=int(p[1]))
    elif kind == "hlv": cfg.update(HL_VOL=int(p[1]))
    elif kind == "reb":
        cfg.update(REB=int(p[1]))
        if len(p) > 2 and p[2] == "skipDCC": skip = ["DCC-GARCH(1,1)"]
    elif kind == "zero": cfg.update(ZERO_MAX=float(p[1]))
    elif kind == "delist": pass
    methods = [k for k in FULL if k not in skip]
    for lo in (True, False):
        t0 = time.time()
        d = ns["run_full_scn"](":".join(p[1:]), cfg, lo, methods) if kind == "delist" else ns["run_full"](cfg, lo, methods)
        print(f"[{job}] {'long_only' if lo else 'short_ok'}: {len(d['ulog'])} kỳ, {time.time()-t0:.0f}s, "
              f"sec/lần: { {k: round(v, 3) for k, v in d['sec'].items()} }", flush=True)
def diag(job):
    import json, re
    n = re.sub(r"[^A-Za-z0-9]+", "_", job); dl = ns["DCC_LOG"]
    json.dump(dict(job=job, newton=ns["_STATS"], wesper_safe=ns["_WSP_SAFE"], wesper_nfev=[int(x) for x in ns["_WSP"]["nfev"]],
                   wesper_rmse=[float(x) for x in ns["_WSP"]["cost"]], dcc=[{k: (float(v) if not isinstance(v, bool) else v) for k, v in r.items()} for r in dl],
                   pca_k=[int(k) for k in ns["PCA_K"]]), open(f"results_v5/logs/diag_{n}.json", "w"))
for j in sys.argv[1:]: one(j); diag(j)
