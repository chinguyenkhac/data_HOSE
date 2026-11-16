# ---- T5a: Bảng 30 (cụm C theo giai đoạn), Hình 15 (hình của v3) ----
def per_rows(pairs, modes=("short_ok", "long_only")):
    rows = []
    for m in modes:
        for g, a, b in pairs:
            for nm, s0, s1 in [("Toàn mẫu", None, None)] + list(PERIODS):
                ra, rb = OUT0[m][a]["r"], OUT0[m][b]["r"]
                if s0 is not None: ra, rb = ra[s0:s1], rb[s0:s1]
                if len(ra) <= 21: continue
                lo_, hi_ = block_bootstrap_ci(ra.values, rb.values)
                rows.append({"Chế độ": VN[m], "Cặp": f"{a} − {b}", "Giai đoạn": nm, "phiên": len(ra), "ΔVol (pp)": (ra.std() - rb.std()) * np.sqrt(252) * 100, "CI lo": lo_, "CI hi": hi_})
    return pd.DataFrame(rows)
PC = [p for p in PAIRS12 if p[0].startswith("C")]
T30 = per_rows(PC); save(T30, "T5a_vs_periods")
def per_table(T):
    t = T.assign(o=[f"{dv(d)} [{dv(l)}; {dv(h)}]" for d, l, h in zip(T["ΔVol (pp)"], T["CI lo"], T["CI hi"])])
    return t.pivot_table(index=["Chế độ", "Cặp"], columns="Giai đoạn", values="o", aggfunc="first", sort=False)[["Toàn mẫu"] + [p for p, _, _ in PERIODS if p in set(T["Giai đoạn"])]]
cap("Bảng", "Cụm C (trước và sau VS): ΔVol (pp/năm) [CI 95% bootstrap khối] theo giai đoạn thị trường; < 0: VS giảm rủi ro. Mô tả, không Holm.")
display(per_table(T30))
T5P = T30[T30["Giai đoạn"] != "Toàn mẫu"].pivot_table(index="Giai đoạn", columns=["Chế độ", "Cặp"], values="ΔVol (pp)", sort=False)
fig, ax = plt.subplots(1, 2, figsize=(13, 3.8), sharey=True)
for a, m in zip(ax, (VN["short_ok"], VN["long_only"])):
    d = T5P[m]; x = np.arange(len(d))
    for j, (c, col) in enumerate(zip(d.columns, ["#2a78d6", "#eb6834", "#1baf7a"])): a.bar(x + (j - 1) * .27, d[c], .25, color=col, label=c)
    a.axhline(0, color="#52514e", lw=.8); a.set_xticks(x, d.index, rotation=20, fontsize=8); a.grid(axis="y", alpha=.3)
    a.set_title(f"{m}: ΔVol do VS theo giai đoạn (pp/năm; < 0 ⇒ VS giảm rủi ro)", fontsize=10)
ax[0].legend(fontsize=8); plt.tight_layout(); savefig(fig, "fig_15_vs_periods")
cap("Hình", "Hình của v3: ΔVol do VS theo giai đoạn thị trường, ba cặp của cụm C.")
neg = {m: [p for p in T5P.index if (T5P.loc[p, VN[m]] < 0).all()] for m in MODES}
cv = T30[(T30["Giai đoạn"] == "2020Q1 COVID")].set_index(["Chế độ", "Cặp"])["ΔVol (pp)"]
md("**Kết quả.** Giai đoạn cả ba cặp đều âm (VS giảm rủi ro) — " + "; ".join(f"{VN[m]}: {', '.join(neg[m]) if neg[m] else 'không có'}" for m in ("short_ok", "long_only"))
   + f". 2020Q1 COVID: " + ", ".join(f"{e_(p)} {dv(v)}" for (mm, p), v in cv.items() if mm == VN['long_only']) + " (chỉ mua).\n\n"
   f"**Kết luận.** VS giảm rủi ro nhiều nhất ở giai đoạn {T5P.mean(axis=1).idxmin()} (ΔVol trung bình {dv(T5P.mean(axis=1).min())} pp); "
   f"{int(((T30['CI hi'] < 0) & (T30['Giai đoạn'] != 'Toàn mẫu')).sum())}/{int((T30['Giai đoạn'] != 'Toàn mẫu').sum())} ô (giai đoạn × cặp × chế độ) có CI nằm hẳn dưới 0.")
