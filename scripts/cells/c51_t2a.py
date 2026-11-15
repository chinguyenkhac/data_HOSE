# T2a. Lưới REB ∈ {5, 21, 63} × COST ∈ {0,15%; 0,25%; 0,40%}, đủ FULL, cả hai chế độ (DCC có thể bỏ ở REB = 5 nếu quá 45 phút, xem Ghi chú).
# Vol chỉ phụ thuộc REB. COST không đổi tỷ trọng ⇒ mỗi (REB, chế độ) một backtest; Sharpe sau phí ở từng COST tính lại từ chuỗi turnover (kiểm ở T2c).
REBS, COSTS = (5, 21, 63), (0.0015, 0.0025, 0.004)
DCC_SKIP_REB = ()                                     # REB bị bỏ DCC-GARCH (điền khi DCC > 45 phút; xem BAO_CAO_V4.md)
T2R = {(reb, m): run_full(dict(CONFIG, REB=reb), lo, [k for k in FULL if not (reb in DCC_SKIP_REB and k.startswith("DCC"))]) for reb in REBS for m, lo in MODES.items()}
T2A = pd.DataFrame([dict(mode=m, REB=reb, COST=c, method=k, **metrics(o, c), **{"Turnover/năm": o["m"]["Turnover/kỳ"] * 252 / reb})
                    for (reb, m), d in T2R.items() for k, o in d["out"].items() for c in COSTS])
save(T2A, "T2a_reb_cost_grid_full")
g = T2A.sort_values("COST").groupby(["method", "mode", "REB"])
assert g["Sharpe sau phí"].apply(lambda s: (s.diff().dropna() <= 1e-12).all()).all(), "COST tăng mà Sharpe sau phí tăng?"

tb = T2A[T2A.COST == CONFIG["COST"]].pivot_table(index=["mode", "REB"], columns="method", values="Vol %")[[k for k in MAIN]]
cap("Bảng", "Vol (%/năm, gộp) theo tần suất tái cân bằng REB, các phương pháp chính; N = 100, h = 60, mỗi REB dùng đúng cùng ngày cho mọi phương pháp. Đủ FULL: `results_v4/T2a_reb_cost_grid_full.csv`.")
show(tb.rename(index=VN, level=0), 2)
ts = T2A[T2A.method.isin(MAIN)].pivot_table(index=["mode", "REB", "COST"], columns="method", values="Sharpe sau phí")[MAIN]
cap("Bảng", "Sharpe sau phí theo REB × COST (COST: phí một chiều), các phương pháp chính. Sharpe trước phí ≈ 0,3–0,6 nên sau phí mọi GMV ≈ 0.")
show(ts.rename(index=VN, level=0), 3)

# compare_to ở từng REB (kèm ΔTurnover): họ lõi, p Holm trên 4 đối thủ
T2C_ = {}
for (reb, m), d in T2R.items():
    T2C_[(m, reb)] = cmp_table(d["out"], "EW-RIE*", reb_dates=[u["date"] for u in d["ulog"]])
T2CMP = pd.concat(T2C_, names=["mode", "REB", "rival"]); save(T2CMP.reset_index(), "T2a_compare_full")
cap("Bảng", "EW-RIE\\* so với họ lõi theo REB (COST = 0,25%): ΔVol (pp, < 0: EW-RIE\\* thấp hơn), p Holm (4 đối thủ lõi), ΔTurnover/kỳ [CI 95% theo kỳ] (< 0: EW-RIE\\* giao dịch ít hơn).")
x = T2CMP.loc[(slice(None), slice(None), CORE5), ["ΔVol (pp)", "CI lo", "CI hi", "p Holm", "ΔTurnover", "Turn CI lo", "Turn CI hi"]]
x = x.assign(**{"ΔVol [CI]": [f"{a:+.2f} [{b:+.2f}; {c:+.2f}]" for a, b, c in zip(x["ΔVol (pp)"], x["CI lo"], x["CI hi"])],
                "ΔTurnover [CI]": [f"{a:+.2f} [{b:+.2f}; {c:+.2f}]" for a, b, c in zip(x["ΔTurnover"], x["Turn CI lo"], x["Turn CI hi"])]})
show(x[["ΔVol [CI]", "p Holm", "ΔTurnover [CI]"]].rename(index=VN, level=0), 3)

# COST hòa vốn: mức COST mà Sharpe sau phí của EW-RIE* bằng đối thủ (REB = 21)
cg = np.linspace(0, 0.02, 801); be = {}
for m in MODES:
    for b in CORE5:
        a_s = np.array([ann(net(T2R[21, m]["out"]["EW-RIE*"], c))[1] for c in cg]); b_s = np.array([ann(net(T2R[21, m]["out"][b], c))[1] for c in cg])
        sg = np.sign(a_s - b_s); i = np.where(np.diff(sg) != 0)[0]
        be[(VN[m], b)] = f"{cg[i[0]]:.2%}" if len(i) else ("EW-RIE* hơn ở mọi COST" if sg[0] > 0 else "EW-RIE* kém ở mọi COST")
BE = pd.Series(be, name="COST hòa vốn Sharpe sau phí (EW-RIE* = đối thủ)")
cap("Bảng", "COST một chiều mà tại đó Sharpe sau phí của EW-RIE\\* bằng đối thủ (REB = 21, quét 0–2%).")
show(BE.to_frame(), 3)

fig, ax = plt.subplots(1, 2, figsize=(12, 3.9), sharey=False)
for a, m in zip(ax, MODES):
    for k in MAIN: v = T2A[(T2A["mode"] == m) & (T2A.COST == CONFIG["COST"]) & (T2A.method == k)].sort_values("REB"); a.plot(v.REB, v["Vol %"], marker="o", lw=2.2 if k == "EW-RIE*" else 1.4, color=col_of(k), label=k)
    a.set_xticks(REBS); a.set_xlabel("REB (phiên)"); a.set_ylabel("Vol (%/năm)"); a.set_title(VN[m], fontsize=10); a.grid(alpha=.3)
ax[0].legend(fontsize=8, loc="upper center", bbox_to_anchor=(1.1, -0.2), ncol=5, frameon=False)
plt.tight_layout(); savefig(fig, "fig_reb_vol")
cap("Hình", "Vol ngoài mẫu theo REB (COST không ảnh hưởng Vol); N = 100, h = 60, chuẩn ZERO_MAX = 20%.")
fig, ax = plt.subplots(1, 2, figsize=(12, 3.9))
for a, m in zip(ax, MODES):
    for k in MAIN: a.plot(np.array(COSTS) * 100, [T2A[(T2A["mode"] == m) & (T2A.REB == 21) & (T2A.COST == c) & (T2A.method == k)]["Sharpe sau phí"].iloc[0] for c in COSTS],
                          marker="o", lw=2.2 if k == "EW-RIE*" else 1.4, color=col_of(k), label=k)
    a.set_xlabel("COST một chiều (%)"); a.set_ylabel("Sharpe sau phí"); a.set_title(VN[m], fontsize=10); a.grid(alpha=.3); a.axhline(0, color="#52514e", lw=.8)
ax[0].legend(fontsize=8, loc="upper center", bbox_to_anchor=(1.1, -0.2), ncol=5, frameon=False)
plt.tight_layout(); savefig(fig, "fig_cost_sharpe")
cap("Hình", "Sharpe sau phí theo COST (REB = 21).")
