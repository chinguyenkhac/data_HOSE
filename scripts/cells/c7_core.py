# ---- 7.0 Lõi phần 7: tỷ trọng đích (cùng cách chọn universe và ước lượng như run_backtest), NAV có trôi tỷ trọng, phí thật ----
# Không sửa mã/kết quả v6: mọi hàm mới ở đây; ước lượng dùng đúng các hàm của §1 (build_estimators/build_full), GMV của thầy.
import re
R7, F7, C7 = "./results_v7", "./figs_v7", "./results_v7/cache"
for d in (R7, F7, C7): os.makedirs(d, exist_ok=True)
def save7(df, name): df.to_csv(f"{R7}/{name}.csv")
def savefig7(fig, name): fig.savefig(f"{F7}/{name}.png", dpi=150, bbox_inches="tight"); plt.show()
_CAP.update({"Bảng": max(_CAP["Bảng"], 34), "Hình": max(_CAP["Hình"], 17)})     # phần 7 đánh số tiếp sau v6 (34 bảng, 17 hình)

BUY, SELL, RF_SAV = 0.0015, 0.0015 + 0.001, 0.05       # phí mua; phí bán + thuế bán; lãi tiết kiệm (GIẢ ĐỊNH, làm mốc)
VS_HL = {"VS-NL-LW": 20, "VS-NL-LW (HL 10)": 10, "VS-NL-LW (HL 40)": 40}
M7 = ["EW-RIE*", "VS-NL-LW", "NL-LW", "EW-NL-LW", "EW-WeSpeR", "1/N"]       # 6 phương pháp chính (EW-WeSpeR ~1,2 s/kỳ: vẫn chạy được)
M7X = M7 + ["VS-NL-LW (HL 10)", "VS-NL-LW (HL 40)"]                          # + VS với HL_VOL 10, 40
COL.update({"1/N": "#5f6368", "VS-NL-LW (HL 10)": "#f3cf55", "VS-NL-LW (HL 40)": "#9c7400", "Thị trường EW": "#202124",
            "Tiết kiệm 5%": "#9aa0a6", "Q1 ít biến động": "#1a73e8", "Q5 biến động cao": "#d93025"})

W7, N7 = CONFIG["WINDOW"], CONFIG["N"]
DATES7, TICK7 = R_BT.index, R_BT.columns
RH = np.nan_to_num(R_BT.values)                          # lợi suất nắm giữ: NaN → 0 (như run_backtest: Y = ….fillna(0))
PX_OK = P.reindex(index=DATES7, columns=TICK7).notna().values      # có giá ở phiên đó (dùng để bán bắt buộc mã mất giá)
S_REG = [POS[d] for d in REB_DATES]                       # 118 kỳ đều của v6 (chỉ số phiên s: ước lượng đến s−1, nắm giữ từ s)
OOS0 = OUT0["long_only"]["EW-RIE*"]["r"].index
END7 = POS[OOS0[-1]] + 1                                  # mẫu ngoài mẫu giống v6: 2016-12-08 → 2026-11-10
assert DATES7[S_REG[0]] == OOS0[0] and len(OOS0) == END7 - S_REG[0]

def eligible(s, zero_max=None):
    # đúng bộ lọc của run_backtest (+ lọc đứng giá của §3.2): đủ 95% phiên trong cửa sổ, có giá ở s−1, tỷ lệ r = 0 ≤ ZERO_MAX
    win = R_BT.iloc[s - W7:s]; ok = (win.notna().mean() >= .95) & P.iloc[s - 1].notna()
    ok &= (win == 0).mean() <= (CONFIG["ZERO_MAX"] if zero_max is None else zero_max)
    return win, ok

def universe(s):
    win, ok = eligible(s)
    if ok.sum() < N7: return None
    tick = V.iloc[s - W7:s].loc[:, ok].median().sort_values(ascending=False).index[:N7]      # = run_backtest
    return tick, win[tick].fillna(0).values

def proj_capped(v, c):
    # chiếu Euclid lên {0 ≤ w ≤ c, Σw = 1} (cần c·n ≥ 1): s(τ) = Σ clip(v − τ, 0, c) tuyến tính từng khúc, nội suy tại điểm gãy
    b = np.sort(np.concatenate([v - c, v])); sv = np.clip(v[None, :] - b[:, None], 0, c).sum(1)
    k = int(np.searchsorted(-sv, -1.0)); k = min(max(k, 1), len(b) - 1)
    t0, t1, s0, s1 = b[k - 1], b[k], sv[k - 1], sv[k]
    tau = t1 if s0 == s1 else t0 + (s0 - 1) * (t1 - t0) / (s0 - s1)
    return np.clip(v - tau, 0, c)

