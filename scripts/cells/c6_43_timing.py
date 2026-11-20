# ---- 4.3 Thời gian chạy: một lần ước lượng ma trận N×N (ms, chưa gồm giải GMV) ----
N_GRID, K_WIN, REPS = (50, 100, 150), 12, 3

def timing_windows(N, K=K_WIN, cfg=CONFIG):
    # các cửa sổ ước lượng thật (đúng universe của run_backtest có lọc), K cửa sổ rải đều theo thời gian
    W = cfg["WINDOW"]; R = np.log(P).diff(); R = np.expm1(R.mask(R.abs() > cfg["MAX_ABS_RET"], 0.0)); Xs = []
    for s in range(W + 1, len(R) - 1, cfg["REB"]):
        win = R.iloc[s - W:s]; ok = (win.notna().mean() >= .95) & P.iloc[s - 1].notna()
        ok &= (win == 0).mean() <= cfg.get("ZERO_MAX", 1.0)
        if ok.sum() < N: continue
        tick = V.iloc[s - W:s].loc[:, ok].median().sort_values(ascending=False).index[:N]
        Xs.append(win[tick].fillna(0).values)
    return [Xs[i] for i in np.linspace(0, len(Xs) - 1, min(K, len(Xs))).astype(int)]

def _ms(f, X, reps):
    best = np.inf
    for _ in range(reps):
        t = time.perf_counter(); f(X); best = min(best, time.perf_counter() - t)
    return best * 1e3

def _wsp_cold_call(C, w):
    _WSP["warm"].clear(); return ew_wesper_corr(C, w)                       # gọi thẳng, không qua _WSP_CACHE, khởi tạo lại

E_T = build_full(CONFIG); TIME_EST = {k: E_T[k] for k in M12 + ["PCA-auto", "1/N"] if k != "EW-WeSpeR"}
TIME_EST["EW-WeSpeR"] = make_ew(_wsp_cold_call, CONFIG["HL_EW"]); TIME_EST["DCC-GARCH(1,1)"] = lambda X: est_dcc(X, use_cache=False)
_s0 = dict(_STATS); rows = []
for N_ in N_GRID:
    Xs = timing_windows(N_); _NULL_CACHE.clear(); E_T["EW-RIE*"](Xs[0])                  # lần đầu: mô phỏng phổ null (không tính)
    for k, f in TIME_EST.items():
        v = np.array([_ms(f, X, REPS) for X in (Xs[:3] if k.startswith("DCC") else Xs)])
        rows.append(dict(N=N_, method=k, ms=np.median(v), K=len(v)))
_STATS.update(_s0)                                                                     # không làm bẩn bộ đếm Newton
TIMING = pd.DataFrame(rows); TT = TIMING.pivot(index="method", columns="N", values="ms")
TT["× NL-LW (N = 100)"] = TT[100] / TT.loc["NL-LW", 100]; save(TT, "T43_timing")
try:
    from threadpoolctl import threadpool_info; BLAS = sorted({(d["internal_api"], d["num_threads"]) for d in threadpool_info()})
except Exception: BLAS = os.environ.get("OMP_NUM_THREADS", "?")
cpu = next((l.split(":")[1].strip() for l in open("/proc/cpuinfo") if l.startswith("model name")), platform.processor()) if os.path.exists("/proc/cpuinfo") else platform.processor()
TT12 = TT.reindex(M12 + ["DCC-GARCH(1,1)"]); TT12.columns = [f"N = {c}" if isinstance(c, (int, np.integer)) else c for c in TT12.columns]
cap("Bảng", f"Thời gian một lần ước lượng (ms, trung vị trên {K_WIN} cửa sổ HOSE thật; DCC: 3 cửa sổ), 12 phương pháp và DCC-GARCH. Máy: {cpu}, {os.cpu_count()} lõi; BLAS: {BLAS}.")
show(TT12, 1)
x_ = lambda k: TT.loc[k, 100]
md(f"**Kết quả.** Ở N = 100: NL-LW {f2(x_('NL-LW'), 1)} ms, EW-NL-LW {f2(x_('EW-NL-LW'), 1)} ms, RIE {f2(x_('RIE'), 1)} ms, **EW-RIE\\* {f2(x_('EW-RIE*'), 0)} ms**, "
   f"**EW-WeSpeR {f2(x_('EW-WeSpeR'), 0)} ms** ({f2(x_('EW-WeSpeR') / x_('EW-RIE*'), 1)} × EW-RIE\\*), VS-EW-RIE\\* {f2(x_('VS-EW-RIE*'), 0)} ms, DCC-GARCH {f2(x_('DCC-GARCH(1,1)') / 1e3, 1)} s.\n\n"
   f"**Kết luận.** EW-RIE\\* chậm hơn các bộ co cổ điển cỡ {f2(x_('EW-RIE*') / x_('NL-LW'), 0)} lần nhưng nhanh hơn EW-WeSpeR cỡ {f2(x_('EW-WeSpeR') / x_('EW-RIE*'), 0)} lần; cả hai đều không đáng kể so với một kỳ tái cân bằng.")
