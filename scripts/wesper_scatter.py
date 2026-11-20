"""Bước 2 (v5): lưu ξ của bản nhóm và bản gốc cho MỘT mẫu giả lập (h = 60, mẫu đầu của wesper_check sim) và MỘT cửa sổ HOSE (cửa sổ 10), để vẽ scatter ξ_nhóm – ξ_gốc."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wesper_check as wc, numpy as np
ns, np_ = wc.ns, wc.np
rng = np.random.default_rng(0); N_, T_ = 100, 250; out = {}
w = wc.ew_weights(T_, 60); Ct = wc.factor_corr(N_, rng); X = rng.standard_normal((T_, N_)) @ np.linalg.cholesky(Ct).T; C, sd_ = wc.ew_corr(X, w); Xs = (X - w @ X) / sd_
def one(C, w, Xs):
    _, info = wc.ew_wesper_corr(C, w, return_info=True); xi_o, tau_o, U, sec, est = wc.oriol(C, w, Xs, n_epochs=wc.NEP); N = len(C); xi_o = xi_o * N / xi_o.sum()
    return np.asarray(info["xi"]), xi_o, np.sort(info["tau"]), np.sort(tau_o)
out["sim"] = one(C, w, Xs)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cells", "c43_timing.py")).read().split("hl = CONFIG")[0], ns)
Xs = ns["timing_windows"](100); w = wc.ew_weights(250, wc.CONFIG["HL_EW"]); X0 = Xs[10]; C, sd_ = wc.ew_corr(X0, w); out["hose"] = one(C, w, (X0 - w @ X0) / sd_)
np.savez("results_v5/T1b_oriol_scatter.npz", **{f"{k}_{n}": v for k, vs in out.items() for n, v in zip(("xi_nhom", "xi_oriol", "tau_nhom", "tau_oriol"), vs)}); print("saved")
