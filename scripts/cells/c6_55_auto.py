# ---- 5.5 Bảng 18: tham số tự chọn từ quá khứ (ghép chuỗi lợi suất gộp đã có; phép thử độ nhạy, chưa tính phí do đổi tham số) ----
CAND = {"EW-RIE*": ("h", {h_: (lambda m, h_=h_: GR[(100, h_, m)]["out"]["EW-RIE*"]["r"]) for h_ in HS}, 60),
        "EW-NL-LW": ("h", {h_: (lambda m, h_=h_: GR[(100, h_, m)]["out"]["EW-NL-LW"]["r"]) for h_ in HS}, 60),
        "VS-NL-LW": ("HL_VOL", {hv: (lambda m, hv=hv: HV[(hv, m)]["out"]["VS-NL-LW"]["r"]) for hv in HVS}, 20)}
def auto_select(m, k, look=252):
    par, getr, std_ = CAND[k]; R_ = pd.DataFrame({p: f(m) for p, f in getr.items()}); idx = R_.index; assert all(R_[p].notna().all() for p in R_)
    reb = [d for d in REB_DATES if d in idx]; out = pd.Series(np.nan, index=idx); choice = []
    for i, d0 in enumerate(reb):
        d1 = reb[i + 1] if i + 1 < len(reb) else None; pos = idx.get_loc(d0); hist = R_.iloc[max(0, pos - look):pos]
        p = hist.std().idxmin() if len(hist) >= look else std_; choice.append(p)
        sl = (idx >= d0) & ((idx < d1) if d1 is not None else True); out[sl] = R_.loc[sl, p]
    return out, pd.Series(choice, index=reb)
AUTO, ROWS18 = {}, []
for m in ("short_ok", "long_only"):
    for k, (par, getr, std_) in CAND.items():
        r_, ch = auto_select(m, k); AUTO[(m, k)] = r_
        ROWS18.append({"Chế độ": VN[m], "Bộ": k, "Vol (tham số chuẩn)": getr[std_](m).std() * np.sqrt(252) * 100, "Vol (tự chọn)": r_.std() * np.sqrt(252) * 100,
                       "Số lần đổi": int((ch != ch.shift()).iloc[1:].sum()), **{f"tỷ lệ chọn {par} = {p}": (ch == p).mean() for p in getr}})
T18 = pd.DataFrame(ROWS18).set_index(["Chế độ", "Bộ"]); save(T18, "T5_auto_select")
PT18 = pd.concat({VN[m]: pair_table({f"{k} (tự chọn)": dict(r=AUTO[(m, k)]) for k in CAND},
                                    [("tự chọn", "EW-RIE* (tự chọn)", "VS-NL-LW (tự chọn)"), ("tự chọn", "EW-RIE* (tự chọn)", "EW-NL-LW (tự chọn)")]).droplevel(0)
                  for m in ("short_ok", "long_only")}, names=["Chế độ", "Cặp"]); save(PT18, "T5_auto_select_pairs")
cap("Bảng", "Tham số tự chọn từ quá khứ (252 phiên ngoài mẫu trước mỗi ngày tái cân bằng; 118 kỳ, cùng ngày với cấu hình chuẩn). Trên: Vol %/năm ở tham số chuẩn và tự chọn, số lần đổi, tỷ lệ số kỳ chọn từng giá trị "
    "(tỷ lệ tính theo h với EW-RIE\\*, EW-NL-LW và theo HL\\_VOL với VS-NL-LW). Dưới: kiểm định hai cặp \"tự chọn với tự chọn\" (Holm trên 2 cặp). Phép thử độ nhạy, không thay cấu hình chuẩn; chưa tính phí giao dịch phát sinh khi đổi tham số.")
show(T18, 3); show(PT18[["ΔVol (pp)", "CI lo", "CI hi", "p LW-HAC", "p LW-boot", "p Holm", "p JKM"]], 3)
pe = lambda m: PT18.loc[(VN[m], "EW-RIE* (tự chọn) − VS-NL-LW (tự chọn)")]
md("**Kết quả.** Vol tự chọn so với tham số chuẩn — " + "; ".join(f"{VN[m]}: " + ", ".join(f"{e_(k)} {f2(T18.loc[(VN[m], k), 'Vol (tham số chuẩn)'])} → {f2(T18.loc[(VN[m], k), 'Vol (tự chọn)'])}" for k in CAND) for m in ("short_ok", "long_only"))
   + ". EW-RIE\\* (tự chọn) − VS-NL-LW (tự chọn): " + "; ".join(f"{VN[m]} {dv(pe(m)['ΔVol (pp)'])} pp (p Holm {f2(pe(m)['p Holm'])})" for m in ("short_ok", "long_only")) + ".\n\n"
   f"**Kết luận.** Chọn tham số chỉ bằng quá khứ {'không làm đổi' if all(pe(m)['p Holm'] >= .05 for m in MODES) else 'làm đổi'} kết luận so sánh EW-RIE\\* với VS-NL-LW.")
