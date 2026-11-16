# 5.2 (hình phụ, lấy lại từ v3_nho): Vol EW-RIE* và ΔVol so với EW-NL-LW theo N × h
fig, ax = plt.subplots(2, 2, figsize=(11, 7))
for i, m in enumerate(MODES):
    t = T6[T6["mode"] == m]
    for j, (col, ttl, cm_) in enumerate([("Vol EW-RIE*", "Vol EW-RIE* (%/năm)", "Blues"), ("ΔVol vs EW-NL-LW", "ΔVol so với EW-NL-LW (pp)", "RdYlGn_r")]):
        M = t.pivot(index="N", columns="h", values=col); a = ax[i, j]; v = np.abs(M.values).max() if j else None
        im = a.imshow(M.values, cmap=cm_, aspect="auto", **({"vmin": -v, "vmax": v} if j else {}))
        a.set_xticks(range(3), M.columns); a.set_yticks(range(3), M.index); a.set_xlabel("h (half-life, phiên)"); a.set_ylabel("N"); mid = (M.values.min() + M.values.max()) / 2
        for (y, x), val in np.ndenumerate(M.values): a.text(x, y, f2(val), ha="center", va="center", fontsize=10, color="white" if (j == 0 and val > mid) else "black")
        a.set_title(f"{VN[m]} – {ttl}", fontsize=10)
fig.suptitle("Độ nhạy theo N và half-life h (mỗi N có tập OOS riêng: Vol không so giữa các hàng)"); plt.tight_layout(); savefig(fig, "fig_T6_N_h_grid")
cap("Hình", "Hình phụ (v3): Vol của EW-RIE\\* (%/năm) và ΔVol so với EW-NL-LW theo N × h. Mỗi N có tập kỳ OOS riêng, chỉ so Vol trong cùng hàng N.")
