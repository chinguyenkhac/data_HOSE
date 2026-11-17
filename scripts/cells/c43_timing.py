# ---- 4.3 Thời gian chạy: một lần ước lượng ma trận N×N (ms, chưa gồm giải GMV) ----
N_GRID, K_WIN, REPS = (50, 100, 150, 200), 12, 3

def timing_windows(N, K=K_WIN, cfg=CONFIG):
    W = cfg["WINDOW"]; R = np.log(P).diff(); R = np.expm1(R.mask(R.abs() > cfg["MAX_ABS_RET"], 0.0)); Xs = []
    for s in range(W + 1, len(R) - 1, cfg["REB"]):
        win = R.iloc[s - W:s]; ok = (win.notna().mean() >= .95) & P.iloc[s - 1].notna()
        ok &= (win == 0).mean() <= cfg.get("ZERO_MAX", 1.0)
        if ok.sum() < N: continue
        tick = V.iloc[s - W:s].loc[:, ok].median().sort_values(ascending=False).index[:N]
        Xs.append(win[tick].fillna(0).values)
    return [Xs[i] for i in np.linspace(0, len(Xs) - 1, min(K, len(Xs))).astype(int)]     # theo thứ tự thời gian

def _ms(f, X, reps):
    best = np.inf
    for _ in range(reps):
        t = time.perf_counter(); f(X); best = min(best, time.perf_counter() - t)
    return best * 1e3

def _wsp_cold_call(C, w):
    _WSP["warm"].clear(); return ew_wesper_corr(C, w)

hl = CONFIG["HL_EW"]; E_FULL = build_full(CONFIG)
TIME_EST = {k: f for k, f in E_FULL.items() if k != "EW-WeSpeR"}
TIME_EST["DCC-GARCH(1,1)"] = lambda X: est_dcc(X, use_cache=False)            # không qua _DCC_CACHE
TIME_EST["EW-WeSpeR (nguội)"] = make_ew(_wsp_cold_call, hl)
TIME_EST["EW-WeSpeR (ấm)"] = make_ew(ew_wesper_corr, hl)

rows = []
for N_ in N_GRID:
    Xs = timing_windows(N_)
    if not Xs: continue
    _NULL_CACHE.clear(); t = time.perf_counter(); E_FULL["EW-RIE*"](Xs[0])             # lần đầu: gồm cả mô phỏng phổ null
    rows.append(dict(N=N_, method="EW-RIE* (lần đầu)", ms=(time.perf_counter() - t) * 1e3, q1=np.nan, q3=np.nan, K=1))
    for k, f in TIME_EST.items():
        warm = k.endswith("(ấm)"); Xk = Xs[:3] if k.startswith("DCC") else Xs          # DCC chậm: chỉ 3 cửa sổ
        if warm: _WSP["warm"].clear(); f(Xs[0])                                          # kỳ 0 chỉ để tạo khởi tạo ấm
        v = np.array([_ms(f, X, 1 if warm else REPS) for X in (Xs[1:] if warm else Xk)])
        rows.append(dict(N=N_, method=k, ms=np.median(v), q1=np.percentile(v, 25), q3=np.percentile(v, 75), K=len(v)))
    print(f"N = {N_}: xong ({len(Xs)} cửa sổ)", flush=True)
TIMING = pd.DataFrame(rows); save(TIMING, "T43_timing_long")
TT = TIMING.pivot(index="method", columns="N", values="ms")
nref = 100 if 100 in TT else TT.columns[0]; TT = TT.loc[TT[nref].sort_values().index]
TT[f"× NL-LW (N={nref})"] = TT[nref] / TT.loc["NL-LW", nref]
n0, n1 = TIMING.N.min(), TIMING.N.max()
TT["bậc theo N"] = np.log(TT[n1] / TT[n0]) / np.log(n1 / n0)                                # độ dốc log–log
save(TT, "T43_timing")

def profile_ew_rie(X, hl=hl):                                                               # EW-RIE* tốn thời gian ở bước nào
    w = ew_weights(len(X), hl); C, _ = ew_corr(X, w); N = len(C); eta = 1 / np.sqrt(N); T = {}
    t = time.perf_counter(); lam, Vv = np.linalg.eigh(C); lam = np.maximum(lam, 1e-10); T["phân rã riêng (eigh)"] = time.perf_counter() - t
    null = _null_spectrum(N, w); s2 = np.median(lam) / np.median(null); D = lam[:, None] - lam[None, :]
    dens = (eta / (D**2 + eta**2)).sum(1) - 1 / eta; out = np.where(dens < 0.1 / eta)[0]; bulk = np.setdiff1d(np.arange(N), out)
    t = time.perf_counter(); _xi(lam, lam[bulk], w, N, eta); T["Newton – phần khối"] = time.perf_counter() - t
    t = time.perf_counter(); _xi_outliers(lam, out, w, N) if len(out) else None; T["Newton – ngoại lai"] = time.perf_counter() - t
    t = time.perf_counter(); _xi(null, lam[bulk] / s2, w, N, eta); T["hiệu chỉnh N hữu hạn"] = time.perf_counter() - t
    return T
_s0 = dict(_STATS)                                                                           # không làm bẩn bộ đếm Newton
prof = pd.DataFrame([profile_ew_rie(X) for X in timing_windows(100)]).median() * 1e3
_STATS.update(_s0)
PROF = pd.DataFrame({"ms": prof, "%": prof / prof.sum() * 100}); save(PROF, "T43_ew_rie_profile")
try:
    from threadpoolctl import threadpool_info; BLAS = sorted({(d["internal_api"], d["num_threads"]) for d in threadpool_info()})
except Exception: BLAS = os.environ.get("OMP_NUM_THREADS", "?")
cpu = next((l.split(":")[1].strip() for l in open("/proc/cpuinfo") if l.startswith("model name")), platform.processor()) if os.path.exists("/proc/cpuinfo") else platform.processor()
HW = f"CPU: {cpu}, {os.cpu_count()} lõi; BLAS/OpenMP luồng: {BLAS}; numpy {np.__version__}"
