# 5.2 (T6) Lưới N × h, hai chế độ, đủ FULL. N = 200 bỏ: chỉ 74/129 kỳ còn đủ 200 mã sau lọc đứng giá 20% (xem Ghi chú v4). Mỗi N có tập kỳ OOS riêng ⇒ KHÔNG so Vol tuyệt đối giữa các N.
NS, HS = (50, 100, 150), (30, 60, 120)
GR = {(n_, h_, m): run_full(dict(CONFIG, N=n_, HL_EW=h_), lo) for n_ in NS for h_ in HS for m, lo in MODES.items()}
GC = {k: cmp_table(d["out"], "EW-RIE*", reb_dates=[u["date"] for u in d["ulog"]]) for k, d in GR.items()}
qeff = lambda n_, h_: n_ * (ew_weights(CONFIG["WINDOW"], h_) ** 2).sum()
rows = []
for (n_, h_, m), d in GR.items():
    vol = pd.Series({k: o["m"]["Vol %"] for k, o in d["out"].items()}); c = GC[(n_, h_, m)]
    rows.append(dict(mode=m, N=n_, h=h_, q_eff=qeff(n_, h_), kỳ=len(d["ulog"]), ngày=len(d["out"]["EW-RIE*"]["r"]), **{"Vol EW-RIE*": vol["EW-RIE*"], "Hạng EW-RIE*": int(vol.rank()["EW-RIE*"]),
                     "Đứng đầu": vol.idxmin(), "Vol đứng đầu": vol.min(), "Vol VS-NL-LW": vol["VS-NL-LW"], "ΔVol vs VS-NL-LW": c.loc["VS-NL-LW", "ΔVol (pp)"],
                     "CI lo": c.loc["VS-NL-LW", "CI lo"], "CI hi": c.loc["VS-NL-LW", "CI hi"], "p LW-boot": c.loc["VS-NL-LW", "p LW-boot"], "p Holm": c.loc["VS-NL-LW", "p Holm"],
                     "ΔVol vs EW-NL-LW": c.loc["EW-NL-LW", "ΔVol (pp)"], "p Holm EW-NL-LW": c.loc["EW-NL-LW", "p Holm"],
                     "ΔVol vs EW-WeSpeR": c.loc["EW-WeSpeR", "ΔVol (pp)"], "p Holm EW-WeSpeR": c.loc["EW-WeSpeR", "p Holm"],
                     "ΔVol vs VS-EW-RIE*": c.loc["VS-EW-RIE*", "ΔVol (pp)"], "p LW-boot VS-EW-RIE*": c.loc["VS-EW-RIE*", "p LW-boot"],
                     "ΔTurnover vs VS-NL-LW": c.loc["VS-NL-LW", "ΔTurnover"], "Newton thất bại": d["newton"][0]}))
T6 = pd.DataFrame(rows); save(T6, "T6_N_h_grid_full")
save(pd.concat({f"{n_}_{h_}_{m}": c for (n_, h_, m), c in GC.items()}, names=["cell", "rival"]).reset_index(), "T6_N_h_compare_full")
for m in MODES:
    t = T6[T6["mode"] == m].copy(); t["ΔVol vs VS-NL-LW [CI]"] = [f"{a:+.2f} [{b:+.2f}; {c:+.2f}]" for a, b, c in zip(t["ΔVol vs VS-NL-LW"], t["CI lo"], t["CI hi"])]
    cap("Bảng", f"{VN[m]}: lưới N × h (Vol %/năm gộp; mỗi N có tập kỳ OOS riêng nên chỉ so trong cùng N). ΔVol = Vol(EW-RIE\\*) − Vol(VS-NL-LW) [CI 95%], p Holm trên 4 đối thủ lõi; q_eff = N·Σw². Đủ FULL: `results_v5/T6_N_h_grid_full.csv`.")
    show(t[["N", "h", "q_eff", "kỳ", "Vol EW-RIE*", "Hạng EW-RIE*", "Đứng đầu", "Vol đứng đầu", "ΔVol vs VS-NL-LW [CI]", "p Holm", "ΔVol vs EW-WeSpeR", "p Holm EW-WeSpeR", "ΔVol vs VS-EW-RIE*", "p LW-boot VS-EW-RIE*"]].set_index(["N", "h"]), 3)
