h_ = lambda hv, m: T6H[(T6H.HL_VOL == hv) & (T6H["mode"] == m)].iloc[0]
md("**Kết quả** (ΔVol = EW-RIE\\* h = 60 − VS-NL-LW cùng HL\\_VOL, pp [CI 95%]; p Holm).\n\n"
   + "\n".join(f"- **{VN[m]}:** " + "; ".join(f"HL\\_VOL = {hv}: {dci(h_(hv, m)['ΔVol EW-RIE* − VS-NL-LW'], h_(hv, m)['CI lo'], h_(hv, m)['CI hi'])}, p {pv(h_(hv, m)['p Holm'])} (Vol VS-NL-LW {f2(h_(hv, m)['Vol VS-NL-LW'])}%)" for hv in HVS) + "." for m in MODES) + "\n"
   + "- **Mỗi bên ở tham số tốt nhất (hậu kiểm, chỉ tham khảo):** " + "; ".join(f"{m}: {r['EW-RIE* tốt nhất']} vs {r['VS-NL-LW tốt nhất']}: {dci(r['ΔVol (pp)'], r['CI lo'], r['CI hi'])}" for m, r in BEST.iterrows()) + ".\n\n"
   f"**Kết luận.** VS-NL-LW {'dẫn đầu ở mọi HL_VOL' if all(h_(hv, m)['ΔVol EW-RIE* − VS-NL-LW'] > 0 for hv in HVS for m in MODES) else 'không dẫn đầu ở mọi HL_VOL'} (ΔVol > 0 ở {sum(h_(hv, m)['ΔVol EW-RIE* − VS-NL-LW'] > 0 for hv in HVS for m in MODES)}/6 ô); "
   f"vị thế của EW-RIE\\* so với VS-NL-LW phụ thuộc HL\\_VOL: ΔVol thay đổi trong khoảng {f2(min(h_(hv, m)['ΔVol EW-RIE* − VS-NL-LW'] for hv in HVS for m in MODES))} đến {f2(max(h_(hv, m)['ΔVol EW-RIE* − VS-NL-LW'] for hv in HVS for m in MODES))} pp.")
