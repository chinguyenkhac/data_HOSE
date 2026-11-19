# ---- Kết quả cấu hình chuẩn cho FULL (từ cache; phần nặng chạy bằng scripts/run_grid.py, mỗi phương pháp một cache) ----
STD = {m: run_full(CONFIG, lo) for m, lo in MODES.items()}
U0 = STD["long_only"]["ulog"]; REB_DATES = [u["date"] for u in U0]; OUT0 = {m: STD[m]["out"] for m in MODES}
for m in MODES:    # run_full tái tạo đúng §4 (EW-WeSpeR: khởi tạo ấm phụ thuộc thứ tự chạy nên chỉ báo sai khác)
    bad = {k: float(np.abs(OUT0[m][k]["r"].values - o["r"].values).max()) for k, o in RESULTS[m]["out"].items()}
    assert all(v < 1e-12 for k, v in bad.items() if k != "EW-WeSpeR"), (m, bad)
    print(f"{VN[m]}: run_full trùng §4 cho 10 bộ (sai lệch tối đa {max(v for k, v in bad.items() if k != 'EW-WeSpeR'):.0e}); EW-WeSpeR lệch tối đa {bad['EW-WeSpeR']:.1e}")
print(f"OOS: {len(U0)} kỳ, {len(OUT0['long_only']['EW-RIE*']['r'])} phiên ({U0[0]['date'].date()} → {OUT0['long_only']['EW-RIE*']['r'].index[-1].date()}) | "
      f"mã đủ ĐK mỗi kỳ {min(u['n_eligible'] for u in U0)}–{max(u['n_eligible'] for u in U0)} (N={CONFIG['N']}, ZERO_MAX={CONFIG['ZERO_MAX']:.0%})")
