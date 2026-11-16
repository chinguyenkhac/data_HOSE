# Mục lục v6 (PIPELINE_V6 mục 5). ("n", i[, tags]) = ô của v3_nho (gồm ô của thầy); ("t", i) = ô của thầy (EW_RIE_HOSE.ipynb); ("f", file) = ô mới; ("m", file) / ("mt", text) = markdown
D = ("defs",)
T = lambda s: ("mt", s)
PAIRS_OLD = '''PAIRS = [("EW-RIE*", "EW-RIE (q_eff)"), ("EW-RIE*", "EW-NL-LW"), ("EW-RIE*", "NL-LW"), ("EW-RIE*", "RIE"),
         ("NL-LW", "Ledoit-Wolf"), ("VS-NL-LW", "NL-LW")]'''
PAIRS_NEW = '''PAIRS = [("EW-RIE*", "EW-RIE (q_eff)"), ("EW-RIE*", "EW-NL-LW"), ("EW-RIE*", "NL-LW"), ("EW-RIE*", "RIE"),
         ("NL-LW", "Ledoit-Wolf"), ("VS-NL-LW", "NL-LW"),
         ("EW-RIE*", "VS-NL-LW"), ("EW-RIE*", "EW-WeSpeR")]      # nhóm: thêm hai cặp (EW-RIE* vs VS-NL-LW, EW-RIE* vs EW-WeSpeR)'''
LAYOUT = [
    ("m", "m6_intro0.md"), ("t", 1),
    # ---------------- 0 ----------------
    ("n", 3), ("n", 4, D), ("n", 5, D), ("f", "c00_helpers6.py", D),
    # ---------------- 1 ----------------
    ("n", 6), T("### 1.1 Bộ của thầy"), ("n", 7, D), ("n", 8, D), ("n", 9, D), ("n", 10, D),
    ("m", "m6_12_lib.md"), ("n", 12, D), ("n", 13, D),
    # ---------------- 1b ----------------
    ("n", 14), T("**Test 1** (trọng số đều ⇒ EW-RIE\\* trùng RIE cổ điển)."), ("n", 15), T("**Test 2** (mô hình nhân tố, N = 100, T = 250)."), ("n", 16),
    ("m", "m6_test2b.md"), ("f", "c6_test2b.py"),
    ("m", "m6_oriol.md"), ("f", "c6_oriol.py"),
    # ---------------- 2 ----------------
    ("m", "m6_20_data.md"),
    T("### 2.1 Nạp dữ liệu, lọc khoảng niêm yết\n\nCó sẵn `data_hose/` cạnh notebook thì dùng; không thì tải từ GitHub (repo public). Ô nạp của thầy đọc `prices.csv`, `values.csv` ở thư mục hiện hành nên ô đầu đổi thư mục, ô sau đổi lại. `security_master.csv`: mỗi dòng = một giai đoạn niêm yết; giá ngoài khoảng niêm yết bị loại, **mã hủy niêm yết được giữ** trong thời gian còn niêm yết."),
    ("n", 22, D), ("n", 23, D), ("n", 25, D), ("n", 26), ("f", "c6_21_cap.py"),
    T("### 2.2 Chất lượng dữ liệu"), ("f", "c6_22_cap.py"), ("n", 28), ("n", 29),
    T("### 2.3 Lịch sử niêm yết và hủy niêm yết"), ("f", "c6_23_listing.py"), ("n", 32),
    T("### 2.4 Chọn ngưỡng lọc đứng giá"), ("f", "c6_24_cap.py"), ("n", 34), ("n", 35),
    # ---------------- 3 ----------------
    ("n", 36), T("### 3.1 `run_backtest` (của thầy)"), ("n", 37, D),
    ("m", "m6_32_zero.md"), ("f", "c32_v6.py", D),
    ("m", "m6_33_utils.md"), ("f", "c33_utils.py", D), ("f", "c33_tests6.py", D), ("f", "c33_full.py", D), ("f", "c33_v6.py", D),
    # ---------------- 4 ----------------
    ("n", 40), T("### 4.1 Bảng kết quả"), ("f", "c6_41_cap.py"), ("ne", 41, [(PAIRS_OLD, PAIRS_NEW)]),
    T("### 4.2 Hình"), ("n", 42), ("f", "c6_42_cap.py"), ("n", 43), ("n", 44), ("f", "c6_std.py", D),
    ("m", "m6_43_timing.md"), ("f", "c6_43_timing.py"),
    ("m", "m6_44_spectrum.md"), ("f", "c6_44_spectrum.py"),
    # ---------------- 5 ----------------
    ("m", "m6_50_sens.md"), T("### 5.1 Half-life (ô của thầy)"), ("f", "c6_51_cap.py"), ("n", 46), ("n", 47),
    ("m", "m6_5nh.md"), ("f", "c6_5nh_figs.py"),
    ("m", "m6_52.md"), ("f", "c6_52_tableA.py"),
    ("m", "m6_53.md"), ("f", "c6_53_pairs.py"),
    ("m", "m6_53b.md"), ("f", "c6_53b_hhv.py"),
    ("m", "m6_54.md"), ("f", "c6_54_window.py"),
    ("m", "m6_55.md"), ("f", "c6_55_auto.py"),
    # ---------------- 6 ----------------
    ("n", 48),
    ("m", "m6_t2.md"), ("n", 52), ("m", "m6_t2a.md"), ("f", "c6_t2a.py"),
    ("m", "m6_t2b.md"), ("f", "c6_t2b.py"),
    ("m", "m6_t2c.md"), ("f", "c6_t2c.py"),
    ("m", "m6_t2d.md"), ("f", "c62_delist_defs.py", D), ("f", "c6_t2d.py"),
    ("m", "m6_t3.md"), ("n", 60), ("m", "m6_t3a.md"), ("m", "m6_t3b.md"), ("f", "c6_t3b.py"),
    ("m", "m6_t3c.md"), ("f", "c6_t3c.py"),
    ("m", "m6_t5.md"), ("n", 70), ("m", "m6_t5a.md"), ("f", "c6_t5a.py"),
    ("m", "m6_t5b.md"), ("f", "c6_t5b.py"),
    ("m", "m6_t5c.md"), ("f", "c6_t5c.py"),
    ("m", "m6_t5d.md"), ("f", "c6_t5d.py"),
    ("m", "m6_sum.md"), ("f", "c6_sum.py"),
    ("f", "c6_99_check.py"),
    # ---------------- Ghi chú ----------------
    ("n", 78), ("m", "m6_notes.md"),
]
