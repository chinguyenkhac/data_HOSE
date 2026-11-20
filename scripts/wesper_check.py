"""Bước 3: đối chiếu EW-WeSpeR (bản numpy của nhóm) với mã gốc (PyTorch) của tác giả.
Mã gốc: https://github.com/nlcvbo/wesper (thư mục code/), commit 1df4890cd2f21951d36988f4f16d84f4eff442e0 (xem CHECK_LOG).
Quy đổi trọng số: bản nhóm Σw = 1 (w_t); mã gốc W_t = T·w_t (trung bình 1), S = XᵀWX/T, c = N/T; phân phối trọng số = các giá trị W_t (Ndiracs, khối lượng 1/T).
Đầu vào chung (C, w): C = tương quan có trọng số EW (ew_corr); mã gốc nhận trị riêng/vector riêng của chính C."""
import sys, os, time, json, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, "/home/user/nlcvbo/wesper/code")
from hose_ns import load_ns
ns = load_ns("EW_RIE_HOSE_v5.ipynb")
import numpy as np, pandas as pd, torch
from scipy.stats import wasserstein_distance
from WeSpeR_MD import WeSpeR_MD
from weighted_LWO_estimator import wLWO_estimator
import WeSpeR_MD_utils as _U, scipy.optimize as _so
def _min_np(fun, x0=None, args=(), **k):      # tương thích scipy mới: x0 phải là numpy (mã gốc truyền tensor torch); không đổi mã gốc
    x0 = np.asarray(x0.numpy() if hasattr(x0, "numpy") else x0, dtype=float)
    return _so.minimize(fun, x0, args=args, **k)
_U.minimize = _min_np
def _fl(f): return lambda *a, **k: float(f(*a, **k))      # scipy mới: hàm mục tiêu phải trả float, không phải tensor torch
for _n in [n for n in dir(_U) if n.endswith(("_w","_w_ewma","_w_unif")) and "_loss_" in n and callable(getattr(_U, n))]: setattr(_U, _n, _fl(getattr(_U, _n)))
ew_weights, ew_corr, ew_wesper_corr, renorm, gmv, P, V, CONFIG = (ns[k] for k in ("ew_weights", "ew_corr", "ew_wesper_corr", "renorm", "gmv_unconstrained", "P", "V", "CONFIG"))
timing_windows_src = None
RES = "results_v5"; LOG = []

def factor_corr(N, rng):          # đúng như Test 2 (§1b)
    sec = rng.integers(0, 8, N); B = np.zeros((N, 9))
    B[:, 0] = rng.uniform(.4, .8, N); B[np.arange(N), 1 + sec] = rng.uniform(.2, .5, N)
    return renorm(B @ B.T + np.diag(rng.uniform(.3, .6, N)))

def tau_init_lwo(Xs, w):
    # khởi tạo τ như WeSpeR_experiments.py (dòng 117–128): trị riêng của bản co weighted-LWO (wLWO_estimator), thêm điểm lấp đầy, chuẩn hóa trung bình
    T = len(w); SLWO = wLWO_estimator(np.array(Xs, float), np.asarray(w, float), assume_centered=True, S_r=None, est=False)
    e = np.linalg.eigvalsh((SLWO + SLWO.T) / 2); ti = np.unique(np.around(e, 6)); add = np.linspace(e.min(), e.max(), e.shape[0] - ti.shape[0] + 2)[1:-1]
    ti = np.sort(np.concatenate([ti, add])); return torch.tensor(ti / ti.mean() * e.mean())

def oriol(C, w, Xs, n_epochs=10, lr=5e-2, seed=0, mu=0.1):
    # mã gốc: fit_from_F (trị riêng/vector riêng của C), weights = 'Ndiracs' với d = W (giá trị trọng số), wd = 1/T; tau_init như mã thí nghiệm của tác giả
    T, N = len(w), len(C); W = T * w; lam, U = np.linalg.eigh(C); c = N / T
    d = torch.tensor(np.sort(W)); wd = torch.ones(T, dtype=torch.float64) / T
    np.random.seed(seed); torch.manual_seed(seed); t0 = time.time()
    est = WeSpeR_MD(bias=True, assume_centered=True).fit_from_F(lam, U, W, c=c, d=d, wd=wd, weights="Ndiracs", tau_init=tau_init_lwo(Xs, w),
                                                              w_args=[1, 30], n_epochs=n_epochs, lr=lr, mu=mu, omega=min(400, N), method="root", verbose=False)
    S = est.get_covariance(d=d, wd=wd, weights="Ndiracs", w_args=[1, 30], method="root", verbose=False)
    sec = time.time() - t0; xi = np.asarray(est.h_lambda_, float); tau = np.sort(est.tau_fit_.detach().numpy())
    return xi, tau, U, sec, est

