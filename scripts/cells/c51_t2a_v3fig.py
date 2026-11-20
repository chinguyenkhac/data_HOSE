# T2a (hình phụ, lấy lại từ v3_nho): heatmap Vol (gộp) và Sharpe sau phí theo REB × COST, chỉ mua, cùng thang màu giữa 3 phương pháp
CORE3 = ["NL-LW", "EW-NL-LW", "EW-RIE*"]
fig, ax = plt.subplots(2, 3, figsize=(13, 6.3)); LOD = T2A[T2A["mode"] == "long_only"]
for j, k in enumerate(CORE3):
    for i, (col, cm_) in enumerate([("Vol %", "Blues"), ("Sharpe sau phí", "Greens")]):
        M = LOD[LOD.method == k].pivot(index="REB", columns="COST", values=col); lo_, hi_ = LOD[LOD.method.isin(CORE3)][col].min(), LOD[LOD.method.isin(CORE3)][col].max()
        ax[i, j].imshow(M.values, cmap=cm_, aspect="auto", vmin=lo_, vmax=hi_)
        ax[i, j].set_xticks(range(3), [f"{c:.2%}" for c in M.columns]); ax[i, j].set_yticks(range(3), M.index)
        for (y, x), v in np.ndenumerate(M.values): ax[i, j].text(x, y, f2(v), ha="center", va="center", fontsize=9, color="white" if v > (lo_ + hi_) / 2 else "black")
        ax[i, j].set_title(f"{k} — {col}", fontsize=10); ax[i, j].set_xlabel("COST (1 chiều)"); ax[i, j].set_ylabel("REB (phiên)")
fig.suptitle("Chỉ mua: Vol (gộp) và Sharpe sau phí theo REB × COST (cùng thang màu giữa 3 phương pháp)"); plt.tight_layout(); savefig(fig, "fig_T2a_heatmap")
cap("Hình", "Hình phụ (v3): heatmap Vol (%/năm, gộp) và Sharpe sau phí theo REB × COST, chế độ chỉ mua, NL-LW / EW-NL-LW / EW-RIE\\*; cùng thang màu giữa ba phương pháp.")
