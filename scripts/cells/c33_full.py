# ---- 3.3 (tiếp) Đối chứng bổ sung (1/N, PCA, DCC-GARCH, VS-EW-RIE*), tập FULL, chạy từng phương pháp có cache ----
from arch import arch_model

def est_equal_weight_proxy(X):
    # 1/N: dùng ma trận đơn vị -> GMV = 1/N (chiến lược phân bổ, KHÔNG phải bộ ước lượng hiệp phương sai)
    return np.eye(X.shape[1])

def est_pca(k):
    # Σ = B Bᵀ + diag(ψ): k thành phần chính của hiệp phương sai mẫu, phần dư chéo (đối xứng, PSD theo cấu trúc)
    def est(X):
        S = np.cov(X, rowvar=False); lam, Q = np.linalg.eigh(S); B = Q[:, -k:] * np.sqrt(lam[-k:])
        return B @ B.T + np.diag(np.maximum(np.diag(S) - (B**2).sum(1), 1e-10))
    return est

PCA_K = []
def est_pca_auto(X, ks=(1, 3, 5), split=0.7):
    # chọn k CHỈ trong cửa sổ huấn luyện: ước lượng trên 70% đầu, đo phương sai GMV trên 30% cuối, rồi ước lượng lại trên cả cửa sổ
    n = int(len(X) * split)
    k = min(ks, key=lambda k: np.var(X[n:] @ gmv_unconstrained(est_pca(k)(X[:n]))))
    PCA_K.append(k); return est_pca(k)(X)

DCC_LOG, _DCC_CACHE = [], {}
def _dcc_ncl(p, Z, Qbar):
    # −composite log-lik (Engle, Shephard & Sheppard 2008): tổng log-lik 2×2 của các cặp kề nhau (i, i+1).
    a, b = p
    if a < 0 or b < 0 or a + b >= 0.999: return 1e10
    z1, z2 = Z[:, :-1], Z[:, 1:]; q11, q22, q12 = np.diag(Qbar)[:-1], np.diag(Qbar)[1:], np.diag(Qbar, 1)
    c11, c22, c12 = q11.copy(), q22.copy(), q12.copy(); nll = 0.0
    for t in range(len(Z)):
        if t:
            c11 = (1-a-b)*q11 + a*z1[t-1]**2 + b*c11; c22 = (1-a-b)*q22 + a*z2[t-1]**2 + b*c22
            c12 = (1-a-b)*q12 + a*z1[t-1]*z2[t-1] + b*c12
        rho = c12 / np.sqrt(c11 * c22); d = 1 - rho**2
        nll += 0.5 * np.sum(np.log(d) + (z1[t]**2 + z2[t]**2 - 2*rho*z1[t]*z2[t]) / d)
    return nll

def est_dcc(X, h=21, use_cache=True):
    # DCC-GARCH(1,1) (Engle 2002): bước 1 GARCH(1,1) đơn biến (`arch`) cho từng mã; bước 2 (a, b) bằng composite
    # likelihood + correlation targeting; ma trận Q_t đầy đủ N×N. Dự báo: D = căn phương sai GARCH trung bình h phiên tới, R = R_{T+1|T}; Σ = D R D.
    key = hash(X.tobytes())
    if use_cache and key in _DCC_CACHE: return _DCC_CACHE[key]               # cùng cửa sổ ở long_only/short_ok → không ước lượng lại
    T, N = X.shape; Z = np.empty_like(X); hv = np.empty(N); bad = 0
    for i in range(N):
        try:
            r = arch_model(100 * X[:, i], mean="Constant", vol="GARCH", p=1, q=1, rescale=False).fit(disp="off", show_warning=False)
            ok = r.convergence_flag == 0 and r.params["alpha[1]"] + r.params["beta[1]"] < 1
        except Exception:
            ok = False
        if ok:
            Z[:, i] = r.std_resid; hv[i] = r.forecast(horizon=h, reindex=False).variance.values[-1].mean() / 1e4
        else:                                                   # dự phòng: phương sai mẫu (đếm vào DCC_LOG)
            bad += 1; Z[:, i] = (X[:, i] - X[:, i].mean()) / X[:, i].std(); hv[i] = X[:, i].var()
    Qbar = Z.T @ Z / T
    res = minimize(_dcc_ncl, x0=[0.02, 0.95], args=(Z, Qbar), method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-3, maxiter=200))
    a, b = res.x if res.fun < 1e9 else (0.0, 0.0)
    Qt = Qbar.copy()
    for t in range(1, T + 1): Qt = (1 - a - b) * Qbar + a * np.outer(Z[t-1], Z[t-1]) + b * Qt    # Q_{T+1}
    d = 1 / np.sqrt(np.diag(Qt)); sd = np.sqrt(hv)
    S = (Qt * np.outer(d, d)) * np.outer(sd, sd)
    DCC_LOG.append(dict(a=a, b=b, garch_fail=bad, dcc_ok=bool(res.success)))
    if use_cache: _DCC_CACHE[key] = S
    return S

