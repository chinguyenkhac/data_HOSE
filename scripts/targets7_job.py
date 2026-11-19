"""Tính tỷ trọng đích phần 7 cho một/nhiều phương pháp (chạy nền, mỗi tiến trình một phương pháp): python scripts/targets7_job.py "EW-RIE*" ..."""
import sys, time, v7ns
ns = v7ns.boot(); v7ns.run(ns, ["c7_core.py"])
for nm in sys.argv[1:]:
    t0 = time.time(); D = ns["targets7"](nm); print(nm, len(D), f"{time.time() - t0:.0f}s", flush=True)
    print(ns["check_v6_regression"]([nm]).to_string(), flush=True)
