# ---- Kết luận cuối §6 (v5): 3–5 câu, mọi số lấy từ bảng ----
_P = pd.read_csv(f"{RESULTS_DIR}/T5_periods_ew_rie_vs_vsnllw.csv")
_sigP = _P[(_P["CI lo"] > 0) | (_P["CI hi"] < 0)]
_ptxt = "; ".join((f"{r['period'].split(' ', 1)[0]} {r['period'].split(' ', 1)[1]} ({VN[r['mode']].lower()}, ΔVol {r['ΔVol (pp)']:+.2f} pp, " + ("EW-RIE\\* cao hơn" if r["ΔVol (pp)"] > 0 else "EW-RIE\\* thấp hơn") + ")").replace(".", ",") for r in _sigP.to_dict("records"))
_cm = cm.copy(); _n = len(_cm); _TT = {t_: {m: WC[(t_, m)].loc["VS-NL-LW"] for m in MODES} for t_ in WINS}
_strong = [t_ for t_ in WINS if all(_TT[t_][m]["p Holm"] < .05 and _TT[t_][m]["ΔVol (pp)"] < 0 for m in MODES)]
_cnt = lambda a_, b_: int(CNT.loc[a_, b_])
_ndist = {m: int((PWS[m][0]["p_holm"] < .05).sum()) for m in MODES}
md("**Kết luận (v5).** "
   f"(1) So với VS-NL-LW, EW-RIE\\* **ngang về rủi ro** ở cấu hình chuẩn (ΔVol {f2(T3C['long_only'].loc['VS-NL-LW', 'ΔVol (pp)'])} / {f2(T3C['short_ok'].loc['VS-NL-LW', 'ΔVol (pp)'])} pp, chỉ mua / bán khống, p Holm ≈ 1) và trên các ô độ vững: ΔVol < 0 ở {int((_cm['ΔVol (pp)'] < 0).sum())}/{_n} ô, "
   f"thấp hơn có ý nghĩa ở {_cnt('EW-RIE*', 'VS-NL-LW')} ô, cao hơn có ý nghĩa ở {_cnt('VS-NL-LW', 'EW-RIE*')} ô (trong từng ô, p Holm trên 15 cặp). "
   + (f"Chỗ EW-RIE\\* **hơn** rõ: T = {', '.join(map(str, _strong))} (cửa sổ ngắn, q = N/T lớn; VS-NL-LW suy giảm mạnh) ở cả hai chế độ. " if _strong else "Không có T nào EW-RIE\\* hơn VS-NL-LW có ý nghĩa ở cả hai chế độ. ")
   + (f"T = {', '.join(str(t_) for t_ in WINS if t_ not in _strong and all(_TT[t_][m]['ΔVol (pp)'] < 0 for m in MODES))}: ΔVol < 0 ở cả hai chế độ nhưng không có ý nghĩa sau Holm. " if any(t_ not in _strong and all(_TT[t_][m]['ΔVol (pp)'] < 0 for m in MODES) for t_ in WINS) else "")
   + (f"Chỗ **kém/hơn theo giai đoạn** (CI 95% không chứa 0): {_ptxt}. " if len(_sigP) else "")
   + f"Về độ ổn định giữa các ô, hạng Vol (1 = thấp nhất, trên {len(RK)} ô) của EW-RIE\\* nằm trong [{int(RK['EW-RIE*'].min())}; {int(RK['EW-RIE*'].max())}] (trung vị {RK['EW-RIE*'].median():.0f}), của VS-NL-LW trong [{int(RK['VS-NL-LW'].min())}; {int(RK['VS-NL-LW'].max())}] (trung vị {RK['VS-NL-LW'].median():.0f}). "
   + f"(2) Nhóm dẫn đầu **không phân biệt được** về rủi ro: ở cấu hình chuẩn chỉ {_ndist['long_only']}/15 (chỉ mua) và {_ndist['short_ok']}/15 (bán khống) cặp có p Holm < 0,05, đều là cặp với EW-NL-LW; EW-RIE\\*, VS-NL-LW, VS-EW-RIE\\*, EW-WeSpeR, VS-RIE ngang nhau. "
   f"(3) Điểm mạnh của EW-RIE\\* nằm ở **turnover** (ΔTurnover/kỳ trung bình so với VS-NL-LW trên mọi ô: {f2(_cm['ΔTurnover'].mean())}) và **thời gian chạy** (≈ {f2(TT.loc['EW-WeSpeR (nguội)', 100] / TT.loc['EW-RIE*', 100], 0) if 'EW-WeSpeR (nguội)' in TT.index else '8'} lần nhanh hơn EW-WeSpeR ở N = 100), không nằm ở rủi ro; "
   f"Sharpe sau phí của EW-RIE\\* thấp hơn VS-NL-LW ở phí thực tế 0–0,25% (T2c) và chỉ vượt khi phí một chiều > {BEs['long_only']} (chỉ mua) / {BEs['short_ok']} (bán khống).")
