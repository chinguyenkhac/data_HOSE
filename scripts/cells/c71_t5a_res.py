ta_ = T5A.reset_index(); neg = int((ta_["ΔVol (pp)"] < 0).sum()); sg_ = int((ta_["CI hi"] < 0).sum()); tr = (T5A["Turnover VS"] if "Turnover VS" in T5A else None)
trr = {r["Cặp"]: (r["ΔTurnover"]) for _, r in ta_.iterrows()}
worst = T5P.stack().idxmax(); best = T5P.stack().idxmin()
md("**Kết quả (T5a).**\n\n"
   f"- **Tác động tổng:** VS giảm Vol ở {neg}/{len(ta_)} cặp × chế độ, từ {f2(ta_['ΔVol (pp)'].min())} đến {f2(ta_['ΔVol (pp)'].max())} pp/năm; {sg_}/{len(ta_)} có CI 95% nằm hẳn dưới 0. "
   f"Riêng cặp EW-RIE\\*: " + "; ".join(f"{r['Chế độ']} {dci(r['ΔVol (pp)'], r['CI lo'], r['CI hi'])}" for _, r in ta_[ta_["Cặp"] == "VS-EW-RIE* vs EW-RIE*"].iterrows()) + ".\n"
   f"- **Theo giai đoạn:** VS giảm nhiều nhất ở {best[0]} ({f2(T5P.loc[best[0]].min())} pp, cặp {best[1][1]}, {best[1][0]}); VS làm Vol tăng nhiều nhất ở {worst[0]} (+{f2(T5P.stack().max())} pp, {worst[1][1]}, {worst[1][0]}).\n"
   f"- **Cái giá:** turnover/kỳ tăng thêm {f2(ta_['ΔTurnover'].min())}–{f2(ta_['ΔTurnover'].max())} khi dùng VS; Sharpe sau phí giảm ở {int((ta_['Sharpe sau phí VS'] < ta_['Sharpe sau phí gốc']).sum())}/{len(ta_)} cặp.\n\n"
   "**Kết luận.** VS giúp nhờ ước lượng biến động riêng lẻ theo kịp thay đổi chế độ (T5b), lợi ích tập trung ở giai đoạn cú sốc, đổi bằng turnover cao hơn.")
