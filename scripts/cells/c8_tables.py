# ---- 8.1 Tầng 1: quét từng siêu tham số — Bảng A (Vol) và heatmap 11 cặp; kiểm định chung mỗi lần quét ----
T8 = pd.read_csv(f"{R8}/tests_raw.csv") if os.path.exists(f"{R8}/tests_raw.csv") else None
assert T8 is not None, "chạy scripts/run8.py trước (cache lưới ở results_v8)"
T8["p Holm"] = np.nan
for (tier, sw, lab, m), d in T8.groupby(["tier", "sweep", "label", "mode"]):     # Holm trên các cặp trong mỗi cột (tầng 1: 11 cặp)
    if tier == "T1": T8.loc[d.index, "p Holm"] = holm(d["p_bt"].values)
for (tier, sw, pk, m), d in T8[T8.tier != "T1"].groupby(["tier", "sweep", "pair", "mode"]):   # tầng 2, 3: Holm trên các ô của lưới, mỗi cặp
    T8.loc[d.index, "p Holm"] = holm(d["p_bt"].values)
save8(T8, "kiem_dinh_tat_ca")

def vol_table8(sw, m):
    # Vol (%/năm) của 8 bộ theo các cột của lần quét (đọc lợi suất đã cache)
    cols = SWEEP8[sw]; return pd.DataFrame({lab: {nm: returns8(nm, c, reb)[m][0].std() * np.sqrt(252) * 100 for nm in M8} for lab, c, reb in cols})

def joint8(sw, pk, m, M=2000, block=21, seed=0):
    # kiểm định chung trên một lần quét: TB ΔVol qua các cột và max|t|; bootstrap khối vòng dùng CÙNG chỉ số ngày (phần ngày chung)
    a, b = next((x, y) for k, x, y in PAIRS8 if k == pk); cols = SWEEP8[sw]
    R = [(returns8(a, c, reb)[m][0], returns8(b, c, reb)[m][0]) for _, c, reb in cols]
    idx = R[0][0].index
    for ra, _ in R[1:]: idx = idx.intersection(ra.index)
    A = np.column_stack([ra.loc[idx].values for ra, _ in R]); B = np.column_stack([rb.loc[idx].values for _, rb in R])
    d0 = (A.std(0) - B.std(0)) * np.sqrt(252) * 100; rng = np.random.default_rng(seed); T = len(idx); l = T // block; bs = np.empty((M, len(cols)))
    for i in range(M):
        ix = ((rng.integers(0, T, l)[:, None] + np.arange(block)) % T).ravel(); bs[i] = (A[ix].std(0) - B[ix].std(0)) * np.sqrt(252) * 100
    se = bs.std(0); mean_p = (np.sum(np.abs(bs.mean(1) - d0.mean()) >= abs(d0.mean())) + 1) / (M + 1)
    tmax = np.abs(d0 / se).max(); max_p = (np.sum(np.abs((bs - d0) / se).max(1) >= tmax) + 1) / (M + 1)
    return dict(sweep=sw, pair=pk, mode=MODES8[m], n_ngay=T, dvol_TB=d0.mean(), p_TB=mean_p, t_max=tmax, p_max=max_p,
                am=int((d0 < 0).sum()), duong=int((d0 > 0).sum()))

def heat8(sw):
    # heatmap 11 cặp × cột của lần quét, hai chế độ; * = p Holm < 0,05 (Holm trên 11 cặp trong cột)
    d = T8[(T8.tier == "T1") & (T8.sweep == sw)]; labs = [str(l) for l, _, _ in SWEEP8[sw]]
    fig, axs = plt.subplots(1, 2, figsize=(4 + 1.35 * len(labs) * 2, 5.4), sharey=True)
    for a, m in zip(axs, ("so", "lo")):
        D = d[d["mode"] == m].pivot(index="pair", columns="label", values="dvol").reindex(index=[k for k, _, _ in PAIRS8], columns=labs)
        Pm = d[d["mode"] == m].pivot(index="pair", columns="label", values="p Holm").reindex(index=D.index, columns=labs)
        vm = 1.0; a.imshow(D.values, cmap="RdBu_r", vmin=-vm, vmax=vm, aspect="auto")
        for i in range(D.shape[0]):
            for j in range(D.shape[1]):
                v = D.values[i, j]; a.text(j, i, dv(v) + ("*" if Pm.values[i, j] < .05 else ""), ha="center", va="center", fontsize=8,
                                           color="white" if abs(v) > .6 * vm else "#202124")
        a.set_xticks(range(len(labs))); a.set_xticklabels(labs, rotation=30, ha="right", fontsize=8); a.set_title(MODES8[m], fontsize=10)
        a.set_yticks(range(len(D))); a.set_yticklabels([PLAB8[k] for k in D.index], fontsize=8)
        for y in (1.5, 3.5, 6.5, 9.5): a.axhline(y, color="white", lw=2)
    plt.tight_layout(); return fig

