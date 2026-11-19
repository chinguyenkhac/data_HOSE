f3 = lambda x: f2(x, 2)
md(f"**Kết quả Test 2b** (rủi ro GMV / rủi ro tối ưu, 1 = hoàn hảo).\n\n"
   f"- h = 15 (N > T\\_eff): EW-NL-LW bản thầy {f3(t2b.loc['EW-NL-LW (v2)', 15])} → bản sửa **{f3(t2b.loc['EW-NL-LW', 15])}** (oracle {f3(t2b.loc['Oracle', 15])}); EW-WeSpeR {f3(t2b.loc['EW-WeSpeR', 15])}; EW-RIE\\* {f3(t2b.loc['EW-RIE*', 15])}.\n"
   f"- h = 60 (N < T\\_eff): hai bản EW-NL-LW trùng nhau ({f3(t2b.loc['EW-NL-LW', 60])}); EW-RIE\\* {f3(t2b.loc['EW-RIE*', 60])}, EW-WeSpeR {f3(t2b.loc['EW-WeSpeR', 60])}.\n\n"
   f"**Kết luận.** Bản sửa đúng (không kém bản thầy ở mọi h); EW-WeSpeR sát oracle (trong {f2(100 * (t2b.loc['EW-WeSpeR'] / t2b.loc['Oracle']).max() - 100, 1)}%); EW-RIE\\* kém hơn khi N > T\\_eff.")
