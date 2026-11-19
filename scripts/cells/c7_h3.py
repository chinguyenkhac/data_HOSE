# ---- 7.3 Hướng 3: khủng hoảng — nghiên cứu sự kiện (COVID 2020, 2022, thuế quan 4/2025) và "cầu chì"; Bảng 39, 40; Hình 24–26 ----
# Thị trường EW trên toàn lưới 21 phiên (từ phiên W + 1) để có lịch sử cho EWMA và trung vị 250 phiên trước mẫu ngoài mẫu
GRID = [s for s in range(W7 + 1, END7, 21) if eligible(s)[1].sum() >= 20]
MK_FULL = simulate({s: _eq(eligible(s)[0].columns[eligible(s)[1]]) for s in GRID}, GRID, None, cost=False)[0]
assert np.allclose(MK_FULL.loc[RG["mk"].index].values, RG["mk"].values)          # trùng Thị trường EW của Hướng 1 trên mẫu chung
mkn = (1 + MK_FULL).cumprod()

EVW = {"COVID 2020": ("2020-01-01", "2020-06-30"), "Năm 2022": ("2022-01-01", "2022-12-31"), "Thuế quan 4/2025": ("2025-03-15", "2025-06-30")}
EV = {}
for k, (a, b) in EVW.items():
    seg = mkn.loc[a:b]; tr = seg.idxmin(); pk = seg.loc[:tr].idxmax(); EV[k] = (pk, tr)
navs = {nm: (1 + R1[nm]).cumprod() for nm in M7}; navs["Thị trường EW"] = mkn.loc[R1["EW-RIE*"].index[0]:] / mkn.loc[R1["EW-RIE*"].index[0]]
def ev_stats(nav, r, pk, tr, tg=None):
    i_pk, i_tr = DATES7.get_loc(pk), DATES7.get_loc(tr); w = nav.loc[pk:DATES7[i_tr + 20]]
    rec = nav.loc[tr:][nav.loc[tr:] >= nav.loc[pk]]
    out = {"Mức sụt %": (w.min() / nav.loc[pk] - 1) * 100, "Hồi phục (phiên)": (DATES7.get_loc(rec.index[0]) - i_tr) if len(rec) else np.nan,
           "Vol 21 phiên lớn nhất %": (r.rolling(21).std() * np.sqrt(252) * 100).loc[pk:DATES7[i_tr + 20]].max()}
    if tg is not None:
        sb = max(s for s in S_REG if s <= i_pk); sa = min(s for s in S_REG if s >= i_tr)
        wb, wa = np.zeros(len(TICK7)), np.zeros(len(TICK7)); wb[tg[sb][0]] = tg[sb][1][0]; wa[tg[sa][0]] = tg[sa][1][0]
        out["Δ tỷ trọng %"] = 50 * np.abs(wa - wb).sum()
    return out
rows = []
for k, (pk, tr) in EV.items():
    for nm in M7 + ["Thị trường EW"]:
        r = R1[nm] if nm in R1 else MK_FULL.loc[R1["EW-RIE*"].index]
        rows.append({"Sự kiện": f"{k} ({pk:%d/%m/%y}→{tr:%d/%m/%y})", "Phương pháp": nm, **ev_stats(navs[nm], r, pk, tr, TG.get(nm))})
T39 = pd.DataFrame(rows).set_index(["Sự kiện", "Phương pháp"]); save7(T39, "H3_su_kien")
cap("Bảng", "Ba đợt khủng hoảng (đỉnh → đáy của Thị trường EW, xác định từ dữ liệu theo quy tắc đăng ký trước), chỉ mua, NAV ròng, REB = 21: "
    "mức sụt = NAV thấp nhất trong [đỉnh, đáy + 20 phiên] so với NAV tại đỉnh; hồi phục = số phiên từ đáy thị trường tới khi NAV vượt NAV tại đỉnh "
    "(– = chưa); Vol 21 phiên lớn nhất (%/năm) trong cùng khoảng; Δ tỷ trọng = ½Σ|w(kỳ đầu sau đáy) − w(kỳ cuối trước đỉnh)| (%).")
show(T39)

# ---- cầu chì: σ EWMA (hl = 10) của Thị trường EW > 1,5 × trung vị 250 phiên trước ⇒ tái cân bằng thêm ở phiên kế tiếp ----
lam = .5 ** (1 / 10); rm = MK_FULL.values; s2 = np.empty(len(rm)); s2[0] = rm[:10].var()
for t in range(1, len(rm)): s2[t] = lam * s2[t - 1] + (1 - lam) * rm[t] ** 2          # σ²_t gồm lợi suất ngày t (biết lúc đóng cửa t)
s2 = pd.Series(s2, index=MK_FULL.index)
SIG = np.sqrt(s2 * 252) * 100; THR = 1.5 * SIG.shift(1).rolling(250).median()
above = SIG > THR; cross = above & ~above.shift(1, fill_value=False) & THR.notna()
FUSE = []
for d in cross[cross].index:
    s = DATES7.get_loc(d) + 1
    if S_REG[0] < s < END7 and min(abs(s - x) for x in S_REG) > 5: FUSE.append(s)
