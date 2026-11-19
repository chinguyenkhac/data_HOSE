# ---- 7.4 Hướng 4: danh mục thực thi được — trần tỷ trọng, trần turnover, sức chứa vốn; Bảng 41, 42; Hình 27, 28 ----
from scipy.stats import kendalltau
CFG4 = {"A chuẩn": ("lo", None), "B trần 20%": ("c20", None), "C trần 10%": ("c10", None),
        "D turnover ≤ 10%": ("lo", .10), "E trần 10% + turnover ≤ 10%": ("c10", .10)}
SIM4 = {(nm, c): (SIM1[nm] if c == "A chuẩn" else simulate(TG[nm], S_REG, k, to_cap=tc)) for nm in M7X for c, (k, tc) in CFG4.items()}
pd.to_pickle({k: v[0] for k, v in SIM4.items()}, f"{R7}/H4_returns.pkl")
P4 = {k: perf7(*v) for k, v in SIM4.items()}
VOL4 = pd.DataFrame({c: {nm: P4[(nm, c)]["Vol %"] for nm in M7X} for c in CFG4}); RK = VOL4.loc[M7].rank()
rows, pE = {}, []
for c in CFG4:
    rows[c] = {nm: f"{f2(VOL4.loc[nm, c])}" + (f" ({int(RK.loc[nm, c])})" if nm in M7 else "") for nm in M7X}
    dv_, _, p_bt = lw7(SIM4[("EW-RIE*", c)][0], SIM4[("VS-NL-LW", c)][0]); pE.append(p_bt)
    rows[c].update({"CAGR EW-RIE* / VS-NL-LW %": f"{f2(P4[('EW-RIE*', c)]['CAGR %'])} / {f2(P4[('VS-NL-LW', c)]['CAGR %'])}",
                    "Turnover/năm EW-RIE* / VS-NL-LW %": f"{f2(P4[('EW-RIE*', c)]['Turnover/năm %'], 0)} / {f2(P4[('VS-NL-LW', c)]['Turnover/năm %'], 0)}",
                    "Kendall τ so với A (6 phương pháp)": f2(kendalltau(RK["A chuẩn"], RK[c])[0]), "ΔVol EW-RIE* − VS-NL-LW (pp)": dv(dv_)})
for c, p in zip(CFG4, holm(pE)): rows[c]["p Holm (5 cấu hình)"] = pv(p)
T41 = pd.DataFrame(rows); save7(T41, "H4_thu_hang"); save7(VOL4, "H4_vol")
cap("Bảng", "Danh mục thực thi được, chỉ mua, NAV ròng, REB = 21: Vol (%/năm) và (hạng trong 6 phương pháp chính) theo cấu hình — trần tỷ trọng 20%, 10% "
    "(GMV có trần, cùng ma trận hiệp phương sai), trần turnover một chiều 10%/kỳ (đi một phần về đích). Dưới: CAGR, turnover, Kendall τ của thứ hạng so với A, "
    "ΔVol EW-RIE\\* − VS-NL-LW và p Ledoit–Wolf bootstrap khối (Holm trên 5 cấu hình).")
display(T41.style.set_properties(**{"text-align": "right"}))

ADV20 = V.rolling(20, min_periods=10).mean().shift(1).values        # TB giá trị GD 20 phiên TRƯỚC kỳ (đồng; giá điều chỉnh × KL)
FUNDS = {"100 tỷ": 100e9, "1 000 tỷ": 1000e9}
def capacity(nm, kind, F):
    out = []
    for s in S_REG:
        ix, Wm = TG[nm][s]; w = Wm[KINDS.index(kind)]; held = w > 1e-4; w, ix = w[held], ix[held]
        adv = ADV20[s, ix]; days = np.where(adv > 0, F * w / (.1 * np.where(adv > 0, adv, 1)), np.inf)
        o = np.argsort(days); cw = np.cumsum(w[o]) / w.sum()
        out.append({"date": DATES7[s], "% vị thế > 10% ADV20": 100 * (days > 1).mean(), "% NAV trong các vị thế đó": 100 * w[days > 1].sum(),
                    "Số ngày (trung vị theo tỷ trọng)": days[o][np.searchsorted(cw, .5)], "Số ngày lớn nhất": days.max(),
                    "% NAV bán được trong 5 phiên": 100 * (w * np.minimum(1, 5 / days)).sum()})
    return pd.DataFrame(out).set_index("date")
