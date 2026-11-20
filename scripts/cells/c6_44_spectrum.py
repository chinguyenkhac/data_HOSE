# ---- 4.4 Phổ trị riêng trước và sau làm sạch: giả lập (có oracle) và cửa sổ HOSE cuối ----
def spec_clean(C, w):
    lam, Vv = np.linalg.eigh(C); proj = lambda M: np.einsum("ij,jk,ki->i", Vv.T, M, Vv)
    return lam, Vv, {"EW-NL-LW": proj(renorm(nl_lw_S(C, 1 / (w**2).sum()))), "EW-RIE (q_eff)": proj(rie_corr(C, len(C) * (w**2).sum())),
                     "EW-WeSpeR": proj(ew_wesper_corr(C, w)), "EW-RIE*": proj(ew_rie_corr(C, w))}
_rng44 = np.random.default_rng(44); w44 = ew_weights(CONFIG["WINDOW"], CONFIG["HL_EW"])
Ct44 = factor_corr(100, _rng44); X44 = _rng44.standard_normal((CONFIG["WINDOW"], 100)) @ np.linalg.cholesky(Ct44).T
lam_s, V_s, XI_s = spec_clean(ew_corr(X44, w44)[0], w44); XI_s["Oracle"] = np.einsum("ij,jk,ki->i", V_s.T, Ct44, V_s)
u_last = STD0["ulog"][-1]; s_ = POS[u_last["date"]]; X_h = R_BT.iloc[s_ - CONFIG["WINDOW"]:s_][u_last["tickers"]].fillna(0).values
lam_h, V_h, XI_h = spec_clean(ew_corr(X_h, w44)[0], w44)
SPC = {"lấy mẫu": "#9aa0a6", "EW-NL-LW": COL["EW-NL-LW"], "EW-RIE (q_eff)": "#2a78d6", "EW-WeSpeR": COL["EW-WeSpeR"], "EW-RIE*": COL["EW-RIE*"]}
fig, ax = plt.subplots(1, 2, figsize=(12.5, 5))
for a, lam_, XI, ttl in ((ax[0], lam_s, XI_s, "Giả lập (mô hình nhân tố, biết ma trận thật)"), (ax[1], lam_h, XI_h, f"HOSE: cửa sổ tái cân bằng cuối ({u_last['date'].date()})")):
    a.plot(lam_, lam_, color="#9aa0a6", lw=1, ls="--", label="y = x (không làm sạch)")
    for k in ("EW-NL-LW", "EW-RIE (q_eff)", "EW-WeSpeR", "EW-RIE*"): a.plot(lam_, XI[k], color=SPC[k], lw=1.6 if k == "EW-RIE*" else 1.2, label=k)
    if "Oracle" in XI: a.scatter(lam_, XI["Oracle"], s=10, color="black", zorder=3, label="oracle vᵀC_thật v")
    a.set_xscale("log"); a.set_yscale("log"); a.set_xlabel("λ (trị riêng tương quan mẫu có trọng số)"); a.set_ylabel("ξ (trị riêng sau làm sạch)"); a.set_title(ttl, fontsize=10); a.grid(alpha=.3, which="both")
ax[0].legend(fontsize=8); plt.tight_layout(); savefig(fig, "fig_5_pho_tri_rieng")
cap("Hình", "Phổ trị riêng trước (trục x) và sau làm sạch (trục y), log–log; N = 100, T = 250, h = 60. Trái: giả lập có oracle; phải: cửa sổ HOSE thật (không có oracle).")
bulk = lam_s < np.quantile(lam_s, .9)
err = {k: (np.median(np.abs(np.log(XI_s[k][bulk] / XI_s["Oracle"][bulk]))), abs(np.log(XI_s[k][-1] / XI_s["Oracle"][-1]))) for k in ("EW-NL-LW", "EW-RIE (q_eff)", "EW-WeSpeR", "EW-RIE*")}
bb, bt = min(err, key=lambda k: err[k][0]), min(err, key=lambda k: err[k][1])
md(f"**Kết quả.** Ở giả lập, bám oracle nhất ở phần khối (90% trị riêng nhỏ, sai lệch log trung vị) là **{e_(bb)}** ({f2(err[bb][0], 3)}; EW-RIE\\* {f2(err['EW-RIE*'][0], 3)}), ở trị riêng lớn nhất là **{e_(bt)}** "
   f"(oracle {f2(XI_s['Oracle'][-1], 1)}; EW-RIE\\* {f2(XI_s['EW-RIE*'][-1], 1)}, EW-NL-LW {f2(XI_s['EW-NL-LW'][-1], 1)}, EW-RIE (q\\_eff) {f2(XI_s['EW-RIE (q_eff)'][-1], 1)}). "
   f"Trên HOSE, trị riêng lớn nhất (mode thị trường) λ = {f2(lam_h[-1], 1)} được giữ là {f2(XI_h['EW-RIE*'][-1], 1)} (EW-RIE\\*) và {f2(XI_h['EW-NL-LW'][-1], 1)} (EW-NL-LW).\n\n"
   f"**Kết luận.** Các bộ khác nhau chủ yếu ở phần khối và ở mode thị trường; lệch oracle nhiều nhất ở phần khối là {e_(max(err, key=lambda k: err[k][0]))}.")