def compare(C, w, Xs, Ct=None, tag="", n_epochs=10):
    N = len(C); out_n, info = ew_wesper_corr(C, w, return_info=True); lam, V_ = np.linalg.eigh(C)
    t0 = time.time(); ew_wesper_corr(C, w); sec_n = time.time() - t0
    xi_o, tau_o, U, sec_o, est = oriol(C, w, Xs, n_epochs=n_epochs); fin = bool(np.isfinite(np.asarray(est.loss, float)).all()) if hasattr(est.loss, '__len__') else True
    xi_n = info["xi"]; xi_o = xi_o * N / xi_o.sum()                       # cùng chuẩn hóa vết (tr = N) như bản nhóm
    tau_n = np.sort(info["tau"]); sc = lambda t: t / t.mean()
    w1 = wasserstein_distance(sc(tau_n), sc(tau_o))                      # Wasserstein-1 chuẩn hóa (trung bình = 1)
    rel = np.abs(xi_o / xi_n - 1)
    row = dict(tag=tag, loss_finite=fin, W1_tau=w1, xi_med=np.median(rel), xi_max=rel.max(), sec_nhom=sec_n, sec_oriol=sec_o)
    if Ct is not None:
        best = gmv(Ct) @ Ct @ gmv(Ct)
        for nm, xi in (("nhom", xi_n), ("oriol", xi_o)):
            Ch = renorm((U * xi) @ U.T) if nm == "oriol" else out_n; wh = gmv(Ch); row[f"risk_{nm}"] = wh @ Ct @ wh / best
        row["risk_diff"] = row["risk_oriol"] / row["risk_nhom"] - 1
    return row

NEP = 50      # số epoch của mã gốc (tác giả: 10 trong thí nghiệm, 100 mặc định); 50 cho loss ≈ 1e-3 ở N = 100

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "sim"
    try:
        if mode == "sim":          # python wesper_check.py sim H REPS
            hl = int(sys.argv[2]); REPS = int(sys.argv[3]); N_, T_ = 100, 250; rows = []; rng = np.random.default_rng(hl); w = ew_weights(T_, hl)
            for rep in range(REPS):
                Ct = factor_corr(N_, rng); X = rng.standard_normal((T_, N_)) @ np.linalg.cholesky(Ct).T; C, sd_ = ew_corr(X, w); Xs = (X - w @ X) / sd_
                r = compare(C, w, Xs, Ct, tag=f"mô phỏng h={hl}", n_epochs=NEP); r.update(h=hl, rep=rep, src="sim"); rows.append(r); print(r, flush=True)
                pd.DataFrame(rows).to_csv(f"{RES}/T1b_oriol_check_sim_h{hl}.csv", index=False)
        else:                      # python wesper_check.py hose
            exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cells", "c43_timing.py")).read().split("hl = CONFIG")[0], ns)
            Xs_ = ns["timing_windows"](100); w = ew_weights(250, CONFIG["HL_EW"]); real = []
            for i, X in enumerate(Xs_):
                C, sd_ = ew_corr(X, w); Xs = (X - w @ X) / sd_; r = compare(C, w, Xs, None, tag=f"HOSE cửa sổ {i}", n_epochs=NEP); r.update(h=CONFIG["HL_EW"], rep=i, src="hose"); real.append(r); print(r, flush=True)
                pd.DataFrame(real).to_csv(f"{RES}/T1b_oriol_check_hose.csv", index=False)
    except Exception:
        traceback.print_exc(); open(f"{RES}/logs/oriol_error_{mode}.txt", "w").write(traceback.format_exc())