def gmv_capped(S, c, iters=3000):
    # GMV chỉ mua có trần tỷ trọng c: cùng FISTA như gmv_long_only của thầy, chỉ thay phép chiếu
    n = len(S); L = 2 * np.linalg.eigvalsh(S)[-1]; w = y = np.full(n, 1 / n); t = 1.0
    for _ in range(iters):
        wn = proj_capped(y - 2 * S @ y / L, c); tn = (1 + np.sqrt(1 + 4*t*t)) / 2
        y = wn + (t - 1) / tn * (wn - w)
        if np.abs(wn - w).max() < 1e-9: return wn
        w, t = wn, tn
    return w

_S0 = np.cov(np.random.default_rng(SEED).standard_normal((250, 30)) * np.linspace(.5, 2, 30), rowvar=False)
assert np.abs(gmv_capped(_S0, 1.0) - gmv_long_only(_S0)).max() < 1e-6          # trần 100% ⇒ trùng GMV chỉ mua của thầy
_w = gmv_capped(_S0, .05); assert _w.max() <= .05 + 1e-12 and abs(_w.sum() - 1) < 1e-12 and _w.min() >= 0

def est7(name, cfg=CONFIG):
    # bộ ước lượng của §1/§3.3 (đúng hàm v6 dùng)
    if name in VS_HL: return build_estimators(dict(cfg, HL_VOL=VS_HL[name]))["VS-NL-LW"]
    return build_full(cfg)[name]

KINDS = ["lo", "so", "c20", "c10"]                        # chỉ mua | bán khống (tham khảo) | chỉ mua trần 20% | trần 10%
def _solve_all(S):
    return np.vstack([gmv_long_only(S), gmv_unconstrained(S), gmv_capped(S, .20), gmv_capped(S, .10)])

def targets7(name, extra=()):
    # tỷ trọng đích tại mọi kỳ đều (+ các phiên `extra`, ví dụ cầu chì) ; cache theo phương pháp: {s: (chỉ số cột, ma trận 4 × N)}
    f = f"{C7}/tgt_{re.sub(r'[^A-Za-z0-9]+', '_', name)}.pkl"; D = pd.read_pickle(f) if os.path.exists(f) else {}
    todo = [s for s in S_REG if s not in D]; new = [s for s in sorted(set(extra)) if s not in D and s not in S_REG]
    if todo or new:
        est = est7(name)
        if name == "EW-WeSpeR": _WSP["warm"].clear()        # như run_full: khởi tạo ấm xóa trước chuỗi kỳ đều ⇒ tái lập v6
        for s in todo + new:
            if name == "EW-WeSpeR" and s in new: _WSP["warm"].clear()       # kỳ thêm: khởi tạo lạnh (tất định)
            u = universe(s)
            if u is None: continue
            tick, X = u; S = est(X); check_cov(S, name)
            D[s] = (np.array([TICK7.get_loc(t) for t in tick]), _solve_all(S))
        pd.to_pickle(D, f)
    return D

def simulate(tg, sched, kind="lo", band=0.0, to_cap=None, cost=True, end=None):
    # NAV 1 đồng: tỷ trọng trôi theo giá giữa hai kỳ; tại kỳ s: (1) mã mất giá ở s−1 bị bán, (2) vùng không giao dịch `band`
    # (giữ mã có |đích − hiện| ≤ band, phần còn lại về đích rồi co giãn cho tổng = 1), (3) trần turnover một chiều `to_cap`
    # (đi một phần về đích). Phí: mua BUY, bán SELL trên giá trị giao dịch, trừ vào NAV ngày s. Trả lợi suất ngày ròng + nhật ký.
    end = end or END7; k = KINDS.index(kind) if isinstance(kind, str) else None
    n = len(TICK7); h = np.zeros(n); nav = 1.0; navs = np.empty(end - sched[0]); log = []
    sch = set(sched)
    for t in range(sched[0], end):
        if t in sch and t in tg:
            ix, Wm = tg[t]; wt = np.zeros(n); wt[ix] = Wm[k] if k is not None else Wm
            wc = h / nav if h.any() else np.zeros(n); dead = (wc != 0) & ~PX_OK[t - 1]
            wn = wt.copy()
            if band > 0 and h.any():
                keep = (np.abs(wt - wc) <= band) & ~dead; Sk = wc[keep].sum(); St = wt[~keep].sum()
                wn = np.where(keep, wc, wt * (1 - Sk) / St) if St > 0 else np.where(keep, wc + (1 - Sk) * wt / wt.sum(), 0.0)
            if to_cap is not None and h.any():
                to = .5 * np.abs(wn - wc).sum()
                if to > to_cap: wn = wc + (to_cap / to) * (wn - wc); wn[dead] = 0.0; wn /= wn.sum()
            buy, sell = np.clip(wn - wc, 0, None).sum(), np.clip(wc - wn, 0, None).sum()
            c = (BUY * buy + SELL * sell) if cost else 0.0
            log.append(dict(s=t, date=DATES7[t], buy=buy, sell=sell, cost=c, first=not h.any(), wmax=wn.max(), neff=1 / (wn**2).sum()))
            nav *= 1 - c; h = wn * nav
        h = h * (1 + RH[t]); nav = h.sum(); navs[t - sched[0]] = nav
    nv = pd.Series(navs, index=DATES7[sched[0]:end]); r = nv.pct_change(); r.iloc[0] = nv.iloc[0] - 1
    return r, pd.DataFrame(log)

