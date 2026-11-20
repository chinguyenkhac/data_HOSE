from matplotlib.colors import to_rgb
# ---- 7.1 Hướng 1: Hình 18 (tài sản, thang log), Hình 19 (sụt giảm), Hình 20 (donut tỷ trọng), Kết quả & Kết luận ----
LINE = {"Thị trường EW": dict(color=COL["Thị trường EW"], ls="--", lw=1.4), "VN30 (chỉ số giá)": dict(color="#80868b", ls="-.", lw=1.3), "Tiết kiệm 5%": dict(color=COL["Tiết kiệm 5%"], ls=":", lw=1.6)}
SER1 = {**{nm: R1[nm] for nm in M7}, "Thị trường EW": RG["mk"], "VN30 (chỉ số giá)": R_VN30, "Tiết kiệm 5%": R_SAV}
fig, ax = plt.subplots(figsize=(12, 5.2)); ends = []
for nm, r in SER1.items():
    nav = (1 + r).cumprod(); st = LINE.get(nm, dict(color=col_of(nm), lw=1.8 if nm in ("EW-RIE*", "VS-NL-LW") else 1.2))
    ax.plot(nav.index, nav.values, label=nm, **st); ends.append((nav.iloc[-1], nm, st["color"]))
ax.set_yscale("log"); ax.set_ylabel("Giá trị 1 đồng (thang log)"); ax.grid(alpha=.3, which="both")
x_end = SER1["EW-RIE*"].index[-1]; prev = None
for v, nm, c in sorted(ends):                                    # nhãn trực tiếp ở mép phải, giãn theo thang log để không đè nhau
    y = v if prev is None else max(v, prev * 1.07); prev = y
    ax.annotate(f"{nm}: {f2(v)}", xy=(x_end, v), xytext=(x_end + pd.Timedelta(days=100), y), fontsize=8, va="center", color="#202124",
                arrowprops=dict(arrowstyle="-", color=c, lw=.6), annotation_clip=False)
ax.legend(loc="upper left", fontsize=8, ncol=2, frameon=False); ax.set_xlim(right=SER1["EW-RIE*"].index[-1] + pd.Timedelta(days=700))
plt.tight_layout(); savefig7(fig, "fig_18_tai_san_log")
cap("Hình", "Giá trị 1 đồng đầu tư, thang log: 6 phương pháp (chỉ mua, REB = 21, NAV ròng sau phí và thuế), Thị trường EW (thay VN-Index, không phí), "
    "VN30 (chỉ số giá, không gồm cổ tức; tham khảo) và tiết kiệm 5%/năm (giả định). Nhãn cuối đường: giá trị cuối kỳ.")

fig, ax = plt.subplots(figsize=(12, 4.2))
mk = (1 + RG["mk"]).cumprod(); ddm = mk / mk.cummax() - 1
ax.fill_between(ddm.index, ddm.values * 100, 0, color="#dadce0", label="Thị trường EW", lw=0)
v30 = (1 + R_VN30).cumprod(); ax.plot(v30.index, (v30 / v30.cummax() - 1).values * 100, color="#80868b", ls="-.", lw=1.1, label="VN30 (chỉ số giá)")
for nm in M7:
    nav = (1 + R1[nm]).cumprod(); dd = nav / nav.cummax() - 1
    ax.plot(dd.index, dd.values * 100, color=col_of(nm), lw=1.6 if nm in ("EW-RIE*", "VS-NL-LW") else 1.0, label=nm)
ax.set_ylabel("Sụt so với đỉnh trước, %"); ax.grid(alpha=.3); ax.legend(fontsize=8, ncol=4, frameon=False, loc="lower left")
plt.tight_layout(); savefig7(fig, "fig_19_sut_giam")
cap("Hình", "Mức sụt so với đỉnh trước (drawdown, %) của NAV ròng, chỉ mua; nền xám: Thị trường EW; gạch chấm: VN30 (chỉ số giá, tham khảo).")

# donut: ngày định trước (đăng ký trước): kỳ cuối ≤ 22/01/2020; kỳ gần đáy Thị trường EW (2–4/2020) nhất; kỳ gần 30/06/2022 nhất
reb = pd.DatetimeIndex(REB_DATES); m20 = mk.loc["2020-02-01":"2020-04-30"]; T_TROUGH20 = m20.idxmin()
D_DON = {"Trước COVID": reb[reb <= "2020-01-22"][-1], "Đáy 3/2020": reb[np.argmin(np.abs(reb - T_TROUGH20))],
         "Giữa 2022": reb[np.argmin(np.abs(reb - pd.Timestamp("2022-06-30")))]}
