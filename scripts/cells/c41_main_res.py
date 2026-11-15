# Bảng 1 + Kết quả/Kết luận §4 (số lấy từ RESULTS của ô trên và bảng so sánh cặp)
tb1 = pd.concat({VN[m]: RESULTS[m]["table"].loc[MAIN, ["Vol %", "Sharpe sau phí", "Turnover/kỳ", "Số mã hiệu dụng"]] for m in MODES}, axis=1)
cap("Bảng", f"Phương pháp chính, cấu hình chuẩn (N = 100, T = 250, h = 60, REB = 21, COST = 0,25%, ZERO\\_MAX = 20%); {th(len(RESULTS['long_only']['out']['NL-LW']['r']))} phiên OOS ({RESULTS['long_only']['out']['NL-LW']['r'].index[0]:%m/%Y}–{RESULTS['long_only']['out']['NL-LW']['r'].index[-1]:%m/%Y}). Vol: %/năm, gộp. Đủ 11 bộ: bảng in ở ô trên.")
show(tb1, 2)
t1 = {m: RESULTS[m]["table"]["Vol %"] for m in MODES}; c1 = {m: RESULTS[m]["ci"] for m in MODES}
ln = []
for m in ("short_ok", "long_only"):
    r = c1[m].loc["EW-RIE* vs VS-NL-LW"]
    ln.append(f"- **{VN[m]}:** {order_txt(t1[m], ['VS-NL-LW', 'EW-RIE*', 'EW-WeSpeR', 'EW-NL-LW', 'NL-LW'])}. "
              f"EW-RIE\\* − VS-NL-LW = {dci(t1[m]['EW-RIE*'] - t1[m]['VS-NL-LW'], r['CI 2.5%'], r['CI 97.5%'])} pp ⇒ {verdict(t1[m]['EW-RIE*'] - t1[m]['VS-NL-LW'], r['CI 2.5%'], r['CI 97.5%'])} (CI 95% block bootstrap).")
for m in ("short_ok", "long_only"):
    rs = {b: c1[m].loc[f"EW-RIE* vs {b}"] for b in ("NL-LW", "EW-NL-LW", "EW-WeSpeR")}
    ln.append(f"- **{VN[m]}, kiểm định cặp:** " + "; ".join(f"so với {b}: {verdict(0, r['CI 2.5%'], r['CI 97.5%'])}" for b, r in rs.items()) + ".")
md("**Kết quả** (Vol ngoài mẫu %/năm).\n\n" + "\n".join(ln))
lowest = {m: t1[m][MAIN].idxmin() for m in MODES}
md(f"**Kết luận.** Ở cấu hình chuẩn, Vol thấp nhất trong năm phương pháp chính là **{lowest['long_only'].replace('*', chr(92) + '*')}** (chỉ mua) và **{lowest['short_ok'].replace('*', chr(92) + '*')}** (bán khống). "
   f"Các bộ EW chênh nhau < {max(t1[m][['EW-RIE*', 'EW-WeSpeR', 'EW-NL-LW']].max() - t1[m][['EW-RIE*', 'EW-WeSpeR', 'EW-NL-LW']].min() for m in MODES):.2f} pp nên cần kiểm định cặp đủ phương pháp (T3, Bảng 7).")
