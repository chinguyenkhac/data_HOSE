g_ = lambda m, b, c: T3C[m].loc[b, c]
lin = []
for m in ("long_only", "short_ok"):
    lin.append(f"- **{VN[m]}** (EW-RIE\\* − đối thủ, ΔVol [CI 95%], p Holm): " + "; ".join(
        f"{b.replace('*', chr(92) + '*')} {dci(g_(m, b, 'ΔVol (pp)'), g_(m, b, 'CI lo'), g_(m, b, 'CI hi'))}, p {pv(g_(m, b, 'p Holm'))}" for b in CORE5) + ".")
vs_ = lambda m: T3C[m].loc["VS-NL-LW"]
sh_ = lambda m: all(T3C[m].loc[b, "p JKM"] > .05 for b in CORE5)
tv_ = lambda m: T3C[m].loc["VS-NL-LW"]
sx = lambda m: T3X[m]
res_vs = {m: ("thấp hơn" if vs_(m)["ΔVol (pp)"] < 0 else "cao hơn") + (" VS-NL-LW có ý nghĩa" if vs_(m)["p Holm"] < .05 else " VS-NL-LW nhưng không có ý nghĩa sau Holm") for m in MODES}
md("**Kết quả** (ΔVol < 0: EW-RIE\\* rủi ro thấp hơn).\n\n" + "\n".join(lin) + "\n"
   f"- **Cặp quan trọng nhất, EW-RIE\\* vs VS-NL-LW:** chỉ mua {dci(vs_('long_only')['ΔVol (pp)'], vs_('long_only')['CI lo'], vs_('long_only')['CI hi'])} pp, bán khống {dci(vs_('short_ok')['ΔVol (pp)'], vs_('short_ok')['CI lo'], vs_('short_ok')['CI hi'])} pp; EW-RIE\\* {res_vs['long_only']} (chỉ mua) và {res_vs['short_ok']} (bán khống); "
   f"ΔTurnover/kỳ {dci(tv_('long_only')['ΔTurnover'], tv_('long_only')['Turn CI lo'], tv_('long_only')['Turn CI hi'])} (chỉ mua), {dci(tv_('short_ok')['ΔTurnover'], tv_('short_ok')['Turn CI lo'], tv_('short_ok')['Turn CI hi'])} (bán khống).\n"
   f"- **Với EW-WeSpeR:** {dci(g_('long_only', 'EW-WeSpeR', 'ΔVol (pp)'), g_('long_only', 'EW-WeSpeR', 'CI lo'), g_('long_only', 'EW-WeSpeR', 'CI hi'))} (chỉ mua), {dci(g_('short_ok', 'EW-WeSpeR', 'ΔVol (pp)'), g_('short_ok', 'EW-WeSpeR', 'CI lo'), g_('short_ok', 'EW-WeSpeR', 'CI hi'))} (bán khống): {'không khác biệt' if (g_('long_only', 'EW-WeSpeR', 'p Holm') > .05 and g_('short_ok', 'EW-WeSpeR', 'p Holm') > .05) else 'có khác biệt có ý nghĩa ở ít nhất một chế độ'}.\n"
   f"- **VS-EW-RIE\\*:** so với VS-NL-LW {dci(sx('long_only').loc['VS-NL-LW', 'ΔVol (pp)'], sx('long_only').loc['VS-NL-LW', 'CI lo'], sx('long_only').loc['VS-NL-LW', 'CI hi'])} (chỉ mua), {dci(sx('short_ok').loc['VS-NL-LW', 'ΔVol (pp)'], sx('short_ok').loc['VS-NL-LW', 'CI lo'], sx('short_ok').loc['VS-NL-LW', 'CI hi'])} (bán khống); so với EW-RIE\\* {dci(sx('long_only').loc['EW-RIE*', 'ΔVol (pp)'], sx('long_only').loc['EW-RIE*', 'CI lo'], sx('long_only').loc['EW-RIE*', 'CI hi'])} / {dci(sx('short_ok').loc['EW-RIE*', 'ΔVol (pp)'], sx('short_ok').loc['EW-RIE*', 'CI lo'], sx('short_ok').loc['EW-RIE*', 'CI hi'])}.\n"
   f"- **Sharpe (JKM):** {'không có chênh lệch nào có ý nghĩa với họ lõi (p JKM > 0,05)' if sh_('long_only') and sh_('short_ok') else 'có chênh lệch có ý nghĩa với ít nhất một đối thủ lõi (xem cột p JKM)'}.\n\n"
   f"**Kết luận.** So với họ lõi: EW-RIE\\* {res_vs['long_only']} (chỉ mua) và {res_vs['short_ok']} (bán khống). Các đối thủ còn lại xem dấu ▼/▲ ở bảng: "
   + "; ".join(f"{VN[m]}: " + ", ".join(f"{k.replace('*', chr(92) + '*')} {s}" for k, s in zip(T3C[m].index, sig_mark(T3C[m]))) for m in MODES) + ".")
