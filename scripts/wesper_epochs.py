"""v6 Bước 3: mã gốc Oriol đến 200 epoch cho 1 mẫu giả lập (h, rep), ghi sai lệch ξ ở epoch 50, 100, 200.
Dùng: python wesper_epochs.py H REP. Mẫu giống hệt mẫu thứ REP của v5 (rng = default_rng(H)).
Giai đoạn 50 → 100 → 200 epoch: mỗi giai đoạn khởi tạo τ bằng τ của giai đoạn trước (Adam khởi động lại); ghi rõ trong báo cáo."""
import sys, os, time; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wesper_check as wc, numpy as np, pandas as pd, torch
H, REP = int(sys.argv[1]), int(sys.argv[2]); N_, T_ = 100, 250; rng = np.random.default_rng(H); w = wc.ew_weights(T_, H)
for r in range(REP + 1):
    Ct = wc.factor_corr(N_, rng); X = rng.standard_normal((T_, N_)) @ np.linalg.cholesky(Ct).T
C, sd = wc.ew_corr(X, w); Xs = (X - w @ X) / sd; lam, U = np.linalg.eigh(C)
out_n, info = wc.ew_wesper_corr(C, w, return_info=True); xi_n = np.asarray(info["xi"])
gmv = wc.gmv; best = gmv(Ct) @ Ct @ gmv(Ct); wn = gmv(out_n); risk_n = wn @ Ct @ wn / best
W = T_ * w; c = N_ / T_; d = torch.tensor(np.sort(W)); wd = torch.ones(T_, dtype=torch.float64) / T_
tau = wc.tau_init_lwo(Xs, w); ep = 0; rows = []; t0 = time.time()
for stage in (50, 50, 100):
    np.random.seed(0); torch.manual_seed(0)
    est = wc.WeSpeR_MD(bias=True, assume_centered=True).fit_from_F(lam, U, W, c=c, d=d, wd=wd, weights="Ndiracs", tau_init=tau, w_args=[1, 30],
                                                                n_epochs=stage, lr=5e-2, mu=0.1, omega=min(400, N_), method="root", verbose=False)
    ep += stage; L = np.asarray(est.loss, float); fin = bool(np.isfinite(L).all())
    est.get_covariance(d=d, wd=wd, weights="Ndiracs", w_args=[1, 30], method="root", verbose=False)
    xi_o = np.asarray(est.h_lambda_, float); xi_o = xi_o * N_ / xi_o.sum(); rel = np.abs(xi_o / xi_n - 1)
    So = (U * xi_o) @ U.T; dg = np.sqrt(np.diag(So)); So = So / np.outer(dg, dg); wo = gmv(So); risk_o = wo @ Ct @ wo / best
    rows.append(dict(h=H, rep=REP, epoch=ep, loss_last=float(L[-1]) if len(L) else np.nan, loss_finite=fin, xi_med=float(np.median(rel)), xi_max=float(rel.max()),
                     risk_nhom=risk_n, risk_oriol=risk_o, risk_diff=risk_o / risk_n - 1, sec_total=time.time() - t0))
    print(rows[-1], flush=True)
    pd.DataFrame(rows).to_csv(f"results_v6/T1b_oriol_epochs_h{H}_r{REP}.csv", index=False)
    if not fin: break
    tau = est.tau_fit_.detach().clone()
