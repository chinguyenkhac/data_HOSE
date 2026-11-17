# BAO_CAO_V5 — EW-RIE\* trên HOSE (pipeline v5)

Notebook: `notebooks/EW_RIE_HOSE_v5.ipynb` (+ `.html`). Dữ liệu: `data_hose/` như v4, không mở rộng. Mọi số trong báo cáo lấy từ `notebooks/results_v5/*.csv`.

## 1. Đối chiếu EW-WeSpeR với mã gốc

- Repo dùng: `github.com/nlcvbo/wesper` (commit `1df4890`, MIT). **Chưa xác minh được đây là repo chính thức**: arXiv 2410.14413 không mở được (mạng chặn) và trang repo không có README/liên kết tới bài báo.
- Chạy bằng `scripts/wesper_check.py` (torch 2.15 CPU); không sửa mã gốc, chỉ bọc 2 chỗ tương thích scipy mới. τ khởi tạo theo mã thí nghiệm của tác giả (trị riêng bản co wLWO), 50 epoch, lr 5e-2.
- **Lỗi của người chạy, đã sửa:** lần đầu dùng khởi tạo mặc định của `fit_from_F` ⇒ loss NaN, ξ lệch ~25%; kết quả bỏ (`results_v5/logs/old_badinit/`), chạy lại.
- Giả lập (mô hình nhân tố Test 2, N = 100, T = 250): số mẫu mỗi h theo bảng (không đủ 20 vì mã gốc chậm 130–900 s/lần; dừng theo giới hạn 3 giờ). Cột: W1 = Wasserstein-1 chuẩn hóa của phổ τ; xi_med = sai lệch tương đối trung vị của ξ; risk_diff = chênh tỷ số rủi ro GMV/tối ưu (gốc so với nhóm).

| h | mẫu | W1 | xi_med | xi_max | risk_diff | giây_gốc | giây_nhóm |
|---|---|---|---|---|---|---|---|
| 15 | 9 | 0,146 | 0,122 | 1,934 | 0,000 | 793 | 19,71 |
| 30 | 16 | 0,158 | 0,115 | 0,826 | 0,004 | 468 | 1,77 |
| 60 | 19 | 0,088 | 0,032 | 0,410 | 0,000 | 232 | 0,90 |

- Mã gốc trả NaN ở 3/47 mẫu giả lập (loại khỏi bảng trên).
- HOSE (N = 100, h = 60): mã gốc trả NaN (loss không hữu hạn) ở 7/12 cửa sổ; 5 cửa sổ chạy được cho sai lệch ξ trung vị 4,4%, lớn nhất 171%.
- Tiêu chí (ξ trung vị < 5% và chênh rủi ro < 1%): KHÔNG đạt (ξ trung vị: h=15: 12,2%, h=30: 11,5%, h=60: 3,2%; chênh rủi ro trung bình đều < 1%).
- Thời gian: mã gốc ≥ 130 s/lần ⇒ không chạy backtest "EW-WeSpeR (Oriol)" (ngưỡng 30 s). Bản nhóm ≈ 0,1–1 s/lần.
- Hình mới: scatter ξ nhóm – ξ gốc (`figs_v5/fig_oriol_xi_scatter.png`).

## 2. Cửa sổ T (§5.4)

| T | q = N/T | q_eff = N·Σw² | T_eff = 1/Σw² | số kỳ OOS | bắt đầu OOS | số phiên OOS |
|---|---|---|---|---|---|---|
| 120 | 0,833 | 0,963 | 103,875 | 120 | 2016-10-05 | 2520 |
| 250 | 0,400 | 0,646 | 154,863 | 118 | 2016-12-08 | 2475 |
| 500 | 0,200 | 0,581 | 172,055 | 111 | 2017-07-12 | 2330 |

ΔVol = Vol(EW-RIE\*) − Vol(đối thủ), pp/năm (cùng T, cùng ngày). Đủ CI, p Holm, 15 bộ: `T6_window_compare_full.csv`.

| mode | rival | 120 | 250 | 500 |
|---|---|---|---|---|
| long_only | EW-NL-LW | -0,06 | -0,06 | -0,10 |
| long_only | EW-WeSpeR | 0,01 | 0,01 | 0,00 |
| long_only | NL-LW | -0,71 | -0,65 | -0,77 |
| long_only | VS-NL-LW | -4,42 | 0,13 | -0,59 |
| short_ok | EW-NL-LW | 0,01 | -0,16 | -0,18 |
| short_ok | EW-WeSpeR | -0,32 | -0,01 | -0,02 |
| short_ok | NL-LW | -0,48 | -0,54 | -0,55 |
| short_ok | VS-NL-LW | -4,79 | 0,07 | -0,66 |

## 3. So sánh mọi cặp trong nhóm dẫn đầu (§4.4)

Cấu hình chuẩn: 3/30 cặp (2 chế độ × 15) có p Holm < 0,05:

| mode | a | b | dvol | p_holm |
|---|---|---|---|---|
| long_only | EW-RIE* | EW-NL-LW | -0,06 | 0,015 |
| long_only | EW-WeSpeR | EW-NL-LW | -0,07 | 0,049 |
| short_ok | EW-RIE* | EW-NL-LW | -0,16 | 0,007 |

