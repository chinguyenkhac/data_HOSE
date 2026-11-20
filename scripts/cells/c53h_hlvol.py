# 5.3 (mới) HL_VOL ∈ {10, 20, 40}: VS-NL-LW, VS-RIE, VS-EW-RIE* (đủ FULL; phần không phụ thuộc HL_VOL lấy từ cache chuẩn). Cấu hình chuẩn khác không đổi.
HVS = (10, 20, 40)
HVR = {(hv, m): run_full(dict(CONFIG, HL_VOL=hv), lo) for hv in HVS for m, lo in MODES.items()}
HVC = {k: cmp_table(d["out"], "EW-RIE*", reb_dates=[u["date"] for u in d["ulog"]]) for k, d in HVR.items()}
VSK = ["VS-NL-LW", "VS-RIE", "VS-EW-RIE*"]
rows = []
for (hv, m), d in HVR.items():
    c = HVC[(hv, m)]
    rows.append(dict(mode=m, HL_VOL=hv, **{f"Vol {k}": d["out"][k]["m"]["Vol %"] for k in VSK}, **{"Vol EW-RIE* (h = 60)": d["out"]["EW-RIE*"]["m"]["Vol %"],
                     "ΔVol EW-RIE* − VS-NL-LW": c.loc["VS-NL-LW", "ΔVol (pp)"], "CI lo": c.loc["VS-NL-LW", "CI lo"], "CI hi": c.loc["VS-NL-LW", "CI hi"],
                     "p LW-boot": c.loc["VS-NL-LW", "p LW-boot"], "p Holm": c.loc["VS-NL-LW", "p Holm"], "ΔTurnover": c.loc["VS-NL-LW", "ΔTurnover"]}))
T6H = pd.DataFrame(rows); save(T6H, "T6_hl_vol")
# hậu kiểm: mỗi bên ở tham số tốt nhất (EW-RIE*: h ∈ {30, 60, 120}; VS-NL-LW: HL_VOL ∈ {10, 20, 40}) – CHỈ để tham khảo
BEST = []
for m, lo in MODES.items():
    ew = {h_: run_full(dict(CONFIG, HL_EW=h_), lo, ["EW-RIE*"]) for h_ in (30, 60, 120)}; hb = min(ew, key=lambda h_: ew[h_]["out"]["EW-RIE*"]["m"]["Vol %"])
    vb = min(HVS, key=lambda hv: HVR[(hv, m)]["out"]["VS-NL-LW"]["m"]["Vol %"]); ra, rb = ew[hb]["out"]["EW-RIE*"]["r"], HVR[(vb, m)]["out"]["VS-NL-LW"]["r"]; assert ra.index.equals(rb.index)
    lo_, hi_ = block_bootstrap_ci(ra.values, rb.values)
    BEST.append({"Chế độ": VN[m], "EW-RIE* tốt nhất": f"h = {hb}", "VS-NL-LW tốt nhất": f"HL_VOL = {vb}", "Vol EW-RIE*": ra.std() * np.sqrt(252) * 100, "Vol VS-NL-LW": rb.std() * np.sqrt(252) * 100,
                 "ΔVol (pp)": (ra.std() - rb.std()) * np.sqrt(252) * 100, "CI lo": lo_, "CI hi": hi_, "p LW-boot": lw_var_test(ra.values, rb.values, M=1000)[3]})
BEST = pd.DataFrame(BEST).set_index("Chế độ"); save(BEST.reset_index(), "T6_hl_vol_best_vs_best")
t = T6H.copy(); t["ΔVol [CI]"] = [f"{a:+.2f} [{b:+.2f}; {c:+.2f}]" for a, b, c in zip(t["ΔVol EW-RIE* − VS-NL-LW"], t["CI lo"], t["CI hi"])]
cap("Bảng", "Vol (%/năm, gộp) của các bộ VS theo HL_VOL, cấu hình chuẩn (N = 100, h = 60); ΔVol = Vol(EW-RIE\\*, h = 60) − Vol(VS-NL-LW) cùng HL_VOL, CI 95% block bootstrap b = 21, p Holm trên 4 đối thủ lõi.")
show(t.assign(mode=t["mode"].map(VN)).set_index(["mode", "HL_VOL"])[[f"Vol {k}" for k in VSK] + ["Vol EW-RIE* (h = 60)", "ΔVol [CI]", "p Holm"]], 3)
cap("Bảng", "Hậu kiểm, chỉ để tham khảo (chọn tham số theo kết quả ngoài mẫu nên thiên lệch có lợi cho cả hai bên): mỗi bên ở tham số cho Vol thấp nhất.")
show(BEST, 3)
