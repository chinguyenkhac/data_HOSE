# ---- T5c: Bảng 32 (cụm D, E theo giai đoạn), Hình 17 (ΔVol trượt 252 phiên của EW-RIE* − VS-NL-LW) ----
T32 = per_rows([p for p in PAIRS12 if p[0][0] in "DE"]); save(T32, "T5c_periods_DE")
cap("Bảng", "Cụm D (trong họ VS) và cụm E (EW-RIE\\* − VS-NL-LW): ΔVol (pp/năm) [CI 95% bootstrap khối] theo giai đoạn. Mô tả, không Holm.")
display(per_table(T32))
fig, ax = plt.subplots(2, 1, figsize=(12, 6), sharex=True); PCOL = ["#f2f2f2", "#e3ecf7"]
for a, m in zip(ax, ("short_ok", "long_only")):
    ra, rb = OUT0[m]["EW-RIE*"]["r"], OUT0[m]["VS-NL-LW"]["r"]
    roll = (ra.rolling(252).std() - rb.rolling(252).std()) * np.sqrt(252) * 100
    for i, (nm, s0, s1) in enumerate(PERIODS):
        a.axvspan(max(pd.Timestamp(s0), ra.index[0]), min(pd.Timestamp(s1), ra.index[-1]), color=PCOL[i % 2], zorder=0)
        a.text(max(pd.Timestamp(s0), ra.index[0]), .97, nm, transform=a.get_xaxis_transform(), fontsize=7, va="top", color="#52514e")
    a.plot(roll.index, roll.values, color=COL["EW-RIE*"], lw=1.4); a.axhline(0, color="#52514e", lw=1)
    a.set_ylabel("ΔVol trượt 252 phiên, pp"); a.set_title(VN[m], fontsize=10); a.grid(alpha=.3)
plt.tight_layout(); savefig(fig, "fig_17_rolling_E")
cap("Hình", "ΔVol trượt 1 năm (252 phiên) của EW-RIE\\* − VS-NL-LW theo thời gian; nền: các giai đoạn trong `PERIODS`; > 0: EW-RIE\\* rủi ro cao hơn. Mô tả.")
E_ = T32[T32["Cặp"] == "EW-RIE* − VS-NL-LW"]; sgn = E_[(E_["Giai đoạn"] != "Toàn mẫu") & ((E_["CI lo"] > 0) | (E_["CI hi"] < 0))]
md("**Kết quả.** Cặp E có CI 95% không chứa 0 ở: " + ("; ".join(f"{r['Giai đoạn']} ({r['Chế độ'].lower()}, {dv(r['ΔVol (pp)'])} pp)" for _, r in sgn.iterrows()) if len(sgn) else "không giai đoạn nào")
   + f". Tỷ lệ ngày ΔVol trượt > 0: " + ", ".join(f"{VN[m]} {f2(100 * ((OUT0[m]['EW-RIE*']['r'].rolling(252).std() - OUT0[m]['VS-NL-LW']['r'].rolling(252).std()).dropna() > 0).mean(), 0)}%" for m in ("short_ok", "long_only")) + ".\n\n"
   f"**Kết luận.** Theo giai đoạn, VS-NL-LW thấp hơn rõ ở {', '.join(sorted(set(sgn[sgn['ΔVol (pp)'] > 0]['Giai đoạn']))) or 'không giai đoạn nào'}, "
   f"EW-RIE\\* thấp hơn rõ ở {', '.join(sorted(set(sgn[sgn['ΔVol (pp)'] < 0]['Giai đoạn']))) or 'không giai đoạn nào'}; trên toàn mẫu CI {'chứa' if all((E_[E_['Giai đoạn'] == 'Toàn mẫu']['CI lo'] < 0) & (E_[E_['Giai đoạn'] == 'Toàn mẫu']['CI hi'] > 0)) else 'không chứa'} 0.")