FUSE_SKIP = sum(S_REG[0] < DATES7.get_loc(d) + 1 < END7 for d in cross[cross].index) - len(FUSE)
TGF = {nm: targets7(nm, extra=FUSE) for nm in M7X}
SIM3 = {nm: simulate(TGF[nm], sorted(S_REG + FUSE), "lo") for nm in M7X}
rows = []
for nm in M7X:
    r0, r1 = R1[nm], SIM3[nm][0]; a0, a1 = perf7(r0, SIM1[nm][1]), perf7(r1, SIM3[nm][1]); dv_, p_hac, p_bt = lw7(r1, r0)
    rows.append({"Phương pháp": nm, "Vol không %": a0["Vol %"], "Vol có %": a1["Vol %"], "ΔVol (pp)": dv_, "p LW-boot": p_bt,
                 "CAGR không %": a0["CAGR %"], "CAGR có %": a1["CAGR %"], "MDD không %": a0["MDD %"], "MDD có %": a1["MDD %"],
                 "Chi phí không %/năm": a0["Chi phí %/năm"], "Chi phí có %/năm": a1["Chi phí %/năm"]})
T40 = pd.DataFrame(rows).set_index("Phương pháp"); T40.insert(4, "p Holm", holm(T40["p LW-boot"].values)); save7(T40, "H3_cau_chi")
dEVf, _, pEVf = lw7(SIM3["EW-RIE*"][0], SIM3["VS-NL-LW"][0])
cap("Bảng", f"Cầu chì định trước: σ EWMA (hl = 10) của Thị trường EW vượt 1,5 × trung vị 250 phiên trước ⇒ tái cân bằng thêm ở phiên kế tiếp "
    f"(bỏ nếu cách kỳ đều ≤ 5 phiên): {len(FUSE)} lần kích hoạt trong mẫu (bỏ {FUSE_SKIP} lần gần kỳ đều). Chỉ mua, NAV ròng; ΔVol = Vol(có) − Vol(không), "
    "p Ledoit–Wolf (2011) bootstrap khối, Holm trên 8 phương pháp.")
show(T40)

C3 = {"EW-RIE*": COL["EW-RIE*"], "VS-NL-LW": COL["VS-NL-LW"], "NL-LW": COL["NL-LW"], "Thị trường EW": COL["Thị trường EW"]}
fig, axs = plt.subplots(2, 3, figsize=(14, 7.2))
for j, (k, (pk, tr)) in enumerate(EV.items()):
    i0, i1 = DATES7.get_loc(pk) - 21, min(DATES7.get_loc(tr) + 126, END7 - 1); d0, d1 = DATES7[i0], DATES7[i1]
    for nm, c in C3.items():
        nv = navs[nm].loc[d0:d1]; ls = "--" if nm == "Thị trường EW" else "-"
        axs[0, j].plot(nv.index, nv.values / navs[nm].loc[pk], color=c, ls=ls, lw=1.6, label=nm)
        r = R1[nm] if nm in R1 else MK_FULL
        axs[1, j].plot(nv.index, (r.rolling(21).std() * np.sqrt(252) * 100).loc[d0:d1], color=c, ls=ls, lw=1.4, label=nm)
    for a in axs[:, j]:
        a.axvline(pk, color="#9aa0a6", lw=.8); a.axvline(tr, color="#9aa0a6", lw=.8, ls=":"); a.grid(alpha=.3); a.tick_params(axis="x", labelsize=8, rotation=30)
    axs[0, j].set_title(f"{k}: đỉnh {pk:%d/%m/%y}, đáy {tr:%d/%m/%y}", fontsize=10)
axs[0, 0].set_ylabel("NAV / NAV tại đỉnh"); axs[1, 0].set_ylabel("Vol trượt 21 phiên, %/năm"); axs[0, 0].legend(fontsize=8, frameon=False)
plt.tight_layout(); savefig7(fig, "fig_24_su_kien")
cap("Hình", "Ba đợt khủng hoảng: NAV chuẩn hóa tại đỉnh (trên) và Vol trượt 21 phiên (dưới) của EW-RIE\\*, VS-NL-LW, NL-LW và Thị trường EW "
    "(từ 21 phiên trước đỉnh tới 126 phiên sau đáy; vạch liền: đỉnh, vạch chấm: đáy).")

