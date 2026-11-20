# ---- 8.4 Kiểm định chung theo lần quét + kết luận theo ngưỡng đăng ký trước + khi nào nên dùng EW-RIE* ----
from scipy.stats import spearmanr
J8 = pd.DataFrame(JOINT8).set_index(["sweep", "pair", "mode"]); save8(J8, "kiem_dinh_chung")
cap("Bảng", "Kiểm định chung cho mỗi lần quét tầng 1 (trên phần ngày chung của các cột): ΔVol trung bình qua các cột, p (TB = 0) và p max|t| "
    "(có cột nào khác 0, đã tính bội), bootstrap khối vòng b = 21, M = 2 000; số cột ΔVol âm/dương. E1 = EW-RIE\\* − VS-NL-LW, D1 = VS-EW-RIE\\* − VS-NL-LW, C3 = VS-EW-RIE\\* − EW-RIE\\*.")
display(J8[["n_ngay", "dvol_TB", "p_TB", "t_max", "p_max", "am", "duong"]].style.format(precision=2, decimal=",").format(pv, subset=["p_TB", "p_max"]))
sgJ = J8[(J8.p_TB < .05) | (J8.p_max < .05)]
md("*Nhận xét.* Các dòng có ý nghĩa (p TB hoặc p max|t| < 0,05): " + ("; ".join(f"{i[1]} {i[2].lower()} ở quét {i[0]} (TB {dv(r.dvol_TB)} pp)" for i, r in sgJ.iterrows()) if len(sgJ) else "không có")
   + ". Đây là câu trả lời gộp cho câu hỏi \"đổi siêu tham số thì kết luận còn giữ không\", không phải chọn cột đẹp.")

def _e1(sw, m="lo"):
    x = T8[(T8.tier == "T1") & (T8.sweep == sw) & (T8.pair == "E1") & (T8["mode"] == m)]
    v = x.label.str.extract(r"(\d+)")[0].astype(float); return spearmanr(v, x.dvol)[0], x
rT, xT = _e1("T"); rR, xR = _e1("REB")
H8A = rT < 0 and rR < 0
d1 = pd.concat([GD[5], GD[21]]); d1 = d1[d1.pair == "D1"]; H8B = not (d1["p Holm"] < .05).any()
fz = GD[5][(GD[5].pair == "E1") & GD[5].label.map(FAST)]; H8C = {m: (fz[fz["mode"] == m].dvol > 0).mean() for m in ("lo", "so")}
md(f"**Kết luận theo ngưỡng đăng ký trước.**\n\n"
   f"- **H8a** (EW-RIE\\* tốt dần khi T dài và REB dài, chỉ mua): Spearman(ΔVol E1, T) = {f2(rT)}, Spearman(ΔVol E1, REB) = {f2(rR)} ⇒ **{'đạt' if H8A else 'không đạt'}**.\n"
   f"- **H8b** (bộ làm sạch không tạo khác biệt khi đã VS: D1 không có ô nào p Holm < 0,05 trên lưới h × HL_VOL): **{'đạt' if H8B else 'không đạt'}** "
   f"({int((d1['p Holm'] < .05).sum())}/{len(d1)} ô có ý nghĩa; ΔVol từ {dv(d1.dvol.min())} đến {dv(d1.dvol.max())} pp).\n"
   f"- **H8c** (gấp và nhanh — REB 5, h ≤ 30, HL_VOL ≤ 10 — VS-NL-LW tốt hơn EW-RIE\\*, E1 > 0 ở đa số ô): chỉ mua {f2(100 * H8C['lo'], 0)}% ô, bán khống {f2(100 * H8C['so'], 0)}% ô ⇒ "
   f"**{'đạt' if min(H8C.values()) > .5 else 'không đạt'}**.")
