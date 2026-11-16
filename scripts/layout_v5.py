D = ("defs",)
T = lambda s: ("mt", s)
PAIRS_OLD = '''PAIRS = [("EW-RIE*", "EW-RIE (q_eff)"), ("EW-RIE*", "EW-NL-LW"), ("EW-RIE*", "NL-LW"), ("EW-RIE*", "RIE"),
         ("NL-LW", "Ledoit-Wolf"), ("VS-NL-LW", "NL-LW")]'''
PAIRS_NEW = '''PAIRS = [("EW-RIE*", "EW-RIE (q_eff)"), ("EW-RIE*", "EW-NL-LW"), ("EW-RIE*", "NL-LW"), ("EW-RIE*", "RIE"),
         ("NL-LW", "Ledoit-Wolf"), ("VS-NL-LW", "NL-LW"),
         ("EW-RIE*", "VS-NL-LW"), ("EW-RIE*", "EW-WeSpeR"), ("EW-RIE*", "VS-RIE")]      # v4: ba cặp định trước thêm vào bảng chính'''
LAYOUT = [
    ("m", "m00_intro.md"), ("m", "m01_intro.md"),
    # ---------------- 0 ----------------
    ("n", 3), ("n", 4, D), ("n", 5, D), ("f", "c00_helpers.py", D),
    # ---------------- 1 ----------------
    T("## 1. Thư viện: các bộ ước lượng\n\n### 1.1 Bộ của thầy\n\nKhông cần sửa. Mỗi bộ ước lượng nhận ma trận lợi suất `X` (T×N) và trả về ma trận hiệp phương sai N×N."),
    ("n", 7, D), ("n", 8, D), ("n", 9, D), ("n", 10, D),
    ("m", "m12_lib.md"), ("n", 12, D), ("n", 13, D),
    # ---------------- 1b ----------------
    ("n", 14), ("n", 15), ("n", 16),
    T("### Test 2b (bổ sung) — kiểm tra bản sửa EW-NL-LW và WeSpeR\n\nNhư Test 2 của thầy nhưng thêm half-life 15 (N = 100 > T\\_eff ≈ 43), bản NL-LW cũ/mới và EW-WeSpeR."),
    ("n", 18), ("f", "c1b_test2b_res.py"),
    ("m", "m1b_oriol.md"), ("f", "c1b_oriol_view.py"),
    # ---------------- 2 ----------------
    T("## 2. Dữ liệu (T1)\n\nKết quả chuẩn: `P` (giá đóng cửa điều chỉnh, dòng = ngày, cột = mã) và `V` (giá trị giao dịch, cùng kích thước). Nguồn `data_hose/` (vnstock 5.2.2, VCI) 2015-01 → 2026-11, **493 mã có giá gồm cả mã đã hủy niêm yết**; lịch sử niêm yết từ `security_master.csv`."),
    T("### 2.1 Nạp dữ liệu và lọc khoảng niêm yết\n\nCó sẵn `data_hose/` cạnh notebook thì dùng; không thì tải từ GitHub (repo public). Ô nạp của thầy (không sửa) đọc `prices.csv`, `values.csv` ở thư mục hiện hành nên ô đầu đổi thư mục, ô sau đổi lại. `security_master.csv`: mỗi dòng = một giai đoạn niêm yết; giá ngoài khoảng niêm yết bị loại, **mã hủy niêm yết được giữ** trong thời gian còn niêm yết."),
    ("n", 22, D), ("n", 23, D), ("n", 25, D), ("n", 26),
    T("### 2.2 Chất lượng dữ liệu\n\n**Tổng quan:**"), ("n", 28), ("n", 29),
    T("### 2.3 Lịch sử niêm yết và hủy niêm yết\n\n**Theo năm:**"), ("n", 31), ("n", 32),
    T("### 2.4 Chọn ngưỡng lọc đứng giá\n\n**Số mã đủ điều kiện mỗi kỳ tái cân bằng theo ngưỡng lọc đứng giá** (cơ sở chọn `ZERO_MAX`):"), ("n", 34), ("n", 35),
    # ---------------- 3 ----------------
    ("n", 36), ("m", "m31_bt.md"), ("n", 37, D),
    ("m", "m32_zero.md"), ("f", "c32_zero_adj.py", D),
    ("m", "m33_utils.md"), ("f", "c33_utils.py", D), ("f", "c33_tests.py", D), ("f", "c33_full.py", D),
    # ---------------- 4 ----------------
    ("m", "m40_main.md"),
    ("ne", 41, [(PAIRS_OLD, PAIRS_NEW)]), T("### 4.2 Hình\n\nHình cột của thầy (Vol ngoài mẫu từng phương pháp)."), ("n", 42), ("f", "c41_main_res.py"), ("m", "m41_note.md"), ("n", 44),
    ("m", "m43_timing.md"), ("f", "c43_timing.py"), ("f", "c43_timing_res.py"),
    ("m", "m44_pairwise.md"), ("f", "c40_std.py"), ("f", "c44_pairwise.py"),
    # ---------------- 5 ----------------
    ("m", "m50_sens.md"), ("n", 46), ("f", "c51_h_res.py"), ("f", "c51_h_ext.py"),
    ("m", "m52_grid.md"), ("f", "c52g_grid.py"), ("f", "c52g_v3fig.py"),
    ("m", "m53_hlvol.md"), ("f", "c53h_hlvol.py"), ("f", "c53h_fig.py"),
    ("m", "m54_window.md"), ("f", "c54w_window.py"),
    # ---------------- 6 ----------------
    ("m", "m60_group.md"),
    ("m", "m_t2.md"), ("n", 52), ("m", "m_t2a.md"), ("f", "c51_t2a.py"), ("f", "c51_t2a_res.py"), ("f", "c51_t2a_v3fig.py"),
    ("m", "m_t2b.md"), ("f", "c52_t2b.py"), ("f", "c52_t2b_res.py"),
    ("m", "m_t2c.md"), ("f", "c53_t2c.py"), ("f", "c53_t2c_res.py"), ("f", "c53_t2c_ext.py"),
    ("m", "m_t2d.md"), ("f", "c62_delist_defs.py", D), ("f", "c54_t2d.py"), ("f", "c54_t2d_res.py"),
    ("m", "m_t3.md"), ("n", 60), ("m", "m_t3b.md"), ("f", "c63_t3b.py"), ("f", "c63_t3b_res.py"),
    ("m", "m_t3c.md"), ("f", "c64_t3c.py"), ("f", "c64_t3c_res.py"), ("f", "c64_t3c_v3fig.py"),
    ("m", "m_t5.md"), ("n", 70), ("m", "m_t5a.md"), ("f", "c71_t5a.py"), ("f", "c71_t5a_res.py"),
    ("m", "m_t5b.md"), ("f", "c72_t5b.py"), ("f", "c72_t5b_res.py"),
    ("m", "m_t5p.md"), ("f", "c73_t5p.py"),
    ("m", "m_sum.md"), ("f", "c69_summary.py"), ("f", "c69_summary_res.py"), ("f", "c69b_summary_ext.py"), ("f", "c70_conclusion.py"),
    ("f", "c99_selfcheck.py"),
    # ---------------- Ghi chú ----------------
    ("n", 78), ("m", "m_notes_v5.md"), ("m", "m_status_v5.md"), ("m", "m02_changes.md"),
]