TOP = ["EW-RIE*", "VS-NL-LW"]; fig, ax = plt.subplots(figsize=(12, 4.6))
for nm in TOP:
    w = pd.Series({DATES7[s]: 1 / (TG[nm][s][1][0] ** 2).sum() for s in S_REG}); ax.step(w.index, w.values, where="post", color=col_of(nm), lw=1.6, label=f"{nm}: N hiệu dụng")
for k, (pk, tr) in EV.items(): ax.axvspan(pk, tr, color="#f1f3f4", zorder=0); ax.text(pk, .98, k, transform=ax.get_xaxis_transform(), fontsize=8, va="top")
ax.set_ylabel("Số mã hiệu dụng 1/Σw² (tỷ trọng đích)"); ax.grid(alpha=.3); ax.legend(fontsize=8, frameon=False, loc="upper right")
plt.tight_layout(); savefig7(fig, "fig_25_neff")
cap("Hình", "Độ tập trung danh mục đích chỉ mua (số mã hiệu dụng 1/Σw²) của EW-RIE\\* và VS-NL-LW qua các kỳ; nền xám: ba đợt khủng hoảng (đỉnh → đáy).")

fig, ax = plt.subplots(figsize=(12, 3.8)); oos = SIG.loc[R1["EW-RIE*"].index[0]:]
ax.plot(oos.index, oos.values, color=COL["Thị trường EW"], lw=1.1, label="σ EWMA hl = 10 (Thị trường EW), %/năm")
ax.plot(oos.index, THR.loc[oos.index].values, color="#d93025", lw=1.1, ls="--", label="ngưỡng 1,5 × trung vị 250 phiên")
ax.plot(DATES7[[s - 1 for s in FUSE]], SIG.loc[DATES7[[s - 1 for s in FUSE]]].values, "v", color="#d93025", ms=8, label=f"kích hoạt ({len(FUSE)} lần)")
ax.set_ylabel("%/năm"); ax.grid(alpha=.3); ax.legend(fontsize=8, frameon=False, loc="upper left"); plt.tight_layout(); savefig7(fig, "fig_26_cau_chi")
cap("Hình", "Cầu chì: biến động EWMA (hl = 10) của Thị trường EW, ngưỡng 1,5 × trung vị 250 phiên trước, và các lần kích hoạt trong mẫu ngoài mẫu.")

dd = {k: (T39.loc[(kk, "EW-RIE*"), "Mức sụt %"], T39.loc[(kk, "VS-NL-LW"), "Mức sụt %"]) for k in EV for kk in T39.index.levels[0] if kk.startswith(k)}
n_less = sum(e > v for e, v in dd.values())                                    # sụt ít hơn = mức sụt (âm) lớn hơn
fE = T40.loc["EW-RIE*"]; H3B = (fE["ΔVol (pp)"] <= -.10 and fE["p LW-boot"] < .05) or (fE["MDD có %"] - fE["MDD không %"] >= 2)
md("**Kết quả.** Mức sụt EW-RIE\\* / VS-NL-LW / Thị trường EW: " + "; ".join(
       f"{k} {f2(dd[k][0], 1)} / {f2(dd[k][1], 1)} / {f2(T39.loc[(kk, 'Thị trường EW'), 'Mức sụt %'], 1)}%" for k in EV for kk in T39.index.levels[0] if kk.startswith(k))
   + f". Cầu chì kích hoạt {len(FUSE)} lần; với EW-RIE\\*: ΔVol {dv(fE['ΔVol (pp)'])} pp (p {pv(fE['p LW-boot'])}), MDD {f2(fE['MDD không %'], 1)} → {f2(fE['MDD có %'], 1)}%, "
   f"chi phí {f2(fE['Chi phí không %/năm'])} → {f2(fE['Chi phí có %/năm'])} %/năm. Có cầu chì, ΔVol EW-RIE\\* − VS-NL-LW = {dv(dEVf)} pp (p {pv(pEVf)}).\n\n"
   f"**Kết luận (theo ngưỡng đăng ký trước).** H3a (EW-RIE\\* sụt ít hơn VS-NL-LW ở ≥ 2/3 sự kiện): **{'đạt' if n_less >= 2 else 'không đạt'}** ({n_less}/3; chỉ mô tả, 3 sự kiện). "
   f"H3b (cầu chì có lợi cho EW-RIE\\*): **{'đạt' if H3B else 'không đạt'}**.")

