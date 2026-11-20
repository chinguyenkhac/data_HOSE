# ---- 8.0 Lõi phần 8: lưới siêu tham số (cùng cách chọn universe, cùng bộ ước lượng và GMV của §1–§3), cache theo phương pháp × cấu hình ----
import hashlib
R8, F8, C8 = "./results_v8", "./figs_v8", "./results_v8/cache"
for d in (R8, F8, C8): os.makedirs(d, exist_ok=True)
def save8(df, name): df.to_csv(f"{R8}/{name}.csv")
def savefig8(fig, name): fig.savefig(f"{F8}/{name}.png", dpi=150, bbox_inches="tight"); plt.show()
_CAP.update({"Bảng": max(_CAP["Bảng"], 42), "Hình": max(_CAP["Hình"], 28)})       # đánh số tiếp sau phần 7

STD8 = dict(N=100, W=250, h=60, hv=20, z=0.20)
M8 = ["EW-RIE*", "VS-EW-RIE*", "VS-NL-LW", "NL-LW", "EW-NL-LW", "EW-RIE (q_eff)", "RIE", "VS-RIE"]
USES_H8 = {"EW-RIE*", "VS-EW-RIE*", "EW-NL-LW", "EW-RIE (q_eff)"}; USES_HV8 = {"VS-EW-RIE*", "VS-NL-LW", "VS-RIE"}
PAIRS8 = [("A1", "EW-RIE*", "EW-NL-LW"), ("A2", "EW-RIE*", "EW-RIE (q_eff)"), ("B1", "EW-NL-LW", "NL-LW"), ("B2", "EW-RIE*", "RIE"),
          ("C1", "VS-NL-LW", "NL-LW"), ("C2", "VS-RIE", "RIE"), ("C3", "VS-EW-RIE*", "EW-RIE*"),
          ("D1", "VS-EW-RIE*", "VS-NL-LW"), ("D2", "VS-EW-RIE*", "VS-RIE"), ("D3", "VS-RIE", "VS-NL-LW"), ("E1", "EW-RIE*", "VS-NL-LW")]
PLAB8 = {k: f"{k} {a} − {b}" for k, a, b in PAIRS8}
MODES8 = {"lo": "Chỉ mua", "so": "Bán khống"}

def canon8(nm, c):
    return dict(c, h=c["h"] if nm in USES_H8 else 60, hv=c["hv"] if nm in USES_HV8 else 20)
def est8(nm, c):
    if nm == "VS-EW-RIE*": return make_vs_ew_rie(c["hv"], c["h"])
    return build_estimators(dict(CONFIG, HL_EW=c["h"], HL_VOL=c["hv"]))[nm]
def _key8(*a): return hashlib.md5(repr(a).encode()).hexdigest()[:12]

_SCH8, _UNI8 = {}, {}
def sched8(c, step):
    # lịch như run_backtest: s = W+1, W+1+step, …; bỏ kỳ có < N mã đủ điều kiện (≥ 95% phiên, có giá ở s−1, tỷ lệ r = 0 ≤ ngưỡng lọc)
    k = (c["W"], c["N"], c["z"], step)
    if k not in _SCH8:
        f = f"{C8}/sch_{_key8(*k)}.pkl"
        if os.path.exists(f): _SCH8[k] = pd.read_pickle(f)
        else:
            W, out = c["W"], []
            for s in range(W + 1, len(DATES7) - 1, step):
                win = R_BT.iloc[s - W:s]; ok = (win.notna().mean() >= .95) & P.iloc[s - 1].notna(); ok &= (win == 0).mean() <= c["z"]
                if ok.sum() >= c["N"]:
                    tick = V.iloc[s - W:s].loc[:, ok].median().sort_values(ascending=False).index[:c["N"]]
                    out.append((s, np.array([TICK7.get_loc(t) for t in tick])))
            _SCH8[k] = out; pd.to_pickle(out, f)
    return _SCH8[k]