fig, axs = plt.subplots(2, 3, figsize=(13, 8.6)); DON = []
for i, nm in enumerate(["EW-RIE*", "VS-NL-LW"]):
    for j, (lab, d) in enumerate(D_DON.items()):
        ix, Wm = TG[nm][POS[d]]; w = pd.Series(Wm[0], index=TICK7[ix]).sort_values(ascending=False); top = w.iloc[:8]
        vals = list(top.values) + [1 - top.sum()]; names = list(top.index) + ["Khác"]
        base = to_rgb(col_of(nm)); shades = [tuple(1 - (1 - c) * (1 - .07 * k) for c in base) for k in range(8)] + [(.9, .9, .9)]
        a = axs[i, j]; wd, _ = a.pie(vals, colors=shades, startangle=90, counterclock=False, wedgeprops=dict(width=.38, edgecolor="white", linewidth=2))
        for wdg, n_, v in zip(wd, names, vals):
            if v < .025: continue
            ang = np.deg2rad((wdg.theta1 + wdg.theta2) / 2); a.text(1.18 * np.cos(ang), 1.18 * np.sin(ang), f"{n_}\n{f2(100 * v, 1)}%", ha="center", va="center", fontsize=7.5)
        neff = 1 / (Wm[0] ** 2).sum(); a.text(0, 0, f"{nm}\n{d:%d/%m/%Y}\nN hiệu dụng {f2(neff, 1)}", ha="center", va="center", fontsize=8.5)
        a.set_title(lab if i == 0 else "", fontsize=10); DON.append(dict(pp=nm, moc=lab, ngay=d.date(), top8=top.sum(), neff=neff, top=", ".join(top.index[:3])))
plt.tight_layout(); savefig7(fig, "fig_20_donut")
DON = pd.DataFrame(DON); save7(DON, "H1_donut")
cap("Hình", f"Tỷ trọng đích chỉ mua của EW-RIE\\* (trên) và VS-NL-LW (dưới) tại ba kỳ định trước: kỳ cuối trước 22/01/2020, kỳ gần đáy Thị trường EW "
    f"({T_TROUGH20:%d/%m/%Y}) nhất, kỳ gần 30/06/2022 nhất; 8 mã lớn nhất + nhóm Khác. Màu chỉ để phân đoạn, tên mã ghi trực tiếp.")

# ---- Kết quả & kết luận (sinh từ số liệu; ngưỡng đã đăng ký trước trong PROGRESS.md) ----
e, v_ = T35.loc["EW-RIE*"], T35.loc["VS-NL-LW"]; mrow, s_ = T35.loc["Thị trường EW"], T35.loc["Tiết kiệm 5%"]
p1 = T36.loc["VS-NL-LW", "p LW-boot"]; fee5, fee5e = T36.loc["VS-NL-LW", "γ = 5"], T36.loc["VS-NL-LW", "γ = 5 (cùng TB)"]
H1C = {}
for lab, q, b in (("mọi mã đủ điều kiện", "q1", "mk"), ("top-100", "q1t", "1/N gộp")):
    dlt, p = nw_mean_test(RG[q].values - RG[b].values); H1C[lab] = (dlt * 252 * 100, p, perf7(RG[q])["CAGR %"] - perf7(RG[b])["CAGR %"])
def _h1c(lab):
    d_, p_, dc = H1C[lab]
    v = "tăng **kém** thị trường" if (d_ < 0 and p_ < .05) else ("tăng **hơn** thị trường" if (d_ > 0 and p_ < .05) else "**chưa đủ bằng chứng** khác thị trường")
    return v, f"chênh TB {dv(d_)} pp/năm, p HAC {pv(p_)}, chênh CAGR {dv(dc)} pp"