# ---- Đào sâu (mô tả, KHÔNG đăng ký trước): phép thử giả dược — tái cân bằng thêm vào 11 ngày NGẪU NHIÊN (cùng quy tắc cách kỳ đều > 5 phiên) ----
def lo_at(nm, days):
    # tỷ trọng chỉ mua tại các phiên bất kỳ (cache riêng, chỉ lời giải chỉ mua)
    f = f"{C7}/placebo_{re.sub(r'[^A-Za-z0-9]+', '_', nm)}.pkl"; D = pd.read_pickle(f) if os.path.exists(f) else {}
    todo = [s for s in days if s not in D]
    if todo:
        est = est7(nm)
        for s in todo:
            tick, X = universe(s); D[s] = (np.array([TICK7.get_loc(t) for t in tick]), gmv_long_only(est(X))[None, :])
        pd.to_pickle(D, f)
    return D
rng = np.random.default_rng(SEED); CAND = [s for s in range(S_REG[0] + 1, END7) if min(abs(s - x) for x in S_REG) > 5]
PLA = [sorted(rng.choice(CAND, len(FUSE), replace=False).tolist()) for _ in range(30)]
rows = []
for nm in ("EW-RIE*", "VS-NL-LW"):
    D = lo_at(nm, sorted({s for st in PLA for s in st})); b0 = perf7(R1[nm])
    for i, st in enumerate(PLA):
        tg = {**TG[nm], **{s: D[s] for s in st}}; a = perf7(simulate(tg, sorted(S_REG + st), "lo")[0])
        rows.append({"pp": nm, "bộ": i, "ΔMDD (pp)": a["MDD %"] - b0["MDD %"], "ΔVol (pp)": a["Vol %"] - b0["Vol %"], "ΔCAGR (pp)": a["CAGR %"] - b0["CAGR %"]})
PLT = pd.DataFrame(rows); save7(PLT, "H3_gia_duoc")
fz = {nm: (T40.loc[nm, "MDD có %"] - T40.loc[nm, "MDD không %"], T40.loc[nm, "ΔVol (pp)"], T40.loc[nm, "CAGR có %"] - T40.loc[nm, "CAGR không %"]) for nm in ("EW-RIE*", "VS-NL-LW")}
skip_ev = [f"{d:%d/%m/%y}" for d in cross[cross].index if (DATES7.get_loc(d) + 1) not in FUSE and any(pk - pd.Timedelta(days=30) <= d <= tr for pk, tr in EV.values())]
def _pl(nm):
    q = PLT[PLT.pp == nm]; m, v, c = fz[nm]
    return (f"{nm}: cầu chì ΔMDD {dv(m)}, ΔVol {dv(v)}, ΔCAGR {dv(c)} pp; giả dược ΔMDD TB {dv(q['ΔMDD (pp)'].mean())} pp "
            f"(≥ mức của cầu chì ở {int((q['ΔMDD (pp)'] >= m).sum())}/30 bộ), ΔVol TB {dv(q['ΔVol (pp)'].mean())}, ΔCAGR TB {dv(q['ΔCAGR (pp)'].mean())} pp")
md(f"**Đào sâu (mô tả, không đăng ký trước).** Giả dược: 30 bộ, mỗi bộ {len(FUSE)} phiên chọn ngẫu nhiên (cách kỳ đều > 5 phiên) để tái cân bằng thêm. {_pl('EW-RIE*')}. {_pl('VS-NL-LW')}. "
   f"Lần cắt ngưỡng bị bỏ vì sát kỳ đều nằm trong các đợt khủng hoảng: {', '.join(skip_ev) if skip_ev else 'không có'} — tức ở các cú sốc lớn, lịch 21 phiên đã tự tái cân bằng gần như cùng lúc. "
   + (f"Giả dược hiếm khi đạt mức cải thiện MDD của cầu chì (p hoán vị ≈ {f2((int((PLT[PLT.pp == 'EW-RIE*']['ΔMDD (pp)'] >= fz['EW-RIE*'][0]).sum()) + 1) / 31, 2)} cho EW-RIE\\*) "
      "⇒ thời điểm cầu chì chọn có vai trò, không chỉ do tái cân bằng nhiều hơn. Nhưng MDD là MỘT đợt sụt (" + f"{sum(DATES7[s].year == 2022 for s in FUSE)}/{len(FUSE)} lần kích hoạt rơi vào 2022"
      + ") nên đây là bằng chứng yếu, cần kiểm trên thị trường/giai đoạn khác."
      if (PLT[PLT.pp == "EW-RIE*"]["ΔMDD (pp)"] >= fz["EW-RIE*"][0]).mean() <= .1 else
      "Giả dược cải thiện MDD tương đương cầu chì ⇒ lợi ích đến từ việc tái cân bằng nhiều hơn, không phải từ thời điểm cầu chì chọn."))
