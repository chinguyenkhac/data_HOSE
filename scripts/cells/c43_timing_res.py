nn = 100 if 100 in TT.columns else TT.columns[0]; ncols = [c for c in TT.columns if isinstance(c, (int, np.integer))]
cap("Bảng", f"Thời gian một lần ước lượng ma trận N × N (ms, chưa gồm giải GMV): trung vị trên {K_WIN} cửa sổ HOSE thật (DCC: 3 cửa sổ), mỗi cửa sổ gọi {REPS} lần lấy nhỏ nhất; cấu hình chuẩn h = 60. "
   f"\"× NL-LW\": bội số tại N = {nn}; \"bậc\": độ dốc log–log từ N = {n0} đến {n1}. {HW}.")
show(TT.reindex(columns=ncols + [c for c in TT.columns if c not in ncols]), 1)
Q = TIMING[TIMING.method.isin(["EW-RIE*", "EW-WeSpeR (nguội)", "EW-WeSpeR (ấm)", "EW-NL-LW", "NL-LW", "VS-NL-LW", "VS-EW-RIE*", "DCC-GARCH(1,1)"])].pivot(index="method", columns="N", values=["q1", "q3"])
cap("Bảng", "Khoảng tứ phân vị [Q1; Q3] (ms) của các bộ chính trên các cửa sổ.")
show(pd.DataFrame({n_: [f"[{Q[('q1', n_)][k]:.1f}; {Q[('q3', n_)][k]:.1f}]" for k in Q.index] for n_ in ncols}, index=Q.index), 1)
cap("Bảng", f"EW-RIE\\*: thời gian theo bước (ms, N = 100, trung vị {K_WIN} cửa sổ). Lần gọi đầu tiên (gồm mô phỏng phổ null) ở N = 100: {TT.loc['EW-RIE* (lần đầu)', 100]:.0f} ms.")
show(PROF.round(1), 1)
fig, ax = plt.subplots(figsize=(7.5, 4.6))
for k in TT.index:
    if k.endswith("(lần đầu)") or k == "1/N": continue
    ax.plot(ncols, [TT.loc[k, n_] for n_ in ncols], marker="o", lw=2.4 if k == "EW-RIE*" else 1.4, color=col_of(k.replace(" (nguội)", "")), ls=":" if "ấm" in k else "-", label=k)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xticks(ncols, ncols); ax.set_xlabel("N"); ax.set_ylabel("ms / lần ước lượng"); ax.grid(alpha=.3, which="both")
ax.legend(fontsize=7, ncol=2, loc="upper left"); plt.tight_layout(); savefig(fig, "fig_timing_loglog")
cap("Hình", "Thời gian một lần ước lượng theo N (log–log); đường chấm: EW-WeSpeR khởi tạo ấm.")
x = lambda k, n_=nn: TT.loc[k, n_]
chk = {"EW-WeSpeR (nguội) chậm hơn EW-NL-LW ≥ 10 lần": x("EW-WeSpeR (nguội)") >= 10 * x("EW-NL-LW"), "EW-WeSpeR không còn ≈ 0,001 s": x("EW-WeSpeR (ấm)") > 5, "EW-RIE* ở N = 100 trong 0,05–0,5 s": 50 < x("EW-RIE*") < 500}
md(f"**Kết quả.** Ở N = {nn}: NL-LW {x('NL-LW'):.1f} ms, EW-NL-LW {x('EW-NL-LW'):.1f} ms, **EW-RIE\\* {x('EW-RIE*'):.0f} ms** ({x('EW-RIE*') / x('NL-LW'):.0f}× NL-LW), "
   f"**EW-WeSpeR {x('EW-WeSpeR (nguội)'):.0f} ms nguội / {x('EW-WeSpeR (ấm)'):.0f} ms ấm** ({x('EW-WeSpeR (nguội)') / x('EW-RIE*'):.1f}× / {x('EW-WeSpeR (ấm)') / x('EW-RIE*'):.1f}× EW-RIE\\*; {x('EW-WeSpeR (nguội)') / x('EW-NL-LW'):.0f}× EW-NL-LW), "
   f"DCC-GARCH {x('DCC-GARCH(1,1)') / 1e3:.1f} s. Bậc theo N: EW-RIE\\* {TT.loc['EW-RIE*', 'bậc theo N']:.2f}, EW-WeSpeR (nguội) {TT.loc['EW-WeSpeR (nguội)', 'bậc theo N']:.2f}, NL-LW {TT.loc['NL-LW', 'bậc theo N']:.2f}. "
   f"Bước tốn nhất của EW-RIE\\*: {PROF['%'].idxmax()} ({PROF['%'].max():.0f}%).\n\n"
   f"**Kết luận.** EW-RIE\\* nhanh hơn EW-WeSpeR cỡ {x('EW-WeSpeR (nguội)') / x('EW-RIE*'):.0f} lần (nguội), nhưng chậm hơn EW-NL-LW và NL-LW; chi phí này không đáng kể so với một kỳ tái cân bằng. "
   f"Kiểm tra: " + "; ".join(f"{k}: {'đạt' if v else 'không đạt'}" for k, v in chk.items()) + ".")
