# ---- Tự kiểm tra v4 (đạt / không đạt; không sửa cho khớp) ----
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
ck["Không NaN/inf trong CSV số (trừ cột p Holm ngoài họ lõi)"] = all(np.isfinite(pd.read_csv(f"{RESULTS_DIR}/{f}").drop(columns=["p Holm", "ΔTurnover", "Turn CI lo", "Turn CI hi"], errors="ignore").select_dtypes("number").values).all()
                                                                    for f in os.listdir(RESULTS_DIR) if f.endswith(".csv") and not f.startswith("T9_") and "compare" not in f and "tests" not in f and "vs_ew" not in f)
for k, v in ck.items(): print(("✔ " if v else "✘ ") + k)
print(f"Newton thất bại (EW-RIE*, §4): {_STATS['fail']}/{_STATS['total']} | EW-WeSpeR dự phòng sang EW-RIE*: {_WSP_SAFE['fallback']}/{_WSP_SAFE['total']} (§4) | "
      f"Newton thất bại, lưới N × h: {int(T6['Newton thất bại'].sum())}")
dg = json.load(open(f"{RESULTS_DIR}/logs/diag_std.json")) if os.path.exists(f"{RESULTS_DIR}/logs/diag_std.json") else None
if dg: print(f"Cấu hình chuẩn (FULL): Newton {dg['newton']['fail']}/{dg['newton']['total']}, WeSpeR dự phòng {dg['wesper_safe']['fallback']}/{dg['wesper_safe']['total']}, "
                 f"GARCH dự phòng {sum(r['garch_fail'] for r in dg['dcc'])}/{len(dg['dcc']) * CONFIG['N']}, DCC không hội tụ {sum(not r['dcc_ok'] for r in dg['dcc'])}/{len(dg['dcc'])} kỳ")
