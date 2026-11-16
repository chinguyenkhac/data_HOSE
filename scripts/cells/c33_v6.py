# ---- 3.3 (v6) Bộ ước lượng bổ sung cho §5.4 và T5d; 12 phương pháp, 12 cặp định trước; bảng A và heatmap cặp ----
def timed(name, f):                     # (định nghĩa lại) giữ thuộc tính `pre` của bộ VS "đủ T" khi bọc đo thời gian
    def g(X):
        t = time.perf_counter(); S = f(X); TIMES.setdefault(name, []).append(time.perf_counter() - t); check_cov(S, name); return S
    g.pre = getattr(f, "pre", 0); return g

def with_pre(est, pre):                 # bộ VS "đủ T": nhận thêm `pre` = HL_VOL phiên ngay trước cửa sổ để khởi động EWMA, rồi dùng đủ T phiên
    est.pre = pre; return est

def ewma_sig(X, hl):
    # độ lệch chuẩn EWMA dùng tại từng phiên, đúng số học của ewma_standardize của thầy; trả về (σ_t cho t = 0..T−1, σ sau phiên cuối)
    lam = 0.5 ** (1 / hl); s2 = X[:hl].var(0) + 1e-10; S = np.empty_like(X)
    for t in range(len(X)):
        S[t] = np.sqrt(s2); s2 = lam * s2 + (1 - lam) * X[t]**2
    return S, np.sqrt(s2)

def make_vs_split(part, hl_vol):
    # T5d (cách nhóm hiểu gợi ý (a) của thầy): σ_m = EWMA của lợi suất trung bình đều N mã; ρ_i = σ_i / σ_m. Cùng bộ làm sạch NL-LW, cùng bỏ HL_VOL phiên đầu như make_vs.
    clean = lambda Z: renorm(nl_lw_S(np.cov(Z, rowvar=False), len(Z) - 1))
    def est(X):
        Si, si_T = ewma_sig(X, hl_vol); Sm, sm_T = ewma_sig(X.mean(1, keepdims=True), hl_vol)
        if part == "chung":                       # chỉ phần chung: Z = X / σ_m
            Z = (X / Sm)[hl_vol:]; s = Z.std(0, ddof=1); return clean(Z) * np.outer(s, s)
        rho = Si / Sm; Z = (X / rho)[hl_vol:]     # chỉ phần riêng: Z = X / ρ
        s = Z.std(0, ddof=1) * (si_T / sm_T); return clean(Z) * np.outer(s, s)
    return est

EXTRA6 = ["VS-NL-LW (đủ T)", "VS-RIE (đủ T)", "VS-EW-RIE* (đủ T)", "VS chỉ phần chung", "VS chỉ phần riêng"]
_build_full5 = build_full
def build_full(cfg):
    E = _build_full5(cfg); hv, hl = cfg["HL_VOL"], cfg["HL_EW"]
    E.update({"VS-NL-LW (đủ T)": with_pre(make_vs(lambda Z: renorm(nl_lw_S(np.cov(Z, rowvar=False), len(Z) - 1)), hv), hv),
              "VS-RIE (đủ T)": with_pre(make_vs(lambda Z: rie_corr(np.corrcoef(Z, rowvar=False), Z.shape[1] / len(Z)), hv), hv),
              "VS-EW-RIE* (đủ T)": with_pre(make_vs_ew_rie(hv, hl), hv),
              "VS chỉ phần chung": make_vs_split("chung", hv), "VS chỉ phần riêng": make_vs_split("riêng", hv)})
    return E
USES_HL_EW |= {"VS-EW-RIE* (đủ T)"}; USES_HL_VOL |= {"VS-NL-LW (đủ T)", "VS-RIE (đủ T)", "VS-EW-RIE* (đủ T)", "VS chỉ phần chung", "VS chỉ phần riêng"}

