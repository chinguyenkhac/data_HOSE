import sys, time; sys.path.insert(0, "/home/user/data_HOSE/scripts")
from hose_ns import load_ns
ns = load_ns("EW_RIE_HOSE_v5.ipynb")
import pandas as pd
CONFIG, P, V = ns["CONFIG"], ns["P"], ns["V"]
E = ns["build_estimators"](CONFIG); res = {}
for lo in (False, True):
    t0 = time.time(); out = ns["run_backtest"](P, V, E, CONFIG, lo)
    res["long_only" if lo else "short_ok"] = pd.Series({k: o["m"]["Vol %"] for k, o in out.items()})
    print(("long_only" if lo else "short_ok"), f"{time.time()-t0:.0f}s", len(next(iter(out.values()))["r"]), flush=True)
t = pd.DataFrame(res).round(2); print(t)
t.to_csv("results_v5/step0_regression.csv")
