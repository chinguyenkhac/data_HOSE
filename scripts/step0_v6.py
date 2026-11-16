import sys; sys.path.insert(0, "/home/user/data_HOSE/scripts")
from hose_ns import load_ns
import pandas as pd
ns = load_ns("EW_RIE_HOSE_v6.ipynb"); M12 = ns["M12"]
res = {}
for m, lo in (("short_ok", False), ("long_only", True)):
    d = ns["run_full"](ns["CONFIG"], lo, M12); res[m] = pd.Series({k: d["out"][k]["m"]["Vol %"] for k in M12})
    print(m, len(d["ulog"]), "kỳ", len(d["out"]["EW-RIE*"]["r"]), "phiên", d["ulog"][0]["date"].date(), d["out"]["EW-RIE*"]["r"].index[-1].date(), flush=True)
t = pd.DataFrame(res).round(2); print(t)
ref = {"Sample": (14.58, 13.52), "Ledoit-Wolf": (13.63, 13.64), "NL-LW": (13.10, 13.72), "MP-clip": (13.48, 13.67), "RIE": (13.30, 14.02), "VS-NL-LW": (12.49, 12.93),
       "VS-RIE": (12.63, 13.30), "EW-NL-LW": (12.72, 13.12), "EW-RIE (q_eff)": (14.30, 14.76), "EW-WeSpeR": (12.57, 13.05), "EW-RIE*": (12.56, 13.07), "VS-EW-RIE*": (12.43, 12.96)}
bad = {k: (t.loc[k, "short_ok"], t.loc[k, "long_only"]) for k, (a, b) in ref.items() if abs(t.loc[k, "short_ok"] - a) > .01 or abs(t.loc[k, "long_only"] - b) > .01}
print("LỆCH:", bad if bad else "không (khớp đến 0,01)"); t.to_csv("results_v6/step0_regression.csv")
