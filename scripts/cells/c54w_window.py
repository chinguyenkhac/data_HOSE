# 5.4 (mới, v5) T ∈ {120, 250, 500}: cấu hình chuẩn khác không đổi; T = 250 lấy từ STD (§4.4). Mỗi T có tập kỳ OOS riêng ⇒ chỉ so trong cùng T.
WINS = (120, 250, 500)
WR = {(t_, m): (STD[m] if t_ == 250 else run_full(dict(CONFIG, WINDOW=t_), lo)) for t_ in WINS for m, lo in MODES.items()}
WINFO = []
for t_ in WINS:
    w_ = ew_weights(t_, CONFIG["HL_EW"]); d = WR[(t_, "long_only")]
    WINFO.append({"T": t_, "q = N/T": CONFIG["N"] / t_, "q_eff = N·Σw²": CONFIG["N"] * (w_ ** 2).sum(), "T_eff = 1/Σw²": 1 / (w_ ** 2).sum(), "số kỳ OOS": len(d["ulog"]),
                  "bắt đầu OOS": str(d["ulog"][0]["date"].date()), "số phiên OOS": len(d["out"]["EW-RIE*"]["r"])})
WINFO = pd.DataFrame(WINFO).set_index("T"); save(WINFO.reset_index(), "T6_window_info")
cap("Bảng", "Cửa sổ T: q = N/T, q$_{\\text{eff}}$ = N·Σw² (h = 60), số kỳ và ngày bắt đầu OOS. Tập OOS khác nhau giữa các T.")
show(WINFO, 2)
WV = {m: pd.DataFrame({t_: pd.Series({k: o["m"]["Vol %"] for k, o in WR[(t_, m)]["out"].items()}) for t_ in WINS}) for m in MODES}
WRK = {m: WV[m].rank(method="min").astype(int) for m in MODES}
for m in MODES:
    tab = pd.concat({"Vol %/năm": WV[m], "Hạng (trong cùng T)": WRK[m]}, axis=1).loc[WV[m][250].sort_values().index]
    cap("Bảng", f"{VN[m]}: Vol (%/năm, gộp) và hạng của 15 phương pháp theo T (sắp theo Vol ở T = 250). Không so Vol giữa các cột T.")
    show(tab, 2)
save(pd.concat({m: pd.concat({"Vol": WV[m], "Hạng": WRK[m]}, axis=1) for m in MODES}, names=["mode"]).reset_index(), "T6_window_vol_rank")
WC = {k: cmp_table(d["out"], "EW-RIE*", reb_dates=[u["date"] for u in d["ulog"]]) for k, d in WR.items()}
save(pd.concat(WC, names=["T", "mode", "rival"]).reset_index(), "T6_window_compare_full")
WP = {k: pairwise_top(d["out"], TOP, [u["date"] for u in d["ulog"]]) for k, d in WR.items()}
save(pd.concat({k: v[0] for k, v in WP.items()}, names=["T", "mode", "i"]).reset_index().drop(columns="i"), "T6_window_pairwise")
for m in MODES:
    rows = []
    for t_ in WINS:
        c = WC[(t_, m)]
        for r_ in CORE5: rows.append({"T": t_, "đối thủ": r_, "ΔVol [CI 95%]": f"{c.loc[r_, 'ΔVol (pp)']:+.2f} [{c.loc[r_, 'CI lo']:+.2f}; {c.loc[r_, 'CI hi']:+.2f}]".replace(".", ","),
                                       "p LW-boot": c.loc[r_, "p LW-boot"], "p Holm": c.loc[r_, "p Holm"], "ΔTurnover": c.loc[r_, "ΔTurnover"]})
    cap("Bảng", f"{VN[m]}: EW-RIE\\* so với 4 đối thủ lõi theo T (ΔVol < 0: EW-RIE\\* thấp hơn; p Holm trên 4 đối thủ lõi). Đủ FULL: `{RESULTS_DIR}/T6_window_compare_full.csv`.")
    show(pd.DataFrame(rows).set_index(["T", "đối thủ"]), 3)
for m in MODES:
    cap("Bảng", f"{VN[m]}: cặp trong nhóm dẫn đầu phân biệt được ở từng T (p Holm < 0,05 trên 15 cặp; ΔVol = Vol(A) − Vol(B)). Đủ 15 cặp: `{RESULTS_DIR}/T6_window_pairwise.csv`.")
    show(pd.concat({t_: (WP[(t_, m)][0].query("p_holm < .05")[["a", "b", "dvol", "p_boot", "p_holm"]].set_index(["a", "b"])) for t_ in WINS}, names=["T"]), 3)
# Hình 1: Vol theo T (6 bộ TOP, hai chế độ); Hình 2: ΔVol (EW-RIE* − VS-NL-LW) với CI theo T
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
for a, m in zip(ax, MODES):
    for k in TOP: a.plot(WINS, [WV[m].loc[k, t_] for t_ in WINS], "o-", color=col_of(k) if k in COL else {"VS-EW-RIE*": "#c0392b", "VS-RIE": "#5d6d7e"}[k], label=k, lw=2 if k == "EW-RIE*" else 1.3)
    a.set_xticks(WINS); a.set_xlabel("T (phiên); mỗi T có tập OOS riêng"); a.set_ylabel("Vol %/năm (trục không từ 0)"); a.set_title(VN[m], fontsize=10); a.grid(alpha=.3)
    a.set_ylim(top=20)
    for k in TOP:
        for t_ in WINS:
            if WV[m].loc[k, t_] > 20: a.annotate(f"{k}: {f2(WV[m].loc[k, t_], 1)}% (ngoài khung)", (t_, 20), xytext=(8, -14), textcoords="offset points", fontsize=7, color="#c0392b")