def heat(col, ttl, fname, other=None):
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
    for a, m in zip(ax, MODES):
        t = T6[T6["mode"] == m]; M_ = t.pivot(index="N", columns="h", values=col); S_ = t.pivot(index="N", columns="h", values=other) if other else None
        v = np.abs(M_.values).max(); im = a.imshow(M_.values, cmap="RdYlGn_r", aspect="auto", vmin=-v, vmax=v)
        a.set_xticks(range(len(HS)), HS); a.set_yticks(range(len(NS)), NS); a.set_xlabel("h (half-life, phiên)"); a.set_ylabel("N"); a.set_title(VN[m], fontsize=10)
        for (y, x), val in np.ndenumerate(M_.values):
            st = "*" if other and S_.values[y, x] < 0.05 else ""; a.text(x, y, f"{val:+.2f}{st}".replace(".", ","), ha="center", va="center", fontsize=10)
    fig.colorbar(im, ax=ax, shrink=.8, label="pp/năm"); savefig(fig, fname)
heat("ΔVol vs VS-NL-LW", "", "fig_heat_nh_vs_vsnllw", other="p Holm")
cap("Hình", "Heatmap ΔVol = Vol(EW-RIE\\*) − Vol(VS-NL-LW) theo N × h (pp/năm; xanh: EW-RIE\\* thấp hơn); \\* = p Holm < 0,05 (4 đối thủ lõi, mô tả, không hiệu chỉnh xuyên lưới).")
heat("ΔVol vs EW-NL-LW", "", "fig_heat_nh_vs_ewnllw", other="p Holm EW-NL-LW")
cap("Hình", "Phụ: heatmap cũ, ΔVol = Vol(EW-RIE\\*) − Vol(EW-NL-LW) theo N × h; \\* = p Holm < 0,05.")
heat("ΔVol vs EW-WeSpeR", "", "fig_heat_nh_vs_wesper", other="p Holm EW-WeSpeR")
cap("Hình", "Heatmap ΔVol = Vol(EW-RIE\\*) − Vol(EW-WeSpeR) theo N × h (pp/năm; xanh: EW-RIE\\* thấp hơn); \\* = p Holm < 0,05.")
n_top = {m: int((T6[T6["mode"] == m]["Đứng đầu"] == "EW-RIE*").sum()) for m in MODES}; n_cells = T6[T6["mode"] == "long_only"].shape[0]
n_neg = {m: int((T6[T6["mode"] == m]["ΔVol vs VS-NL-LW"] < 0).sum()) for m in MODES}
n_sig_lo = {m: int(((T6[T6["mode"] == m]["ΔVol vs VS-NL-LW"] < 0) & (T6[T6["mode"] == m]["p Holm"] < .05)).sum()) for m in MODES}
n_sig_hi = {m: int(((T6[T6["mode"] == m]["ΔVol vs VS-NL-LW"] > 0) & (T6[T6["mode"] == m]["p Holm"] < .05)).sum()) for m in MODES}
md(f"**Kết quả (sinh từ bảng).** Trong {n_cells} tổ hợp N × h mỗi chế độ, EW-RIE\\* có Vol thấp nhất trong 15 phương pháp ở {n_top['long_only']} (chỉ mua) và {n_top['short_ok']} (bán khống) tổ hợp. "
   f"So với VS-NL-LW: ΔVol < 0 ở {n_neg['long_only']}/{n_cells} (chỉ mua) và {n_neg['short_ok']}/{n_cells} (bán khống); thấp hơn có ý nghĩa (p Holm < 0,05) ở {n_sig_lo['long_only']} và {n_sig_lo['short_ok']}, cao hơn có ý nghĩa ở {n_sig_hi['long_only']} và {n_sig_hi['short_ok']}.")
