# T2d. Độ nhạy lợi suất ngày hủy niêm yết. Hiện trạng: mã hủy trong kỳ nắm giữ có lợi suất 0 các ngày còn lại (giả định bán đúng giá cuối).
# 4a. Đếm lượt mã trong universe bị hủy TRONG kỳ nắm giữ: ngày giao dịch đầu tiên sau ngày có giá cuối rơi vào kỳ nắm giữ và mã nằm trong universe kỳ đó.
dts = R_BT.index; ev = DL_EVENTS.set_index("ticker"); rows = []
for u in U0:
    s = POS[u["date"]]; win = dts[s:s + CONFIG["REB"]]
    for t in u["tickers"]:
        if t in ev.index and ev.loc[t, "next_day"] in win: rows.append(dict(date=u["date"], year=u["date"].year, ticker=t, reason=ev.loc[t, "reason"], next_day=ev.loc[t, "next_day"]))
HOLD = pd.DataFrame(rows); N_SLOT = len(U0) * CONFIG["N"]
RNV = {"bat_buoc": "bắt buộc", "hop_nhat": "hợp nhất", "tu_nguyen": "tự nguyện", "chuyen_san": "chuyển sàn", "chua_ro": "chưa rõ"}
if len(HOLD):
    save(HOLD, "T2d_events")
    tab = HOLD.assign(reason=HOLD.reason.map(RNV)).pivot_table(index="year", columns="reason", values="ticker", aggfunc="count", fill_value=0); tab["Tổng"] = tab.sum(1); tab.loc["Tổng"] = tab.sum()
    cap("Bảng", f"Lượt mã trong universe bị hủy niêm yết TRONG kỳ nắm giữ, theo năm và lý do (cấu hình chuẩn: {len(U0)} kỳ × N = {CONFIG['N']} = {N_SLOT:,} vị thế).".replace(",", " "))
    show(tab.astype(int).T, 0)
else:
    print("Không có mã nào trong universe bị hủy niêm yết trong kỳ nắm giữ ⇒ T2d chỉ còn mục 4d.")
n_dl16 = int((MISSING.delisting_date >= U0[0]["date"]).sum()); n_dl_all = int(MISSING.delisting_date.notna().sum())
print(f"4d. Hạn chế còn lại: {len(MISSING)} mã thiếu giá (VCI không còn mã); {n_dl_all} mã đã hủy, {n_dl16} mã hủy từ {U0[0]['date']:%m/%Y} (tức trong mẫu OOS) không bao giờ vào universe ⇒ không thể đo ảnh hưởng của chúng.")