ax[0].legend(fontsize=8); plt.tight_layout(); savefig(fig, "fig_window_vol")
cap("Hình", "Vol theo cửa sổ T của 6 bộ đầu bảng (N = 100, h = 60). Chỉ so vị trí tương đối giữa các bộ trong cùng T, không so độ cao giữa các T (tập OOS khác nhau).")
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
for a, m in zip(ax, MODES):
    for i, t_ in enumerate(WINS):
        c = WC[(t_, m)].loc["VS-NL-LW"]; a.errorbar(i, c["ΔVol (pp)"], yerr=[[c["ΔVol (pp)"] - c["CI lo"]], [c["CI hi"] - c["ΔVol (pp)"]]], fmt="o", color=COL["EW-RIE*"], capsize=5, ms=7)
    a.axhline(0, color="#52514e", lw=1); a.set_xticks(range(len(WINS)), [f"T = {t_}" for t_ in WINS]); a.set_ylabel("ΔVol = Vol(EW-RIE*) − Vol(VS-NL-LW), pp/năm"); a.set_title(VN[m], fontsize=10); a.grid(axis="y", alpha=.3)
plt.tight_layout(); savefig(fig, "fig_window_dvol")
cap("Hình", "ΔVol (EW-RIE\\* − VS-NL-LW) theo T, CI 95% block bootstrap (b = 21), cùng ngày OOS trong từng T. ΔVol > 0: EW-RIE\\* rủi ro cao hơn.")
# Kết quả/Kết luận sinh từ bảng
def _dvw(m, t_, r_="VS-NL-LW"): c = WC[(t_, m)].loc[r_]; return f"{c['ΔVol (pp)']:+.2f} (CI {c['CI lo']:+.2f}; {c['CI hi']:+.2f}, p Holm {pv(c['p Holm']) if np.isfinite(c['p Holm']) else '–'})".replace(".", ",")
EWG, FLG = ["EW-NL-LW", "EW-WeSpeR", "EW-RIE*"], ["NL-LW", "RIE", "VS-NL-LW", "VS-RIE"]
rel = {m: WV[m].div(WV[m].loc["NL-LW"], axis=1) for m in MODES}                      # Vol tương đối so với NL-LW cùng T
spread = {m: {g: float(np.mean([rel[m].loc[k].max() - rel[m].loc[k].min() for k in ks])) for g, ks in (("EW", EWG), ("phẳng", [k for k in FLG if k != "NL-LW"]))} for m in MODES}
md("**Kết quả.** " + " ".join(f"**{VN[m]}:** ΔVol(EW-RIE\\* − VS-NL-LW) = " + "; ".join(f"T = {t_}: {_dvw(m, t_)}" for t_ in WINS) + ". "
   f"Hạng EW-RIE\\* theo T = {', '.join(str(int(WRK[m].loc['EW-RIE*', t_])) for t_ in WINS)}; hạng VS-NL-LW = {', '.join(str(int(WRK[m].loc['VS-NL-LW', t_])) for t_ in WINS)}. "
   f"Vol tương đối so với NL-LW cùng T dao động (max − min qua 3 T, trung bình): nhóm EW {spread[m]['EW']:.3f}, nhóm cửa sổ phẳng (RIE, VS-NL-LW, VS-RIE) {spread[m]['phẳng']:.3f}. " for m in MODES))
_nsig = {m: int(sum((WP[(t_, m)][0]["p_holm"] < .05).sum() for t_ in WINS)) for m in MODES}
md(f"**Kết luận.** Số cặp phân biệt được trong nhóm dẫn đầu (p Holm < 0,05, tổng 3 T): chỉ mua {_nsig['long_only']}/45, bán khống {_nsig['short_ok']}/45. "
   "Câu hỏi 'EW-RIE\\* hơn/ngang/kém VS-NL-LW theo T' đọc trực tiếp từ dấu và CI của ΔVol ở bảng trên; không kết luận vượt quá CI.")
_bad = [f"{_e(k)} ({VN[m].lower()}, T = {t_}: Vol {f2(WV[m].loc[k, t_])}%, trung vị các bộ {f2(WV[m][t_].median())}%)" for m in MODES for t_ in WINS for k in WV[m].index if k != "1/N" and WV[m].loc[k, t_] > 1.5 * WV[m][t_].median()]
if _bad: md("**Bộ mất ổn định ở một số T (Vol > 1,5 × trung vị cùng T, không tính 1/N):** " + "; ".join(_bad) + ". Nguyên nhân khả dĩ: T = 120 với N = 100 cho q$_{\\text{eff}}$ ≈ 0,96 (gần 1), ma trận làm sạch gần suy biến; ở chế độ bán khống GMV không bị chặn nên đòn bẩy cực lớn. Đây là mô tả từ số liệu, chưa kiểm nguyên nhân bằng thí nghiệm riêng.")
