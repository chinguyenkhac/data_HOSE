# Đối chiếu EW-WeSpeR (bản numpy của nhóm) với mã gốc PyTorch của tác giả: kết quả từ scripts/wesper_check.py (chạy riêng, nặng; đọc CSV)
_f = [f"{RESULTS_DIR}/T1b_oriol_check_sim.csv", f"{RESULTS_DIR}/T1b_oriol_check_hose.csv"]
if all(os.path.exists(f) for f in _f):
    OS, OH = (pd.read_csv(f) for f in _f)
    g = OS.groupby("h").agg(**{"W1 phổ τ (chuẩn hóa)": ("W1_tau", "median"), "sai lệch ξ, trung vị": ("xi_med", "median"), "sai lệch ξ, lớn nhất": ("xi_max", "max"),
                               "rủi ro GMV/tối ưu – nhóm": ("risk_nhom", "mean"), "rủi ro GMV/tối ưu – gốc": ("risk_oriol", "mean"), "chênh tỷ số rủi ro (TB)": ("risk_diff", "mean"),
                               "s/lần – nhóm": ("sec_nhom", "mean"), "s/lần – gốc": ("sec_oriol", "mean")})
    gh = OH.agg({"W1_tau": "median", "xi_med": "median", "xi_max": "max", "sec_nhom": "mean", "sec_oriol": "mean"}).to_frame("HOSE (12 cửa sổ)").T
    cap("Bảng", "Đối chiếu EW-WeSpeR của nhóm với mã gốc (nlcvbo/wesper): mô hình nhân tố Test 2 (N = 100, T = 250, 20 lần lặp/h) và 12 cửa sổ HOSE. ξ: sai lệch tương đối của trị riêng sau co (cùng chuẩn hóa vết); W1: khoảng cách Wasserstein-1 của phổ quần thể τ chia cho trung bình.")
    show(g, 4); show(gh, 4)
    OK_XI, OK_RISK = (OS.xi_med.median() < 0.05) and (OH.xi_med.median() < 0.05), abs(OS.risk_diff.mean()) < 0.01
    md(f"**Kết quả.** Sai lệch tương đối trung vị của ξ: {f2(100 * OS.xi_med.median(), 2)}% (mô phỏng), {f2(100 * OH.xi_med.median(), 2)}% (HOSE); lớn nhất {f2(100 * OS.xi_max.max(), 1)}% / {f2(100 * OH.xi_max.max(), 1)}%. "
       f"Chênh tỷ số rủi ro GMV so với tối ưu (mô phỏng): {f2(100 * OS.risk_diff.mean(), 2)}%. Tiêu chí đạt (ξ < 5% và chênh rủi ro < 1%): **{'đạt' if OK_XI and OK_RISK else 'không đạt'}** (báo nguyên số, không sửa bản nhóm). "
       f"Thời gian mã gốc {f2(OS.sec_oriol.mean(), 1)} s/lần (mô phỏng) và {f2(OH.sec_oriol.mean(), 1)} s/lần (HOSE) so với {f2(OS.sec_nhom.mean(), 2)} s/lần của bản nhóm.")
else:
    md("**Đối chiếu mã gốc:** chưa có kết quả (lý do ở ô trên). Thay bằng Test 2b với 30 lần lặp có sai số chuẩn (ô dưới).")
# Test 2b-30: như Test 2b (mô hình nhân tố, N = 100, T = 250) nhưng 30 lần lặp/h, báo trung bình ± sai số chuẩn và chênh ghép cặp so với oracle
_f30 = f"{RESULTS_DIR}/T1b_test2b_30reps.csv"
if os.path.exists(_f30): R30 = pd.read_csv(_f30)
else:
    rng30 = np.random.default_rng(30); rows30 = []
    for hl in (15, 30, 60):
        w = ew_weights(T_, hl)
        for rep in range(30):
            Ct = factor_corr(N_, rng30); X = rng30.standard_normal((T_, N_)) @ np.linalg.cholesky(Ct).T; C, _ = ew_corr(X, w); lam, V_ = np.linalg.eigh(C)
            Co = renorm((V_ * np.einsum("ij,jk,ki->i", V_.T, Ct, V_)) @ V_.T); best = gmv(Ct) @ Ct @ gmv(Ct)
            for k, Ch in {"EW-NL-LW (v2)": renorm(nl_lw_S_v2(C, 1 / (w**2).sum())), "EW-NL-LW": renorm(nl_lw_S(C, 1 / (w**2).sum())), "EW-WeSpeR": ew_wesper_corr(C, w),
                          "EW-RIE*": ew_rie_corr(C, w), "Oracle": Co}.items():
                wh = gmv(Ch); rows30.append(dict(h=hl, rep=rep, method=k, ratio=wh @ Ct @ wh / best))
    R30 = pd.DataFrame(rows30); R30.to_csv(_f30, index=False)
g30 = R30.groupby(["method", "h"]).ratio.agg(["mean", lambda x: x.std() / np.sqrt(len(x))]).unstack("h"); g30.columns = [f"{'TB' if a == 'mean' else 'SE'} h={h}" for a, h in g30.columns]
pw = R30.pivot_table(index=["h", "rep"], columns="method", values="ratio"); pd_ = pd.DataFrame({h: {"EW-WeSpeR / Oracle − 1 (TB ± SE, %)": f"{100 * (pw.loc[h]['EW-WeSpeR'] / pw.loc[h]['Oracle'] - 1).mean():.2f} ± {100 * (pw.loc[h]['EW-WeSpeR'] / pw.loc[h]['Oracle'] - 1).std() / np.sqrt(30):.2f}",
    "EW-RIE* / Oracle − 1 (TB ± SE, %)": f"{100 * (pw.loc[h]['EW-RIE*'] / pw.loc[h]['Oracle'] - 1).mean():.2f} ± {100 * (pw.loc[h]['EW-RIE*'] / pw.loc[h]['Oracle'] - 1).std() / np.sqrt(30):.2f}"} for h in (15, 30, 60)})
cap("Bảng", "Test 2b với 30 lần lặp mỗi h (N = 100, T = 250, mô hình nhân tố như Test 2): rủi ro GMV / rủi ro tối ưu, trung bình (TB) và sai số chuẩn (SE); hàng dưới: chênh ghép cặp so với oracle.")
show(g30, 3); show(pd_, 3)
