# ---- T3b: Bảng 25 — 15 bộ, cấu hình chuẩn: Vol, Sharpe, Sharpe sau phí, turnover, chi phí giao dịch %/năm, số mã hiệu dụng, tỷ trọng max, ms/lần (Bảng 12) ----
M15 = M12 + ["1/N", "PCA-auto", "DCC-GARCH(1,1)"]
T25 = pd.concat({VN[m]: pd.DataFrame({k: {"Vol %": OUT0[m][k]["m"]["Vol %"], "Sharpe": OUT0[m][k]["m"]["Sharpe"], "Sharpe sau phí": OUT0[m][k]["m"]["Sharpe sau phí"],
                                            "Turnover/kỳ": OUT0[m][k]["m"]["Turnover/kỳ"], "Chi phí GD %/năm": OUT0[m][k]["m"]["Turnover/kỳ"] * CONFIG["COST"] * 252 / CONFIG["REB"] * 100,
                                            "Số mã hiệu dụng": OUT0[m][k]["m"]["Số mã hiệu dụng"], "Tỷ trọng max %": OUT0[m][k]["m"]["Tỷ trọng max %"],
                                            "ms/lần (N = 100)": TT[100].get(k, np.nan)} for k in M15}).T for m in ("short_ok", "long_only")}, names=["Chế độ", "Phương pháp"])
save(T25, "T3b_benchmark")
for m in MODES: assert T25.loc[VN[m], "Turnover/kỳ"].idxmin() == "1/N"            # 1/N ít giao dịch nhất
cap("Bảng", f"Cấu hình chuẩn, 15 bộ ({len(U0)} kỳ, {th(len(OUT0['long_only']['EW-RIE*']['r']))} phiên). Chi phí GD %/năm = turnover × COST × 252/REB. Số mã hiệu dụng = 1/Σw²; tỷ trọng max trung bình theo kỳ. ms/lần lấy từ Bảng 12.")
show(T25, 2)
t_ = lambda m, k, c: T25.loc[(VN[m], k), c]
md("**Kết quả.** " + "; ".join(f"{VN[m]}: Vol thấp nhất {e_(T25.loc[VN[m], 'Vol %'].idxmin())} ({f2(T25.loc[VN[m], 'Vol %'].min())}), Sharpe sau phí cao nhất {e_(T25.loc[VN[m], 'Sharpe sau phí'].idxmax())} ({f2(T25.loc[VN[m], 'Sharpe sau phí'].max(), 3)}); "
   f"chi phí GD EW-RIE\\* {f2(t_(m, 'EW-RIE*', 'Chi phí GD %/năm'))}%/năm so với VS-NL-LW {f2(t_(m, 'VS-NL-LW', 'Chi phí GD %/năm'))}%/năm" for m in ("short_ok", "long_only")) + ".\n\n"
   f"**Kết luận.** Hạng Vol (trong 15) của 1/N, PCA-auto, DCC-GARCH: " + "; ".join(f"{VN[m]} " + ", ".join(str(int(T25.loc[VN[m], 'Vol %'].rank()[k])) for k in ("1/N", "PCA-auto", "DCC-GARCH(1,1)")) for m in ("short_ok", "long_only"))
   + "; năm bộ đầu (chỉ mua): " + ", ".join(e_(k) for k in T25.loc[VN['long_only'], 'Vol %'].nsmallest(5).index) + ".")