def perf7(r, log=None):
    # chỉ tiêu dài hạn trên lợi suất ngày ròng r
    nav = (1 + r).cumprod(); n = len(r); peak = nav.cummax(); dd = nav / peak - 1; t_tr = dd.idxmin()
    rec = nav.loc[t_tr:][nav.loc[t_tr:] >= peak.loc[t_tr]]
    uw = (dd < 0).values; runs, cur = [], 0
    for u in uw: cur = cur + 1 if u else 0; runs.append(cur)
    m = (1 + r).groupby(r.index.to_period("M")).prod() - 1; k5 = int(np.ceil(.05 * len(m)))
    cagr = nav.iloc[-1] ** (252 / n) - 1; yrs = n / 252
    out = {"CAGR %": cagr * 100, "Vol %": r.std() * np.sqrt(252) * 100, "MDD %": dd.min() * 100,
           "Hồi phục (phiên)": (DATES7.get_loc(rec.index[0]) - DATES7.get_loc(t_tr)) if len(rec) else np.nan,
           "Dưới đỉnh dài nhất (phiên)": max(runs), "CVaR 5% tháng %": np.sort(m.values)[:k5].mean() * 100,
           "Calmar": cagr / abs(dd.min())}
    if log is not None and len(log):
        L = log[~log["first"]]
        out.update({"Turnover/năm %": (L["buy"] + L["sell"]).sum() / 2 / yrs * 100, "Chi phí %/năm": log["cost"].sum() / yrs * 100})
    return out

def fko_fee(ra, rb, gamma, equal_mean=False):
    # Fleming–Kirby–Ostdiek (2001): phí Δ (bps/năm) nhà đầu tư γ sẵn lòng trả để chuyển từ a sang b (> 0: b tốt hơn).
    # Ū = mean(R) − k·mean(R²), R = 1 + r, k = γ / (2(1 + γ)); giải kΔ² + (1 − 2k·m_b)Δ − (Ū_b − Ū_a) = 0.
    ra, rb = np.asarray(ra), np.asarray(rb)
    if equal_mean: rb = rb - rb.mean() + ra.mean()          # coi lợi suất kỳ vọng như nhau: chỉ còn khác biệt rủi ro
    k = gamma / (2 * (1 + gamma)); A, B = 1 + ra, 1 + rb
    Ua, Ub = A.mean() - k * (A**2).mean(), B.mean() - k * (B**2).mean(); b1 = 1 - 2 * k * B.mean()
    return (-b1 + np.sqrt(b1**2 + 4 * k * (Ub - Ua))) / (2 * k) * 252 * 1e4

_r = np.random.default_rng(1).standard_normal(2000) * .01
assert abs(fko_fee(_r, _r, 5)) < 1e-9 and fko_fee(_r, _r + 1e-4, 5) > 0 and fko_fee(_r, .5 * _r, 5, equal_mean=True) > 0

def lw7(ra, rb):
    # kiểm định LW (2011) như v6: trả ΔVol (pp), p HAC, p bootstrap khối
    ra, rb = np.asarray(ra), np.asarray(rb); d, se, p_hac, p_bt = lw_var_test(ra, rb, block=21, M=2000)
    return (ra.std() - rb.std()) * np.sqrt(252) * 100, p_hac, p_bt

def nw_mean_test(x):
    # kiểm định trung bình = 0, sai số chuẩn Newey–West (hàm hac của §3.3: Bartlett, L = ⌊4(T/100)^(2/9)⌋); trả TB và p hai phía
    x = np.asarray(x, float); T = len(x); se = np.sqrt(hac((x - x.mean())[:, None])[0, 0] / T)
    return x.mean(), 2 * norm.sf(abs(x.mean() / se))

# kiểm hồi quy: lợi suất Y·w (không trôi, như run_backtest) từ tỷ trọng tính lại phải trùng cache v6 ở mọi phương pháp
def check_v6_regression(names):
    rows = {}
    for nm in names:
        tg = targets7(nm); r = []
        for i, s in enumerate(S_REG):
            e = S_REG[i + 1] if i + 1 < len(S_REG) else END7; ix, Wm = tg[s]; r.append(RH[s:e][:, ix] @ Wm[0])
        r = np.concatenate(r)
        if nm in OUT0["long_only"]: ref = OUT0["long_only"][nm]["r"].values
        else:
            ref = run_full(dict(CONFIG, HL_VOL=VS_HL[nm]), True, ["VS-NL-LW"])["out"]["VS-NL-LW"]["r"].values
        rows[nm] = float(np.abs(r - ref).max())
    return pd.Series(rows, name="lệch lớn nhất so với cache v6")
