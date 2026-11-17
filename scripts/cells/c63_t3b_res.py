v3b = lambda m: T3B[T3B["mode"] == m].set_index("method")["Vol %"]
sb = lambda m: T3B[T3B["mode"] == m].set_index("method")["Sharpe sau phí"]
per_lo = P3.loc[VN["long_only"]].loc[MAIN]
md("**Kết quả.**\n\n"
   f"- **Chỉ mua:** {order_txt(v3b('long_only'), MAIN + ['PCA-auto', 'DCC-GARCH(1,1)', '1/N'])}.\n"
   f"- **Bán khống:** {order_txt(v3b('short_ok'), MAIN + ['PCA-auto', 'DCC-GARCH(1,1)', '1/N'])}.\n"
   f"- **Hạng trong 15 phương pháp** (chỉ mua): EW-RIE\\* {int(v3b('long_only').rank()['EW-RIE*'])}, VS-NL-LW {int(v3b('long_only').rank()['VS-NL-LW'])}, EW-WeSpeR {int(v3b('long_only').rank()['EW-WeSpeR'])}; thấp nhất: {v3b('long_only').idxmin().replace('*', chr(92) + '*')} ({f2(v3b('long_only').min())}%); bán khống thấp nhất: {v3b('short_ok').idxmin().replace('*', chr(92) + '*')} ({f2(v3b('short_ok').min())}%).\n"
   f"- **Theo giai đoạn** (chỉ mua): EW-RIE\\* thấp hơn NL-LW nhiều nhất ở {(per_lo.loc['NL-LW'] - per_lo.loc['EW-RIE*']).idxmax()} ({f2((per_lo.loc['NL-LW'] - per_lo.loc['EW-RIE*']).max())} pp); VS-NL-LW thấp hơn EW-RIE\\* nhiều nhất ở {(per_lo.loc['EW-RIE*'] - per_lo.loc['VS-NL-LW']).idxmax()} ({f2((per_lo.loc['EW-RIE*'] - per_lo.loc['VS-NL-LW']).max())} pp).\n"
   f"- **Sau phí:** Sharpe sau phí cao nhất {sb('long_only').idxmax().replace('*', chr(92) + '*')} ({f2(sb('long_only').max(), 3)}); nhóm EW-RIE\\*/VS-NL-LW/EW-WeSpeR: {f2(sb('long_only')['EW-RIE*'], 3)} / {f2(sb('long_only')['VS-NL-LW'], 3)} / {f2(sb('long_only')['EW-WeSpeR'], 3)}.\n"
   f"- **Thời gian/lần ước lượng (N = 100):** EW-RIE\\* {TS['EW-RIE*']:.2f} s, EW-WeSpeR {TS['EW-WeSpeR']:.2f} s (nguội), VS-NL-LW {TS['VS-NL-LW']:.3f} s, DCC-GARCH {TS['DCC-GARCH(1,1)']:.1f} s (bảng đo ở §4.3; không còn trúng cache).\n\n"
   "**Kết luận.** Thứ hạng và khác biệt có ý nghĩa xem Bảng kiểm định ngay dưới (T3c).")
