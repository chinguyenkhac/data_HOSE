# ---- T2d: Bảng 23 (lượt hủy trong kỳ nắm giữ theo năm và lý do), Bảng 24 (A theo kịch bản) ----
dts = R_BT.index; ev = DL_EVENTS.set_index("ticker"); rows = []
for u in U0:
    s = POS[u["date"]]; win = dts[s:s + CONFIG["REB"]]
    for t in u["tickers"]:
        if t in ev.index and ev.loc[t, "next_day"] in win: rows.append(dict(date=u["date"], year=u["date"].year, ticker=t, reason=ev.loc[t, "reason"]))
HOLD = pd.DataFrame(rows); save(HOLD, "T2d_events")
RNV = {"bat_buoc": "bắt buộc", "hop_nhat": "hợp nhất", "tu_nguyen": "tự nguyện", "chuyen_san": "chuyển sàn", "chua_ro": "chưa rõ"}
tab = HOLD.assign(reason=HOLD.reason.map(RNV)).pivot_table(index="year", columns="reason", values="ticker", aggfunc="count", fill_value=0); tab["Tổng"] = tab.sum(1); tab.loc["Tổng"] = tab.sum()
ever = set().union(*[set(u["tickers"]) for u in U0]); dl_px = set(DL_EVENTS.ticker); n_in = len(dl_px & ever)
cap("Bảng", f"Lượt mã trong universe bị hủy niêm yết trong kỳ nắm giữ, theo năm và lý do (cấu hình chuẩn: {len(U0)} kỳ × N = {CONFIG['N']} = {th(len(U0) * CONFIG['N'])} vị thế). "
    f"Trong {len(dl_px)} mã hủy có giá, {n_in} mã từng vào universe (danh mục) ít nhất một kỳ.")
show(tab.astype(int), 0)
ADJ["d"] = {}                                                                          # d = 0 ⇒ trùng hệt bản chuẩn (kiểm tra cài đặt)
for lo, m in ((True, "long_only"), (False, "short_ok")):
    z_ = run_backtest(P, V, {k: ESTIMATORS[k] for k in ("NL-LW", "EW-NL-LW")}, CONFIG, lo)
    assert all(np.array_equal(z_[k]["r"].values, OUT0[m][k]["r"].values) for k in z_)
ADJ["d"] = None
TD = {(sc, m): run_full_scn(sc, CONFIG, lo, M12) for sc in SCENARIOS for m, lo in MODES.items()}
T24 = pd.concat({(VN[m], sc.split(" (")[0] if "(" in sc else sc): vols(TD[(sc, m)]["out"], M12) for m in ("short_ok", "long_only") for sc in SCENARIOS}, axis=1); save(T24, "T2d_tableA_scenarios")
cap("Bảng", "Vol (%/năm, gộp) theo kịch bản lợi suất ngày hủy niêm yết (S0 = 0%, S1 = −30%, S2 = −100% cho hủy bắt buộc và chưa rõ; S1 mọi lý do), 12 phương pháp; in đậm: thấp nhất mỗi cột.")
display(table_a(T24))
rk = T24.rank(); same = {m: all((rk[(VN[m], c)] == rk[(VN[m], "S0")]).all() for c in rk[VN[m]].columns) for m in MODES}
dmax = max(abs(T24[(VN[m], c)] - T24[(VN[m], "S0")]).max() for m in MODES for c in T24[VN[m]].columns)
md(f"**Kết quả.** {len(HOLD)} lượt mã bị hủy trong kỳ nắm giữ ({', '.join(f'{k}: {int(v)}' for k, v in tab.loc['Tổng'].drop('Tổng').items())}); Vol đổi tối đa {f2(dmax, 3)} pp giữa các kịch bản; "
   + "; ".join(f"{VN[m]}: thứ hạng 12 bộ {'không đổi' if same[m] else 'có đổi'}" for m in ("short_ok", "long_only")) + ".\n\n"
   f"**Kết luận.** Cách xử lý lợi suất ngày hủy niêm yết {'không ảnh hưởng thứ hạng' if all(same.values()) else 'chỉ làm đổi thứ hạng ở mức nhỏ'}; hạn chế còn lại là {len(MISSING)} mã hủy thiếu giá không bao giờ vào universe.")
