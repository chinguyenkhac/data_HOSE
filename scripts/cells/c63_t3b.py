# T3b. Bảng benchmark: cùng ngày OOS, cùng universe, REB = 21, COST = 0,25%, hai chế độ, đủ FULL.
TS = {k: TT.loc[k if k != "EW-WeSpeR" else "EW-WeSpeR (nguội)", 100] / 1e3 for k in FULL if (k if k != "EW-WeSpeR" else "EW-WeSpeR (nguội)") in TT.index}   # giây / lần ước lượng, N = 100 (§4.3)
T3B = pd.DataFrame([dict(mode=m, method=k, **metrics(o), **{"Tỷ trọng max %": o["m"]["Tỷ trọng max %"], "Giây/lần ước lượng": TS.get(k, np.nan)})
                    for m in MODES for k, o in OUT0[m].items()])
save(T3B, "T3b_benchmark_full")
for m in MODES: assert T3B[T3B["mode"] == m].set_index("method")["Turnover/kỳ"].idxmin() == "1/N"   # 1/N ít giao dịch nhất
tb = T3B.pivot(index="method", columns="mode", values=["Vol %", "Sharpe sau phí", "Turnover/kỳ", "Số mã hiệu dụng"]).reindex(MAIN)
tb.columns = tb.columns.swaplevel(); tb = tb[[c for m in MODES for c in tb.columns if c[0] == m]]
tb["Giây/lần"] = pd.Series(TS)
cap("Bảng", "Phương pháp chính, cấu hình chuẩn (N = 100, T = 250, h = 60, REB = 21, COST = 0,25%; 118 kỳ, 2.475 phiên OOS). Vol: %/năm, gộp. Giây/lần: một lần ước lượng ma trận N × N (§4.3). Đủ 15 phương pháp: `results_v4/T3b_benchmark_full.csv`.")
show(tb.rename(columns=VN, level=0), 2)
P3 = pd.concat({VN[m]: summarize(OUT0[m], [])[1] for m in MODES}); save(P3, "T3b_periods_full")
cap("Bảng", "Vol (%/năm) theo giai đoạn thị trường, các phương pháp chính. Đủ FULL: `results_v4/T3b_periods_full.csv`.")
show(P3.loc[(slice(None), MAIN), :], 2)
dg = json.load(open(f"{RESULTS_DIR}/logs/diag_std.json")) if os.path.exists(f"{RESULTS_DIR}/logs/diag_std.json") else None
if dg:
    dd = pd.DataFrame(dg["dcc"]); n_per = len(U0)
    print(f"DCC-GARCH: a TB {dd.a.mean():.3f}, b TB {dd.b.mean():.3f}; GARCH dùng dự phòng {int(dd.garch_fail.sum())}/{n_per * CONFIG['N']} lần fit; DCC không hội tụ {int((~dd.dcc_ok).sum())}/{len(dd)} kỳ "
          f"| PCA-auto chọn k = 1/3/5: {[dg['pca_k'].count(k) for k in (1, 3, 5)]} kỳ")