M12 = ["Sample", "Ledoit-Wolf", "NL-LW", "MP-clip", "RIE", "VS-NL-LW", "VS-RIE", "EW-NL-LW", "EW-RIE (q_eff)", "EW-WeSpeR", "EW-RIE*", "VS-EW-RIE*"]
PAIRS12 = [("A. Làm sạch", "EW-RIE*", "EW-NL-LW"), ("A. Làm sạch", "EW-RIE*", "EW-RIE (q_eff)"), ("A. Làm sạch", "EW-RIE*", "EW-WeSpeR"),
           ("B. Trọng số mũ", "EW-NL-LW", "NL-LW"), ("B. Trọng số mũ", "EW-RIE*", "RIE"),
           ("C. Trước/sau VS", "VS-NL-LW", "NL-LW"), ("C. Trước/sau VS", "VS-RIE", "RIE"), ("C. Trước/sau VS", "VS-EW-RIE*", "EW-RIE*"),
           ("D. Trong họ VS", "VS-EW-RIE*", "VS-NL-LW"), ("D. Trong họ VS", "VS-EW-RIE*", "VS-RIE"), ("D. Trong họ VS", "VS-RIE", "VS-NL-LW"),
           ("E. EW hay VS", "EW-RIE*", "VS-NL-LW")]

def holm(p):
    p = np.asarray(p, float); o = np.argsort(p); adj = np.minimum(1, np.maximum.accumulate(p[o] * (len(p) - np.arange(len(p)))))
    out = np.empty(len(p)); out[o] = adj; return out

def turnover_series(o, reb_dates, cost=None):
    # turnover từng kỳ, khôi phục từ r − r_net tại các ngày tái cân bằng (kỳ đầu không có turnover)
    return ((o["r"] - o["r_net"]).reindex(reb_dates[1:]) / (cost or CONFIG["COST"])).values

def pair_table(out, pairs=PAIRS12, reb_dates=None, block=21, M=2000, B=2000, seed=0):
    # Bảng kiểm định chi tiết: mỗi cặp (a, b) chỉ khác một thành phần. ΔVol = Vol(a) − Vol(b); < 0 ⇒ a rủi ro thấp hơn.
    rows = []
    for g, a, b in pairs:
        assert out[a]["r"].index.equals(out[b]["r"].index), f"khác mẫu: {a}, {b}"
        ra, rb = out[a]["r"].values, out[b]["r"].values; lo, hi = block_bootstrap_ci(ra, rb, block=block)
        d, se, p_hac, p_bt = lw_var_test(ra, rb, block=block, M=M)
        row = {"Cụm": g, "Cặp": f"{a} − {b}", "ΔVol (pp)": (ra.std() - rb.std()) * np.sqrt(252) * 100, "CI lo": lo, "CI hi": hi,
               "p LW-HAC": p_hac, "p LW-boot": p_bt, "p JKM": jkm_test(ra, rb)[1]}
        if reb_dates is not None:                                   # chênh lệch turnover/kỳ + CI bootstrap theo kỳ (ghép cặp)
            dt = turnover_series(out[a], reb_dates) - turnover_series(out[b], reb_dates); dt = dt[~np.isnan(dt)]; rng = np.random.default_rng(seed)
            bs = dt[rng.integers(0, len(dt), (B, len(dt)))].mean(1)
            row.update({"ΔTurnover": dt.mean(), "Turn CI lo": np.percentile(bs, 2.5), "Turn CI hi": np.percentile(bs, 97.5)})
        rows.append(row)
    T = pd.DataFrame(rows); T.insert(T.columns.get_loc("p LW-boot") + 1, "p Holm", holm(T["p LW-boot"].values))   # Holm trên cả 12 cặp
    return T.set_index(["Cụm", "Cặp"])

