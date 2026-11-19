# ---- T2b: Bảng 21 (A theo mức lọc, ngày chung), Hình 12 (của v3), Hình 13 (heatmap cặp theo mức lọc) ----
ZL = {"không lọc": 1.0, "5%": 0.05, "10%": 0.10, "15%": 0.15, "20% (chuẩn)": 0.20, "30%": 0.30}
ZB = {(z, m): run_full(dict(CONFIG, ZERO_MAX=v), lo, M12) for z, v in ZL.items() for m, lo in MODES.items()}
NK = {z: len(ZB[(z, "long_only")]["ulog"]) for z in ZL}; ZOK = [z for z in ZL if NK[z] >= 60]
COMMON = sorted(set.intersection(*[set(ZB[(z, "long_only")]["out"]["NL-LW"]["r"].index) for z in ZOK])); COMMON = pd.DatetimeIndex(COMMON)
def on_dates(out, dates): return {k: dict(r=o["r"].loc[dates], r_net=o["r_net"].loc[dates]) for k, o in out.items()}
T21 = pd.concat({VN[m]: pd.DataFrame({z: pd.Series({k: ZB[(z, m)]["out"][k]["r"].loc[COMMON].std() * np.sqrt(252) * 100 for k in M12}) for z in ZOK}) for m in ("short_ok", "long_only")}, names=["Chế độ", "Phương pháp"])
save(T21, "T2b_tableA_zero")
info = "; ".join(f"{z}: {NK[z]} kỳ, {len(ZB[(z, 'long_only')]['out']['NL-LW']['r'])} phiên" for z in ZL)
cap("Bảng", f"Vol (%/năm, gộp) theo mức lọc đứng giá, trên {th(len(COMMON))} phiên chung ({COMMON[0].date()} → {COMMON[-1].date()}) của các mức có ≥ 60 kỳ; khối trên: bán khống, khối dưới: chỉ mua; in đậm: thấp nhất trong từng cột của mỗi khối. Số kỳ và phiên ngoài mẫu của từng mức — {info}.")
display(T21.style.format(precision=2, decimal=",").apply(lambda c: ["font-weight: bold" if v == c.loc[g].min() else "" for (g, _), v in c.items()], axis=0))
for z in ZL:
    if z not in ZOK:
        md(f"*Mức {z}:* {NK[z]} kỳ (< 60) — " + ("không có kỳ nào đủ N = 100 mã, không tính được." if NK[z] == 0 else
           "trên ngày của chính nó: " + ", ".join(f"{e_(k)} {f2(ZB[(z, 'long_only')]['out'][k]['m']['Vol %'])}" for k in ("NL-LW", "EW-NL-LW", "EW-RIE*", "VS-NL-LW")) + " (chỉ mua)."))
CORE3 = ["NL-LW", "EW-NL-LW", "EW-RIE*"]; tb = T21.loc[:, ZOK]
fig, ax = plt.subplots(1, 2, figsize=(13, 3.8), sharey=True); cols_ = ["#9aa0a6", "#2a78d6", "#1baf7a", "#eda100", "#8e44ad", "#eb6834"]
for a, m in zip(ax, ("short_ok", "long_only")):
    d = tb.loc[VN[m]].loc[CORE3]; x = np.arange(len(CORE3)); wd_ = .8 / len(ZOK)
    for j, z in enumerate(ZOK):
        a.bar(x + (j - (len(ZOK) - 1) / 2) * wd_, d[z], wd_ * .95, color=cols_[j], label=z)
        for i, v in enumerate(d[z]): a.text(i + (j - (len(ZOK) - 1) / 2) * wd_, v, f"{v:.1f}", ha="center", va="bottom", fontsize=6)
    a.set_xticks(x, CORE3); a.set_ylim(tb.loc[:, ZOK].loc[(slice(None), CORE3), :].values.min() - 1.5, tb.values.max() + .8); a.set_title(f"{VN[m]}: Vol %/năm theo mức lọc đứng giá", fontsize=10); a.grid(axis="y", alpha=.3)
ax[0].legend(fontsize=7, ncol=2); plt.tight_layout(); savefig(fig, "fig_12_zero_filter")
cap("Hình", "Hình của v3: Vol (%/năm) của NL-LW, EW-NL-LW, EW-RIE\\* theo mức lọc đứng giá, trên ngày chung (trục không từ 0).")
G2B = {VN[m]: pair_grid({z: on_dates(ZB[(z, m)]["out"], COMMON) for z in ZOK}) for m in ("short_ok", "long_only")}; save_grid(G2B, "T2b_pairs_zero")
pair_heatmap(G2B, "12 cặp theo mức lọc đứng giá (ngày chung)", fname="fig_13_pairs_zero")
cap("Hình", "ΔVol (pp/năm) của 12 cặp theo mức lọc đứng giá, trên ngày chung; \\* = p Holm < 0,05 trong từng cột (mô tả). Số liệu: `T2b_pairs_zero.csv`.")
md("**Kết quả.** Bộ có Vol thấp nhất theo mức lọc — " + "; ".join(f"{VN[m]}: " + ", ".join(f"{z}: {e_(T21.loc[VN[m], z].idxmin())}" for z in ZOK) for m in ("short_ok", "long_only")) + ".\n\n"
   f"**Kết luận.** {concl_grid(G2B)}")
