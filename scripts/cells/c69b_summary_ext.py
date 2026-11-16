# ---- Tổng kết (v5): so sánh mọi cặp ở mọi ô độ vững + hai hình tổng kết ----
PWA = pd.concat({k: v for k, v in SPW.items()}, names=["config", "mode", "i"]).reset_index().drop(columns="i"); save(PWA, "pairwise_all_cells")
CNT = pd.DataFrame(0, index=TOP, columns=TOP, dtype=int)
for r in PWA.itertuples():
    if r.p_holm < .05: CNT.loc[(r.a, r.b) if r.dvol < 0 else (r.b, r.a)] += 1
nC = len(SPW)
cap("Bảng", f"Số ô (trên {nC} ô = cấu hình × chế độ) mà bộ ở hàng có Vol thấp hơn bộ ở cột **có ý nghĩa** (p Holm < 0,05 trên 15 cặp trong từng ô; bootstrap M = 1000). Mô tả, không hiệu chỉnh xuyên lưới. Đủ cặp: `{RESULTS_DIR}/pairwise_all_cells.csv`.")
show(CNT, 0)
# Hình (i): hạng của 6 bộ TOP qua mọi ô
fig, ax = plt.subplots(figsize=(9, 4.4)); rng_ = np.random.default_rng(0)
for i, k in enumerate(TOP):
    y = RK[k].values; ax.scatter(i + rng_.uniform(-.18, .18, len(y)), y, s=14, alpha=.45, color=col_of(k) if k in COL else {"VS-EW-RIE*": "#c0392b", "VS-RIE": "#5d6d7e"}[k])
    ax.plot([i - .3, i + .3], [np.median(y)] * 2, color="black", lw=2)
ax.set_xticks(range(len(TOP)), TOP, rotation=20); ax.set_ylabel("Hạng Vol trong ô (1 = thấp nhất)"); ax.invert_yaxis(); ax.grid(axis="y", alpha=.3)
plt.tight_layout(); savefig(fig, "fig_rank_top_cells")
cap("Hình", f"Hạng Vol của 6 bộ đầu bảng qua {nC} ô độ vững (mỗi chấm một ô; vạch đen = trung vị).")
# Hình (ii): Vol – turnover ở cấu hình chuẩn, FULL, hai chế độ
fig, ax = plt.subplots(1, 2, figsize=(13, 5))
for a, m in zip(ax, MODES):
    for k, o in OUT0[m].items():
        v_, t_ = o["m"]["Vol %"], o["m"]["Turnover/kỳ"]; a.scatter(t_, v_, s=60 if k in TOP else 28, color=col_of(k) if k in COL else GREY, zorder=3)
        off = {"EW-RIE*": (-12, 14), "EW-WeSpeR": (-52, -16), "EW-NL-LW": (6, 10), "VS-NL-LW": (6, -14), "VS-EW-RIE*": (-6, -17), "VS-RIE": (6, 4), "NL-LW": (-34, 6)}.get(k)
        if off is None and k not in ("DCC-GARCH(1,1)", "Sample", "EW-RIE (q_eff)", "PCA-auto", "RIE"): continue
        a.annotate(k, (t_, v_), fontsize=7, xytext=off or (4, 3), textcoords="offset points", arrowprops=dict(arrowstyle="-", lw=.4, color="#9aa0a6") if off else None)
    a.set_xscale("log"); a.set_xlabel("Turnover/kỳ (log)"); a.set_ylabel("Vol %/năm"); a.set_title(VN[m], fontsize=10); a.grid(alpha=.3)
    a.set_ylim(top=min(a.get_ylim()[1], 18))
plt.tight_layout(); savefig(fig, "fig_vol_turnover")
cap("Hình", "Vol và turnover mỗi kỳ ở cấu hình chuẩn, đủ FULL (1/N ở Vol ≈ 23% nằm ngoài khung). Gần góc dưới trái: rủi ro thấp và ít giao dịch.")
_t = lambda k, m: OUT0[m][k]["m"]["Turnover/kỳ"]
md(f"**Kết quả (v5).** Trên {nC} ô, cặp phân biệt được nhiều ô nhất: "
   + ", ".join(f"{_e(a_)} < {_e(b_)} ({int(CNT.loc[a_, b_])} ô)" for a_, b_ in sorted([(a, b) for a in TOP for b in TOP if a != b], key=lambda p: -CNT.loc[p])[:4] if CNT.loc[a_, b_] > 0)
   + f". EW-RIE\\* thấp hơn VS-NL-LW có ý nghĩa ở {int(CNT.loc['EW-RIE*', 'VS-NL-LW'])} ô, cao hơn có ý nghĩa ở {int(CNT.loc['VS-NL-LW', 'EW-RIE*'])} ô; "
   f"turnover ở cấu hình chuẩn (chỉ mua / bán khống): EW-RIE\\* {f2(_t('EW-RIE*', 'long_only'))} / {f2(_t('EW-RIE*', 'short_ok'))}, VS-NL-LW {f2(_t('VS-NL-LW', 'long_only'))} / {f2(_t('VS-NL-LW', 'short_ok'))}.")
