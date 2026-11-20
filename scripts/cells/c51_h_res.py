T51 = pd.DataFrame(rows).assign(delta=lambda d: d.vol_EWRIE - d.vol_EWNLLW); save(T51, "T6_half_life_ewrie_vs_ewnllw")
cap("Bảng", "Độ nhạy half-life (ô của thầy; chỉ EW-NL-LW và EW-RIE\\*): Vol (%/năm) và CI 95% bootstrap khối của Vol(EW-RIE\\*) − Vol(EW-NL-LW). Đủ 15 phương pháp: §5.2 (lưới N × h).")
show(T51.set_index(["hl", "mode"]), 3)
g = lambda h, m: T51[(T51.hl == h) & (T51["mode"] == m)].iloc[0]
md("**Kết quả** (EW-RIE\\* − EW-NL-LW, pp). " + "; ".join(f"h = {h}: chỉ mua {dci(g(h, 'long_only').delta, g(h, 'long_only').CI_lo, g(h, 'long_only').CI_hi)}, bán khống {dci(g(h, 'short_ok').delta, g(h, 'short_ok').CI_lo, g(h, 'short_ok').CI_hi)}" for h in (30, 60, 120))
   + ".\n\n**Kết luận.** Lợi thế so với EW-NL-LW " + ("lớn nhất ở h = 30 và nhỏ dần khi h tăng" if g(30, 'long_only').delta < g(120, 'long_only').delta else "không đơn điệu theo h") + "; h = 30 có q\\_eff = 1,16 (N > T\\_eff). So với VS-NL-LW xem 5.2.")
