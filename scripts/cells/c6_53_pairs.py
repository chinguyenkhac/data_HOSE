# ---- 5.3 Heatmap cặp: 12 cặp × 9 cấu hình, hai chế độ (dấu * = p Holm < 0,05 trong từng cột, mô tả) ----
G53 = {}
for m in MODES:
    D, Pm = {}, {}
    for lab in SENS:
        k, v = SENS[lab]; key = ("nh", v, 60, m) if k == "N" else ("nh", 100, v, m) if k == "h" else ("hv", v, m)
        d = sens_d(lab, m); out = sens_out(lab, m)
        t = ptab(key, dict(out=out, ulog=d["ulog"])) if k != "hv" or v != 20 else ptab(("hv20", m), dict(out=out, ulog=d["ulog"]))
        idx = pd.MultiIndex.from_tuples([(g, f"{a} − {b}") for g, a, b in PAIRS12], names=["Cụm", "Cặp"])
        D[lab], Pm[lab] = t["ΔVol (pp)"].reindex(idx), t["p Holm"].reindex(idx)
    G53[VN[m]] = (pd.DataFrame(D), pd.DataFrame(Pm))
G53 = {k: G53[k] for k in ("Bán khống", "Chỉ mua")}; save_grid(G53, "T5_pairs_sens")
pair_heatmap(G53, "12 cặp theo N, h, HL_VOL", fname="fig_8_pairs_sens")
cap("Hình", "ΔVol (pp/năm) của 12 cặp định trước theo N, h, HL\\_VOL; xanh: bộ đứng trước rủi ro thấp hơn; màu cắt ở ±1 pp. \\* = p Holm < 0,05 trên các cặp trong cùng cột (mô tả, không hiệu chỉnh xuyên cột). Số liệu: `T5_pairs_sens.csv`.")
md("**Kết quả.** Số ô (cấu hình × chế độ) có ΔVol < 0 / âm có ý nghĩa / dương có ý nghĩa: " + "; ".join(
   f"{e_(p)}: {c[1]}/{c[0]} / {c[2]} / {c[3]}" for p in ("EW-RIE* − EW-NL-LW", "EW-RIE* − VS-NL-LW", "VS-NL-LW − NL-LW", "VS-EW-RIE* − VS-NL-LW") for c in [grid_count(G53, p)]) + ".\n\n"
   f"**Kết luận.** {concl_grid(G53)}")
