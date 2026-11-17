# T5 – theo giai đoạn: ΔVol (EW-RIE* − VS-NL-LW) trong từng giai đoạn của PERIODS, CI 95% block bootstrap (b = 21), p LW-bootstrap.
rows = []
for m in MODES:
    for p_, s_, e_ in PERIODS:
        ra, rb = OUT0[m]["EW-RIE*"]["r"][s_:e_].values, OUT0[m]["VS-NL-LW"]["r"][s_:e_].values
        if len(ra) < 40: continue
        lo_, hi_ = block_bootstrap_ci(ra, rb); pb = lw_var_test(ra, rb, M=1000)[3]
        rows.append(dict(mode=m, period=p_, n=len(ra), **{"Vol EW-RIE*": ra.std() * np.sqrt(252) * 100, "Vol VS-NL-LW": rb.std() * np.sqrt(252) * 100,
                          "ΔVol (pp)": (ra.std() - rb.std()) * np.sqrt(252) * 100, "CI lo": lo_, "CI hi": hi_, "p LW-boot": pb}))
T5G = pd.DataFrame(rows); save(T5G, "T5_periods_ew_rie_vs_vsnllw")
cap("Bảng", "ΔVol = Vol(EW-RIE\\*) − Vol(VS-NL-LW) theo giai đoạn (> 0: VS-NL-LW rủi ro thấp hơn); CI 95% block bootstrap b = 21; p: kiểm định phương sai LW-bootstrap (mô tả, không hiệu chỉnh).")
show(T5G.assign(mode=T5G["mode"].map(VN)).set_index(["mode", "period"]), 3)
fig, ax = plt.subplots(1, 2, figsize=(12, 3.8), sharey=True)
for a, m in zip(ax, MODES):
    d = T5G[T5G["mode"] == m].reset_index(drop=True); y = np.arange(len(d))
    a.errorbar(d["ΔVol (pp)"], y, xerr=[d["ΔVol (pp)"] - d["CI lo"], d["CI hi"] - d["ΔVol (pp)"]], fmt="o", color=COL["EW-RIE*"], capsize=4)
    a.axvline(0, color="#52514e", lw=1); a.set_yticks(y, d["period"], fontsize=8); a.invert_yaxis(); a.grid(axis="x", alpha=.3); a.set_title(VN[m], fontsize=10)
    a.set_xlabel("ΔVol = Vol(EW-RIE*) − Vol(VS-NL-LW), pp/năm (> 0: VS-NL-LW thấp hơn)")
plt.tight_layout(); savefig(fig, "fig_period_dvol")
cap("Hình", "ΔVol (EW-RIE\\* − VS-NL-LW) theo giai đoạn, CI 95% block bootstrap (b = 21).")
def _per_txt(m):
    d = T5G[T5G["mode"] == m]; ev = d[d["CI lo"] > 0]; ew = d[d["CI hi"] < 0]; ne = d[(d["CI lo"] <= 0) & (d["CI hi"] >= 0)]
    return f"{VN[m]}: VS-NL-LW thấp hơn có ý nghĩa ở {', '.join(ev.period) or 'không giai đoạn nào'}; EW-RIE\\* thấp hơn ở {', '.join(ew.period) or 'không giai đoạn nào'}; không khác biệt ở {', '.join(ne.period) or 'không giai đoạn nào'}."
md("**Kết quả theo giai đoạn (sinh từ bảng).** " + " ".join(_per_txt(m) for m in MODES))
