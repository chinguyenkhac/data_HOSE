best_m = fa.drop(index=[c for c in fa.index if c.startswith("QLIKE")], errors="ignore").idxmin(); ql = tbl.loc["QLIKE (toàn mẫu)"]
md("**Kết quả (T5b)** — dự báo vol 21 phiên, toàn mẫu: " + f"RMSE tốt nhất là **{best_m}** ({f2(fa.min())}%/năm) so với cửa sổ phẳng {W} phiên {f2(fa[f'Phẳng {W} phiên'])}% và phẳng 63 phiên {f2(fa['Phẳng 63 phiên'])}%; QLIKE tốt nhất: {ql.idxmin()}. "
   f"Trong COVID 2020Q1: EWMA hl = 10 {f2(cv['EWMA hl=10'])}% so với phẳng {W} phiên {f2(cv[f'Phẳng {W} phiên'])}%. "
   f"Giai đoạn cửa sổ phẳng {W} phiên thắng mọi EWMA: " + (", ".join(M_.index[M_[f'Phẳng {W} phiên'] < M_[[c for c in M_.columns if c.startswith('EWMA')]].min(axis=1)]) or "không giai đoạn nào") + ".\n\n"
   "**Kết luận.** EWMA dự báo biến động riêng lẻ tốt hơn cửa sổ phẳng khi biến động đổi nhanh; điều này khớp với việc lợi ích của VS tập trung ở giai đoạn cú sốc (T5a).")
