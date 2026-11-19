# ---- 3.3 Tiện ích chung cho §4–§6 (tái dùng run_backtest, summarize, block_bootstrap_ci của thầy) ----
import hashlib, json, platform, importlib.util
from IPython.display import Markdown
from scipy.stats import norm
if importlib.util.find_spec("arch") is None:      # Colab chưa có sẵn `arch` (dùng cho DCC-GARCH)
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "arch"], check=True)
RECOMPUTE = False                       # True: chạy lại mọi backtest; False: dùng cache results_v4/cache/*.pkl nếu có
MODES = {"long_only": True, "short_ok": False}
COL = {"EW-RIE*": "#1baf7a", "NL-LW": "#2a78d6", "EW-NL-LW": "#eb6834", "EW-WeSpeR": "#8e44ad", "VS-NL-LW": "#e0a800"}
GREY = "#9aa0a6"; col_of = lambda k: COL.get(k, GREY)

TIMES = {}
def check_cov(S, name=""):                      # đối xứng, PSD, không NaN
    ev = np.linalg.eigvalsh((S + S.T) / 2)
    assert np.isfinite(S).all() and np.allclose(S, S.T, rtol=0, atol=1e-10 * np.abs(S).max()) and ev[0] > -1e-10 * ev[-1], name
    return ev
def timed(name, f):
    def g(X):
        t = time.perf_counter(); S = f(X); TIMES.setdefault(name, []).append(time.perf_counter() - t); check_cov(S, name); return S
    return g

def run(est, cfg=None, long_only=True, data=None, tag=""):
    # backtest có cache: khóa = tên bộ ước lượng + cfg + chế độ (+ tag dữ liệu). Trả về out, log universe, thời gian, số lần Newton thất bại.
    cfg = cfg or CONFIG; Pd, Vd = data if data is not None else (P, V)
    f = f"{CACHE}/{hashlib.md5(repr((sorted(est), sorted(cfg.items()), long_only) + ((tag,) if tag else ())).encode()).hexdigest()[:12]}.pkl"
    if os.path.exists(f) and not RECOMPUTE: d = pd.read_pickle(f)
    else:
        TIMES.clear(); ULOG.clear(); f0, n0 = _STATS["fail"], _STATS["total"]
        out = run_backtest(Pd, Vd, {k: timed(k, g) for k, g in est.items()}, cfg, long_only)
        d = dict(out=out, ulog=list(ULOG), sec={k: np.mean(v) for k, v in TIMES.items()},
                 newton=(_STATS["fail"] - f0, _STATS["total"] - n0)); pd.to_pickle(d, f)
    idx = [o["r"].index for o in d["out"].values()]
    assert all(i.equals(idx[0]) for i in idx), "common-sample vi phạm"      # cùng ngày OOS cho mọi phương pháp
    return d

net = lambda o, c: o["r"] - (c / CONFIG["COST"]) * (o["r"] - o["r_net"])   # r_net ở mức phí c (phí không đổi tỷ trọng)
ann = lambda r: (r.std() * np.sqrt(252) * 100, r.mean() / r.std() * np.sqrt(252))
def metrics(o, cost=None, dates=None):
    r, rn = o["r"], net(o, cost or CONFIG["COST"])
    if dates is not None: r, rn = r.loc[dates], rn.loc[dates]
    return {"Vol %": ann(r)[0], "Sharpe": ann(r)[1], "Sharpe sau phí": ann(rn)[1], "LN/năm %": r.mean() * 252 * 100,
            "Turnover/kỳ": o["m"]["Turnover/kỳ"], "Số mã hiệu dụng": o["m"]["Số mã hiệu dụng"], "Số ngày OOS": len(r)}


R_BT = np.log(P).diff(); R_BT = np.expm1(R_BT.mask(R_BT.abs() > CONFIG["MAX_ABS_RET"], 0.0))   # đúng như trong run_backtest
POS = {d: i for i, d in enumerate(R_BT.index)}