Trên 42 ô độ vững (cấu hình × chế độ): số ô mà bộ ở hàng thấp hơn bộ ở cột có ý nghĩa (p Holm < 0,05 trong ô; mô tả):

| index | EW-RIE* | VS-NL-LW | VS-EW-RIE* | EW-WeSpeR | EW-NL-LW | VS-RIE |
|---|---|---|---|---|---|---|
| EW-RIE* | 0 | 2 | 1 | 1 | 30 | 9 |
| VS-NL-LW | 0 | 0 | 1 | 0 | 1 | 7 |
| VS-EW-RIE* | 0 | 3 | 0 | 0 | 1 | 8 |
| EW-WeSpeR | 0 | 2 | 1 | 0 | 10 | 9 |
| EW-NL-LW | 0 | 2 | 1 | 1 | 0 | 7 |
| VS-RIE | 0 | 5 | 1 | 0 | 1 | 0 |

## 4. Đã thêm

- **Bước 1:** hai ô mở đầu chép nguyên văn của thầy, chỉ đổi đoạn Kết quả/Hạn chế (số lấy từ CSV).
- **Kiểm định/so sánh:** `pairwise_top` (15 cặp, Holm 15) ở §4.4 và mọi ô độ vững (`pairwise_all_cells.csv`); cửa sổ T (§5.4); §5.1 theo h cho 6 bộ TOP; §5.2 thêm cột/heatmap EW-WeSpeR, VS-EW-RIE\*; T2c: JKM Sharpe sau phí + phí hòa vốn (`T2c_sharpe_jkm.csv`); ghi chú Test 2b-30.
- **Hình mới:** fig_pairwise_std, fig_window_vol, fig_window_dvol, fig_halflife_top6, fig_hlvol, fig_heat_nh_vs_wesper, fig_rank_top_cells, fig_vol_turnover, fig_oriol_xi_scatter; hình phụ lấy lại từ v3: fig_T2a_heatmap, fig_T3d_vs_ew_rie (trục không từ 0), fig_T6_N_h_grid. `%matplotlib inline` ở §0; chạy nbconvert không đặt MPLBACKEND=Agg.

## 5. Tự kiểm

- Ô code của thầy: 15/18 nguyên vẹn (3 ngoại lệ cho phép: CONFIG, RUN_SENS, PAIRS); ô khác: ['# ======================= CONFIG =======================', 'ESTIMATORS = build_estimators(CONFIG)', 'RUN_SENS = False   # đặt True để chạy (~10–20 phút)'].
- Ô mở đầu 0 chỉ khác ở đoạn Kết quả/Hạn chế: ĐẠT; ô 1 (Phân công nhóm) nguyên văn: ĐẠT.
- Lỗi thực thi trong notebook: 0.
- Ảnh nhúng trong HTML: 27 (≥ 22 lời gọi savefig + 2 ô hình của thầy: ĐẠT); chuỗi 'Figure size' không kèm ảnh: 0.

- ✔ §1b Test 1 chạy lại (thư viện không đổi trạng thái)
- ✔ run_full trùng §4 (10 bộ không phải WeSpeR)
- ✔ Mọi bảng so sánh dùng đúng cùng ngày (assert trong run/run_full/compare_to)
- ✔ compare_to EW-RIE* vs NL-LW trùng số cũ T3c (−0,54 / −0,65 pp)
- ✔ EW-RIE* − VS-NL-LW ≈ +0,13 (chỉ mua) / +0,07 (bán khống) pp
- ✔ T2d: d = 0 trùng hệt bản chuẩn (assert ở §3.2 và T2d)
- ✔ EW-WeSpeR không còn 0,001 s (§4.3)
- ✔ 1/N có turnover thấp nhất
- ✔ COST tăng ⇒ Sharpe sau phí không tăng
- ✔ Hồi quy Bước 0: Vol chuẩn khớp v4 (EW-RIE* 12,56/13,07; VS-NL-LW 12,49/12,93; NL-LW 13,10/13,72; EW-NL-LW 12,72/13,12; EW-WeSpeR 12,57/13,05)
- ✔ pairwise_top (EW-RIE* vs VS-NL-LW) cho cùng ΔVol với compare_to
- ✔ Cửa sổ T = 250 trùng cấu hình chuẩn (cùng ΔVol vs VS-NL-LW)
- ✔ Cửa sổ T: mọi bảng cùng ngày trong từng T
- ✔ Không NaN/inf trong CSV số (trừ cột p Holm ngoài họ lõi)
- Newton thất bại (EW-RIE*, §4): 0/263458 | EW-WeSpeR dự phòng sang EW-RIE*: 0/118 (§4) | Newton thất bại, lưới N × h: 0

## 6. Việc chưa xong và lý do

- Đối chiếu mã gốc: số mẫu giả lập ít hơn 20/h (mã gốc rất chậm); 7/12 cửa sổ HOSE mã gốc trả NaN; chưa xác minh repo chính thức (arXiv bị chặn). Không rõ bên nào lệch ở dữ liệu thật (không có đáp án đúng).
- T4 (lý thuyết), VN30/HNX của T6, T7 (viết bài): ngoài phạm vi v5. 19 mã hủy niêm yết thiếu giá (không tải dữ liệu mới theo yêu cầu).
- Git: commit/push theo nhánh `claude/kind-wozniak-z1fq73`, không merge, không đẩy `main`.