CAPS = {(nm, c, f): capacity(nm, k, F) for nm in M7 for c, k in (("A chuẩn", "lo"), ("C trần 10%", "c10")) for f, F in FUNDS.items()}
T42 = pd.DataFrame({k: {**v.mean().to_dict(), "% NAV bán được trong 5 phiên (kỳ xấu nhất)": v["% NAV bán được trong 5 phiên"].min()} for k, v in CAPS.items()}).T
T42.index.names = ["Phương pháp", "Cấu hình", "Quỹ"]; T42 = T42.reorder_levels(["Quỹ", "Cấu hình", "Phương pháp"]).sort_index(level=[0, 1], sort_remaining=False)
save7(T42, "H4_suc_chua"); M42 = ["EW-RIE*", "VS-NL-LW", "NL-LW", "1/N"]
cap("Bảng", "Sức chứa vốn (tỷ trọng đích chỉ mua, 118 kỳ): vị thế = quỹ × tỷ trọng; ADV20 = giá trị giao dịch bình quân 20 phiên trước kỳ (`values.csv` = giá điều chỉnh × khối lượng, "
    "đánh giá thấp những năm đầu ⇒ thận trọng); số ngày thanh lý = vị thế / (10% × ADV20). Trung bình qua các kỳ; cột cuối: kỳ xấu nhất. "
    "EW-NL-LW, EW-WeSpeR gần trùng EW-RIE\\* nên chỉ có trong `results_v7/H4_suc_chua.csv`.")
show(T42[T42.index.get_level_values("Phương pháp").isin(M42)], 1)

fig, ax = plt.subplots(figsize=(11, 4.2)); xs = np.arange(len(CFG4))
for nm in [m for m in M7 if m != "1/N"]:                   # 1/N không đổi (22,6%): bỏ để giữ thang
    ax.plot(xs, VOL4.loc[nm].values, marker="o", ms=6, color=col_of(nm), lw=1.8 if nm in ("EW-RIE*", "VS-NL-LW") else 1.1, label=nm)
ax.set_xticks(xs); ax.set_xticklabels(list(CFG4), fontsize=9); ax.set_ylabel("Vol ngoài mẫu, %/năm"); ax.grid(alpha=.3); ax.legend(fontsize=8, frameon=False, ncol=3)
plt.tight_layout(); savefig7(fig, "fig_27_vol_cau_hinh")
cap("Hình", "Vol (%/năm, chỉ mua, NAV ròng) của 5 phương pháp GMV theo năm cấu hình thực thi (số và hạng ở Bảng 41; 1/N không đổi 22,6%, không vẽ).")

fig, axs = plt.subplots(1, 2, figsize=(13, 4), sharey=True)
for a, f in zip(axs, FUNDS):
    for nm in ("EW-RIE*", "VS-NL-LW", "1/N"):
        a.plot(CAPS[(nm, "A chuẩn", f)].index, CAPS[(nm, "A chuẩn", f)]["% NAV bán được trong 5 phiên"], color=col_of(nm), lw=1.4, label=f"{nm} (A)")
    a.plot(CAPS[("EW-RIE*", "C trần 10%", f)].index, CAPS[("EW-RIE*", "C trần 10%", f)]["% NAV bán được trong 5 phiên"], color=COL["EW-RIE*"], ls="--", lw=1.4, label="EW-RIE* (C trần 10%)")
    a.axhline(95, color="#d93025", lw=.8, ls=":"); a.set_title(f"Quỹ {f} đồng", fontsize=10); a.grid(alpha=.3)
axs[0].set_ylabel("% NAV bán được trong 5 phiên (10% ADV20)"); axs[0].legend(fontsize=8, frameon=False, loc="lower right"); plt.tight_layout(); savefig7(fig, "fig_28_thanh_khoan")
cap("Hình", "Thanh khoản danh mục đích qua các kỳ: % NAV bán được trong 5 phiên khi mỗi phiên chỉ bán tối đa 10% ADV20; vạch chấm: ngưỡng 95% (đăng ký trước).")

tau = {c: kendalltau(RK["A chuẩn"], RK[c])[0] for c in CFG4 if c != "A chuẩn"}
sgn = {c: np.sign(VOL4.loc["EW-RIE*", c] - VOL4.loc["VS-NL-LW", c]) for c in CFG4}; same = all(v == sgn["A chuẩn"] for v in sgn.values())
liq = {f: {nm: T42.loc[(f, "A chuẩn", nm), "% NAV bán được trong 5 phiên"] for nm in M7} for f in FUNDS}
md(f"**Kết quả.** Kendall τ của thứ hạng Vol so với A: " + ", ".join(f"{c[0]} {f2(t)}" for c, t in tau.items())
   + f". ΔVol EW-RIE\\* − VS-NL-LW: " + ", ".join(f"{c[0]} {rows[c]['ΔVol EW-RIE* − VS-NL-LW (pp)']}" for c in CFG4)
   + f" pp. Trần 10% làm Vol EW-RIE\\* {f2(VOL4.loc['EW-RIE*', 'A chuẩn'])} → {f2(VOL4.loc['EW-RIE*', 'C trần 10%'])}%; trần turnover 10% → "
   f"{f2(VOL4.loc['EW-RIE*', 'D turnover ≤ 10%'])}%. % NAV bán được trong 5 phiên (TB, cấu hình A): quỹ 100 tỷ "
   + ", ".join(f"{nm} {f2(v, 1)}" for nm, v in liq['100 tỷ'].items()) + "; quỹ 1 000 tỷ " + ", ".join(f"{nm} {f2(v, 1)}" for nm, v in liq['1 000 tỷ'].items()) + ".\n\n"
   f"**Kết luận (theo ngưỡng đăng ký trước).** Thứ hạng {'**giữ**' if (min(tau.values()) >= .6 and same) else '**không giữ hoàn toàn**'} "
   f"(τ nhỏ nhất {f2(min(tau.values()))}; dấu ΔVol EW-RIE\\* − VS-NL-LW {'không đổi' if same else 'đổi'} qua 5 cấu hình). Sức chứa: quỹ 100 tỷ "
   f"{'vừa sức' if liq['100 tỷ']['EW-RIE*'] >= 95 else 'không vừa sức'} với EW-RIE\\*, quỹ 1 000 tỷ {'vừa sức' if liq['1 000 tỷ']['EW-RIE*'] >= 95 else 'không vừa sức'} "
   f"(ngưỡng 95% NAV trong 5 phiên).")

