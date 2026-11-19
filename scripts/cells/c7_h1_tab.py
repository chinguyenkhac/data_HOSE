# ---- 7.1 Hướng 1: NAV có trôi tỷ trọng, phí mua 0,15% / bán 0,25% (REB = 21, chỉ mua) — Bảng 35, 36 ----
TG = {nm: targets7(nm) for nm in M7X}                                   # tỷ trọng đích (cache results_v7/cache/tgt_*.pkl)
SIM1 = {nm: simulate(TG[nm], S_REG, "lo") for nm in M7X}
R1 = {nm: v[0] for nm, v in SIM1.items()}
R1_SO = {nm: simulate(TG[nm], S_REG, "so")[0] for nm in M7X if nm != "1/N"}          # bán khống: chỉ tham khảo

def _eq(names): return np.array([TICK7.get_loc(t) for t in names]), np.full(len(names), 1 / len(names))
def group_targets():
    # mỗi kỳ: Thị trường EW = mọi mã đủ điều kiện (cùng bộ lọc universe, không cắt top-N); Q1/Q5 = 1/5 mã có Vol 250 phiên
    # quá khứ thấp/cao nhất (mọi mã đủ điều kiện); bản phụ trong top-100. Nhóm đều, giữ 21 phiên có trôi.
    G = {k: {} for k in ("mk", "q1", "q5", "q1t", "q5t")}; nel = []
    for s in S_REG:
        win, ok = eligible(s); el = win.columns[ok]; vol = win[el].std().sort_values(); k = len(vol) // 5; nel.append(len(el))
        G["mk"][s], G["q1"][s], G["q5"][s] = _eq(el), _eq(vol.index[:k]), _eq(vol.index[-k:])
        vt = win[universe(s)[0]].std().sort_values(); kt = len(vt) // 5
        G["q1t"][s], G["q5t"][s] = _eq(vt.index[:kt]), _eq(vt.index[-kt:])
    return G, nel
GT, NEL = group_targets()
RG = {k: simulate(v, S_REG, None, cost=False)[0] for k, v in GT.items()}           # chỉ số/nhóm: không phí
RG["1/N gộp"] = simulate(TG["1/N"], S_REG, "lo", cost=False)[0]
R_SAV = pd.Series((1 + RF_SAV) ** (1 / 252) - 1, index=R1["EW-RIE*"].index)
pd.DataFrame({**R1, **{f"{k} (bán khống)": v for k, v in R1_SO.items()}, **RG, "Tiết kiệm 5%": R_SAV}).to_pickle(f"{R7}/H1_returns.pkl")

LAB = {"mk": "Thị trường EW", "q1": "Q1 ít biến động", "q5": "Q5 biến động cao"}
rows = {nm: {**perf7(R1[nm], SIM1[nm][1]), "Vol bán khống % (tham khảo)": R1_SO[nm].std() * np.sqrt(252) * 100 if nm in R1_SO else np.nan}
        for nm in M7X}
LAB["q1t"] = "Q1 ít biến động (top-100)"
rows.update({LAB[k]: perf7(RG[k]) for k in ("mk", "q1", "q5", "q1t")}); rows["Tiết kiệm 5%"] = perf7(R_SAV)
T35 = pd.DataFrame(rows).T
for c in ("Hồi phục (phiên)", "Dưới đỉnh dài nhất (phiên)"): T35[c.replace("phiên", "tháng")] = T35.pop(c) / 21
T35 = T35[["CAGR %", "Vol %", "MDD %", "Hồi phục (tháng)", "Dưới đỉnh dài nhất (tháng)", "CVaR 5% tháng %", "Calmar",
           "Turnover/năm %", "Chi phí %/năm", "Vol bán khống % (tham khảo)"]]
