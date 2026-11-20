"""Chạy nền phần 8: (1) lịch + universe, (2) tỷ trọng mọi (phương pháp × cấu hình) song song, (3) lợi suất, (4) kiểm định LW mọi ô.
python scripts/run8.py [--workers 4]. Kết quả: notebooks/results_v8/tests_raw.csv (+ cache)."""
import sys, os, time, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import v7ns
NS = v7ns.boot(); v7ns.run(NS, ["c7_core.py", "c8_core.py"]); g = NS
NW = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4

def cells():
    for sw, cols in g["SWEEP8"].items():
        for lab, c, reb in cols: yield ("T1", sw, str(lab), c, reb, [p[0] for p in g["PAIRS8"]])
    for reb, cols in g["GRID8_FAST"].items():
        for lab, c, r in cols: yield ("T2", f"h×HL REB {reb}", str(lab), c, r, g["FOCUS8"])
    for lab, c, r in g["GRID8_TR"]: yield ("T3", "T×REB", str(lab), c, r, g["FOCUS8"])
CELLS = list(cells()); PD = {k: (a, b) for k, a, b in g["PAIRS8"]}

def _w(t):
    nm, c, step = t; t0 = time.time(); g["weights8"](nm, c, step); return nm, c, step, time.time() - t0
def _t(t):
    tier, sw, lab, c, reb, pk, m = t; a, b = PD[pk]
    return dict(tier=tier, sweep=sw, label=lab, reb=reb, pair=pk, mode=m, **g["test8"](a, b, c, reb, m))

if __name__ == "__main__":
    t0 = time.time()
    need = {}
    for tier, sw, lab, c, reb, pairs in CELLS:
        step = 5 if reb in (5, 10) else 21
        for pk in pairs:
            for nm in PD[pk]:
                cc = g["canon8"](nm, c); need[(nm, tuple(sorted(cc.items())), step)] = (nm, cc, step)
    for c, step in {(tuple(sorted(v[1].items())), v[2]) for v in need.values()}: g["sched8"](dict(c), step)      # lịch trước (tránh tranh ghi)
    print(f"{len(CELLS)} ô, {len(need)} bộ tỷ trọng; lịch xong {time.time() - t0:.0f}s", flush=True)
    cost = lambda v: (5 if v[2] == 5 else 1) * (10 if v[0] in ("EW-RIE*", "VS-EW-RIE*") else 1) * v[1]["W"]
    todo = sorted(need.values(), key=cost, reverse=True)
    with mp.get_context("fork").Pool(NW) as pool:
        for i, (nm, c, step, dt) in enumerate(pool.imap_unordered(_w, todo)):
            if dt > 5: print(f"[{i + 1}/{len(todo)}] {nm} {c} REB gốc {step}: {dt:.0f}s ({time.time() - t0:.0f}s)", flush=True)
    print(f"tỷ trọng xong {time.time() - t0:.0f}s", flush=True)
    # kiểm hồi quy: cấu hình chuẩn, REB 21 phải trùng cache v6
    for nm in ("EW-RIE*", "VS-NL-LW", "VS-EW-RIE*", "NL-LW"):
        for m, mm in (("lo", "long_only"), ("so", "short_ok")):
            r = g["returns8"](nm, g["STD8"], 21)[m][0]; ref = g["OUT0"][mm][nm]["r"]
            assert r.index.equals(ref.index) and float(abs(r.values - ref.values).max()) < 1e-12, (nm, m)
    print("hồi quy v6 ✔", flush=True)
    for tier, sw, lab, c, reb, pairs in CELLS:
        for nm in {x for pk in pairs for x in PD[pk]}: g["returns8"](nm, c, reb)
    tasks = [(tier, sw, lab, c, reb, pk, m) for tier, sw, lab, c, reb, pairs in CELLS for pk in pairs for m in ("lo", "so")]
    with mp.get_context("fork").Pool(NW) as pool: rows = pool.map(_t, tasks, chunksize=8)
    import pandas as pd
    pd.DataFrame(rows).to_csv(f"{g['R8']}/tests_raw.csv", index=False); print(f"kiểm định xong: {len(rows)} ({time.time() - t0:.0f}s)", flush=True)