def make_vs_ew_rie(hl_vol, hl):
    # VS + EW-RIE*: chuẩn hóa biến động EWMA (như VS-NL-LW), rồi EW-RIE* trên tương quan trọng số mũ của Z; nhân lại biến động hiện tại
    def est(X):
        Z, sig = ewma_standardize(X, hl_vol); Z = Z[hl_vol:]
        w = ew_weights(len(Z), hl); C, _ = ew_corr(Z, w)
        return ew_rie_corr(C, w) * np.outer(sig, sig)
    return est
est_vs_ew_rie = make_vs_ew_rie(CONFIG["HL_VOL"], CONFIG["HL_EW"])

FULL = ["Sample", "Ledoit-Wolf", "NL-LW", "MP-clip", "RIE", "VS-NL-LW", "VS-RIE", "EW-NL-LW", "EW-RIE (q_eff)", "EW-WeSpeR", "EW-RIE*",
        "PCA-auto", "DCC-GARCH(1,1)", "1/N", "VS-EW-RIE*"]
def build_full(cfg):
    E = build_estimators(dict(cfg, QUICK=False))
    E.update({"PCA-auto": est_pca_auto, "DCC-GARCH(1,1)": est_dcc, "1/N": est_equal_weight_proxy,
              "VS-EW-RIE*": make_vs_ew_rie(cfg["HL_VOL"], cfg["HL_EW"])})
    return {k: E[k] for k in FULL}

# Tham số nào mỗi phương pháp thực sự dùng → chuẩn hóa phần không dùng để một lần tính phục vụ nhiều cấu hình (cache theo từng phương pháp)
USES_HL_EW = {"EW-NL-LW", "EW-RIE (q_eff)", "EW-WeSpeR", "EW-RIE*", "VS-EW-RIE*"}; USES_HL_VOL = {"VS-NL-LW", "VS-RIE", "VS-EW-RIE*"}
def canon_cfg(cfg, k):
    return dict(cfg, HL_EW=cfg["HL_EW"] if k in USES_HL_EW else 60, HL_VOL=cfg["HL_VOL"] if k in USES_HL_VOL else 20)

def run_full(cfg=None, long_only=True, methods=None, data=None, tag=""):
    # chạy TỪNG phương pháp (mỗi cái có cache riêng) rồi ghép ⇒ thêm phương pháp không làm tính lại phương pháp khác
    cfg = cfg or CONFIG; E = build_full(cfg); methods = list(methods or FULL); parts = {}
    for k in methods:
        if k == "EW-WeSpeR": _WSP["warm"].clear()               # khởi tạo ấm không rò giữa các lần chạy ⇒ tái lập được
        parts[k] = run({k: E[k]}, canon_cfg(cfg, k), long_only, data, tag)
    ref = parts[methods[0]]
    for k in methods: assert [u["date"] for u in parts[k]["ulog"]] == [u["date"] for u in ref["ulog"]], f"universe khác: {k}"
    out = {k: parts[k]["out"][k] for k in methods}
    idx = out[methods[0]]["r"].index; assert all(o["r"].index.equals(idx) for o in out.values()), "common-sample vi phạm"
    return dict(out=out, ulog=ref["ulog"], sec={k: parts[k]["sec"].get(k, np.nan) for k in methods},
                newton=tuple(np.sum([parts[k]["newton"] for k in methods], axis=0)))