def pair_grid(outs, pairs=PAIRS12, **kw):
    # outs = {nhãn cột: out}. Trả về D (ΔVol, pp) và P (p Holm trên các cặp có mặt, riêng từng cột); hàng = 12 cặp theo cụm.
    # Cặp có bộ không có trong out (ví dụ cụm A, B ở các cột HL_VOL) để trống.
    D, P = {}, {}; idx = pd.MultiIndex.from_tuples([(g, f"{a} − {b}") for g, a, b in pairs], names=["Cụm", "Cặp"])
    for lab, out in outs.items():
        pr = [p for p in pairs if p[1] in out and p[2] in out]; T = pair_table(out, pr, **kw)
        D[lab], P[lab] = T["ΔVol (pp)"].reindex(idx), T["p Holm"].reindex(idx)
    return pd.DataFrame(D), pd.DataFrame(P)

def pair_heatmap(grids, title, vmax=1.0, fname=None):
    # grids = {"Bán khống": (D, P), "Chỉ mua": (D, P)}. Mỗi ô ghi ΔVol; * nếu p Holm < 0,05. Xanh: bộ đứng trước rủi ro thấp hơn; đỏ: cao hơn.
    n = len(grids); D0 = next(iter(grids.values()))[0]
    fig, axes = plt.subplots(1, n, figsize=(2.6 + n * (1.6 + 0.75 * D0.shape[1]), 0.42 * len(D0) + 1.6), sharey=True)
    for ax, (mode, (D, P)) in zip(np.atleast_1d(axes), grids.items()):
        ax.imshow(D.values, cmap="RdYlGn_r", vmin=-vmax, vmax=vmax, aspect="auto")       # màu cắt ở ±vmax, số trong ô là giá trị thật
        for i in range(D.shape[0]):
            for j in range(D.shape[1]):
                v, p = D.values[i, j], P.values[i, j]
                if np.isnan(v): continue
                ax.text(j, i, f"{v:+.2f}".replace(".", ",").replace("-", "−") + ("*" if p < .05 else ""), ha="center", va="center", fontsize=8,
                        color="white" if abs(v) > .7 * vmax else "black", fontweight="bold" if p < .05 else "normal")
        ax.set_xticks(range(D.shape[1])); ax.set_xticklabels(D.columns, fontsize=8); ax.set_title(mode, fontsize=10)
        cl = D.index.get_level_values(0)
        for i in range(1, len(cl)):
            if cl[i] != cl[i - 1]: ax.axhline(i - .5, color="black", lw=1)                # vạch ngăn giữa các cụm
    a0 = np.atleast_1d(axes)[0]; a0.set_yticks(range(len(D0))); a0.set_yticklabels([f"{c[:1]} | {p}" for c, p in D0.index], fontsize=8)
    fig.suptitle(title + "  (ΔVol, pp; * = p Holm < 0,05)", fontsize=11); plt.tight_layout()
    if fname: savefig(fig, fname)
    return fig

def save_grid(grids, name):
    # lưu số liệu heatmap: ΔVol và p Holm, mọi cột × chế độ
    save(pd.concat({m: pd.concat({"ΔVol (pp)": D, "p Holm": P}, axis=1) for m, (D, P) in grids.items()}, axis=1), name)

def table_a(V, d=2):
    # Bảng A: hàng = phương pháp, cột = giá trị tham số × chế độ; in đậm giá trị thấp nhất mỗi cột
    return V.style.format(precision=d, decimal=",", na_rep="").highlight_min(axis=0, props="font-weight: bold")

vols = lambda out, ks=None: pd.Series({k: out[k]["m"]["Vol %"] for k in (ks or out)})
dv = lambda x, d=2: (f"{x:+.{d}f}").replace(".", ",").replace("-", "−")
e_ = lambda s: s.replace("*", "\\*")

# kiểm tra nhanh (không phải số liệu): ewma_sig đúng số học của ewma_standardize; VS chỉ phần chung với σ_m ≡ 1 là phép nhân hằng
_X = np.random.default_rng(1).standard_normal((120, 5)) * .01; _Z, _s = ewma_standardize(_X, 20); _S, _sT = ewma_sig(_X, 20)
assert np.allclose(_X / _S, _Z) and np.allclose(_s, _sT)
