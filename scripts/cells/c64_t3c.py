# T3c. Kiểm định: ΔVol = Vol(EW-RIE*) − Vol(đối thủ), CI 95% bootstrap khối (b = 21), kiểm định phương sai Ledoit–Wolf (2011), Jobson–Korkie–Memmel.
# Một bảng duy nhất cho đủ FULL; dòng thuộc họ lõi CORE5 in đậm; p Holm chỉ tính trên 4 đối thủ lõi (định trước).
T3C = {m: cmp_table(OUT0[m], "EW-RIE*", reb_dates=REB_DATES) for m in MODES}
save(pd.concat(T3C, names=["mode", "rival"]).reset_index(), "T3c_tests_full")
for m in MODES:
    cap("Bảng", f"{VN[m]}: EW-RIE\\* so với từng đối thủ (ΔVol < 0: EW-RIE\\* rủi ro thấp hơn; CI 95% block bootstrap b = 21; p Holm trên 4 đối thủ lõi, in đậm). "
       f"{th(len(OUT0[m]['EW-RIE*']['r']))} phiên OOS chung. Đủ cột: `results_v4/T3c_tests_full.csv`.")
    display(fmt_cmp(T3C[m].loc[CORE5 + [k for k in T3C[m].index if k not in CORE5]]))

# Bảng phụ: VS + EW-RIE*  (hai cặp định trước)
T3X = {m: cmp_table(OUT0[m], "VS-EW-RIE*", ["VS-NL-LW", "EW-RIE*"]) for m in MODES}
save(pd.concat(T3X, names=["mode", "rival"]).reset_index(), "T3c_vs_ew_rie")
cap("Bảng", "Phụ: VS-EW-RIE\\* (chuẩn hóa biến động EWMA rồi EW-RIE\\*) so với VS-NL-LW và EW-RIE\\*. ΔVol = Vol(VS-EW-RIE\\*) − Vol(đối thủ).")
show(pd.concat({VN[m]: T3X[m][["Vol", "ΔVol (pp)", "CI lo", "CI hi", "p LW-boot", "p JKM", "ΔTurnover"]] for m in MODES}), 3)

# Hình: ΔVol với CI 95% (điểm + thanh sai số, đường dọc tại 0), họ lõi tô màu
fig, ax = plt.subplots(1, 2, figsize=(13, 5.2), sharex=False)
for a, m in zip(ax, MODES):
    C = T3C[m].sort_values("ΔVol (pp)", ascending=False); y = np.arange(len(C)); core = C["lõi"].astype(bool).values
    for i, (k, r) in enumerate(C.iterrows()):
        a.errorbar(r["ΔVol (pp)"], i, xerr=[[r["ΔVol (pp)"] - r["CI lo"]], [r["CI hi"] - r["ΔVol (pp)"]]], fmt="o", color=col_of(k) if core[i] else GREY, ecolor=col_of(k) if core[i] else GREY, capsize=3, ms=6 if core[i] else 4)
    a.axvline(0, color="#52514e", lw=1); a.set_yticks(y, [("**" if c else "") + k for k, c in zip(C.index, core)], fontsize=8); a.grid(axis="x", alpha=.3)
    a.set_xlabel("ΔVol = Vol(EW-RIE*) − Vol(đối thủ), pp/năm (< 0: EW-RIE* thấp hơn)"); a.set_title(VN[m], fontsize=10)
    xl = np.percentile(np.r_[C["CI lo"], C["CI hi"]], [3, 97]); a.set_xlim(min(xl[0], -1.5), max(xl[1], 1.5))
plt.tight_layout(); savefig(fig, "fig_dvol_ci")
cap("Hình", "ΔVol của EW-RIE\\* so với từng đối thủ, CI 95% block bootstrap (b = 21), cùng ngày OOS. Đối thủ họ lõi đánh dấu \\*\\*; trục x cắt ở phân vị 3–97% của các CI (1/N, Sample và EW-RIE (q_eff) nằm ngoài khung nếu CI rộng).")
