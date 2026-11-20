# ---- Kết quả cấu hình chuẩn cho mọi phương pháp (đọc cache run_full; dùng ở §4.4, §5, §6) ----
STD = {m: run_full(CONFIG, lo) for m, lo in MODES.items()}
STD0 = STD["long_only"]; U0 = STD0["ulog"]; REB_DATES = [u["date"] for u in U0]; OUT0 = {m: STD[m]["out"] for m in MODES}
if "RESULTS" in globals():           # run_full tái tạo đúng §4 của thầy (EW-WeSpeR: khởi tạo ấm phụ thuộc thứ tự chạy nên chỉ báo sai khác)
    for m in MODES:
        bad = {k: float(np.abs(OUT0[m][k]["r"].values - o["r"].values).max()) for k, o in RESULTS[m]["out"].items()}
        assert all(v < 1e-12 for k, v in bad.items() if k != "EW-WeSpeR"), (m, bad)
