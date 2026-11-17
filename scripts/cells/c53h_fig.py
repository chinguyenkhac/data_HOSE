# 5.3 (v5) Hình: Vol theo HL_VOL của VS-NL-LW, VS-RIE, VS-EW-RIE*; đường ngang = EW-RIE* (không dùng HL_VOL)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.4))
for a, m in zip(ax, MODES):
    t = T6H[T6H["mode"] == m]
    for k, c_ in zip(VSK, (COL["VS-NL-LW"], "#5d6d7e", "#c0392b")): a.plot(t["HL_VOL"], t[f"Vol {k}"], "o-", color=c_, label=k)
    a.axhline(t["Vol EW-RIE* (h = 60)"].iloc[0], color=COL["EW-RIE*"], lw=2, ls="--", label="EW-RIE* (h = 60)")
    a.set_xticks(HVS); a.set_xlabel("HL_VOL (half-life EWMA biến động, phiên)"); a.set_ylabel("Vol %/năm (trục không từ 0)"); a.set_title(VN[m], fontsize=10); a.grid(alpha=.3)
ax[0].legend(fontsize=8); plt.tight_layout(); savefig(fig, "fig_hlvol")
cap("Hình", "Vol theo HL_VOL của ba bộ VS; đường nét đứt: EW-RIE\\* (h = 60), không phụ thuộc HL_VOL.")