beat = [nm for nm in M7 if T35.loc[nm, "CAGR %"] > mrow["CAGR %"]]
md(f"**Kết quả.** Sau phí và thuế, EW-RIE\\* tăng {f2(e['CAGR %'])}%/năm (MDD {f2(e['MDD %'])}%, Calmar {f2(e['Calmar'])}), VS-NL-LW {f2(v_['CAGR %'])}%/năm "
   f"(MDD {f2(v_['MDD %'])}%, Calmar {f2(v_['Calmar'])}); Thị trường EW {f2(mrow['CAGR %'])}%/năm (MDD {f2(mrow['MDD %'])}%); "
   f"VN30 (chỉ số giá, chưa gồm cổ tức) {f2(T35.loc['VN30 (chỉ số giá, tham khảo)', 'CAGR %'])}%/năm (MDD {f2(T35.loc['VN30 (chỉ số giá, tham khảo)', 'MDD %'])}%); tiết kiệm {f2(s_['CAGR %'])}%/năm. "
   f"Phương pháp có CAGR cao hơn Thị trường EW: {', '.join(beat) if beat else 'không có'}. "
   f"ΔVol EW-RIE\\* − VS-NL-LW = {dv(T36.loc['VS-NL-LW', 'ΔVol (pp)'])} pp (p {pv(p1)}); phí chuyển sang EW-RIE\\* ở γ = 5: {f2(fee5, 1)} bps/năm "
   f"(cùng TB {f2(fee5e, 1)} bps/năm, CI [{f2(CI36[True][0], 1)}; {f2(CI36[True][1], 1)}]). Donut: tỷ trọng 8 mã lớn nhất của EW-RIE\\* "
   + ", ".join(f"{f2(100 * r.top8, 0)}%" for r in DON[DON.pp == 'EW-RIE*'].itertuples()) + " so với VS-NL-LW "
   + ", ".join(f"{f2(100 * r.top8, 0)}%" for r in DON[DON.pp == 'VS-NL-LW'].itertuples()) + " (ba mốc).\n\n"
   f"**Kết luận (theo ngưỡng đăng ký trước).** H1a (EW-RIE\\* rủi ro thấp hơn VS-NL-LW): "
   f"{'đạt' if (T36.loc['VS-NL-LW', 'ΔVol (pp)'] < 0 and p1 < .05) else 'không đạt'}. H1b (giá trị kinh tế đáng kể ≥ 25 bps/năm và CI không chứa 0, γ = 5): "
   f"{'đạt' if (fee5e >= 25 and CI36[True][0] > 0) else 'không đạt'} ở bản cùng TB; bản lợi suất thực {f2(fee5, 1)} bps/năm chủ yếu phản ánh chênh lệch lợi suất trung bình "
   f"(CI [{f2(CI36[False][0], 1)}; {f2(CI36[False][1], 1)}]). H1c: nhóm ít biến động {_h1c('mọi mã đủ điều kiện')[0]} ({_h1c('mọi mã đủ điều kiện')[1]}); "
   f"trong top-100: {_h1c('top-100')[0]} ({_h1c('top-100')[1]}).")

# ---- Đào sâu (mô tả, KHÔNG đăng ký trước): vì sao GMV chỉ mua tăng chậm dù nhóm ít biến động không tăng kém? ----
def contrib7(nm):
    # đóng góp xấp xỉ của từng mã: Σ tỷ trọng đích × lợi suất ngày (không trôi, như run_backtest), %/năm; tỷ trọng đích TB qua 118 kỳ
    c, ws = np.zeros(len(TICK7)), np.zeros(len(TICK7))
    for i, s in enumerate(S_REG):
        e = S_REG[i + 1] if i + 1 < len(S_REG) else END7; ix, Wm = TG[nm][s]; c[ix] += (RH[s:e][:, ix] * Wm[0]).sum(0); ws[ix] += Wm[0]
    return pd.DataFrame({"đóng góp %/năm": c / yrs * 100, "tỷ trọng TB %": ws / len(S_REG) * 100}, index=TICK7)
CB = {nm: contrib7(nm) for nm in ("EW-RIE*", "VS-NL-LW")}; save7(pd.concat(CB, axis=1).loc[lambda d: d.abs().sum(1) > 0], "H1_dong_gop_ma")
def _dig(nm):
    d = CB[nm]; t12 = d["tỷ trọng TB %"].nlargest(12); big = d["tỷ trọng TB %"].idxmax(); neg = d["đóng góp %/năm"].nsmallest(2)
    return (f"{nm}: 12 mã có tỷ trọng TB lớn nhất chiếm {f2(t12.sum(), 0)}% danh mục (lớn nhất {big} {f2(d.loc[big, 'tỷ trọng TB %'], 1)}%), "
            f"đóng góp {f2(d.loc[t12.index, 'đóng góp %/năm'].sum())}/{f2(d['đóng góp %/năm'].sum())} %/năm; kéo lùi nhiều nhất "
            + ", ".join(f"{t} {f2(v)} %/năm (tỷ trọng TB {f2(d.loc[t, 'tỷ trọng TB %'], 1)}%)" for t, v in neg.items()))
q1t = T35.loc["Q1 ít biến động (top-100)"]
md(f"**Đào sâu (mô tả, không đăng ký trước).** Nhóm ít biến động không tăng kém thị trường, vậy lợi suất thấp của GMV chỉ mua không đến từ \"cổ phiếu ít biến động "
   f"tăng chậm\" nói chung mà từ **độ tập trung**: {_dig('EW-RIE*')}. {_dig('VS-NL-LW')}. Đối chứng cùng universe: Q1 trong top-100 (20 mã chia đều, chưa phí) "
   f"có CAGR {f2(q1t['CAGR %'])}%/năm, Vol {f2(q1t['Vol %'])}% ⇒ GMV giảm thêm ~{f2(q1t['Vol %'] - e['Vol %'], 1)} pp Vol nhưng mất ~{f2(q1t['CAGR %'] - e['CAGR %'], 1)} pp "
   f"CAGR mỗi năm. Hàm ý cho nhà đầu tư dài hạn: Vol thấp của GMV trên HOSE đổi bằng lợi suất rất thấp; Hướng 4 kiểm tra trần tỷ trọng có cải thiện điều này không.")
