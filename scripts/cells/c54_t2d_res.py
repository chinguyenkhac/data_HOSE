if len(HOLD):
    v = lambda sc, m, k: T2D[(T2D.scenario == sc) & (T2D["mode"] == m) & (T2D.method == k)]["Vol %"].iloc[0]
    sc_list = list(SCENARIOS); s0, s2 = sc_list[0], sc_list[2]
    chg_rank = any(int(rk.loc[(VN[m], sc), "EW-RIE*"]) != int(rk.loc[(VN[m], s0), "EW-RIE*"]) or rk.loc[(VN[m], sc)].idxmin() != rk.loc[(VN[m], s0)].idxmin() for m in MODES for sc in sc_list)
    chg_sig = any((CS[(sc, m)].loc[b, "p Holm"] < .05) != (CS[(s0, m)].loc[b, "p Holm"] < .05) for m in MODES for sc in sc_list for b in CORE5)
    md("**Kết quả.**\n\n"
       f"- **Số lượt:** {len(HOLD)} lượt mã trong universe bị hủy niêm yết trong kỳ nắm giữ trên {N_SLOT:,} vị thế ({100 * len(HOLD) / N_SLOT:.2f}%); theo lý do: " .replace(",", " ")
       + ", ".join(f"{RNV[k]} {n}" for k, n in HOLD.reason.value_counts().items()) + f". Còn {n_dl16} mã hủy từ {U0[0]['date']:%m/%Y} thiếu giá, không bao giờ vào universe (hạn chế còn lại).\n"
       f"- **Vol theo kịch bản** (EW-RIE\\*, chỉ mua): " + " → ".join(f"{sc.split(' (')[0]} {f2(v(sc, 'long_only', 'EW-RIE*'))}%" for sc in sc_list) + f"; VS-NL-LW: " + " → ".join(f"{f2(v(sc, 'long_only', 'VS-NL-LW'))}%" for sc in sc_list)
       + f". Bán khống (EW-RIE\\*): " + " → ".join(f"{f2(v(sc, 'short_ok', 'EW-RIE*'))}%" for sc in sc_list) + ".\n"
       f"- **ΔVol (EW-RIE\\* − VS-NL-LW)** ở S2 (−100%): chỉ mua {dci(CS[(s2, 'long_only')].loc['VS-NL-LW', 'ΔVol (pp)'], CS[(s2, 'long_only')].loc['VS-NL-LW', 'CI lo'], CS[(s2, 'long_only')].loc['VS-NL-LW', 'CI hi'])}, bán khống {dci(CS[(s2, 'short_ok')].loc['VS-NL-LW', 'ΔVol (pp)'], CS[(s2, 'short_ok')].loc['VS-NL-LW', 'CI lo'], CS[(s2, 'short_ok')].loc['VS-NL-LW', 'CI hi'])}; "
       f"thứ hạng và phương pháp đứng đầu **{'có đổi' if chg_rank else 'không đổi'}** giữa các kịch bản; kết luận kiểm định (p Holm < 0,05) **{'có đổi' if chg_sig else 'không đổi'}** ở họ lõi.\n\n"
       f"**Kết luận.** Kết quả " + ("vững" if not chg_rank and not chg_sig else "nhạy") + " với giả định lợi suất ngày hủy niêm yết, vì mã bị hủy trong kỳ nắm giữ rất hiếm và tỷ trọng của chúng nhỏ (bảng tỷ trọng). Hạn chế: 19 mã hủy thiếu giá và cú sốc −30%/−100% chỉ là kịch bản quy ước (Shumway 1997).")
else:
    md("**Kết quả.** Không có mã nào trong universe bị hủy niêm yết trong kỳ nắm giữ; giả định lợi suất 0 không ảnh hưởng kết quả. Hạn chế còn lại: 19 mã hủy thiếu giá (xem 4d).")
