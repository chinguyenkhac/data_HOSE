vol_ = lambda m, r: T2A[(T2A["mode"] == m) & (T2A.REB == r) & (T2A.COST == CONFIG["COST"])].set_index("method")["Vol %"]
n_main = sum(vol_(m, r)[MAIN].idxmin() == "EW-RIE*" for m in MODES for r in REBS); n_full = sum(vol_(m, r).idxmin() == "EW-RIE*" for m in MODES for r in REBS)
tv = lambda m, b: T2CMP.loc[(m, 21, b)]
sig_t = lambda r: "có ý nghĩa" if (r["Turn CI hi"] < 0 or r["Turn CI lo"] > 0) else "không có ý nghĩa"
ta = {m: T2A[(T2A["mode"] == m) & (T2A.COST == CONFIG["COST"]) & (T2A.method == "EW-RIE*")].sort_values("REB") for m in MODES}
md("**Kết quả.**\n\n"
   f"- **Rủi ro:** EW-RIE\\* có Vol thấp nhất trong 5 phương pháp chính ở {n_main}/6 tổ hợp (REB × chế độ) và trong cả 15 phương pháp ở {n_full}/6. "
   f"So với VS-NL-LW (ΔVol, p Holm): " + "; ".join(f"{VN[m]} REB = {r}: {T2CMP.loc[(m, r, 'VS-NL-LW'), 'ΔVol (pp)']:+.2f} pp, p {pv(T2CMP.loc[(m, r, 'VS-NL-LW'), 'p Holm'])}" for m in MODES for r in REBS) + ".\n"
   f"- **Tần suất** (chỉ mua): REB 5 → 21 → 63 làm Vol EW-RIE\\* {' → '.join(f2(x) for x in ta['long_only']['Vol %'])}% và turnover/năm {' → '.join(f2(x, 1) for x in ta['long_only']['Turnover/năm'])}.\n"
   f"- **Turnover** (REB = 21, EW-RIE\\* − VS-NL-LW, mỗi kỳ): chỉ mua {dci(tv('long_only', 'VS-NL-LW')['ΔTurnover'], tv('long_only', 'VS-NL-LW')['Turn CI lo'], tv('long_only', 'VS-NL-LW')['Turn CI hi'])} ({sig_t(tv('long_only', 'VS-NL-LW'))}), "
   f"bán khống {dci(tv('short_ok', 'VS-NL-LW')['ΔTurnover'], tv('short_ok', 'VS-NL-LW')['Turn CI lo'], tv('short_ok', 'VS-NL-LW')['Turn CI hi'])} ({sig_t(tv('short_ok', 'VS-NL-LW'))}).\n"
   f"- **COST hòa vốn** (EW-RIE\\* = VS-NL-LW về Sharpe sau phí, REB = 21): chỉ mua {BE[(VN['long_only'], 'VS-NL-LW')]}, bán khống {BE[(VN['short_ok'], 'VS-NL-LW')]}.\n\n"
   f"**Kết luận.** Thứ hạng Vol theo REB: EW-RIE\\* {'đứng đầu' if n_main == 6 else 'không luôn đứng đầu'} trong nhóm chính; sau phí mọi GMV có Sharpe ≈ 0 nên đóng góp là ước lượng rủi ro, không phải chiến lược sinh lời.")