if len(HOLD):
    # 4b. Kiểm tra cài đặt: d = 0 trùng hệt bản chuẩn (toàn mẫu, hai bộ nhanh); ADJ chỉ cộng vào lợi suất nắm giữ, không đụng P hay cửa sổ ước lượng.
    ADJ["d"] = {}
    for lo, m in ((True, "long_only"), (False, "short_ok")):
        z = run_backtest(P, V, {k: ESTIMATORS[k] for k in ("NL-LW", "EW-NL-LW")}, CONFIG, lo)
        assert all(np.array_equal(z[k]["r"].values, OUT0[m][k]["r"].values) for k in z)
    ADJ["d"] = None; print("4b. d = 0 ⇒ trùng hệt bản chuẩn (NL-LW, EW-NL-LW; hai chế độ) ✔")
    # 4c. Kịch bản: S0 = 0% (hiện tại) · S1 = −30% · S2 = −100% (áp cho bắt buộc và chưa rõ) · S1 mọi lý do
    TD = {(sc, m): run_full_scn(sc, CONFIG, lo) for sc in SCENARIOS for m, lo in MODES.items()}
    T2D = pd.DataFrame([dict(scenario=sc, mode=m, method=k, **metrics(o)) for (sc, m), d in TD.items() for k, o in d["out"].items()])
    save(T2D, "T2d_scenarios_full")
    cap("Bảng", "Vol (%/năm, gộp) của các phương pháp chính theo kịch bản lợi suất ngày hủy niêm yết (S1/S2 áp cho hủy bắt buộc và chưa rõ; dòng cuối: −30% cho mọi lý do). Đủ FULL: `results_v4/T2d_scenarios_full.csv`.")
    show(T2D[T2D.method.isin(MAIN)].pivot_table(index="scenario", columns=["mode", "method"], values="Vol %").reindex(index=list(SCENARIOS), columns=pd.MultiIndex.from_product([MODES, MAIN])).rename(columns=VN, level=0), 3)
    # tỷ trọng mỗi phương pháp trong các mã hủy tại ngày hủy: S2 − S0 = −Σ w_i (cú sốc −100%)
    wt_ = {}
    for m in MODES:
        dd = {k: (TD[("S2 (−100%)", m)]["out"][k]["r"] - TD[("S0 (0%, hiện tại)", m)]["out"][k]["r"]) for k in MAIN}
        days = [d for d in dd["NL-LW"].index if any(abs(dd[k][d]) > 1e-12 for k in MAIN)]
        wt_[VN[m]] = pd.DataFrame({k: -dd[k].loc[days] * 100 for k in MAIN}).agg(["mean", "max"]).T.rename(columns={"mean": "TB (%)", "max": "Max (%)"})
    wt_ = pd.concat(wt_, axis=1)
    cap("Bảng", "Tỷ trọng (%) của mỗi phương pháp trong các mã bị hủy (bắt buộc/chưa rõ) vào ngày hủy; < 0 là vị thế bán khống.")
    show(wt_, 3)
    CS = {(sc, m): cmp_table(d["out"], "EW-RIE*", reb_dates=[u["date"] for u in d["ulog"]]) for (sc, m), d in TD.items()}
    save(pd.concat(CS, names=["scenario", "mode", "rival"]).reset_index(), "T2d_compare_full")
    rk = pd.DataFrame({(VN[m], sc): pd.Series({k: o["m"]["Vol %"] for k, o in TD[(sc, m)]["out"].items()}).rank() for (sc, m) in TD}).T
    sm = pd.DataFrame([dict(mode=VN[m], scenario=sc, **{"Thứ hạng EW-RIE* (1 = Vol thấp nhất / 15)": int(rk.loc[(VN[m], sc), "EW-RIE*"]),
                      "Thứ hạng VS-NL-LW": int(rk.loc[(VN[m], sc), "VS-NL-LW"]), "Đứng đầu": rk.loc[(VN[m], sc)].idxmin()},
                      **{f"ΔVol vs {b}": CS[(sc, m)].loc[b, "ΔVol (pp)"] for b in ("VS-NL-LW", "EW-WeSpeR")},
                      **{"p Holm vs VS-NL-LW": CS[(sc, m)].loc["VS-NL-LW", "p Holm"]}) for sc in SCENARIOS for m in MODES]).set_index(["mode", "scenario"])
    cap("Bảng", "Thứ hạng và kiểm định EW-RIE\\* theo kịch bản hủy niêm yết (p Holm trên 4 đối thủ lõi).")
    show(sm, 3)
    fig, ax = plt.subplots(1, 2, figsize=(12, 3.6), sharey=True)
    for a, m in zip(ax, MODES):
        c = pd.DataFrame({sc: CS[(sc, m)].loc["VS-NL-LW", ["ΔVol (pp)", "CI lo", "CI hi"]] for sc in SCENARIOS}).T; y = np.arange(len(c))
        a.errorbar(c["ΔVol (pp)"], y, xerr=[c["ΔVol (pp)"] - c["CI lo"], c["CI hi"] - c["ΔVol (pp)"]], fmt="o", color=COL["EW-RIE*"], capsize=4)
        a.axvline(0, color="#52514e", lw=1); a.set_yticks(y, list(SCENARIOS), fontsize=8); a.invert_yaxis(); a.grid(axis="x", alpha=.3); a.set_title(VN[m], fontsize=10)
        a.set_xlabel("ΔVol = Vol(EW-RIE*) − Vol(VS-NL-LW), pp/năm")
    plt.tight_layout(); savefig(fig, "fig_delist_dvol")
    cap("Hình", "ΔVol (EW-RIE\\* − VS-NL-LW) theo kịch bản lợi suất ngày hủy niêm yết, CI 95% block bootstrap (b = 21).")
