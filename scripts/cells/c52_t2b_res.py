z_ = lambda v, m, k: T2B[(T2B.variant == v) & (T2B["mode"] == m) & (T2B.method == k)]["Vol %"].iloc[0]
vk = list(VARS); mono = all(z_(vk[i], "long_only", "EW-RIE*") <= z_(vk[i + 1], "long_only", "EW-RIE*") for i in range(len(vk) - 1))
rk_ = lambda v, m: T2B[(T2B.variant == v) & (T2B["mode"] == m)].set_index("method")["Vol %"].rank()
md("**Kết quả** (ngày OOS chung).\n\n"
   f"- **Mức rủi ro:** Vol chỉ mua của EW-RIE\\*: " + " → ".join(f"{v} {f2(z_(v, 'long_only', 'EW-RIE*'))}%" for v in vk) + f" ({'tăng' if mono else 'không đơn điệu'} theo độ chặt của bộ lọc). % phiên r = 0 trong universe: " + " → ".join(f"{f2(info.loc[v, '% r=0 trong universe'], 1)}%" for v in vk) + ".\n"
   f"- **Số kỳ hợp lệ:** " + ", ".join(f"{v}: {int(info.loc[v, 'Số kỳ hợp lệ'])}" for v in vk) + ".\n"
   f"- **Hạng của EW-RIE\\* / VS-NL-LW trong 15 phương pháp** (chỉ mua): " + "; ".join(f"{v}: {int(rk_(v, 'long_only')['EW-RIE*'])} / {int(rk_(v, 'long_only')['VS-NL-LW'])}" for v in vk) + ".\n"
   f"- **EW-RIE\\* − VS-NL-LW** (chỉ mua, ΔVol [CI], p Holm): " + "; ".join(f"{v}: {dci(T2BC[(v, 'long_only')].loc['VS-NL-LW', 'ΔVol (pp)'], T2BC[(v, 'long_only')].loc['VS-NL-LW', 'CI lo'], T2BC[(v, 'long_only')].loc['VS-NL-LW', 'CI hi'])}, p {pv(T2BC[(v, 'long_only')].loc['VS-NL-LW', 'p Holm'])}" for v in vk) + ".\n\n"
   f"**Kết luận.** Lọc mã đứng giá làm Vol ngoài mẫu {'tăng' if mono else 'đổi'} đồng loạt (Vol không lọc đánh giá thấp rủi ro thật vì GMV dồn vào chuỗi 'đứng'); thứ hạng giữa các phương pháp xem hàng hạng ở trên. Chuẩn vẫn là 20% (giữ 118 kỳ).")
