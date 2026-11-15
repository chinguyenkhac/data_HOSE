# ---- Kết quả cấu hình chuẩn cho FULL (từ cache; phần nặng chạy bằng scripts/run_grid.py, mỗi phương pháp một cache) ----
STD = {m: run_full(CONFIG, lo) for m, lo in MODES.items()}
U0 = STD["long_only"]["ulog"]; REB_DATES = [u["date"] for u in U0]; OUT0 = {m: STD[m]["out"] for m in MODES}
for m in MODES:    # run_full tái tạo đúng §4 (EW-WeSpeR: khởi tạo ấm phụ thuộc thứ tự chạy nên chỉ báo sai khác)
    bad = {k: float(np.abs(OUT0[m][k]["r"].values - o["r"].values).max()) for k, o in RESULTS[m]["out"].items()}
    assert all(v < 1e-12 for k, v in bad.items() if k != "EW-WeSpeR"), (m, bad)
    print(f"{VN[m]}: run_full trùng §4 cho 10 bộ (sai lệch tối đa {max(v for k, v in bad.items() if k != 'EW-WeSpeR'):.0e}); EW-WeSpeR lệch tối đa {bad['EW-WeSpeR']:.1e}")
print(f"OOS: {len(U0)} kỳ, {len(OUT0['long_only']['EW-RIE*']['r'])} phiên ({U0[0]['date'].date()} → {OUT0['long_only']['EW-RIE*']['r'].index[-1].date()}) | "
      f"mã đủ ĐK mỗi kỳ {min(u['n_eligible'] for u in U0)}–{max(u['n_eligible'] for u in U0)} (N={CONFIG['N']}, ZERO_MAX={CONFIG['ZERO_MAX']:.0%})")

def restrict(out, dates):
    # cắt mọi chuỗi về cùng tập ngày (so sánh trên ngày chung khi các cấu hình có số kỳ khác nhau)
    return {k: dict(o, r=o["r"].loc[dates], r_net=o["r_net"].loc[dates]) for k, o in out.items()}

def cmp_table(out, target="EW-RIE*", rivals=None, reb_dates=None, **kw):
    # compare_to; reb_dates chỉ giữ ngày tái cân bằng nằm trong chuỗi
    idx = out[target]["r"].index; rd = [d for d in (reb_dates if reb_dates is not None else REB_DATES) if d in idx]
    return compare_to(out, target, rivals, reb_dates=rd, **kw)

def fmt_cmp(C):
    # định dạng bảng so sánh: ΔVol [CI], p; dòng thuộc họ lõi (CORE5) in đậm
    t = pd.DataFrame({"Vol (%)": C["Vol"], "ΔVol (pp)": C["ΔVol (pp)"], "CI 95% (pp)": [f"[{a:+.2f}; {b:+.2f}]" for a, b in zip(C["CI lo"], C["CI hi"])],
                      "p LW-boot": C["p LW-boot"], "p LW-HAC": C["p LW-HAC"], "p Holm": C["p Holm"], "p JKM": C["p JKM"]})
    if "ΔTurnover" in C: t["ΔTurnover [CI]"] = [f"{a:+.2f} [{b:+.2f}; {c:+.2f}]" for a, b, c in zip(C["ΔTurnover"], C["Turn CI lo"], C["Turn CI hi"])]
    core = C["lõi"].astype(bool).values
    return t.style.format({"Vol (%)": "{:.2f}", "ΔVol (pp)": "{:+.2f}", "p LW-boot": "{:.3f}", "p LW-HAC": "{:.3f}", "p Holm": "{:.3f}", "p JKM": "{:.3f}"}, decimal=",", na_rep="–").apply(
        lambda r: ["font-weight: bold" if core[list(t.index).index(r.name)] else "" for _ in r], axis=1)

def sig_mark(C, a=0.05):
    # ▼ EW-RIE* thấp hơn có ý nghĩa (p Holm < a với họ lõi; p LW-boot < a ngoài họ), ▲ cao hơn, = không khác biệt
    p = C["p Holm"].where(C["p Holm"].notna(), C["p LW-boot"]); return np.where(p < a, np.where(C["ΔVol (pp)"] < 0, "▼", "▲"), "=")
