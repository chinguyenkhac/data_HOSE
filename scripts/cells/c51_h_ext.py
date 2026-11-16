# 5.1 (v5) Mở rộng ô của thầy: Vol theo h ∈ {30, 60, 120} cho 6 bộ TOP (N = 100; bộ không phụ thuộc h là đường ngang) + compare_to theo h. Lấy từ cache lưới N × h.
HH = (30, 60, 120)
H5 = {(h_, m): (STD[m] if h_ == 60 else run_full(dict(CONFIG, HL_EW=h_), lo)) for h_ in HH for m, lo in MODES.items()}
for (h_, m), d in H5.items(): assert d["out"]["EW-RIE*"]["r"].index.equals(STD[m]["out"]["EW-RIE*"]["r"].index)       # cùng ngày OOS với cấu hình chuẩn
H5V = {m: pd.DataFrame({h_: pd.Series({k: H5[(h_, m)]["out"][k]["m"]["Vol %"] for k in TOP}) for h_ in HH}) for m in MODES}
H5C = {k: cmp_table(d["out"], "EW-RIE*", reb_dates=[u["date"] for u in d["ulog"]]) for k, d in H5.items()}
save(pd.concat(H5V, names=["mode"]).reset_index(), "T6_half_life_top6_vol"); save(pd.concat({f"{h_}_{m}": c for (h_, m), c in H5C.items()}, names=["cell", "rival"]).reset_index(), "T6_half_life_compare_full")
for m in MODES:
    cap("Bảng", f"{VN[m]}: Vol (%/năm, gộp) của 6 bộ đầu bảng theo half-life h (N = 100, T = 250; VS-NL-LW và VS-RIE không dùng h nên không đổi).")
    show(H5V[m], 3)
    rows = [{"h": h_, "đối thủ": r_, "ΔVol [CI 95%]": f"{H5C[(h_, m)].loc[r_, 'ΔVol (pp)']:+.2f} [{H5C[(h_, m)].loc[r_, 'CI lo']:+.2f}; {H5C[(h_, m)].loc[r_, 'CI hi']:+.2f}]".replace(".", ","),
             "p Holm": H5C[(h_, m)].loc[r_, "p Holm"], "ΔTurnover": H5C[(h_, m)].loc[r_, "ΔTurnover"]} for h_ in HH for r_ in CORE5]
    cap("Bảng", f"{VN[m]}: EW-RIE\\* so với 4 đối thủ lõi theo h (ΔVol < 0: EW-RIE\\* thấp hơn; p Holm trên 4 đối thủ lõi).")
    show(pd.DataFrame(rows).set_index(["h", "đối thủ"]), 3)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6)); TCOL = {**COL, "VS-EW-RIE*": "#c0392b", "VS-RIE": "#5d6d7e"}
for a, m in zip(ax, MODES):
    for k in TOP:
        dep = k in USES_HL_EW; y = H5V[m].loc[k]
        a.plot(HH if dep else [HH[0], HH[-1]], y.values if dep else [y.iloc[0]] * 2, "o-" if dep else "--", color=TCOL[k], label=k + ("" if dep else " (không phụ thuộc h)"), lw=2 if k == "EW-RIE*" else 1.3)
    a.set_xticks(HH); a.set_xlabel("h (half-life, phiên)"); a.set_ylabel("Vol %/năm (trục không từ 0)"); a.set_title(VN[m], fontsize=10); a.grid(alpha=.3)
ax[0].legend(fontsize=7); plt.tight_layout(); savefig(fig, "fig_halflife_top6")
cap("Hình", "Vol theo half-life h của 6 bộ đầu bảng (N = 100); nét đứt: bộ không phụ thuộc h.")
_c = lambda h_, m, r_: H5C[(h_, m)].loc[r_]
md("**Kết quả (v5).** ΔVol(EW-RIE\\* − VS-NL-LW) theo h = 30/60/120: " + "; ".join(f"{VN[m]} " + ", ".join(f"{_c(h_, m, 'VS-NL-LW')['ΔVol (pp)']:+.2f}" for h_ in HH) for m in MODES)
   + ". So với EW-WeSpeR: " + "; ".join(f"{VN[m]} " + ", ".join(f"{_c(h_, m, 'EW-WeSpeR')['ΔVol (pp)']:+.2f}" for h_ in HH) for m in MODES) + " (pp/năm, xem p Holm và CI ở bảng trên).")
