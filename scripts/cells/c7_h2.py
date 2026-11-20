# ---- 7.2 Hướng 2: tái cân bằng thưa — REB ∈ {21, 63, 126, 252} × vùng không giao dịch ∈ {0, 1%, 2%}; Bảng 37, 38; Hình 21–23 ----
REBS, BANDS = (21, 63, 126, 252), (0.0, 0.01, 0.02)
def sched7(K, phase=0):
    # lịch REB = K: mỗi K/21 kỳ của lịch 21 (cùng tỷ trọng đích); pha p > 0 vẫn mua ban đầu ở kỳ đầu ⇒ mọi lịch cùng mẫu ngày
    st = S_REG[phase::K // 21]; return st if phase == 0 else [S_REG[0]] + st
SIM2 = {(nm, K, b): simulate(TG[nm], sched7(K), "lo", band=b) for nm in M7X for K in REBS for b in BANDS}
PH2 = {(nm, K, p): simulate(TG[nm], sched7(K, p), "lo")[0] for nm in ("EW-RIE*", "VS-NL-LW") for K in REBS for p in range(K // 21)}
pd.to_pickle({"SIM2": {k: v[0] for k, v in SIM2.items()}, "PH2": PH2}, f"{R7}/H2_returns.pkl")
P2 = {k: perf7(*v) for k, v in SIM2.items()}

V37 = pd.DataFrame({(f"REB {K}", c): {nm: P2[(nm, K, 0.0)][c] for nm in M7X} for c in ("Vol %", "CAGR %") for K in REBS})
V37 = V37[[(f"REB {K}", c) for K in REBS for c in ("Vol %", "CAGR %")]]; save7(V37, "H2_vol_cagr")
cap("Bảng", "Tái cân bằng thưa, chỉ mua, không có vùng không giao dịch: Vol (%/năm) và CAGR ròng (%/năm, sau phí mua 0,15% / bán 0,25%) theo chu kỳ "
    "tái cân bằng REB (phiên). Cùng tỷ trọng đích như REB = 21 (lấy mỗi REB/21 kỳ), cùng mẫu ngày; đậm: Vol thấp nhất mỗi cột REB.")
display(V37.style.format(precision=2, decimal=",").highlight_min(subset=[(f"REB {K}", "Vol %") for K in REBS], axis=0, props="font-weight: bold"))

rows = []
for K in REBS:
    for b in BANDS:
        rE, lE = SIM2[("EW-RIE*", K, b)]; rV, lV = SIM2[("VS-NL-LW", K, b)]; dv_, p_hac, p_bt = lw7(rE, rV)
        row = {"REB": K, "Vùng %": int(round(b * 100)), "ΔVol (pp)": dv_, "p LW-boot": p_bt, "ΔCAGR (pp)": P2[("EW-RIE*", K, b)]["CAGR %"] - P2[("VS-NL-LW", K, b)]["CAGR %"],
               "Turnover/năm E %": P2[("EW-RIE*", K, b)]["Turnover/năm %"], "Turnover/năm V %": P2[("VS-NL-LW", K, b)]["Turnover/năm %"],
               "Chi phí E %/năm": P2[("EW-RIE*", K, b)]["Chi phí %/năm"], "Chi phí V %/năm": P2[("VS-NL-LW", K, b)]["Chi phí %/năm"],
               "ΔVol vs HL 10": (rE.std() - SIM2[("VS-NL-LW (HL 10)", K, b)][0].std()) * np.sqrt(252) * 100,
               "ΔVol vs HL 40": (rE.std() - SIM2[("VS-NL-LW (HL 40)", K, b)][0].std()) * np.sqrt(252) * 100}
        if b == 0:
            dph = [(PH2[("EW-RIE*", K, p)].std() - PH2[("VS-NL-LW", K, p)].std()) * np.sqrt(252) * 100 for p in range(K // 21)]
            row.update({"ΔVol TB pha": np.mean(dph), "pha min": np.min(dph), "pha max": np.max(dph)})
        rows.append(row)
T38 = pd.DataFrame(rows); T38.insert(4, "p Holm", holm(T38["p LW-boot"].values)); T38 = T38.set_index(["REB", "Vùng %"]); save7(T38, "H2_cap_E_V")
cap("Bảng", "EW-RIE\\* (E) so với VS-NL-LW (V, HL_VOL = 20) theo REB × vùng không giao dịch (theo từng mã): ΔVol = Vol(E) − Vol(V), pp/năm; "
    "p Ledoit–Wolf (2011) bootstrap khối, Holm trên 12 ô; ΔCAGR ròng; turnover một chiều và chi phí (%/năm) của từng bộ; ΔVol so với VS-NL-LW HL_VOL 10, 40 (mô tả); "
    "ở vùng 0: ΔVol trung bình và khoảng qua mọi pha của lịch (REB = 63: 3 pha, 126: 6, 252: 12).")
display(T38.style.format(precision=2, decimal=",", thousands=" ", na_rep="–").format(pv, subset=[c for c in T38.columns if str(c).startswith("p ")]))

fig, axs = plt.subplots(1, 2, figsize=(12, 4.2))
XR = np.arange(len(REBS))                                  # trục REB dạng hạng mục (21, 63, 126, 252)
for nm in M7:
    for a, c in zip(axs, ("Vol %", "CAGR %")):
        if c == "Vol %" and nm == "1/N": continue               # 1/N ~22%: bỏ khỏi khung Vol để giữ thang (số ở Bảng 37)
        a.plot(XR, [P2[(nm, K, 0.0)][c] for K in REBS], marker="o", ms=5, color=col_of(nm), lw=1.8 if nm in ("EW-RIE*", "VS-NL-LW") else 1.1, label=nm)
for a, c in zip(axs, ("Vol ngoài mẫu, %/năm", "CAGR ròng, %/năm")):
    a.set_xticks(XR); a.set_xticklabels(REBS); a.set_xlabel("REB (phiên)"); a.set_ylabel(c); a.grid(alpha=.3)
axs[1].legend(fontsize=8, frameon=False, ncol=2); plt.tight_layout(); savefig7(fig, "fig_21_reb_vol_cagr")
cap("Hình", "Vol (trái) và CAGR ròng (phải) theo chu kỳ tái cân bằng, 6 phương pháp, chỉ mua, vùng không giao dịch 0 (số ở Bảng 37; khung Vol không vẽ 1/N ≈ 22%).")

D = T38["ΔVol (pp)"].unstack("Vùng %"); Pm = T38["p Holm"].unstack("Vùng %"); vm = max(.3, np.abs(D.values).max())
fig, ax = plt.subplots(figsize=(5.6, 3.8)); im = ax.imshow(D.values, cmap="RdBu_r", vmin=-vm, vmax=vm, aspect="auto")
for i in range(D.shape[0]):
    for j in range(D.shape[1]):
        ax.text(j, i, dv(D.values[i, j]) + ("*" if Pm.values[i, j] < .05 else ""), ha="center", va="center", fontsize=9,
                color="white" if abs(D.values[i, j]) > .55 * vm else "#202124")
ax.set_xticks(range(D.shape[1])); ax.set_xticklabels([f"{f2(c, 0)}%" for c in D.columns]); ax.set_yticks(range(D.shape[0])); ax.set_yticklabels(D.index)
ax.set_xlabel("Vùng không giao dịch"); ax.set_ylabel("REB (phiên)"); fig.colorbar(im, ax=ax, label="ΔVol EW-RIE* − VS-NL-LW, pp"); plt.tight_layout()
savefig7(fig, "fig_22_heat_reb_vung")
cap("Hình", "ΔVol EW-RIE\\* − VS-NL-LW (pp/năm) theo REB × vùng không giao dịch, chỉ mua; xanh: EW-RIE\\* rủi ro thấp hơn; * = p Holm < 0,05 (12 ô).")

fig, axs = plt.subplots(1, len(BANDS), figsize=(13, 3.8), sharey=True)
for a, b in zip(axs, BANDS):
    for nm in M7:
        a.plot(XR, [P2[(nm, K, b)]["Chi phí %/năm"] for K in REBS], marker="o", ms=5, color=col_of(nm), lw=1.8 if nm in ("EW-RIE*", "VS-NL-LW") else 1.1, label=nm)
    a.set_xticks(XR); a.set_xticklabels(REBS); a.set_title(f"Vùng không giao dịch {f2(100 * b, 0)}%", fontsize=10)
    a.set_xlabel("REB (phiên)"); a.grid(alpha=.3)
axs[0].set_ylabel("Chi phí giao dịch, %/năm"); axs[0].legend(fontsize=8, frameon=False); plt.tight_layout(); savefig7(fig, "fig_23_chi_phi")
cap("Hình", "Chi phí giao dịch thực tế (%/năm NAV, phí mua 0,15% / bán 0,25%) theo REB, ba mức vùng không giao dịch, chỉ mua.")

d0 = T38.xs(0, level="Vùng %")["ΔVol (pp)"]; ph = T38.xs(0, level="Vùng %")["ΔVol TB pha"]
mono = bool(np.all(np.diff(d0.values) < 0)); drop = d0.loc[252] - d0.loc[21]; mono_ph = bool(ph.loc[252] - ph.loc[21] < 0)        # (iii) trung bình theo pha cùng chiều giảm
strong = bool(((T38.reset_index()["REB"] >= 126) & (T38.reset_index()["ΔVol (pp)"] < 0) & (T38.reset_index()["p Holm"] < .05)).any())
H2V = ("bác bỏ" if drop >= 0 else ("ủng hộ mạnh" if (mono and drop <= -.10 and mono_ph and strong) else ("ủng hộ" if (mono and drop <= -.10 and mono_ph) else "không kết luận")))
cheap = {nm: P2[(nm, 252, 0.0)]["Chi phí %/năm"] for nm in M7}
md(f"**Kết quả.** Ở vùng 0, ΔVol EW-RIE\\* − VS-NL-LW theo REB 21/63/126/252: {' / '.join(dv(x) for x in d0.values)} pp "
   f"(trung bình theo pha: {' / '.join(dv(x) for x in ph.values)} pp; khoảng pha ở REB 252: [{dv(T38.loc[(252, 0), 'pha min'])}; {dv(T38.loc[(252, 0), 'pha max'])}]). "
   f"Số ô p Holm < 0,05: {int((T38['p Holm'] < .05).sum())}/12. Vol của EW-RIE\\* tăng từ {f2(P2[('EW-RIE*', 21, 0.0)]['Vol %'])}% (REB 21) lên "
   f"{f2(P2[('EW-RIE*', 252, 0.0)]['Vol %'])}% (REB 252); chi phí giảm từ {f2(P2[('EW-RIE*', 21, 0.0)]['Chi phí %/năm'])} xuống "
   f"{f2(P2[('EW-RIE*', 252, 0.0)]['Chi phí %/năm'])} %/năm. Vùng 2% ở REB 21 cắt chi phí EW-RIE\\* còn {f2(P2[('EW-RIE*', 21, 0.02)]['Chi phí %/năm'])} %/năm "
   f"với Vol {f2(P2[('EW-RIE*', 21, 0.02)]['Vol %'])}%.\n\n"
   f"**Kết luận (theo ngưỡng đăng ký trước).** Giả thuyết \"REB càng dài EW-RIE\\* càng có lợi so với VS-NL-LW\": **{H2V}** "
   f"(giảm đơn điệu: {'có' if mono else 'không'}; ΔVol(252) − ΔVol(21) = {dv(drop)} pp; theo pha cùng chiều: {'có' if mono_ph else 'không'}; "
   f"ô REB ≥ 126 có ý nghĩa: {'có' if strong else 'không'}).")

# ---- Đào sâu (mô tả, KHÔNG đăng ký trước): pha của lịch, VS half-life dài hơn, và vai trò của chính EW-RIE* ----
PHT = []
for K in (63, 126, 252):
    for p in range(K // 21):
        rE, rV = PH2[("EW-RIE*", K, p)], PH2[("VS-NL-LW", K, p)]; d_, _, pb = lw7(rE, rV)
        PHT.append({"REB": K, "pha": p, "ΔVol (pp)": d_, "p LW-boot": pb, "CAGR E %": perf7(rE)["CAGR %"], "CAGR V %": perf7(rV)["CAGR %"]})
PHT = pd.DataFrame(PHT); save7(PHT, "H2_pha")
g = PHT.groupby("REB"); sig = g.apply(lambda d: f"{int(((d['ΔVol (pp)'] < 0) & (d['p LW-boot'] < .05)).sum())}/{len(d)}")
cg = g[["CAGR E %", "CAGR V %"]].agg(["mean", "min", "max"])
H40 = {K: lw7(SIM2[("EW-RIE*", K, 0.0)][0], SIM2[("VS-NL-LW (HL 40)", K, 0.0)][0]) for K in (126, 252)}
md(f"**Đào sâu (mô tả, không đăng ký trước).** (1) *Pha của lịch*: số pha có ΔVol < 0 với p < 0,05 (chưa Holm) ở REB 63/126/252: {' / '.join(sig.values)}. "
   f"CAGR trung bình theo pha của EW-RIE\\*: {f2(P2[('EW-RIE*', 21, 0.0)]['CAGR %'])} (REB 21) / " + " / ".join(f2(cg.loc[K, ('CAGR E %', 'mean')]) for K in (63, 126, 252))
   + f" %/năm; ở REB 252 dao động [{f2(cg.loc[252, ('CAGR E %', 'min')])}; {f2(cg.loc[252, ('CAGR E %', 'max')])}] ⇒ pha 0 ({f2(P2[('EW-RIE*', 252, 0.0)]['CAGR %'])}%) là pha may; "
   f"chiều \"REB dài ⇒ CAGR cao hơn\" vẫn đúng ở trung bình theo pha nhưng độ lớn phụ thuộc mạnh vào ngày tái cân bằng. "
   f"(2) *VS với half-life dài hơn*: so với VS-NL-LW HL_VOL 40, ΔVol của EW-RIE\\* ở REB 126/252 chỉ còn {dv(H40[126][0])} (p {pv(H40[126][2])}) / {dv(H40[252][0])} (p {pv(H40[252][2])}) pp "
   f"— một phần lợi thế đến từ việc HL_VOL = 20 quá ngắn cho kỳ nắm giữ dài. (3) *Không riêng EW-RIE\\**: ở REB 252, NL-LW (cửa sổ phẳng) Vol {f2(P2[('NL-LW', 252, 0.0)]['Vol %'])}%, "
   f"EW-NL-LW {f2(P2[('EW-NL-LW', 252, 0.0)]['Vol %'])}%, EW-WeSpeR {f2(P2[('EW-WeSpeR', 252, 0.0)]['Vol %'])}% ≈ EW-RIE\\* {f2(P2[('EW-RIE*', 252, 0.0)]['Vol %'])}% "
   f"⇒ điều quan sát được là **VS (chuẩn hóa theo biến động ngắn hạn) yếu đi khi nắm giữ dài**, không phải EW-RIE\\* mạnh lên.")
