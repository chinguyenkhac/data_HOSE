# ---- 3.3 (tiếp) Kiểm định dùng chung: phương sai Ledoit–Wolf (2011) HAC + bootstrap khối, Jobson–Korkie–Memmel ----
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

# unit test nhanh: gần trùng ⇒ p lớn; gấp đôi biến động ⇒ p≈0; JKM phản đối xứng
_r = np.random.default_rng(SEED).standard_normal(1500) * .01
assert lw_var_test(_r, _r + 1e-5 * np.random.default_rng(1).standard_normal(1500), M=200)[3] > .1
assert lw_var_test(_r, 2 * _r[::-1], M=200)[2] < 1e-6
_q = np.random.default_rng(2).standard_normal(1500) * .01
assert np.isclose(jkm_test(_r, _q)[0], -jkm_test(_q, _r)[0]) and jkm_test(_r + .003, _q - .003)[1] < 1e-6
