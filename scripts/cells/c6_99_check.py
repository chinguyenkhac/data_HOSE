# ---- Tự kiểm tra v6 (đạt / không đạt; không sửa cho khớp) ----
ck = {}
REF0 = {"Sample": (14.58, 13.52), "Ledoit-Wolf": (13.63, 13.64), "NL-LW": (13.10, 13.72), "MP-clip": (13.48, 13.67), "RIE": (13.30, 14.02), "VS-NL-LW": (12.49, 12.93),
        "VS-RIE": (12.63, 13.30), "EW-NL-LW": (12.72, 13.12), "EW-RIE (q_eff)": (14.30, 14.76), "EW-WeSpeR": (12.57, 13.05), "EW-RIE*": (12.56, 13.07), "VS-EW-RIE*": (12.43, 12.96)}
ck["Hồi quy Bước 0: Vol 12 phương pháp khớp đến 0,01 (cache run_full)"] = all(abs(OUT0["short_ok"][k]["m"]["Vol %"] - a) < .01 and abs(OUT0["long_only"][k]["m"]["Vol %"] - b) < .01 for k, (a, b) in REF0.items())
ck["Hồi quy Bước 0: §4 của thầy (tính lại) khớp đến 0,01 cho 11 bộ"] = all(abs(RESULTS["short_ok"]["table"].loc[k, "Vol %"] - a) < .01 and abs(RESULTS["long_only"]["table"].loc[k, "Vol %"] - b) < .01 for k, (a, b) in REF0.items() if k != "VS-EW-RIE*")
ck["Mẫu ngoài mẫu: 118 kỳ, 2 475 phiên"] = len(U0) == 118 and len(OUT0["long_only"]["EW-RIE*"]["r"]) == 2475
ck["Bước 1: EW-RIE* − VS-NL-LW ≈ +0,07 / +0,13; EW-RIE* − EW-NL-LW ≈ −0,16 / −0,06"] = (abs(PT["short_ok"].xs("EW-RIE* − VS-NL-LW", level=1)["ΔVol (pp)"].iloc[0] - .07) < .01 and abs(PT["long_only"].xs("EW-RIE* − VS-NL-LW", level=1)["ΔVol (pp)"].iloc[0] - .13) < .01
    and abs(PT["short_ok"].xs("EW-RIE* − EW-NL-LW", level=1)["ΔVol (pp)"].iloc[0] + .16) < .01 and abs(PT["long_only"].xs("EW-RIE* − EW-NL-LW", level=1)["ΔVol (pp)"].iloc[0] + .06) < .01)
ck["Bước 2: bộ không phải VS ở mọi T trùng hệt lần chạy thường; cùng ngày ngoài mẫu (assert ở §5.4)"] = True
ck["Bước 2: không kỳ nào thiếu phiên trước cửa sổ cho bộ VS \"đủ T\""] = len(PRE_SHORT) == 0
ck["T5d: VS đầy đủ trùng VS-NL-LW cấu hình chuẩn (assert)"] = True
ck["Số bảng = 34, số hình = 17"] = (_CAP["Bảng"], _CAP["Hình"]) == (34, 17)
grids = {"T5_pairs_sens": G53, "T5_pairs_window": G54, "T2a_pairs_reb": G2A, "T2b_pairs_zero": G2B}
ck["Mọi heatmap cặp đủ 12 cặp và có CSV"] = all(all(len(D) == 12 for D, _ in G.values()) and os.path.exists(f"{RESULTS_DIR}/{n}.csv") for n, G in grids.items())
ck["Mọi Bảng A đủ 12 hàng"] = all(len(t.reindex(M12).dropna(how="all")) == 12 for t in (TA["short_ok"], TA["long_only"], T19, T24)) and len(T17.loc[M12]) == 12 and all(len(T21.loc[VN[m]]) == 12 for m in MODES)
for k, v in ck.items(): print(("✔ " if v else "✘ ") + k)
print(f"Đếm lỗi số — Newton thất bại (EW-RIE*, §4 và các ô tính lại): {_STATS['fail']}/{_STATS['total']} | EW-WeSpeR dùng dự phòng: {_WSP_SAFE['fallback']}/{_WSP_SAFE['total']}")
