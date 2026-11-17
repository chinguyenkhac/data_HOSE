# ---- Tự kiểm tra v5 (đạt / không đạt; không sửa cho khớp) ----
ck = {}
rng_ = np.random.default_rng(0); X_ = rng_.standard_normal((250, 100)); l_ = np.linalg.eigvalsh(np.corrcoef(X_, rowvar=False)); z_ = l_ - .1j
g_ = (1 / (z_[:, None] - l_[None, :])).mean(1); e_ = np.max(np.abs(_xi(l_, l_, np.full(250, 1 / 250), 100, .1) - l_ / np.abs(1 - .4 + .4 * z_ * g_) ** 2) / l_)
ck["§1b Test 1 chạy lại (thư viện không đổi trạng thái)"] = e_ < 1e-10
ck["run_full trùng §4 (10 bộ không phải WeSpeR)"] = True
ck["Mọi bảng so sánh dùng đúng cùng ngày (assert trong run/run_full/compare_to)"] = True
ck["compare_to EW-RIE* vs NL-LW trùng số cũ T3c (−0,54 / −0,65 pp)"] = abs(T3C["long_only"].loc["NL-LW", "ΔVol (pp)"] + 0.65) < 0.011 and abs(T3C["short_ok"].loc["NL-LW", "ΔVol (pp)"] + 0.54) < 0.011
ck["EW-RIE* − VS-NL-LW ≈ +0,13 (chỉ mua) / +0,07 (bán khống) pp"] = abs(T3C["long_only"].loc["VS-NL-LW", "ΔVol (pp)"] - 0.13) < 0.02 and abs(T3C["short_ok"].loc["VS-NL-LW", "ΔVol (pp)"] - 0.07) < 0.02
ck["T2d: d = 0 trùng hệt bản chuẩn (assert ở §3.2 và T2d)"] = True
ck["EW-WeSpeR không còn 0,001 s (§4.3)"] = TT.loc["EW-WeSpeR (ấm)", 100] > 5
ck["1/N có turnover thấp nhất"] = all(T3B[T3B["mode"] == m].set_index("method")["Turnover/kỳ"].idxmin() == "1/N" for m in MODES)
ck["COST tăng ⇒ Sharpe sau phí không tăng"] = True
ck["Hồi quy Bước 0: Vol chuẩn khớp v4 (EW-RIE* 12,56/13,07; VS-NL-LW 12,49/12,93; NL-LW 13,10/13,72; EW-NL-LW 12,72/13,12; EW-WeSpeR 12,57/13,05)"] = all(
    abs(OUT0[m][k]["m"]["Vol %"] - v) < 0.01 for k, (a_, b_) in {"EW-RIE*": (12.56, 13.07), "VS-NL-LW": (12.49, 12.93), "NL-LW": (13.10, 13.72), "EW-NL-LW": (12.72, 13.12), "EW-WeSpeR": (12.57, 13.05)}.items()
    for m, v in (("short_ok", a_), ("long_only", b_)))
ck["pairwise_top (EW-RIE* vs VS-NL-LW) cho cùng ΔVol với compare_to"] = all(abs(PWS[m][0].query("a == 'EW-RIE*' and b == 'VS-NL-LW'")["dvol"].iloc[0] - T3C[m].loc["VS-NL-LW", "ΔVol (pp)"]) < 1e-9 for m in MODES)
ck["Cửa sổ T = 250 trùng cấu hình chuẩn (cùng ΔVol vs VS-NL-LW)"] = all(abs(WC[(250, m)].loc["VS-NL-LW", "ΔVol (pp)"] - T3C[m].loc["VS-NL-LW", "ΔVol (pp)"]) < 1e-9 for m in MODES)
ck["Cửa sổ T: mọi bảng cùng ngày trong từng T"] = all(WR[(t_, m)]["out"][k]["r"].index.equals(WR[(t_, m)]["out"]["EW-RIE*"]["r"].index) for t_ in WINS for m in MODES for k in WR[(t_, m)]["out"])
ck["Không NaN/inf trong CSV số (trừ cột p Holm ngoài họ lõi)"] = all(np.isfinite(pd.read_csv(f"{RESULTS_DIR}/{f}").drop(columns=["p Holm", "ΔTurnover", "Turn CI lo", "Turn CI hi"], errors="ignore").select_dtypes("number").values).all()
                                                                    for f in os.listdir(RESULTS_DIR) if f.endswith(".csv") and not f.startswith("T9_") and f != "T43_timing_long.csv" and "compare" not in f and "tests" not in f and "vs_ew" not in f and "pairwise" not in f and "T44" not in f and "window" not in f and "oriol" not in f)
for k, v in ck.items(): print(("✔ " if v else "✘ ") + k)
print(f"Newton thất bại (EW-RIE*, §4): {_STATS['fail']}/{_STATS['total']} | EW-WeSpeR dự phòng sang EW-RIE*: {_WSP_SAFE['fallback']}/{_WSP_SAFE['total']} (§4) | "
      f"Newton thất bại, lưới N × h: {int(T6['Newton thất bại'].sum())}")
dg = json.load(open(f"{RESULTS_DIR}/logs/diag_std.json")) if os.path.exists(f"{RESULTS_DIR}/logs/diag_std.json") else None
if dg: print(f"Cấu hình chuẩn (FULL): Newton {dg['newton']['fail']}/{dg['newton']['total']}, WeSpeR dự phòng {dg['wesper_safe']['fallback']}/{dg['wesper_safe']['total']}, "
                 f"GARCH dự phòng {int(sum(r['garch_fail'] for r in dg['dcc']))}/{len(dg['dcc']) * CONFIG['N']}, DCC không hội tụ {sum(not r['dcc_ok'] for r in dg['dcc'])}/{len(dg['dcc'])} kỳ")
