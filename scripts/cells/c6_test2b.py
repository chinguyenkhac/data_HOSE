def gmv(S):
    w = np.linalg.solve(S, np.ones(len(S))); return w / w.sum()

def factor_corr(N, rng):
    sec = rng.integers(0, 8, N); B = np.zeros((N, 9))
    B[:, 0] = rng.uniform(.4, .8, N); B[np.arange(N), 1 + sec] = rng.uniform(.2, .5, N)
    return renorm(B @ B.T + np.diag(rng.uniform(.3, .6, N)))

rows = []
for hl in (15, 30, 60):
    w = ew_weights(T_, hl); acc = {}
    for rep in range(20):
        Ct = factor_corr(N_, rng); X = rng.standard_normal((T_, N_)) @ np.linalg.cholesky(Ct).T
        C, _ = ew_corr(X, w); lam, V = np.linalg.eigh(C)
        Co = renorm((V * np.einsum("ij,jk,ki->i", V.T, Ct, V)) @ V.T)    # oracle RIE
        wo = gmv(Ct); best = wo @ Ct @ wo
        for k, Ch in {"EW-Sample": C, "EW-RIE (q_eff)": rie_corr(C, N_ * (w**2).sum()),
                      "EW-NL-LW (v2)": renorm(nl_lw_S_v2(C, 1 / (w**2).sum())), "EW-NL-LW": renorm(nl_lw_S(C, 1 / (w**2).sum())),
                      "EW-WeSpeR": ew_wesper_corr(C, w), "EW-RIE*": ew_rie_corr(C, w), "Oracle": Co}.items():
            wh = gmv(Ch); acc.setdefault(k, []).append(wh @ Ct @ wh / best)
    rows += [dict(hl=hl, method=k, risk_ratio=np.mean(v)) for k, v in acc.items()]
t2b = pd.DataFrame(rows).pivot(index="method", columns="hl", values="risk_ratio").round(3)
teff = {hl: 1 / (ew_weights(T_, hl)**2).sum() for hl in (15, 30, 60)}
cap("Bảng", f"Test 2b: rủi ro GMV / rủi ro tối ưu (1 = hoàn hảo), trung bình 20 lần lặp, mô hình nhân tố N = 100, T = 250; cột = half-life h (T\\_eff = {', '.join(f'{round(v)}' for v in teff.values())}).")
show(t2b, 3)
assert (t2b.loc["EW-RIE*", [30, 60]] < t2b.loc["EW-RIE (q_eff)", [30, 60]]).all()
assert (t2b.loc["EW-NL-LW"] <= t2b.loc["EW-NL-LW (v2)"] + 1e-9).all()                 # bản sửa không kém v2
assert np.isclose(t2b.loc["EW-NL-LW", 60], t2b.loc["EW-NL-LW (v2)", 60])              # N < T_eff: trùng v2
assert (t2b.loc["EW-WeSpeR"] / t2b.loc["Oracle"] < 1.03).all()                        # WeSpeR trong 3% của oracle

g_ = lambda k, h: f2(t2b.loc[k, h], 3)
md(f"**Kết quả.** h = 15 (N > T\\_eff): EW-NL-LW bản thầy {g_('EW-NL-LW (v2)', 15)} → bản sửa **{g_('EW-NL-LW', 15)}** (oracle {g_('Oracle', 15)}); EW-WeSpeR {g_('EW-WeSpeR', 15)}; EW-RIE\\* {g_('EW-RIE*', 15)}. "
   f"h = 60 (N < T\\_eff): hai bản EW-NL-LW trùng nhau ({g_('EW-NL-LW', 60)}); EW-RIE\\* {g_('EW-RIE*', 60)}, EW-WeSpeR {g_('EW-WeSpeR', 60)}.\n\n"
   f"**Kết luận.** Bản sửa EW-NL-LW đúng; EW-WeSpeR cách oracle tối đa {f2(100 * (t2b.loc['EW-WeSpeR'] / t2b.loc['Oracle'] - 1).max(), 1)}%; EW-RIE\\* {'kém hơn' if t2b.loc['EW-RIE*', 15] > t2b.loc['EW-WeSpeR', 15] else 'không kém'} EW-WeSpeR khi N > T\\_eff (h = 15).")
_WSP["warm"].clear()          # xóa khởi tạo ấm của EW-WeSpeR do Test 2b để lại: §4 không phụ thuộc số lần lặp của Test 2b (tái lập được; xem Ghi chú)