# ---- Đào sâu (mô tả, KHÔNG đăng ký trước): độ lệch của values.csv, nghiêng về mã kém thanh khoản, và trần có thật sự tăng CAGR? ----
REC = {k: v.loc["2024-01-01":, "% NAV bán được trong 5 phiên"].mean() for k, v in CAPS.items()}
LIQR = {nm: np.mean([(TG[nm][s][1][0] * np.arange(1, N7 + 1)).sum() for s in S_REG]) for nm in M7}     # hạng thanh khoản TB theo tỷ trọng (1 = lỏng nhất)
DIF = {c: nw_mean_test(SIM4[("EW-RIE*", c)][0].values - SIM4[("EW-RIE*", "A chuẩn")][0].values) for c in CFG4 if c != "A chuẩn"}
DIFH = dict(zip(DIF, holm([p for _, p in DIF.values()])))
md(f"**Đào sâu (mô tả, không đăng ký trước).** (1) *Độ lệch dữ liệu*: `values.csv` = giá điều chỉnh × khối lượng khớp lệnh nên giá trị giao dịch những năm đầu bị đánh giá thấp "
   f"(ví dụ HPG 2017: giá điều chỉnh ~5 500 đồng so với giá thực vài chục nghìn) và bỏ giao dịch thỏa thuận. Chỉ tính các kỳ từ 2024 (độ lệch nhỏ hơn), % NAV bán được trong 5 phiên của EW-RIE\\* "
   f"là {f2(REC[('EW-RIE*', 'A chuẩn', '100 tỷ')], 1)}% (quỹ 100 tỷ) và {f2(REC[('EW-RIE*', 'A chuẩn', '1 000 tỷ')], 1)}% (1 000 tỷ); trần 10%: {f2(REC[('EW-RIE*', 'C trần 10%', '100 tỷ')], 1)}% / "
   f"{f2(REC[('EW-RIE*', 'C trần 10%', '1 000 tỷ')], 1)}%; 1/N: {f2(REC[('1/N', 'A chuẩn', '100 tỷ')], 1)}% / {f2(REC[('1/N', 'A chuẩn', '1 000 tỷ')], 1)}%. "
   f"(2) *Nghiêng về mã kém thanh khoản*: hạng thanh khoản trung bình theo tỷ trọng trong top-100 (1 = lỏng nhất, 1/N = 50,5): "
   + ", ".join(f"{nm} {f2(v, 1)}" for nm, v in LIQR.items() if nm != "1/N")
   + (" ⇒ GMV nghiêng rõ về nửa kém thanh khoản. " if LIQR["EW-RIE*"] > 60 else " ⇒ GMV chỉ hơi nghiêng về phía kém thanh khoản; sức chứa kém chủ yếu do **độ tập trung** (vài vị thế rất lớn, xem Hình 20), không phải do chọn mã kém thanh khoản. ")
   + f"(3) *Trần có tăng CAGR thật không?* Chênh lợi suất TB ngày (quy %/năm) của EW-RIE\\* so với A: "
   + ", ".join(f"{c[0]} {dv(m * 252 * 100)} (p NW {pv(p)}, Holm {pv(DIFH[c])})" for c, (m, p) in DIF.items())
   + " ⇒ " + (f"giới hạn turnover ({', '.join(c[0] for c in DIF if DIFH[c] < .05)}) cho lợi suất cao hơn **có ý nghĩa sau Holm** — cùng chiều với Hướng 2 (REB dài ⇒ CAGR cao hơn): "
              "điều chỉnh CHẬM về danh mục đích có lợi cho lợi suất. Đây là phát hiện khám phá (không đăng ký trước), cần kiểm lại ngoài mẫu."
              if min(DIFH.values()) < .05 else "chênh lệch lợi suất **chưa có ý nghĩa sau Holm** (10 năm dữ liệu khó tách chênh lệch cỡ vài điểm %)."))