def weights8(nm, c, step):
    # tỷ trọng GMV chỉ mua (lo) và bán khống (so) tại mọi kỳ của lịch gốc `step`; cùng Σ cho hai chế độ
    c = canon8(nm, c); f = f"{C8}/w_{_key8(nm, sorted(c.items()), step)}.pkl"
    if os.path.exists(f): return pd.read_pickle(f)
    est = est8(nm, c); D = {}
    for s, ix in sched8(c, step):
        X = np.nan_to_num(R_BT.values[s - c["W"]:s][:, ix]); S = est(X)
        D[s] = (ix, np.vstack([gmv_long_only(S), gmv_unconstrained(S)]))
    pd.to_pickle(D, f); return D

def returns8(nm, c, reb):
    # lợi suất ngày (tỷ trọng cố định trong kỳ, chưa phí, như run_backtest) và turnover Σ|Δw| mỗi kỳ, hai chế độ
    step = 5 if reb in (5, 10) else 21; k = reb // step; c2 = canon8(nm, c)
    f = f"{C8}/r_{_key8(nm, sorted(c2.items()), reb)}.pkl"
    if os.path.exists(f): return pd.read_pickle(f)
    Wd = weights8(nm, c, step); sch = [s for s, _ in sched8(c, step)]; sub = sch[::k]; end = min(sch[-1] + step, len(DATES7))
    out = {}
    for j, m in enumerate(("lo", "so")):
        r, tv, prev = [], [], None
        for i, s in enumerate(sub):
            e = sub[i + 1] if i + 1 < len(sub) else end; ix, Wm = Wd[s]; w = np.zeros(len(TICK7)); w[ix] = Wm[j]
            r.append(RH[s:e][:, ix] @ Wm[j])
            if prev is not None: tv.append(np.abs(w - prev).sum())
            prev = w
        out[m] = (pd.Series(np.concatenate(r), index=DATES7[sub[0]:end]), np.array(tv))
    pd.to_pickle(out, f); return out

def test8(a, b, c, reb, m):
    ra, ta = returns8(a, c, reb)[m]; rb, tb = returns8(b, c, reb)[m]; assert ra.index.equals(rb.index)
    d, p_hac, p_bt = lw7(ra.values, rb.values)
    return dict(dvol=d, p_hac=p_hac, p_bt=p_bt, dturn=float(np.mean(ta - tb)), vol_a=ra.std() * np.sqrt(252) * 100,
                vol_b=rb.std() * np.sqrt(252) * 100, n=len(ra), d0=ra.index[0])

# ---- các ô của lưới (đăng ký trước) ----
def C(**kw): return dict(STD8, **kw)
SWEEP8 = {"HL_VOL": [(f"HL_VOL = {v}", C(hv=v), 21) for v in (5, 10, 20, 30, 40, 60)],
          "h": [(f"h = {v}", C(h=v), 21) for v in (15, 30, 45, 60, 90, 120, 250)],
          "T": [(f"T = {v}", C(W=v), 21) for v in (120, 180, 250, 375, 500, 750)],
          "REB": [(f"REB = {v}", C(), v) for v in (5, 10, 21, 42, 63, 126, 252)],
          "N": [(f"N = {v}", C(N=v), 21) for v in (50, 75, 100, 150)],
          "Lọc": [(lab, C(z=z), 21) for lab, z in (("không lọc", 1.0), ("10%", .10), ("15%", .15), ("20% (chuẩn)", .20), ("30%", .30))]}
GRID8_FAST = {reb: [((h, hv), C(h=h, hv=hv), reb) for h in (15, 30, 60, 120) for hv in (5, 10, 20, 30, 40, 60)] for reb in (5, 21)}
GRID8_TR = [((W, reb), C(W=W), reb) for W in (120, 250, 500, 750) for reb in (5, 21, 63, 252)]
FOCUS8 = ["E1", "D1", "C3"]
