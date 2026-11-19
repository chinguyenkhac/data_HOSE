# ---- T3c: Bảng 26, 27 (pair_table 12 cặp), Bảng 28 (EW-RIE* vs 1/N, PCA, DCC; phụ), Bảng 29 (cặp E theo độ dài khối), Hình 14 ----
PT = {m: pair_table(OUT0[m], reb_dates=REB_DATES) for m in MODES}
save(pd.concat(PT, names=["mode"]), "T3c_pair_table")
COLS_PT = ["ΔVol (pp)", "CI lo", "CI hi", "p LW-HAC", "p LW-boot", "p Holm", "p JKM", "ΔTurnover", "Turn CI lo", "Turn CI hi"]
for m in ("short_ok", "long_only"):
    cap("Bảng", f"{VN[m]}: 12 cặp định trước, cấu hình chuẩn ({th(len(OUT0[m]['EW-RIE*']['r']))} phiên). ΔVol = Vol(bộ trước) − Vol(bộ sau), pp/năm (< 0: bộ trước rủi ro thấp hơn); CI 95% bootstrap khối b = 21; p Holm trên 12 cặp; ΔTurnover/kỳ kèm CI.")
    show(PT[m][COLS_PT], 3)
AUXP = [("phụ", "EW-RIE*", "1/N"), ("phụ", "EW-RIE*", "PCA-auto"), ("phụ", "EW-RIE*", "DCC-GARCH(1,1)")]
T28 = pd.concat({VN[m]: pair_table(OUT0[m], AUXP, reb_dates=REB_DATES).droplevel(0) for m in ("short_ok", "long_only")}, names=["Chế độ", "Cặp"]); save(T28, "T3c_aux")
cap("Bảng", "Phụ (không vào họ Holm): EW-RIE\\* so với 1/N, PCA-auto, DCC-GARCH(1,1), cấu hình chuẩn.")
show(T28[[c for c in COLS_PT if c != "p Holm"]], 3)
rows = []
for m in ("short_ok", "long_only"):
    ra, rb = OUT0[m]["EW-RIE*"]["r"].values, OUT0[m]["VS-NL-LW"]["r"].values
    for b_ in (10, 21, 42):
        lo_, hi_ = block_bootstrap_ci(ra, rb, block=b_); d_, se_, ph, pb = lw_var_test(ra, rb, block=b_)
        rows.append({"Chế độ": VN[m], "Độ dài khối b": b_, "ΔVol (pp)": (ra.std() - rb.std()) * np.sqrt(252) * 100, "CI lo": lo_, "CI hi": hi_, "p LW-HAC": ph, "p LW-boot": pb})
T29 = pd.DataFrame(rows).set_index(["Chế độ", "Độ dài khối b"]); save(T29, "T3c_pairE_blocks")
cap("Bảng", "Cặp E (EW-RIE\\* − VS-NL-LW) với độ dài khối bootstrap 10/21/42 phiên (p HAC không phụ thuộc b).")
show(T29, 3)
fig, ax = plt.subplots(1, 2, figsize=(13, 5.4), sharey=True); GCOL = {"A": "#1baf7a", "B": "#2a78d6", "C": "#eda100", "D": "#8e44ad", "E": "#eb6834"}
for a, m in zip(ax, ("short_ok", "long_only")):
    t = PT[m]; y = np.arange(len(t))[::-1]
    for yi, ((g, p), r) in zip(y, t.iterrows()):
        c = GCOL[g[0]]; a.errorbar(r["ΔVol (pp)"], yi, xerr=[[r["ΔVol (pp)"] - r["CI lo"]], [r["CI hi"] - r["ΔVol (pp)"]]], fmt="o", color=c, ecolor=c, capsize=3, ms=7 if r["p Holm"] < .05 else 5,
                   mfc=c if r["p Holm"] < .05 else "white")
    a.axvline(0, color="#52514e", lw=1); a.set_yticks(y, [f"{g[0]} | {p}" for g, p in t.index], fontsize=8); a.grid(axis="x", alpha=.3); a.set_title(VN[m], fontsize=10)
    a.set_xlabel("ΔVol = Vol(bộ trước) − Vol(bộ sau), pp/năm")
    cl = [g for g, _ in t.index]
    for i in range(1, len(cl)):
        if cl[i] != cl[i - 1]: a.axhline(y[i] + .5, color="#cccccc", lw=.8)
plt.tight_layout(); savefig(fig, "fig_14_pairs_ci")
cap("Hình", "ΔVol và CI 95% (bootstrap khối, b = 21) của 12 cặp, cấu hình chuẩn, xếp theo cụm A–E; chấm đặc: p Holm < 0,05; đường dọc tại 0.")
pe_ = {m: PT[m].xs("EW-RIE* − VS-NL-LW", level=1).iloc[0] for m in MODES}; t25 = lambda m, k, c: T25.loc[(VN[m], k), c]
sig = {m: [f"{e_(p)} ({dv(r['ΔVol (pp)'])})" for (g, p), r in PT[m].iterrows() if r["p Holm"] < .05] for m in MODES}
md("**Kết quả.** Cặp E (EW-RIE\\* − VS-NL-LW): " + "; ".join(f"{VN[m]} ΔVol {dv(pe_[m]['ΔVol (pp)'])} pp [{dv(pe_[m]['CI lo'])}; {dv(pe_[m]['CI hi'])}], p LW-boot {f2(pe_[m]['p LW-boot'], 3)}, p Holm {f2(pe_[m]['p Holm'], 3)}, "
   f"ΔTurnover {dv(pe_[m]['ΔTurnover'])}/kỳ [{dv(pe_[m]['Turn CI lo'])}; {dv(pe_[m]['Turn CI hi'])}], chi phí GD {f2(t25(m, 'EW-RIE*', 'Chi phí GD %/năm'))} so với {f2(t25(m, 'VS-NL-LW', 'Chi phí GD %/năm'))}%/năm, "
   f"số mã hiệu dụng {f2(t25(m, 'EW-RIE*', 'Số mã hiệu dụng'), 1)} so với {f2(t25(m, 'VS-NL-LW', 'Số mã hiệu dụng'), 1)}, tỷ trọng max {f2(t25(m, 'EW-RIE*', 'Tỷ trọng max %'), 1)}% so với {f2(t25(m, 'VS-NL-LW', 'Tỷ trọng max %'), 1)}%" for m in ("short_ok", "long_only"))
   + ". Các cặp có p Holm < 0,05 — " + "; ".join(f"{VN[m]}: " + (", ".join(sig[m]) if sig[m] else "không có") for m in ("short_ok", "long_only")) + ".\n\n"
   f"**Kết luận.** EW-RIE\\* và VS-NL-LW {'ngang nhau về rủi ro' if all(pe_[m]['p Holm'] >= .05 for m in MODES) else 'khác nhau có ý nghĩa về rủi ro'}; "
   f"EW-RIE\\* {'giao dịch ít hơn có ý nghĩa' if all(pe_[m]['Turn CI hi'] < 0 for m in MODES) else 'không giao dịch ít hơn một cách nhất quán'} (CI ΔTurnover {'không chứa' if all(pe_[m]['Turn CI hi'] < 0 for m in MODES) else 'chứa'} 0).")
