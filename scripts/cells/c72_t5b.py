# T5b. Dự báo phương sai 21 phiên tới: EWMA (hl ∈ {10, 20, 40}, đúng hàm ewma_standardize mà VS dùng) vs cửa sổ phẳng 63/250 phiên.
# Mẫu: các mã trong universe chuẩn ở mỗi kỳ; dự báo chỉ dùng cửa sổ quá khứ. Mục tiêu RV = trung bình r² của 21 phiên sau.
# Sai số: RMSE của vol năm hóa (%) và QLIKE = log h + RV/h (dạng Patton 2011, xác định cả khi RV = 0).
W, H = CONFIG["WINDOW"], 21; rows = []
for u in U0:
    s = POS[u["date"]]
    if s + H > len(R_BT): continue
    X = R_BT.iloc[s - W:s][u["tickers"]].fillna(0).values; rv = (R_BT.iloc[s:s + H][u["tickers"]].fillna(0).values ** 2).mean(0)
    fc = {**{f"EWMA hl={h}": ewma_standardize(X, h)[1] ** 2 for h in (10, 20, 40)}, **{f"Phẳng {w} phiên": (X[-w:] ** 2).mean(0) for w in (63, W)}}
    per_ = next((p for p, a_, b_ in PERIODS if pd.Timestamp(a_) <= u["date"] <= pd.Timestamp(b_)), None)
    for k, h in fc.items():
        h = np.maximum(h, 1e-12); rows.append(dict(period=per_, model=k, se=np.mean((np.sqrt(h) - np.sqrt(rv)) ** 2), ql=np.mean(np.log(h) + rv / h)))
F = pd.DataFrame(rows); F = pd.concat([F, F.assign(period="Toàn mẫu")])
T5B = F.groupby(["period", "model"], sort=False).agg(RMSE=("se", lambda x: np.sqrt(x.mean() * 252) * 100), QLIKE=("ql", "mean"), n=("se", "size"))
save(T5B.reset_index(), "T5b_vol_forecast")
tbl = T5B["RMSE"].unstack()[["EWMA hl=10", "EWMA hl=20", "EWMA hl=40", "Phẳng 63 phiên", f"Phẳng {W} phiên"]]
tbl.loc["QLIKE (toàn mẫu)"] = T5B.xs("Toàn mẫu")["QLIKE"]
cap("Bảng", "RMSE dự báo vol 21 phiên (%/năm) theo giai đoạn; dòng cuối: QLIKE toàn mẫu (thấp hơn = tốt hơn).")
show(tbl, 2)
fig, ax = plt.subplots(figsize=(11, 3.8)); M_ = tbl.drop(index="QLIKE (toàn mẫu)"); x = np.arange(len(M_))
for j, (c, col) in enumerate(zip(M_.columns, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#9aa0a6"])): ax.bar(x + (j - 2) * .16, M_[c], .15, color=col, label=c)
ax.set_xticks(x, M_.index, rotation=15, fontsize=8); ax.set_ylabel("RMSE vol (%/năm)"); ax.grid(axis="y", alpha=.3)
ax.legend(fontsize=8, ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.25), frameon=False); plt.tight_layout(); savefig(fig, "fig_vol_forecast")
cap("Hình", "Sai số dự báo vol 21 phiên: EWMA vs cửa sổ phẳng, theo giai đoạn (cấu hình chuẩn).")
fa, cv = M_.loc["Toàn mẫu"], M_.loc["2020Q1 COVID"]
