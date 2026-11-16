# ---- 5.4 Cửa sổ T ∈ {120, 250, 500}: Bảng A (12 + 3 bộ VS "đủ T") và heatmap cặp (VS dùng bản "đủ T") ----
WINS = (120, 250, 500); FT = ["VS-NL-LW (đủ T)", "VS-RIE (đủ T)", "VS-EW-RIE* (đủ T)"]
WR = {(t_, m): run_full(dict(CONFIG, WINDOW=t_), lo, M12 + FT) for t_ in WINS for m, lo in MODES.items()}      # một lần gọi ⇒ assert cùng universe, cùng ngày
for (t_, m), d in WR.items():                                                       # bộ không phải VS: trùng hệt lần chạy thường ở cùng T
    ref = run_full(dict(CONFIG, WINDOW=t_), MODES[m], [k for k in M12 if not k.startswith("VS")])
    assert all(np.array_equal(ref["out"][k]["r"].values, d["out"][k]["r"].values) for k in ref["out"])
T17 = pd.concat({(VN[m], f"T = {t_}"): vols(WR[(t_, m)]["out"], M12 + FT) for m in ("short_ok", "long_only") for t_ in WINS}, axis=1)
save(T17, "T5_window_tableA")
kys = ", ".join(f"T = {t_}: {len(WR[(t_, 'long_only')]['ulog'])} kỳ từ {WR[(t_, 'long_only')]['ulog'][0]['date'].date()}" for t_ in WINS)
cap("Bảng", f"Vol (%/năm, gộp) theo cửa sổ T, 12 phương pháp và ba bộ VS \"đủ T\"; in đậm: thấp nhất mỗi cột. Số kỳ ngoài mẫu — {kys}. Không so giữa các cột T.")
display(table_a(T17))
def ft_out(out):            # các cặp có VS dùng bản "đủ T"
    o = dict(out); o.update({k: out[f"{k} (đủ T)"] for k in VSSET}); return o
G54 = {VN[m]: pair_grid({f"T = {t_}": ft_out(WR[(t_, m)]["out"]) for t_ in WINS}, reb_dates=None) for m in ("short_ok", "long_only")}
save_grid(G54, "T5_pairs_window")
pair_heatmap(G54, "12 cặp theo cửa sổ T (VS: bản \"đủ T\")", fname="fig_9_pairs_window")
cap("Hình", "ΔVol (pp/năm) của 12 cặp theo cửa sổ T; các cặp có VS dùng bản \"đủ T\". \\* = p Holm < 0,05 trong từng cột (mô tả). Số liệu: `T5_pairs_window.csv`.")
v_ = lambda t_, m, k: T17.loc[k, (VN[m], f"T = {t_}")]
import json, glob
_fb = {t_: (lambda j: (j['fallback_cols'], j['calls']))(json.load(open(f'{RESULTS_DIR}/logs/prefb_T{t_}_lo_3.json'))) for t_ in WINS}      # đếm từ lần chạy nặng (scripts/run_extra6.py)
md(f"**Kết quả.** Ở T = 120, VS-NL-LW của thầy có Vol {f2(v_(120, 'short_ok', 'VS-NL-LW'))}% / {f2(v_(120, 'long_only', 'VS-NL-LW'))}% (bán khống / chỉ mua) và VS-EW-RIE\\* {f2(v_(120, 'short_ok', 'VS-EW-RIE*'))}% / {f2(v_(120, 'long_only', 'VS-EW-RIE*'))}%, "
   f"trong khi bản \"đủ T\" chỉ {f2(v_(120, 'short_ok', 'VS-NL-LW (đủ T)'))}% / {f2(v_(120, 'long_only', 'VS-NL-LW (đủ T)'))}% và {f2(v_(120, 'short_ok', 'VS-EW-RIE* (đủ T)'))}% / {f2(v_(120, 'long_only', 'VS-EW-RIE* (đủ T)'))}%: "
   f"do `make_vs` bỏ HL\\_VOL = {CONFIG['HL_VOL']} phiên nên chỉ còn {120 - CONFIG['HL_VOL']} phiên cho 100 mã, ma trận gần suy biến. "
   f"Ở T = 250, bản \"đủ T\" lệch bản của thầy: VS-NL-LW {dv(v_(250, 'short_ok', 'VS-NL-LW (đủ T)') - v_(250, 'short_ok', 'VS-NL-LW'))} / {dv(v_(250, 'long_only', 'VS-NL-LW (đủ T)') - v_(250, 'long_only', 'VS-NL-LW'))} pp, "
   f"VS-EW-RIE\\* {dv(v_(250, 'short_ok', 'VS-EW-RIE* (đủ T)') - v_(250, 'short_ok', 'VS-EW-RIE*'))} / {dv(v_(250, 'long_only', 'VS-EW-RIE* (đủ T)') - v_(250, 'long_only', 'VS-EW-RIE*'))} pp. "
   f"Mã không có đủ {CONFIG['HL_VOL']} phiên trước cửa sổ (chưa niêm yết, hoặc toàn 0) được khởi động EWMA trên đầu cửa sổ như `make_vs`: " + ", ".join(f"T = {t_}: {_fb[t_][0]} lượt (kỳ × mã × 3 bộ) trên {_fb[t_][1]} lần ước lượng" for t_ in WINS) + ". "
   f"Cặp EW-RIE\\* − VS-NL-LW (đủ T): " + "; ".join(f"T = {t_}: {dv(G54['Bán khống'][0].xs('EW-RIE* − VS-NL-LW', level=1).iloc[0][f'T = {t_}'])} / {dv(G54['Chỉ mua'][0].xs('EW-RIE* − VS-NL-LW', level=1).iloc[0][f'T = {t_}'])}" for t_ in WINS) + " pp.\n\n"
   f"**Kết luận.** Kết quả \"EW-RIE\\* hơn hẳn VS-NL-LW ở T = 120\" của v5 là do lỗi khởi động EWMA của bộ VS, không dùng; với bản \"đủ T\": {concl_grid(G54)}")
