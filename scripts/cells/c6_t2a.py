# ---- T2a: Bảng 19 (A theo REB), Bảng 20 (Sharpe sau phí theo COST, REB = 21), Hình 10 (heatmap REB × COST của v3), Hình 11 (heatmap cặp theo REB) ----
REBS, COSTS = (5, 21, 63), (0.0015, 0.0025, 0.004)
T2R = {(reb, m): run_full(dict(CONFIG, REB=reb), lo, M12) for reb in REBS for m, lo in MODES.items()}
T19 = pd.concat({(VN[m], f"REB = {reb}"): vols(T2R[(reb, m)]["out"], M12) for m in ("short_ok", "long_only") for reb in REBS}, axis=1); save(T19, "T2a_tableA_reb")
cap("Bảng", "Vol (%/năm, gộp) theo tần suất tái cân bằng REB (phiên), 12 phương pháp; in đậm: thấp nhất mỗi cột. Mỗi REB một bộ ngày ngoài mẫu chung cho mọi phương pháp.")
display(table_a(T19))
T20 = pd.concat({(VN[m], f"COST = {f2(100 * c)}%"): pd.Series({k: metrics(o, c)["Sharpe sau phí"] for k, o in T2R[(21, m)]["out"].items()}) for m in ("short_ok", "long_only") for c in COSTS}, axis=1).reindex(M12)
save(T20, "T2a_sharpe_cost")
cap("Bảng", "Sharpe sau phí (năm hóa) theo phí một chiều COST, REB = 21, 12 phương pháp; in đậm: **cao nhất** mỗi cột.")
display(T20.style.format(precision=3, decimal=",").highlight_max(axis=0, props="font-weight: bold"))
T2A = pd.DataFrame([dict(mode=m, REB=reb, COST=c, method=k, **metrics(o, c)) for (reb, m), d in T2R.items() for k, o in d["out"].items() for c in COSTS])
g_ = T2A.sort_values("COST").groupby(["method", "mode", "REB"]); assert g_["Sharpe sau phí"].apply(lambda s: (s.diff().dropna() <= 1e-12).all()).all()   # COST tăng ⇒ Sharpe sau phí không tăng
CORE3 = ["NL-LW", "EW-NL-LW", "EW-RIE*"]
fig, ax = plt.subplots(2, 3, figsize=(13, 6.3)); LOD = T2A[T2A["mode"] == "long_only"]
for j, k in enumerate(CORE3):
    for i, (col, cm_) in enumerate([("Vol %", "Blues"), ("Sharpe sau phí", "Greens")]):
        M = LOD[LOD.method == k].pivot(index="REB", columns="COST", values=col); lo_, hi_ = LOD[LOD.method.isin(CORE3)][col].min(), LOD[LOD.method.isin(CORE3)][col].max()
        ax[i, j].imshow(M.values, cmap=cm_, aspect="auto", vmin=lo_, vmax=hi_)
        ax[i, j].set_xticks(range(3), [f"{c:.2%}" for c in M.columns]); ax[i, j].set_yticks(range(3), M.index)
        for (y, x), v in np.ndenumerate(M.values): ax[i, j].text(x, y, f2(v), ha="center", va="center", fontsize=9, color="white" if v > (lo_ + hi_) / 2 else "black")
        ax[i, j].set_title(f"{k} — {col}", fontsize=10); ax[i, j].set_xlabel("COST (1 chiều)"); ax[i, j].set_ylabel("REB (phiên)")
fig.suptitle("Chỉ mua: Vol (gộp) và Sharpe sau phí theo REB × COST (cùng thang màu giữa 3 phương pháp)"); plt.tight_layout(); savefig(fig, "fig_10_T2a_heatmap")
cap("Hình", "Heatmap của v3: Vol (%/năm, gộp) và Sharpe sau phí theo REB × COST, chế độ chỉ mua, NL-LW / EW-NL-LW / EW-RIE\\*.")
G2A = {VN[m]: pair_grid({f"REB = {reb}": T2R[(reb, m)]["out"] for reb in REBS}) for m in ("short_ok", "long_only")}; save_grid(G2A, "T2a_pairs_reb")
pair_heatmap(G2A, "12 cặp theo tần suất tái cân bằng REB", fname="fig_11_pairs_reb")
cap("Hình", "ΔVol (pp/năm) của 12 cặp theo REB; \\* = p Holm < 0,05 trong từng cột (mô tả). Số liệu: `T2a_pairs_reb.csv`.")
bs = {m: T20[[c for c in T20.columns if c[0] == VN[m]]].idxmax() for m in MODES}
md("**Kết quả.** Bộ có Vol thấp nhất theo REB — " + "; ".join(f"{VN[m]}: " + ", ".join(f"REB = {reb}: {e_(T19[(VN[m], f'REB = {reb}')].idxmin())}" for reb in REBS) for m in ("short_ok", "long_only"))
   + ". Sharpe sau phí cao nhất (REB = 21) — " + "; ".join(f"{VN[m]}: " + ", ".join(f"{c[1]}: {e_(k)}" for c, k in bs[m].items()) for m in ("short_ok", "long_only")) + ".\n\n"
   f"**Kết luận.** {concl_grid(G2A)}")
