# ---- T5: Vì sao VS giúp trên HOSE? ----
# T5a. Ablation: mỗi cặp chỉ khác bước chuẩn hóa biến động (VS): RIE ↔ VS-RIE, NL-LW ↔ VS-NL-LW, EW-RIE* ↔ VS-EW-RIE*. Cùng ngày OOS, kiểm định bằng compare_to.
ABL = [("RIE", "VS-RIE"), ("NL-LW", "VS-NL-LW"), ("EW-RIE*", "VS-EW-RIE*")]
rows = []
for m in MODES:
    for b, v in ABL:
        c = compare_to(OUT0[m], v, [b], reb_dates=REB_DATES).loc[b]
        rows.append({"Chế độ": VN[m], "Cặp": f"{v} vs {b}", "Vol gốc": c["Vol"], "Vol VS": c["Vol"] + c["ΔVol (pp)"], "ΔVol (pp)": c["ΔVol (pp)"], "CI lo": c["CI lo"], "CI hi": c["CI hi"],
                     "p LW-boot": c["p LW-boot"], "p JKM": c["p JKM"], "ΔTurnover": c["ΔTurnover"], "Turn CI lo": c["Turn CI lo"], "Turn CI hi": c["Turn CI hi"],
                     "Sharpe sau phí gốc": metrics(OUT0[m][b])["Sharpe sau phí"], "Sharpe sau phí VS": metrics(OUT0[m][v])["Sharpe sau phí"]})
T5A = pd.DataFrame(rows).set_index(["Chế độ", "Cặp"]); save(T5A.reset_index(), "T5a_vs_ablation")
cap("Bảng", "Tác động của VS (ΔVol = Vol có VS − Vol gốc; < 0: VS giảm rủi ro); Vol %/năm gộp; CI 95% block bootstrap b = 21; ΔTurnover/kỳ có VS − gốc.")
show(T5A, 3)
PER = pd.concat({VN[m]: summarize(OUT0[m], [])[1] for m in MODES}); save(PER, "T5a_periods_full")
T5P = pd.DataFrame({(VN[m], f"{v} − {b}"): PER.loc[VN[m]].loc[v] - PER.loc[VN[m]].loc[b] for m in MODES for b, v in ABL})
cap("Bảng", "ΔVol (pp/năm) do VS theo giai đoạn thị trường (< 0: VS giảm rủi ro).")
show(T5P, 2)
fig, ax = plt.subplots(1, 2, figsize=(13, 3.8), sharey=True)
for a, m in zip(ax, MODES):
    d = T5P[VN[m]]; x = np.arange(len(d))
    for j, (c, col) in enumerate(zip(d.columns, ["#2a78d6", "#eb6834", "#1baf7a"])): a.bar(x + (j - 1) * .27, d[c], .26, color=col, label=c)
    a.axhline(0, color="#52514e", lw=.8); a.set_xticks(x, d.index, rotation=20, fontsize=8); a.grid(axis="y", alpha=.3); a.set_title(VN[m], fontsize=10)
ax[0].legend(fontsize=8, loc="upper center", bbox_to_anchor=(1.05, -0.3), ncol=3, frameon=False); plt.tight_layout(); savefig(fig, "fig_vs_periods")
cap("Hình", "ΔVol do VS theo giai đoạn (pp/năm; < 0 ⇒ VS giảm rủi ro), cấu hình chuẩn.")
pm = T5P.mean(axis=0)
