sc_ = lambda m, k, s: T2C.loc[k, (VN[m], s)]
md("**Kết quả.** Với Σw = 1, giá trị mua bằng giá trị bán nên phí thực tế bất đối xứng (mua 0,15% / bán 0,25%) **tương đương COST đối xứng 0,20%** (unit test và lần chạy lại thật). Sharpe sau phí (REB = 21, chỉ mua) ở phí thực tế: "
   + ", ".join(f"{k.replace('*', chr(92) + '*')} {f2(sc_('long_only', k, 'Mua 0,15% / bán 0,25%'), 3)} (gốc 0,25%: {f2(sc_('long_only', k, 'COST 0,25% (gốc)'), 3)})" for k in MAIN) + ".\n\n"
   "**Kết luận.** Giả định 0,25% hơi bảo thủ nhưng không đổi kết luận. Hạn chế: lợi suất kỳ tính bằng tỷ trọng cố định `Y @ w` (không mô phỏng trôi tỷ trọng), chưa có spread/trượt giá, kỳ đầu không trừ phí mua.")
