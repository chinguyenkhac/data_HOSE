# Đối chiếu EW-WeSpeR (bản numpy của nhóm) với mã gốc PyTorch của tác giả: kết quả từ scripts/wesper_check.py (chạy riêng, nặng; đọc CSV)
_f = [f"{RESULTS_DIR}/T1b_oriol_check_sim.csv", f"{RESULTS_DIR}/T1b_oriol_check_hose.csv"]
if all(os.path.exists(f) for f in _f):
    OS, OH = (pd.read_csv(f) for f in _f)
    g = OS.groupby("h").agg(**{"W1 phổ τ (chuẩn hóa)": ("W1_tau", "median"), "sai lệch ξ, trung vị": ("xi_med", "median"), "sai lệch ξ, lớn nhất": ("xi_max", "max"),
                               "rủi ro GMV/tối ưu – nhóm": ("risk_nhom", "mean"), "rủi ro GMV/tối ưu – gốc": ("risk_oriol", "mean"), "chênh tỷ số rủi ro (TB)": ("risk_diff", "mean"),
                               "s/lần – nhóm": ("sec_nhom", "mean"), "s/lần – gốc": ("sec_oriol", "mean")})
    gh = OH.agg({"W1_tau": "median", "xi_med": "median", "xi_max": "max", "sec_nhom": "mean", "sec_oriol": "mean"}).to_frame("HOSE (12 cửa sổ)").T
    cap("Bảng", "Đối chiếu EW-WeSpeR của nhóm với mã gốc (nlcvbo/wesper): mô hình nhân tố Test 2 (N = 100, T = 250, 20 lần lặp/h) và 12 cửa sổ HOSE. ξ: sai lệch tương đối của trị riêng sau co (cùng chuẩn hóa vết); W1: khoảng cách Wasserstein-1 của phổ quần thể τ chia cho trung bình.")
    show(g, 4); show(gh, 4)
    OK_XI, OK_RISK = (OS.xi_med.median() < 0.05) and (OH.xi_med.median() < 0.05), abs(OS.risk_diff.mean()) < 0.01
    md(f"**Kết quả.** Sai lệch tương đối trung vị của ξ: {f2(100 * OS.xi_med.median(), 2)}% (mô phỏng), {f2(100 * OH.xi_med.median(), 2)}% (HOSE); lớn nhất {f2(100 * OS.xi_max.max(), 1)}% / {f2(100 * OH.xi_max.max(), 1)}%. "
       f"Chênh tỷ số rủi ro GMV so với tối ưu (mô phỏng): {f2(100 * OS.risk_diff.mean(), 2)}%. Tiêu chí đạt (ξ < 5% và chênh rủi ro < 1%): **{'đạt' if OK_XI and OK_RISK else 'không đạt'}** (báo nguyên số, không sửa bản nhóm). "
       f"Thời gian mã gốc {f2(OS.sec_oriol.mean(), 1)} s/lần (mô phỏng) và {f2(OH.sec_oriol.mean(), 1)} s/lần (HOSE) so với {f2(OS.sec_nhom.mean(), 2)} s/lần của bản nhóm.")
else:
    md("**Đối chiếu mã gốc:** chưa có kết quả (xem Ghi chú v4: đã thử gì, lỗi gì). Thay bằng Test 2b với 30 lần lặp có sai số chuẩn (ô dưới).")
