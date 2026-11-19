# ---- §5: số liệu dùng chung (đọc cache) + Hình 6 (heatmap N × h của v3) và Hình 7 (ΔVol của EW-RIE* so với VS-NL-LW và EW-WeSpeR) ----
NS, HS, HVS = (50, 100, 150), (30, 60, 120), (10, 20, 40)
GR = {(n_, h_, m): run_full(dict(CONFIG, N=n_, HL_EW=h_), lo, M12) for n_ in NS for h_ in HS for m, lo in MODES.items()}
HV = {(hv, m): run_full(dict(CONFIG, HL_VOL=hv), lo, M12) for hv in HVS for m, lo in MODES.items()}
_PT = {}
def ptab(key, d):           # pair_table có ghi nhớ (cùng cấu hình dùng ở nhiều chỗ chỉ tính một lần)
    if key not in _PT: _PT[key] = pair_table(d["out"], [p for p in PAIRS12 if p[1] in d["out"] and p[2] in d["out"]], reb_dates=[u["date"] for u in d["ulog"]])
    return _PT[key]
rows = []
for (n_, h_, m), d in GR.items():
    t = ptab(("nh", n_, h_, m), d); g = lambda c: t.xs(c, level=1)
    rows.append(dict(mode=m, N=n_, h=h_, kỳ=len(d["ulog"]), **{"Vol EW-RIE*": d["out"]["EW-RIE*"]["m"]["Vol %"]},
                     **{f"ΔVol vs {b}": g(f"EW-RIE* − {b}")["ΔVol (pp)"].iloc[0] for b in ("EW-NL-LW", "VS-NL-LW", "EW-WeSpeR")},
                     **{f"p Holm vs {b}": g(f"EW-RIE* − {b}")["p Holm"].iloc[0] for b in ("EW-NL-LW", "VS-NL-LW", "EW-WeSpeR")}))
T6 = pd.DataFrame(rows); save(T6, "T6_N_h_grid")
def heat2x2(cols, ttls, fname, star=None):
    fig, ax = plt.subplots(2, 2, figsize=(11, 7))
    for i, m in enumerate(MODES):
        t = T6[T6["mode"] == m]
        for j, (col, ttl) in enumerate(zip(cols, ttls)):
            M = t.pivot(index="N", columns="h", values=col); a = ax[i, j]; dif = col.startswith("ΔVol"); v = np.abs(M.values).max()
            a.imshow(M.values, cmap="RdYlGn_r" if dif else "Blues", aspect="auto", **({"vmin": -v, "vmax": v} if dif else {}))
            a.set_xticks(range(3), M.columns); a.set_yticks(range(3), M.index); a.set_xlabel("h (half-life, phiên)"); a.set_ylabel("N"); mid = (M.values.min() + M.values.max()) / 2
            S = t.pivot(index="N", columns="h", values=col.replace("ΔVol", "p Holm")) if (dif and star) else None
            for (y, x), val in np.ndenumerate(M.values):
                a.text(x, y, (dv(val) if dif else f2(val)) + ("*" if S is not None and S.values[y, x] < .05 else ""), ha="center", va="center", fontsize=10,
                       color="white" if (not dif and val > mid) else "black")
            a.set_title(f"{VN[m]} – {ttl}", fontsize=10)
    plt.tight_layout(); savefig(fig, fname)
heat2x2(["Vol EW-RIE*", "ΔVol vs EW-NL-LW"], ["Vol EW-RIE* (%/năm)", "ΔVol so với EW-NL-LW (pp)"], "fig_6_nh_v3")
cap("Hình", "Lưới N × h (heatmap của v3): Vol của EW-RIE\\* (trái) và ΔVol = Vol(EW-RIE\\*) − Vol(EW-NL-LW) (phải); hàng trên: chỉ mua, hàng dưới: bán khống. Chỉ so trong cùng hàng N.")
heat2x2(["ΔVol vs VS-NL-LW", "ΔVol vs EW-WeSpeR"], ["ΔVol so với VS-NL-LW (pp)", "ΔVol so với EW-WeSpeR (pp)"], "fig_7_nh_vs", star=True)
cap("Hình", "Lưới N × h: ΔVol của EW-RIE\\* so với VS-NL-LW (trái) và EW-WeSpeR (phải), pp/năm; xanh: EW-RIE\\* thấp hơn; \\* = p Holm < 0,05 (12 cặp trong từng ô, mô tả).")
def _concl_nh():
    neg = int((T6["ΔVol vs EW-NL-LW"] < 0).sum()); sv = lambda b, sgn: int(((np.sign(T6[f"ΔVol vs {b}"]) == sgn) & (T6[f"p Holm vs {b}"] < .05)).sum())
    return (f"EW-RIE\\* thấp hơn EW-NL-LW ở {neg}/18 ô (cấu hình × chế độ); so với VS-NL-LW: thấp hơn có ý nghĩa {sv('VS-NL-LW', -1)} ô, cao hơn có ý nghĩa {sv('VS-NL-LW', 1)} ô; "
            f"so với EW-WeSpeR: thấp hơn có ý nghĩa {sv('EW-WeSpeR', -1)} ô, cao hơn có ý nghĩa {sv('EW-WeSpeR', 1)} ô (mô tả).")
_n = lambda m, c, cond: int(cond(T6[T6["mode"] == m]).sum())
md("**Kết quả.** " + " ".join(f"{VN[m]}: so với EW-NL-LW, EW-RIE\\* thấp hơn ở {_n(m, 0, lambda t: t['ΔVol vs EW-NL-LW'] < 0)}/9 ô ({_n(m, 0, lambda t: (t['ΔVol vs EW-NL-LW'] < 0) & (t['p Holm vs EW-NL-LW'] < .05))} có ý nghĩa); "
   f"so với VS-NL-LW thấp hơn ở {_n(m, 0, lambda t: t['ΔVol vs VS-NL-LW'] < 0)}/9 ô (có ý nghĩa: thấp hơn {_n(m, 0, lambda t: (t['ΔVol vs VS-NL-LW'] < 0) & (t['p Holm vs VS-NL-LW'] < .05))}, cao hơn {_n(m, 0, lambda t: (t['ΔVol vs VS-NL-LW'] > 0) & (t['p Holm vs VS-NL-LW'] < .05))}); "
   f"so với EW-WeSpeR thấp hơn ở {_n(m, 0, lambda t: t['ΔVol vs EW-WeSpeR'] < 0)}/9 ô (có ý nghĩa: thấp hơn {_n(m, 0, lambda t: (t['ΔVol vs EW-WeSpeR'] < 0) & (t['p Holm vs EW-WeSpeR'] < .05))}, cao hơn {_n(m, 0, lambda t: (t['ΔVol vs EW-WeSpeR'] > 0) & (t['p Holm vs EW-WeSpeR'] < .05))})." for m in MODES)
   + "\n\n**Kết luận.** " + _concl_nh())
