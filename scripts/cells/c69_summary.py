# ---- Tổng kết độ vững: mọi cấu hình đã chạy × hai chế độ ----
CFG_LIST = [("chuẩn", dict(CONFIG), None)] \
    + [(f"N={n_}, h={h_}", dict(CONFIG, N=n_, HL_EW=h_), None) for n_ in NS for h_ in HS if (n_, h_) != (100, 60)] \
    + [(f"T={t_}", dict(CONFIG, WINDOW=t_), None) for t_ in (120, 500)] \
    + [(f"HL_VOL={hv}", dict(CONFIG, HL_VOL=hv), None) for hv in HVS if hv != 20] \
    + [(f"REB={r_}", dict(CONFIG, REB=r_), None) for r_ in REBS if r_ != 21] \
    + [(f"ZERO_MAX={'không lọc' if z_ == 1 else f'{z_:.0%}'}", dict(CONFIG, ZERO_MAX=z_), None) for z_ in (1.0, 0.30, 0.10)] \
    + [(f"hủy niêm yết: {sc}", dict(CONFIG), sc) for sc in SCENARIOS if not sc.startswith("S0")]
SUM, SRANK, SCMP, SPW, SVOL = {}, {}, {}, {}, {}
for lab, cfg, sc in CFG_LIST:
    for m, lo in MODES.items():
        meths = [k for k in FULL if not (cfg["REB"] in DCC_SKIP_REB and k.startswith("DCC"))]
        d = run_full_scn(sc, cfg, lo, meths) if sc else run_full(cfg, lo, meths)
        vol = pd.Series({k: o["m"]["Vol %"] for k, o in d["out"].items()}); SRANK[(lab, m)] = vol.rank(method="min")
        SCMP[(lab, m)] = cmp_table(d["out"], "EW-RIE*", CORE5, reb_dates=[u["date"] for u in d["ulog"]])
        SPW[(lab, m)] = pairwise_top(d["out"], TOP, [u["date"] for u in d["ulog"]], M=1000)[0]; SVOL[(lab, m)] = vol      # v5: 15 cặp mỗi ô (M = 1000 bootstrap)
RK = pd.DataFrame(SRANK).T                                               # hàng = (cấu hình, chế độ), cột = phương pháp
S9 = pd.DataFrame({"Đứng đầu (số ô)": (RK == 1).sum(), "Hạng TB": RK.mean(), "Hạng xấu nhất": RK.max()}).sort_values("Hạng TB")
S9["Đứng đầu (số ô)"] = S9["Đứng đầu (số ô)"].astype(int); S9["Hạng xấu nhất"] = S9["Hạng xấu nhất"].astype(int); save(S9.reset_index().rename(columns={"index": "method"}), "T9_robustness_ranks")
cap("Bảng", f"Tổng kết độ vững: {len(CFG_LIST)} cấu hình × 2 chế độ = {len(RK)} ô; thứ hạng Vol (1 = thấp nhất) của mỗi phương pháp trong FULL (15 bộ; 14 ở ô bỏ DCC).")
show(S9, 2)
cm = pd.DataFrame({k: v.loc["VS-NL-LW"] for k, v in SCMP.items()}).T
cm["Hạng EW-RIE*"] = RK["EW-RIE*"]; cm["Hạng VS-NL-LW"] = RK["VS-NL-LW"]; save(cm.reset_index().rename(columns={"level_0": "config", "level_1": "mode"}), "T9_ew_rie_vs_vsnllw_by_cell")
lower, higher = (cm["ΔVol (pp)"] < 0) & (cm["p Holm"] < .05), (cm["ΔVol (pp)"] > 0) & (cm["p Holm"] < .05)
V9 = pd.Series({"Số ô": len(cm), "ΔVol < 0 (EW-RIE* thấp hơn)": int((cm["ΔVol (pp)"] < 0).sum()), "ΔVol > 0": int((cm["ΔVol (pp)"] > 0).sum()),
                "Thấp hơn có ý nghĩa (p Holm < 0,05)": int(lower.sum()), "Cao hơn có ý nghĩa (p Holm < 0,05)": int(higher.sum()),
                "ΔVol TB (pp)": cm["ΔVol (pp)"].mean(), "ΔTurnover/kỳ TB": cm["ΔTurnover"].mean()})
cap("Bảng", "EW-RIE\\* so với VS-NL-LW trên mọi ô (p Holm trên 4 đối thủ lõi trong từng ô; p-value ở đây mang tính mô tả, không hiệu chỉnh xuyên lưới; kết luận chính dựa vào cấu hình chuẩn và xu hướng nhất quán theo N, h).")
show(V9.to_frame("giá trị"), 3)
by_mode = cm.assign(mode=[k[1] for k in cm.index]).groupby("mode").agg(**{"ΔVol<0": ("ΔVol (pp)", lambda s: int((s < 0).sum())), "n": ("ΔVol (pp)", "size")})