T35.loc["Tiết kiệm 5%", ["Vol %", "MDD %", "Hồi phục (tháng)", "Dưới đỉnh dài nhất (tháng)", "CVaR 5% tháng %", "Calmar"]] = np.nan; save7(T35, "H1_tang_truong")
yrs = len(R_SAV) / 252
cap("Bảng", f"Tăng trưởng tài sản 1 đồng, {R_SAV.index[0]:%m/%Y}–{R_SAV.index[-1]:%m/%Y} ({f2(yrs, 1)} năm, {len(R_SAV)} phiên), chỉ mua, "
    "REB = 21, tỷ trọng trôi giữa kỳ, phí mua 0,15% / bán 0,25% (gồm thuế 0,1%). CAGR, MDD, CVaR (TB 5% tháng xấu nhất) tính trên NAV ròng; "
    "Hồi phục = từ đáy đợt sụt lớn nhất tới khi vượt đỉnh cũ (– = chưa hồi phục). Thị trường EW (thay VN-Index), Q1/Q5 (1/5 mã Vol quá khứ thấp/cao nhất, "
    "mọi mã đủ điều kiện; bản phụ: trong top-100): không phí. Tiết kiệm 5%/năm là giả định. Cột cuối: bán khống, chỉ tham khảo.")
show(T35)

# ---- giá trị kinh tế của việc chuyển sang EW-RIE* (Fleming–Kirby–Ostdiek 2001) ----
OTH = ["VS-NL-LW", "VS-NL-LW (HL 10)", "VS-NL-LW (HL 40)", "NL-LW", "EW-NL-LW", "EW-WeSpeR", "1/N"]; GAM = (1, 5, 10)
rE = R1["EW-RIE*"].values; rows = []
for nm in OTH:
    rX = R1[nm].values; dv_, p_hac, p_bt = lw7(rE, rX)
    rows.append({"Chuyển từ": nm, "ΔVol (pp)": dv_, "p LW-boot": p_bt, "ΔCAGR (pp)": T35.loc["EW-RIE*", "CAGR %"] - T35.loc[nm, "CAGR %"],
                 **{f"γ = {g}": fko_fee(rX, rE, g) for g in GAM}, **{f"γ = {g} (cùng TB)": fko_fee(rX, rE, g, True) for g in GAM}})
T36 = pd.DataFrame(rows).set_index("Chuyển từ"); T36.insert(2, "p Holm", holm(T36["p LW-boot"].values)); save7(T36, "H1_phi_FKO")

def fko_ci(ra, rb, gamma, equal_mean, block=21, B=2000, seed=0):
    # CI 95% bootstrap khối vòng (ghép cặp) cho phí FKO
    rng = np.random.default_rng(seed); T = len(ra); l = T // block; out = np.empty(B)
    for i in range(B):
        ix = ((rng.integers(0, T, l)[:, None] + np.arange(block)) % T).ravel(); out[i] = fko_fee(ra[ix], rb[ix], gamma, equal_mean)
    return np.percentile(out, [2.5, 97.5])
CI36 = {em: fko_ci(R1["VS-NL-LW"].values, rE, 5, em) for em in (False, True)}
cap("Bảng", "Giá trị kinh tế của việc chuyển từ phương pháp ở hàng sang EW-RIE\\* (chỉ mua, NAV ròng như Bảng 35): ΔVol = Vol(EW-RIE\\*) − Vol(hàng), "
    "pp/năm (< 0: EW-RIE\\* rủi ro thấp hơn), p kiểm định Ledoit–Wolf (2011) bootstrap khối, Holm trên 7 hàng; phí Fleming–Kirby–Ostdiek (bps/năm) "
    "mà nhà đầu tư hệ số ngại rủi ro γ sẵn lòng trả để chuyển (> 0: EW-RIE\\* tốt hơn). \"Cùng TB\": coi lợi suất kỳ vọng như nhau, chỉ còn khác biệt rủi ro.")
show(T36)
md(f"CI 95% bootstrap khối (b = 21, B = 2 000) của phí chuyển VS-NL-LW → EW-RIE\\*, γ = 5: lợi suất thực [{f2(CI36[False][0], 1)}; {f2(CI36[False][1], 1)}] bps/năm; "
   f"cùng TB [{f2(CI36[True][0], 1)}; {f2(CI36[True][1], 1)}] bps/năm.")