JOINT8 = []
def sweep_block(sw, title):
    # một lần quét: Bảng Vol (hai chế độ), nhận xét; Hình heatmap 11 cặp, nhận xét; kiểm định chung cho E1, D1, C3
    V = {m: vol_table8(sw, m) for m in ("so", "lo")}; VV = pd.concat({MODES8[m]: V[m] for m in ("so", "lo")}); save8(VV, f"vol_{sw}")
    cap("Bảng", f"{title}: Vol ngoài mẫu (%/năm) của 8 bộ, hai chế độ (các tham số khác ở cấu hình chuẩn N = 100, T = 250, h = 60, HL_VOL = 20, lọc 20%, REB = 21; "
        "tỷ trọng cố định trong kỳ, chưa phí, như kiểm định v6). Đậm: thấp nhất mỗi cột.")
    def _bold(df):
        st = pd.DataFrame("", index=df.index, columns=df.columns)
        for lv in df.index.get_level_values(0).unique():
            sub = df.loc[lv]; st.loc[lv] = np.where(sub.values == sub.min().values, "font-weight: bold", "")
        return st
    display(VV.style.format(precision=2, decimal=",").apply(_bold, axis=None))
    best = {m: V[m].idxmin() for m in V}; E3 = ["EW-RIE*", "VS-EW-RIE*", "VS-NL-LW"]
    win = {m: {nm: int((best[m] == nm).sum()) for nm in E3} for m in V}
    rk = {m: V[m].loc[E3].rank().mean(1) for m in V}
    md(f"*Nhận xét.* Bộ thấp nhất mỗi cột — bán khống: " + ", ".join(f"{lab}: {b}" for lab, b in best['so'].items())
       + "; chỉ mua: " + ", ".join(f"{lab}: {b}" for lab, b in best['lo'].items())
       + f". Trong ba bộ chính, hạng trung bình (1 = thấp nhất) — bán khống: " + ", ".join(f"{k} {f2(v, 1)}" for k, v in rk['so'].items())
       + "; chỉ mua: " + ", ".join(f"{k} {f2(v, 1)}" for k, v in rk['lo'].items()) + f". Khoảng cách giữa ba bộ chính trung bình {f2(np.mean([(V[m].loc[E3].max() - V[m].loc[E3].min()).mean() for m in V]))} pp, "
       f"so với biên độ Vol của EW-RIE\\* theo siêu tham số này {f2(np.mean([V[m].loc['EW-RIE*'].max() - V[m].loc['EW-RIE*'].min() for m in V]))} pp.")
    fig = heat8(sw); savefig8(fig, f"heat_{sw}")
    cap("Hình", f"{title}: ΔVol = Vol(bộ trước) − Vol(bộ sau) (pp/năm) của 11 cặp (A1 … E1); xanh: bộ trước rủi ro thấp hơn; * = p Holm < 0,05 (LW 2011 bootstrap khối, Holm trên 11 cặp trong cột).")
    d = T8[(T8.tier == "T1") & (T8.sweep == sw)]
    for pk in ("E1", "D1", "C3"):
        for m in ("so", "lo"): JOINT8.append(joint8(sw, pk, m))
    J = pd.DataFrame([j for j in JOINT8 if j["sweep"] == sw]).set_index(["pair", "mode"])
    def _s(pk, m):
        x = d[(d.pair == pk) & (d["mode"] == m)]; sg = x[x["p Holm"] < .05]
        return (f"{pk} {MODES8[m].lower()}: ΔVol {dv(x.dvol.min())} … {dv(x.dvol.max())} pp, {len(sg)}/{len(x)} cột có ý nghĩa"
                + (f" ({', '.join(f'{r.label} {dv(r.dvol)}' for r in sg.itertuples())})" if len(sg) else "")
                + f"; chung: TB {dv(J.loc[(pk, MODES8[m]), 'dvol_TB'])} pp, p {pv(J.loc[(pk, MODES8[m]), 'p_TB'])}, p max|t| {pv(J.loc[(pk, MODES8[m]), 'p_max'])}")
    cA = d[d.pair.isin(["A1", "A2", "B2"])]; nA = int((cA["p Holm"] < .05).sum())
    md("*Nhận xét.* " + "; ".join(_s(pk, m) for pk in ("E1", "D1", "C3") for m in ("so", "lo"))
       + f". Cụm A/B2 (EW-RIE\\* so với bản xấp xỉ cùng họ): {nA}/{len(cA)} ô có ý nghĩa, ΔVol trung bình {dv(cA.dvol.mean())} pp.")
