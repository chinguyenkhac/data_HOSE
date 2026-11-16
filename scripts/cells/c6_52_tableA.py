# ---- 5.2 Bảng A: 12 phương pháp × (N, h, HL_VOL), mỗi chế độ một bảng ----
VSSET = ["VS-NL-LW", "VS-RIE", "VS-EW-RIE*"]
SENS = {**{f"N = {n_}": ("N", n_) for n_ in NS}, **{f"h = {h_}": ("h", h_) for h_ in HS}, **{f"HL_VOL = {hv}": ("hv", hv) for hv in HVS}}
def sens_d(lab, m):
    k, v = SENS[lab]
    return GR[(v, 60, m)] if k == "N" else GR[(100, v, m)] if k == "h" else HV[(v, m)]
def sens_out(lab, m):       # cột HL_VOL: chỉ giữ ba bộ VS và các bộ chúng ghép cặp (để heatmap cụm C, D, E)
    d = sens_d(lab, m); return d["out"] if SENS[lab][0] != "hv" else {k: o for k, o in d["out"].items() if k in VSSET + ["NL-LW", "RIE", "EW-RIE*"]}
TA = {}
for m in MODES:
    TA[m] = pd.DataFrame({lab: vols(sens_d(lab, m)["out"], M12).where(lambda s: s.index.isin(VSSET) | (SENS[lab][0] != "hv")) for lab in SENS}).reindex(M12)
    save(TA[m], f"T5_tableA_{m}")
    kys = ", ".join(f"{lab}: {len(sens_d(lab, m)['ulog'])}" for lab in SENS if SENS[lab][0] == "N")
    cap("Bảng", f"{VN[m]}: Vol (%/năm, gộp) của 12 phương pháp khi đổi một tham số (các tham số khác chuẩn); in đậm: thấp nhất mỗi cột. Số kỳ ngoài mẫu — {kys}; cột h và HL\\_VOL: 118 kỳ. Không so giữa các cột N.")
    display(table_a(TA[m]))
best = {m: TA[m].idxmin() for m in MODES}; cnt = {m: best[m].value_counts() for m in MODES}
md("**Kết quả.** Bộ có Vol thấp nhất theo từng cột — " + "; ".join(f"{VN[m]}: " + ", ".join(f"{e_(k)} {v}/9" for k, v in cnt[m].items()) for m in MODES)
   + f". Hạng của EW-RIE\\* trong 12 bộ (các cột N, h): " + "; ".join(f"{VN[m]} " + ", ".join(str(int(TA[m][c].rank()['EW-RIE*'])) for c in TA[m].columns if not c.startswith("HL")) for m in MODES) + ".\n\n"
   f"**Kết luận.** Bộ thấp nhất mỗi cột {'luôn' if all(k.startswith(('EW-', 'VS-')) for m in MODES for k in best[m]) else 'không phải lúc nào cũng'} là bộ có trọng số mũ hoặc VS, và đổi theo tham số; chênh lệch giữa các bộ đầu bảng cần đọc ở kiểm định cặp (5.3).")
