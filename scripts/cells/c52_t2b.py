# T2b. Phiên lợi suất 0. Lọc loại khỏi universe các mã có tỷ lệ r = 0 trong CỬA SỔ QUÁ KHỨ > ngưỡng (không dùng tương lai). Chuẩn vẫn là 20%.
def zero_share(ulog):    # tỷ lệ r=0 trung bình của universe đã chọn (đúng dữ liệu đưa vào estimator)
    return np.mean([(R_BT.iloc[POS[u["date"]] - CONFIG["WINDOW"]:POS[u["date"]]][u["tickers"]].fillna(0) == 0).values.mean() for u in ulog])
VARS = {"không lọc": 1.0, "lọc 30%": 0.30, "lọc 20% (chuẩn)": 0.20, "lọc 10%": 0.10}
T2B_RUN = {(v, m): run_full(dict(CONFIG, ZERO_MAX=z), lo) for v, z in VARS.items() for m, lo in MODES.items()}
COMMON = sorted(set.intersection(*[set(d["out"]["NL-LW"]["r"].index) for d in T2B_RUN.values()]))     # kỳ thiếu mã bị bỏ ⇒ so trên ngày chung
T2B = pd.DataFrame([dict(variant=v, mode=m, method=k, **metrics(o, dates=COMMON), **{"Số kỳ hợp lệ": len(d["ulog"]),
                    "Mã đủ ĐK (TB)": np.mean([u["n_eligible"] for u in d["ulog"]]), "Mã đủ ĐK (min)": min(u["n_eligible"] for u in d["ulog"]),
                    "% r=0 trong universe": 100 * zero_share(d["ulog"])}) for (v, m), d in T2B_RUN.items() for k, o in d["out"].items()])
save(T2B, "T2b_zero_return_full")
T2BC = {(v, m): cmp_table(restrict(d["out"], COMMON), "EW-RIE*", reb_dates=[u["date"] for u in d["ulog"]]) for (v, m), d in T2B_RUN.items()}
save(pd.concat(T2BC, names=["variant", "mode", "rival"]).reset_index(), "T2b_compare_full")
info = T2B[T2B["mode"] == "long_only"].groupby("variant")[["Số kỳ hợp lệ", "Mã đủ ĐK (TB)", "Mã đủ ĐK (min)", "% r=0 trong universe"]].first().loc[list(VARS)]
tb = T2B.pivot_table(index="variant", columns=["mode", "method"], values="Vol %")
cap("Bảng", f"Vol (%/năm, gộp) theo mức lọc mã đứng giá, trên {len(COMMON):,} ngày OOS chung ({COMMON[0].date()} → {COMMON[-1].date()}); các phương pháp chính. Đủ FULL: `results_v4/T2b_zero_return_full.csv`.".replace(",", " "))
show(pd.concat([tb.rename(columns=VN, level=0).reindex(columns=pd.MultiIndex.from_product([VN.values(), MAIN])), pd.concat({"Universe": info}, axis=1)], axis=1).loc[list(VARS)], 2)
rows = [dict(variant=v, mode=VN[m], rival=b, **{c: T2BC[(v, m)].loc[b, c] for c in ("ΔVol (pp)", "CI lo", "CI hi", "p Holm", "ΔTurnover")}) for v in VARS for m in MODES for b in CORE5]
T2BS = pd.DataFrame(rows).set_index(["mode", "variant", "rival"]).sort_index(level=[0, 1], sort_remaining=False)
cap("Bảng", "EW-RIE\\* so với họ lõi theo mức lọc (ngày chung): ΔVol (pp), CI 95%, p Holm.")
show(T2BS, 3)
fig, ax = plt.subplots(1, 2, figsize=(13, 4), sharey=True)
for a, m in zip(ax, MODES):
    d = tb[m][MAIN].loc[list(VARS)]; x = np.arange(len(MAIN)); cols = ["#9aa0a6", "#eda100", "#1baf7a", "#2a78d6"]
    for j, (vn, col) in enumerate(zip(VARS, cols)):
        a.bar(x + (j - 1.5) * .2, d.loc[vn], .19, color=col, label=vn)
        for i, v in enumerate(d.loc[vn]): a.text(i + (j - 1.5) * .2, v, f"{v:.1f}", ha="center", va="bottom", fontsize=6.5)
    a.set_xticks(x, MAIN, fontsize=8); a.set_ylim(tb.values.min() - 1.5, tb.values.max() + 1); a.set_title(VN[m], fontsize=10); a.grid(axis="y", alpha=.3)
ax[0].legend(fontsize=8, loc="upper center", bbox_to_anchor=(1.05, -0.12), ncol=4, frameon=False)
plt.tight_layout(); savefig(fig, "fig_zero_filter")
cap("Hình", "Vol ngoài mẫu theo mức lọc mã đứng giá (trục y không từ 0; ngày OOS chung).")
