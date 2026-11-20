RN = {"bat_buoc": "bắt buộc", "hop_nhat": "hợp nhất/sáp nhập", "tu_nguyen": "tự nguyện", "chuyen_san": "chuyển sàn", "chua_ro": "chưa rõ"}
yrs = list(range(P.index[0].year, P.index[-1].year + 1)); ends = {y: min(pd.Timestamp(f"{y}-12-31"), P.index[-1]) for y in yrs}
tot = pd.Series({y: sum(1 for r in MASTER.itertuples() if r.listing_date <= ends[y] and (pd.isna(r.delisting_date) or r.delisting_date >= ends[y])) for y in yrs})
DY = dl.assign(year=dl.delisting_date.dt.year, reason=dl.reason.map(RN).fillna("chưa rõ")).pivot_table(index="year", columns="reason", values="ticker", aggfunc="count", fill_value=0).reindex(yrs, fill_value=0)
fig0, a0 = plt.subplots(figsize=(7, 3.8)); fig1, a1 = plt.subplots(figsize=(7, 3.8)); ax = [a0, a1]      # v6: tách thành hai hình
ax[0].bar(tot.index, tot.values, color="#2a78d6", width=.7)
for x_, v in tot.items(): ax[0].text(x_, v + 3, str(v), ha="center", fontsize=8)
ax[0].set_xticks(list(tot.index)); ax[1].set_xticks(yrs)
ax[0].set_title("Tổng số cổ phiếu niêm yết trên HOSE (cuối năm; 2026: đến 11/2026)", fontsize=10); ax[0].set_ylim(0, tot.max() * 1.12); ax[0].grid(axis="y", alpha=.3)
bot = np.zeros(len(DY))
for col, c in zip(DY.columns, ["#eb6834", "#2a78d6", "#1baf7a", "#eda100", "#9aa0a6"]):
    ax[1].bar(DY.index, DY[col], bottom=bot, color=c, width=.7, label=col); bot += DY[col].values
for x_, v in zip(DY.index, bot): ax[1].text(x_, v + .3, str(int(v)), ha="center", fontsize=8)
ax[1].set_title("Số cổ phiếu hủy niêm yết (rời HOSE) theo năm và lý do", fontsize=10); ax[1].legend(fontsize=8); ax[1].grid(axis="y", alpha=.3); ax[1].set_ylim(0, bot.max() * 1.15)
fig0.tight_layout(); savefig(fig0, "fig_2_niem_yet"); cap("Hình", "Tổng số cổ phiếu niêm yết trên HOSE cuối mỗi năm (2026: đến 11/2026).")
fig1.tight_layout(); savefig(fig1, "fig_3_huy_niem_yet"); cap("Hình", "Số cổ phiếu hủy niêm yết (rời HOSE) theo năm và lý do.")
cap("Bảng", "Số mã hủy niêm yết theo năm và lý do (cột cuối: tổng số mã niêm yết cuối năm).")
show(DY.assign(**{"Tổng hủy": DY.sum(1), "Niêm yết cuối năm": tot}).astype(int), 0)
