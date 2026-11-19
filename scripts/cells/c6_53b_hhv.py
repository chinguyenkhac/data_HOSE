# ---- 5.3b Bảng 16: VS-EW-RIE* ở h × HL_VOL (N = 100); ΔVol so với VS-NL-LW cùng HL_VOL; * = p Holm < 0,05 trên 9 ô của mỗi chế độ ----
HHV = {}
for m, lo in MODES.items():
    rows = []
    for h_ in HS:
        for hv in HVS:
            d = run_full(dict(CONFIG, HL_EW=h_, HL_VOL=hv), lo, ["VS-EW-RIE*", "VS-NL-LW"]); a_, b_ = d["out"]["VS-EW-RIE*"]["r"].values, d["out"]["VS-NL-LW"]["r"].values
            rows.append(dict(h=h_, HL_VOL=hv, vol=d["out"]["VS-EW-RIE*"]["m"]["Vol %"], dvol=(a_.std() - b_.std()) * np.sqrt(252) * 100, p=lw_var_test(a_, b_)[3]))
    t = pd.DataFrame(rows); t["p_holm"] = holm(t.p.values); HHV[m] = t
save(pd.concat(HHV, names=["mode"]).reset_index(), "T5_hhv_vs_ew_rie")
T16 = pd.concat({VN[m]: HHV[m].assign(o=[f"{f2(v)} ({dv(d_)}{'*' if p < .05 else ''})" for v, d_, p in zip(HHV[m].vol, HHV[m].dvol, HHV[m].p_holm)])
                 .pivot(index="h", columns="HL_VOL", values="o") for m in ("short_ok", "long_only")}, names=["Chế độ", "h"])
T16.columns = [f"HL_VOL = {c}" for c in T16.columns]
cap("Bảng", "VS-EW-RIE\\* theo half-life h × HL\\_VOL (N = 100): Vol %/năm (ΔVol so với VS-NL-LW cùng HL\\_VOL, pp; \\* = p Holm < 0,05 trên 9 ô của mỗi chế độ, kiểm định phương sai bootstrap khối).")
display(T16)
bx = {m: HHV[m].loc[HHV[m].vol.idxmin()] for m in MODES}; ns_ = {m: int((HHV[m].p_holm < .05).sum()) for m in MODES}
md("**Kết quả.** " + "; ".join(f"{VN[m]}: Vol thấp nhất ở h = {int(bx[m].h)}, HL\\_VOL = {int(bx[m].HL_VOL)} ({f2(bx[m].vol)}%, ΔVol so với VS-NL-LW {dv(bx[m].dvol)}); ΔVol < 0 ở {int((HHV[m].dvol < 0).sum())}/9 ô, có ý nghĩa {ns_[m]}/9" for m in MODES) + ".\n\n"
   f"**Kết luận.** VS-EW-RIE\\* {'không hơn VS-NL-LW có ý nghĩa ở tổ hợp nào' if sum(int(((HHV[m].dvol < 0) & (HHV[m].p_holm < .05)).sum()) for m in MODES) == 0 else 'hơn VS-NL-LW có ý nghĩa ở một vài tổ hợp'}; chọn h, HL\\_VOL theo kết quả ngoài mẫu sẽ thiên lệch (xem 5.5).")
