# ---- 3.3 (tiếp) Kiểm định dùng chung: phương sai Ledoit–Wolf (2011), Jobson–Korkie–Memmel, Holm, so sánh cặp `compare_to` ----
def hac(u, L=None):
    # HAC Newey–West (Bartlett), L = ⌊4(T/100)^(2/9)⌋. (LW 2008/2011 dùng QS/Parzen + prewhitening – chưa làm.)
    T = len(u); L = L or int(4 * (T / 100) ** (2 / 9)); S = u.T @ u / T
    for l in range(1, L + 1): G = u[l:].T @ u[:-l] / T; S += (1 - l / (L + 1)) * (G + G.T)
    return S

def _lw_stat(y, Psi=None, b=None):
    # Δ = log σ²_a − log σ²_b (LW 2011, delta method); y_t = (r_a, r_b, r_a², r_b²)
    T = len(y); m = y.mean(0); va, vb = m[2] - m[0]**2, m[3] - m[1]**2
    g = np.array([-2 * m[0] / va, 2 * m[1] / vb, 1 / va, -1 / vb])
    if Psi is None:   # Ψ của bootstrap theo khối (LW 2008, công thức (9))
        z = (y - m)[:T // b * b].reshape(-1, b, 4).sum(1) / np.sqrt(b); Psi = z.T @ z / len(z)
    return np.log(va) - np.log(vb), np.sqrt(g @ Psi @ g / T)

def lw_var_test(ra, rb, block=21, M=2000, seed=SEED):
    # p-value HAC (chuẩn) và p-value studentized circular block bootstrap (LW 2008 Remark 3.2, áp cho phương sai như LW 2011)
    y = np.column_stack([ra, rb, ra**2, rb**2]); T = len(y)
    d, se = _lw_stat(y, hac(y - y.mean(0))); p_hac = 2 * norm.sf(abs(d / se))
    rng = np.random.default_rng(seed); l = T // block; stats = np.empty(M)
    for i in range(M):
        ix = ((rng.integers(0, T, l)[:, None] + np.arange(block)) % T).ravel()      # khối vòng
        ds, ses = _lw_stat(y[ix], b=block); stats[i] = abs(ds - d) / ses
    return d, se, p_hac, (np.sum(stats >= abs(d) / se) + 1) / (M + 1)

def jkm_test(ra, rb):
    # Jobson–Korkie (1981) với hiệu chỉnh Memmel (2003); giả định iid chuẩn
    T = len(ra); m1, m2 = ra.mean(), rb.mean(); s1, s2 = ra.std(ddof=1), rb.std(ddof=1); s12 = np.cov(ra, rb)[0, 1]
    th = (2 * s1**2 * s2**2 - 2 * s1 * s2 * s12 + .5 * m1**2 * s2**2 + .5 * m2**2 * s1**2 - m1 * m2 / (s1 * s2) * s12**2) / T
    z = (s2 * m1 - s1 * m2) / np.sqrt(th); return z, 2 * norm.sf(abs(z))

CORE5 = ["NL-LW", "EW-NL-LW", "EW-WeSpeR", "VS-NL-LW"]            # đối thủ lõi của EW-RIE* (họ Holm chính, định trước)
MAIN = ["EW-RIE*"] + CORE5                                          # bảng chính: EW-RIE* + họ lõi

def holm(p):
    p = np.asarray(p, float); o = np.argsort(p); adj = np.minimum(1, np.maximum.accumulate(p[o] * (len(p) - np.arange(len(p)))))
    out = np.empty(len(p)); out[o] = adj; return out

def turnover_series(o, reb_dates, cost=None):
    # turnover từng kỳ, khôi phục từ r − r_net tại các ngày tái cân bằng (kỳ đầu không có turnover)
    return ((o["r"] - o["r_net"]).reindex(reb_dates[1:]) / (cost or CONFIG["COST"])).values

def compare_to(out, target="EW-RIE*", rivals=None, reb_dates=None, block=21, M=2000, B=2000, seed=0):
    # So target với từng đối thủ trên CÙNG chuỗi ngày. ΔVol < 0 ⇒ target rủi ro thấp hơn.
    rivals = rivals or [k for k in out if k != target]; ra = out[target]["r"].values; rows = {}
    for b in rivals:
        assert out[b]["r"].index.equals(out[target]["r"].index), f"khác mẫu: {b}"
        rb = out[b]["r"].values; lo, hi = block_bootstrap_ci(ra, rb, block=block)
        d, se, p_hac, p_bt = lw_var_test(ra, rb, block=block, M=M)
        row = {"Vol": rb.std() * np.sqrt(252) * 100, "ΔVol (pp)": (ra.std() - rb.std()) * np.sqrt(252) * 100, "CI lo": lo, "CI hi": hi,
               "Δlog σ²": d, "p LW-HAC": p_hac, "p LW-boot": p_bt, "p JKM": jkm_test(ra, rb)[1], "lõi": b in CORE5}
        if reb_dates is not None:                                   # chênh lệch turnover/kỳ + CI bootstrap theo kỳ (ghép cặp)
            dt = turnover_series(out[target], reb_dates) - turnover_series(out[b], reb_dates); rng = np.random.default_rng(seed)
            bs = dt[rng.integers(0, len(dt), (B, len(dt)))].mean(1)
            row.update({"ΔTurnover": dt.mean(), "Turn CI lo": np.percentile(bs, 2.5), "Turn CI hi": np.percentile(bs, 97.5)})
        rows[b] = row
    C = pd.DataFrame(rows).T.infer_objects(); C["p Holm"] = np.nan
    core = C.index[C["lõi"].astype(bool)]
    if len(core): C.loc[core, "p Holm"] = holm(C.loc[core, "p LW-boot"].values.astype(float))   # Holm chỉ trên họ lõi
    return C

# unit test nhanh: gần trùng ⇒ p lớn; gấp đôi biến động ⇒ p≈0; JKM phản đối xứng, Sharpe chênh lớn ⇒ p≈0
_r = np.random.default_rng(SEED).standard_normal(1500) * .01
assert lw_var_test(_r, _r + 1e-5 * np.random.default_rng(1).standard_normal(1500), M=200)[3] > .1
assert lw_var_test(_r, 2 * _r[::-1], M=200)[2] < 1e-6                                   # Δ = −log 4
_q = np.random.default_rng(2).standard_normal(1500) * .01
assert np.isclose(jkm_test(_r, _q)[0], -jkm_test(_q, _r)[0]) and jkm_test(_r + .003, _q - .003)[1] < 1e-6
assert np.allclose(holm([.01, .04, .03]), [.03, .06, .06])

# ---- tiện ích sinh câu chữ từ bảng (mọi con số trong "Kết quả/Kết luận" lấy từ code, không gõ tay) ----
def order_txt(vol, keys=None, tol=0.03, d=2):
    # "A 12,93 < B 13,05 ≈ C 13,07": sắp tăng dần; "≈" khi hai giá trị liền kề chênh < tol
    v = vol.loc[keys] if keys is not None else vol; v = v.sort_values(); s = f"{v.index[0]} {f2(v.iloc[0], d)}"
    for (k0, a), (k1, b) in zip(v.items(), list(v.items())[1:]): s += (" ≈ " if b - a < tol else " < ") + f"{k1} {f2(b, d)}"
    return s.replace("*", "\\*")
def verdict(delta, lo, hi, who="EW-RIE\\*"):
    # kết luận từ CI 95%: thấp hơn / cao hơn có ý nghĩa, hoặc không khác biệt
    return f"{who} thấp hơn có ý nghĩa" if hi < 0 else (f"{who} cao hơn có ý nghĩa" if lo > 0 else "không khác biệt có ý nghĩa")
dci = lambda d, lo, hi: f"{d:+.2f} [{lo:+.2f}; {hi:+.2f}]".replace(".", ",")
