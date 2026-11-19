# Đối chiếu EW-WeSpeR (bản numpy của nhóm) với mã gốc PyTorch của tác giả: kết quả từ scripts/wesper_check.py (chạy riêng, nặng; đọc CSV)
_f = [f"{RESULTS_DIR}/T1b_oriol_check_sim.csv", f"{RESULTS_DIR}/T1b_oriol_check_hose.csv"]
if all(os.path.exists(f) for f in _f):
    OSall, OH = (pd.read_csv(f) for f in _f); OS = OSall[OSall["loss_finite"].astype(bool) & OSall["xi_med"].notna()]; nfail_s = len(OSall) - len(OS)   # mẫu mã gốc trả NaN bị loại khỏi thống kê, đếm riêng
    g = OS.groupby("h").agg(**{"W1 phổ τ (chuẩn hóa)": ("W1_tau", "median"), "sai lệch ξ, trung vị": ("xi_med", "median"), "sai lệch ξ, lớn nhất": ("xi_max", "max"),
                               "rủi ro GMV/tối ưu – nhóm": ("risk_nhom", "mean"), "rủi ro GMV/tối ưu – gốc": ("risk_oriol", "mean"), "chênh tỷ số rủi ro (TB)": ("risk_diff", "mean"),
                               "s/lần – nhóm": ("sec_nhom", "mean"), "s/lần – gốc": ("sec_oriol", "mean")})
    OHf = OH[OH["loss_finite"].astype(bool) & OH["xi_med"].notna()]; nfail = len(OH) - len(OHf)
    gh = OHf.agg({"W1_tau": "median", "xi_med": "median", "xi_max": "max", "sec_nhom": "mean", "sec_oriol": "mean"}).to_frame(f"HOSE ({len(OHf)}/{len(OH)} cửa sổ mã gốc chạy được)").T
    cap("Bảng", f"Đối chiếu EW-WeSpeR của nhóm với mã gốc (nlcvbo/wesper, 50 epoch): mô hình nhân tố Test 2 (N = 100, T = 250, {OS.groupby('h').size().min()}–{OS.groupby('h').size().max()} mẫu hợp lệ/h) và cửa sổ HOSE (N = 100, h = 60). ξ: sai lệch tương đối của trị riêng sau co (cùng chuẩn hóa vết), trung vị trên các trị riêng rồi trên các mẫu; W1: khoảng cách Wasserstein-1 của phổ quần thể τ chia cho trung bình; rủi ro GMV chia cho tối ưu của ma trận thật.")
    show(g, 4); show(gh, 4)
    gx, gr = OS.groupby("h").xi_med.median(), OS.groupby("h").risk_diff.mean()
    OK_XI, OK_RISK = bool((gx < 0.05).all() and OHf.xi_med.median() < 0.05), bool((gr.abs() < 0.01).all())
    md("**Kết quả.** Giả lập (sai lệch tương đối trung vị của ξ; chênh tỷ số rủi ro GMV, bản gốc so với bản nhóm): " + "; ".join(f"h = {h_}: {f2(100 * gx[h_], 1)}%; {f2(100 * gr[h_], 2)}%" for h_ in gx.index)
       + f". Mã gốc trả NaN ở {nfail_s}/{len(OSall)} mẫu giả lập (loại khỏi thống kê). HOSE: mã gốc trả NaN (loss không hữu hạn) ở {nfail}/{len(OH)} cửa sổ; ở {len(OHf)} cửa sổ còn lại sai lệch ξ trung vị {f2(100 * OHf.xi_med.median(), 1)}%, lớn nhất {f2(100 * OHf.xi_max.max(), 0)}% (ξ của vài trị riêng nhỏ nhất lệch xa). "
       f"Tiêu chí đạt (ξ < 5% và chênh rủi ro < 1%): **{'đạt' if OK_XI and OK_RISK else 'không đạt'}** (báo nguyên số, không sửa bản nhóm; không biết bên nào lệch: chưa có đáp án đúng cho dữ liệu thật). "
       f"Thời gian mã gốc {f2(OS.sec_oriol.mean(), 0)} s/lần (giả lập) và {f2(OHf.sec_oriol.mean(), 0)} s/lần (HOSE, cửa sổ chạy được) so với {f2(OS.sec_nhom.mean(), 2)} s/lần của bản nhóm (cùng đo khi nhiều tiến trình chạy song song nên không so được với §4.3); vì ≥ 30 s/lần nên **không** chạy backtest \"EW-WeSpeR (Oriol)\".")
    open(f"{RESULTS_DIR}/wesper_status.txt", "w", encoding="utf-8").write(f"EW-WeSpeR đã đối chiếu với mã gốc nlcvbo/wesper (repo chính thức chưa xác minh được): sai lệch ξ trung vị {f2(100 * float(gx.min()), 1)}–{f2(100 * float(gx.max()), 1)}% (giả lập, theo h), tiêu chí < 5% **{'đạt' if OK_XI and OK_RISK else 'không đạt'}**; mã gốc trả NaN ở {nfail}/{len(OH)} cửa sổ HOSE (§1b)")
    _fz = f"{RESULTS_DIR}/T1b_oriol_scatter.npz"
    if os.path.exists(_fz):
        Z = np.load(_fz); fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.6))
        for a, key, ttl in zip(ax, ("sim", "hose"), ("Mẫu giả lập (h = 60)", "Cửa sổ HOSE 10 (h = 60; mã gốc hội tụ)")):
            xn, xo = Z[f"{key}_xi_nhom"], Z[f"{key}_xi_oriol"]; xs, os_ = np.sort(xn), np.sort(xo)       # ξ ghép theo thứ tự trị riêng (tăng dần)
            a.scatter(xn, xo, s=14, color="#8e44ad"); lim = [min(xn.min(), xo.min()) * .9, max(xn.max(), xo.max()) * 1.1]
            a.plot(lim, lim, color="#52514e", lw=1); a.set_xscale("log"); a.set_yscale("log"); a.set_xlim(lim); a.set_ylim(lim)
            a.set_xlabel("ξ — bản nhóm (numpy)"); a.set_ylabel("ξ — bản gốc (PyTorch)"); a.set_title(ttl, fontsize=10); a.grid(alpha=.3, which="both")
        plt.tight_layout(); savefig(fig, "fig_oriol_xi_scatter")
        cap("Hình", "ξ (trị riêng sau co, cùng chuẩn hóa vết) của bản nhóm so với mã gốc của Oriol, theo thứ tự trị riêng của tương quan mẫu; đường chéo y = x (trục log).")
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
md("*Ghi chú:* bảng Test 2b-30 không có các bộ VS vì dữ liệu giả lập có biến động không đổi theo thời gian nên chuẩn hóa biến động (VS) không có tác dụng; thầy đã lưu ý VS chưa được xác nhận trong mô phỏng.")
