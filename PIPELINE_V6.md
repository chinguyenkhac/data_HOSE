# EW_RIE_HOSE — bản v6 (gọn, theo khuôn của thầy)

Giao việc cho Claude Code. Đọc hết một lượt rồi làm lần lượt Bước 0 → 9. Người giao việc không trực máy: gặp chỗ chưa rõ thì chọn phương án hợp lý nhất, ghi vào `PROGRESS.md` rồi làm tiếp.

---

## 1. Mục tiêu

Bản v5 có 48 bảng, 23 hình: quá nhiều, mà mỗi bảng lại chỉ hiện 5–6 phương pháp. Bản v6 làm lại cho **gọn và dễ đọc**:

- **Nền là `EW_RIE_HOSE_v3_nho`** (bản thầy đã ưng): giữ bố cục, câu chữ, hình của v3_nho.
- **Khung và ô code của thầy** (`EW_RIE_HOSE.ipynb`) giữ nguyên. Dữ liệu là `data_hose/` hiện tại (HOSE 2015–11/2026). Không mở rộng dữ liệu.
- **Chỉ thêm những gì thầy yêu cầu:**
  1. Cặp **EW-RIE\* vs VS-NL-LW** trong danh sách cặp kiểm định.
  2. Đo **thời gian chạy** các phương pháp họ RIE.
  3. **Độ nhạy lợi suất ngày hủy niêm yết.**
  4. **Đối chiếu EW-WeSpeR với mã gốc của Oriol.**
- **Một thay đổi về cách so sánh:** mọi mục dùng cùng một khuôn (Bảng A và heatmap cặp, mục 3) với đủ 12 phương pháp và 12 cặp định trước.

**Không thêm bảng, hình, mục nào ngoài danh sách ở mục 5.** Nếu thấy cần thêm, ghi đề xuất vào `BAO_CAO_V6.md`, không tự thêm vào notebook.

## 2. Quy tắc

1. Không sửa ô code của thầy. Ngoại lệ đã có: ô CONFIG (thêm `ZERO_MAX`, đường dẫn dữ liệu), cờ `RUN_SENS = True`, thêm cặp vào `PAIRS` ở §4.
2. Không chỉnh tham số để EW-RIE\* thắng. Kết quả ra sao viết đúng vậy.
3. Mọi bảng so sánh dùng đúng cùng ngày ngoài mẫu (giữ assert).
4. Kiểm thử hay đối chiếu không đạt: ghi nguyên số, không sửa cho khớp.
5. Sau mỗi bước: cập nhật `PROGRESS.md`, commit, push lên **nhánh hiện tại**. **Không merge, không đẩy `main`.**
6. Phần nặng chạy bằng script nền, log vào `results_v6/logs/`. Khi chờ: `sleep` 5–10 phút rồi xem 20 dòng cuối log. Không kết thúc lượt khi job còn chạy.
7. Cách dựng notebook tùy chọn (sao v3_nho rồi thêm, hoặc sao v5 rồi cắt). Yêu cầu là kết quả đúng mục lục ở mục 5, và các đoạn Kết quả/Kết luận của v3_nho được giữ nguyên văn ở những chỗ số liệu không đổi. Hàm đã viết ở v4/v5 (`run_full`, bản vá hủy niêm yết, đo thời gian, script lưới) được dùng lại.
8. Kết quả vào `results_v6/`, hình vào `figs_v6/`. Dùng lại cache `results_v5/cache/` nếu còn; nếu không còn thì chạy lại bằng script lưới của v5.

---

## 3. Định nghĩa dùng xuyên suốt (khai báo ở §3.3)

**12 phương pháp (`M12`):** 10 bộ của thầy (Sample, Ledoit-Wolf, NL-LW, MP-clip, RIE, VS-NL-LW, VS-RIE, EW-NL-LW, EW-RIE (q_eff), EW-RIE\*), EW-WeSpeR, VS-EW-RIE\*.
Riêng T3 thêm 1/N, PCA-auto, DCC-GARCH(1,1) ở cấu hình chuẩn.

**12 cặp định trước (`PAIRS12`), mỗi cặp chỉ khác một thành phần.** ΔVol = Vol(bộ trước) − Vol(bộ sau); âm là bộ trước rủi ro thấp hơn.

| Cụm | Câu hỏi | Cặp |
|---|---|---|
| A | Làm sạch đúng lý thuyết có hơn xấp xỉ không? | EW-RIE\* − EW-NL-LW · EW-RIE\* − EW-RIE (q_eff) · EW-RIE\* − EW-WeSpeR |
| B | Trọng số mũ có giúp không? | EW-NL-LW − NL-LW · EW-RIE\* − RIE |
| C | Trước và sau chuẩn hóa biến động (VS) | VS-NL-LW − NL-LW · VS-RIE − RIE · VS-EW-RIE\* − EW-RIE\* |
| D | Trong họ VS, ai hơn? | VS-EW-RIE\* − VS-NL-LW · VS-EW-RIE\* − VS-RIE · VS-RIE − VS-NL-LW |
| E | Trọng số mũ hay VS? (cặp thầy hỏi) | EW-RIE\* − VS-NL-LW |

**Kiểm định:** sai khác phương sai Ledoit–Wolf (2011), bản HAC và bản bootstrap khối (b = 21, M ≥ 2000; p bootstrap là kết quả chính). Hiệu chỉnh Holm trên cả 12 cặp, riêng từng cấu hình và từng chế độ. Dùng `lw_var_test`, `jkm_test`, `block_bootstrap_ci` sẵn có của v3 (chuyển định nghĩa lên §3.3).

**Ba mẫu trình bày:**

- **Bảng A (Vol):** hàng = 12 phương pháp, cột = giá trị tham số đang đổi × chế độ (Bán khống, Chỉ mua), ô = Vol %/năm, 2 chữ số thập phân. In đậm giá trị thấp nhất mỗi cột. Số cột ≤ 8 thì gộp hai chế độ vào một bảng; nhiều hơn thì mỗi chế độ một bảng.
- **Heatmap cặp (thay cho bảng cặp):** hàng = 12 cặp xếp theo cụm (có vạch ngăn giữa các cụm), cột = các cấu hình, hai chế độ đặt cạnh nhau. Mỗi ô ghi ΔVol (pp) và dấu \* nếu p Holm < 0,05. Màu: xanh là bộ đứng trước rủi ro thấp hơn, đỏ là cao hơn, thang màu cắt ở ±1 pp. Cùng phong cách với heatmap N × h của v3. Hàm `pair_grid`, `pair_heatmap` ở Phụ lục A. Số liệu của mỗi heatmap (ΔVol, p Holm) lưu CSV.
- **Bảng kiểm định chi tiết** (chỉ ở T3c): hàm `pair_table` ở Phụ lục A.

Dấu \* trong heatmap chỉ hiệu chỉnh trong từng cột (12 cặp); ghi rõ dưới hình là mô tả. Kết luận chính dựa vào bảng kiểm định chi tiết ở cấu hình chuẩn (T3c).

**Khuôn mỗi mục có kết quả:** Câu hỏi (1 dòng) → bảng/hình → **Kết quả** (1–2 câu, sinh từ code) → **Kết luận** (1 câu). Không in log tiến độ.

---

## 4. Các bước

### Bước 0. Chuẩn bị và hồi quy
Tạo `EW_RIE_HOSE_v6.ipynb`. Chạy cấu hình chuẩn, so Vol (%/năm, bán khống / chỉ mua). Lệch quá 0,01 thì dừng tìm nguyên nhân.

| | Bán khống | Chỉ mua | | Bán khống | Chỉ mua |
|---|---|---|---|---|---|
| Sample | 14,58 | 13,52 | VS-RIE | 12,63 | 13,30 |
| Ledoit-Wolf | 13,63 | 13,64 | EW-NL-LW | 12,72 | 13,12 |
| NL-LW | 13,10 | 13,72 | EW-RIE (q_eff) | 14,30 | 14,76 |
| MP-clip | 13,48 | 13,67 | EW-WeSpeR | 12,57 | 13,05 |
| RIE | 13,30 | 14,02 | EW-RIE\* | 12,56 | 13,07 |
| VS-NL-LW | 12,49 | 12,93 | VS-EW-RIE\* | 12,43 | 12,96 |

Mẫu ngoài mẫu: 118 kỳ, 2 475 phiên, 12/2016–11/2026.

### Bước 1. Tiện ích chung (§3.3)
Khai báo `M12`, `PAIRS12`, `holm`, `turnover_series`, `pair_table`, `pair_grid`, `pair_heatmap` (Phụ lục A). Kiểm tra: cặp EW-RIE\* − VS-NL-LW ở cấu hình chuẩn ra ΔVol ≈ +0,07 (bán khống) / +0,13 (chỉ mua); cặp EW-RIE\* − EW-NL-LW ≈ −0,16 / −0,06.

### Bước 2. Sửa lỗi cửa sổ T (cho §5.4)
**Lỗi ở v5:** `make_vs` của thầy bỏ `HL_VOL` phiên đầu cửa sổ để khởi động EWMA (`Z = Z[hl_vol:]`). Với T = 120, N = 100, các bộ VS chỉ còn 100 phiên cho 100 mã nên ma trận gần suy biến (VS-NL-LW 17,85%, VS-EW-RIE\* 78,62% ở v5). Kết quả "EW-RIE\* hơn hẳn VS-NL-LW ở T = 120" của v5 là do lỗi này, **không dùng**.

**Sửa (không đụng ô của thầy):** thêm biến thể "đủ T" cho ba bộ VS: bộ ước lượng nhận thêm `HL_VOL` phiên ngay **trước** cửa sổ (chỉ dữ liệu quá khứ) để khởi động EWMA, rồi tính tương quan trên đủ T phiên. Universe, ngày tái cân bằng và mọi bộ khác không đổi. Cài bằng kỹ thuật `inspect.getsource` như bản vá lọc đứng giá của v3. Nếu thiếu phiên trước cửa sổ thì dùng số phiên có được và báo số kỳ bị thiếu.

**Đạt khi:** (a) các bộ không phải VS cho kết quả trùng hệt lần chạy thường ở cùng T; (b) cùng ngày ngoài mẫu; (c) ở T = 250, bản "đủ T" lệch bản của thầy ít (báo số).

Chạy T ∈ {120, 250, 500}, N = 100, h = 60, hai chế độ, 12 phương pháp + 3 biến thể "đủ T".

### Bước 3. Đối chiếu Oriol (cho §1b)
Đã có ở v5: `scripts/wesper_check.py`, mã `nlcvbo/wesper`, 50 epoch. Kết quả v5: chênh tỷ số rủi ro GMV giữa hai bản 0,03–0,44%; sai lệch trị riêng sau co ξ trung vị 12,2% (h = 15), 11,5% (h = 30), 3,2% (h = 60); mã gốc trả NaN ở 7/12 cửa sổ HOSE.

**Làm thêm:** chạy mã gốc đến 200 epoch cho 3 mẫu giả lập mỗi h ∈ {15, 30}, ghi sai lệch ξ ở epoch 50, 100, 200 (để biết độ lệch có phải do chưa hội tụ). Chạy nền, song song; giới hạn 3 giờ, quá thì dùng số đã có.

**Viết kết luận theo đúng số:** khớp hay không về rủi ro GMV; ξ lệch bao nhiêu và có giảm theo epoch không; mã gốc không hội tụ ở bao nhiêu cửa sổ HOSE. Ghi rõ repo `nlcvbo/wesper` chưa xác minh được là repo chính thức (người giao việc sẽ tự kiểm).

### Bước 4. Dựng notebook theo mục 5
Lấy số từ cache. Thứ tự và đầu ra đúng như mục 5.

**Phần phải chạy mới** (chưa có trong cache v5): (a) cửa sổ T với VS "đủ T" (Bước 2); (b) lọc đứng giá 5% và 15%, 12 phương pháp, hai chế độ; (c) VS-EW-RIE\* ở các tổ hợp h × HL_VOL chưa có (h ∈ {30, 120} × HL_VOL ∈ {10, 40}); (d) đối chiếu Oriol 200 epoch (Bước 3); (e) hai biến thể VS của T5d, hai chế độ (Bước 4b).

### Bước 4b. Ba phần bổ sung

**(1) §4.4 — Hình 5: phổ trị riêng trước và sau làm sạch.** Mục đích: cho người đọc thấy các bộ làm sạch khác nhau ở đâu.
- Ô trái (giả lập): một mẫu từ mô hình nhân tố của Test 2 (`factor_corr`), N = 100, T = 250, trọng số mũ h = 60. Trục x: trị riêng của tương quan mẫu có trọng số (log). Trục y: trị riêng sau làm sạch (log). Vẽ: đường chéo y = x (không làm sạch), EW-NL-LW, EW-RIE (q_eff), EW-WeSpeR, EW-RIE\*, và **oracle** (v_iᵀ C_thật v_i, chấm đen).
- Ô phải (HOSE): cửa sổ tái cân bằng cuối cùng của cấu hình chuẩn; cùng các đường, không có oracle.
- Màu cố định như các hình khác (EW-RIE\* `#1baf7a`, EW-NL-LW `#eb6834`, EW-WeSpeR `#8e44ad`). Một câu Kết quả: bộ nào bám oracle nhất ở phần khối và ở trị riêng lớn nhất.
- Không chạy backtest.

**(2) §5.5 — Bảng 18: tham số tự chọn từ quá khứ.** Mục đích: trả lời "h = 60 và HL_VOL = 20 chọn thế nào" mà không nhìn trước tương lai.
- Ứng viên: EW-RIE\*, EW-NL-LW với h ∈ {30, 60, 120}; VS-NL-LW với HL_VOL ∈ {10, 20, 40}. N = 100, cùng ngày ngoài mẫu như cấu hình chuẩn.
- Quy tắc: tại mỗi ngày tái cân bằng, lấy 252 phiên lợi suất ngoài mẫu **đã xảy ra trước ngày đó** của ba danh mục ứng viên, chọn tham số có độ lệch chuẩn thấp nhất, dùng lợi suất của danh mục đó cho kỳ tới. Khi chưa đủ 252 phiên lịch sử thì dùng tham số chuẩn. Chỉ ghép chuỗi lợi suất gộp đã có, không chạy backtest mới.
- Bảng (hai chế độ): mỗi bộ một dòng với Vol ở tham số chuẩn, Vol tự chọn, số lần đổi tham số, tỷ lệ số kỳ chọn từng giá trị. Hai dòng kiểm định `pair_table`: EW-RIE\* (tự chọn) − VS-NL-LW (tự chọn); EW-RIE\* (tự chọn) − EW-NL-LW (tự chọn).
- Ghi dưới bảng: phép thử độ nhạy, không thay cấu hình chuẩn; chưa tính phí giao dịch phát sinh khi đổi tham số.

**(3) T5d — Bảng 33: VS giúp nhờ phần chung hay phần riêng?** (gợi ý (a) trong ô T5 của thầy; đây là cách nhóm hiểu gợi ý, ghi rõ trong notebook.)
- Ký hiệu trong một cửa sổ X (T × N): σ_i,t = độ lệch chuẩn EWMA (half-life HL_VOL) của mã i như `ewma_standardize` của thầy; σ_m,t = độ lệch chuẩn EWMA cùng half-life của lợi suất trung bình đều của N mã; ρ_i,t = σ_i,t / σ_m,t.
- Bốn bộ, cùng bộ làm sạch NL-LW, cùng cách bỏ HL_VOL phiên đầu như `make_vs`:
  - NL-LW: không chuẩn hóa.
  - VS chỉ phần chung: Z_i,t = X_i,t / σ_m,t. Σ = Corr_sạch(Z) ∘ (s_i s_j), s_i = độ lệch chuẩn mẫu của cột Z_i. (Hệ số chung σ_m,T² không ảnh hưởng tỷ trọng GMV.)
  - VS chỉ phần riêng: Z_i,t = X_i,t / ρ_i,t. Σ = Corr_sạch(Z) ∘ (ρ_i,T s_i)(ρ_j,T s_j).
  - VS đầy đủ: chính là VS-NL-LW hiện có (phải trùng số cấu hình chuẩn; assert).
- Chạy cấu hình chuẩn, hai chế độ. Bảng: Vol toàn mẫu, Vol theo `PERIODS`, ΔVol so với NL-LW kèm CI và p kiểm định phương sai (Holm trên 3 cặp).
- Câu Kết quả phải nói: phần chung hay phần riêng đóng góp chính; ở giai đoạn nào (đặc biệt 2020Q1).

### Bước 5. Phần mở đầu
Ô tiêu đề và ô Phân công nhóm: chép **nguyên văn** từ `EW_RIE_HOSE.ipynb`. Chỉ sửa:
- Dòng `**Kết quả hiện có (HOSE 12/2016–11/2026, N=100, T=250, h=60):**`
- Bảng: giữ khuôn thầy, các dòng NL-LW, EW-NL-LW, EW-RIE ($q_{\text{eff}}$), EW-WeSpeR, VS-NL-LW, **EW-RIE\***.
- Tối đa 3 câu kết quả, trung tính, số lấy từ bảng T3c: EW-RIE\* so với EW-NL-LW và NL-LW; so với VS-NL-LW và EW-WeSpeR; turnover so với VS-NL-LW.
- Một dòng Hạn chế.

Trạng thái các việc T đưa xuống Ghi chú của nhóm.

### Bước 6. Chạy sạch
`%matplotlib inline` ở §0; không đặt `MPLBACKEND=Agg`. Khởi động lại kernel, chạy từ trên xuống không lỗi. Xuất hai bản: `EW_RIE_HOSE_v6.html` (đủ code) và `EW_RIE_HOSE_v6_gon.html` (`--no-input`).

### Bước 7. Tự kiểm (ghi đạt/không đạt vào `BAO_CAO_V6.md`)
1. Ô code của thầy nguyên vẹn; hai ô mở đầu chỉ khác ở đoạn Kết quả/Hạn chế.
2. Test 1, 2, 2b và mọi assert qua.
3. Hồi quy Bước 0 khớp.
4. Số bảng và hình đúng danh sách mục 5 (đếm), mọi hình đều nhúng trong HTML.
5. Mọi Bảng A có đủ 12 hàng; mọi heatmap cặp có đủ 12 cặp và có CSV kèm theo.
6. Mọi con số trong chữ khớp bảng ngay trên.
7. Đếm lỗi số: Newton thất bại, EW-WeSpeR dùng dự phòng.

### Bước 8. Báo cáo `BAO_CAO_V6.md` (ngắn)
1. Bốn ý trả lời thầy (cặp EW-RIE\* vs VS-NL-LW; thời gian chạy; hủy niêm yết; đối chiếu Oriol), mỗi ý 2–3 dòng kèm số.
2. Một bảng ba cột **hơn / ngang / kém** của EW-RIE\* so với VS-NL-LW, mỗi ô kèm số và nơi lấy số: rủi ro ở cấu hình chuẩn; theo N, h, T, HL_VOL; theo giai đoạn; turnover và chi phí giao dịch; mức tập trung danh mục; thời gian chạy; lợi nhuận và Sharpe. Chỉ ghi "hơn" hoặc "kém" khi có kiểm định hoặc CI ủng hộ; còn lại ghi "ngang".
3. Kết quả tự kiểm; việc chưa xong và lý do; đề xuất bổ sung (nếu có).

### Bước 9. Giao
Commit, push nhánh hiện tại, không merge. **Gửi trực tiếp trong phiên chat:** `EW_RIE_HOSE_v6.ipynb`, hai file HTML, `BAO_CAO_V6.md`.

---

## 5. Mục lục và đầu ra của v6

Ký hiệu nguồn: **[Thầy]** ô của thầy · **[v3]** lấy lại từ v3_nho · **[Mới]**.
Tiêu đề mục đặt gọn như dưới đây (bỏ dấu ▶ và các mã §1c, §3b, T1.0 của v3).

### Mở đầu · Phân công nhóm [Thầy]
Theo Bước 5.

### 0. Cài đặt & cấu hình [Thầy]

### 1. Thư viện: các bộ ước lượng
- 1.1 Bộ của thầy [Thầy]
- 1.2 Bổ sung [v3]: EW-NL-LW khi N > T_eff, EW-WeSpeR, VS-EW-RIE\*

### 1b. Kiểm thử (dữ liệu giả lập)
| Mục | Đầu vào | Đầu ra |
|---|---|---|
| Test 1 [Thầy] | Trọng số đều | Dòng in của thầy |
| Test 2 [Thầy] | Mô hình nhân tố, N = 100, T = 250 | Bảng in của thầy |
| Test 2b [v3] | Như trên, 20 lần lặp | **Bảng 1** |
| Đối chiếu Oriol [Mới] | Giả lập + 12 cửa sổ HOSE, mã gốc | **Bảng 2** (theo h: sai lệch ξ ở epoch 50/100/200, chênh rủi ro GMV, số lần không hội tụ, thời gian) |

### 2. Dữ liệu (T1) [v3]
| Mục | Đầu vào | Đầu ra |
|---|---|---|
| 2.1 Nạp dữ liệu, lọc khoảng niêm yết | 5 file `data_hose/` | Dòng tóm tắt; **Hình 1** số mã có dữ liệu theo năm |
| 2.2 Chất lượng dữ liệu | Bảng giá | **Bảng 3** |
| 2.3 Lịch sử niêm yết và hủy | `security_master.csv` | **Hình 2**, **Hình 3**; **Bảng 4** |
| 2.4 Chọn ngưỡng lọc đứng giá | Bảng giá | **Bảng 5** |

### 3. Danh mục & backtest
- 3.1 `run_backtest` [Thầy] · 3.2 Lọc mã đứng giá [v3] · 3.3 Tiện ích chung [v3 + Mới]

### 4. Chạy chính (cấu hình chuẩn)
| Mục | Đầu vào | Đầu ra |
|---|---|---|
| 4.1 Bảng kết quả [Thầy] | 11 bộ, hai chế độ | **Bảng 6–11**: mỗi chế độ ba bảng của thầy (tổng hợp; Vol theo giai đoạn; CI các cặp). `PAIRS` thêm (EW-RIE\*, VS-NL-LW) và (EW-RIE\*, EW-WeSpeR) |
| 4.2 Hình [Thầy] | Bảng tổng hợp | **Hình 4** |
| 4.3 Thời gian chạy [Mới] | 12 cửa sổ HOSE thật, N = 50/100/150 | **Bảng 12**: ms mỗi lần ước lượng (trung vị), 12 phương pháp + DCC, cột "× NL-LW". EW-WeSpeR đo không qua cache |
| 4.4 Minh họa: phổ trị riêng trước và sau làm sạch [Mới] | Một mẫu giả lập (mô hình nhân tố của Test 2, biết ma trận thật) và một cửa sổ HOSE thật; N = 100, T = 250, h = 60 | **Hình 5**, hai ô (xem Bước 4b) |

### 5. Độ nhạy (T6)
Đổi từng tham số một quanh cấu hình chuẩn. Không so Vol giữa các cột N hay T (mẫu ngoài mẫu khác nhau); ghi số kỳ dưới mỗi cột.

| Mục | Đầu vào | Đầu ra |
|---|---|---|
| 5.1 Half-life [Thầy] | h = 30/60/120 | **Bảng 13** (ô của thầy) |
| 5.2 Bảng A [Mới] | N = 50/100/150 · h = 30/60/120 · HL_VOL = 10/20/40 | **Bảng 14** (bán khống), **Bảng 15** (chỉ mua) |
| 5.3 Heatmap cặp [Mới] | Như 5.2 | **Hình 8**: 12 cặp × 9 cấu hình, hai chế độ |
| 5.3b h × HL_VOL cho VS-EW-RIE\* [Mới] | h = 30/60/120 × HL_VOL = 10/20/40, N = 100 | **Bảng 16**: mỗi chế độ một khối 3 × 3; ô = Vol của VS-EW-RIE\*, kèm ΔVol so với VS-NL-LW cùng HL_VOL (dấu \* theo kiểm định phương sai, Holm trên 9 ô) |
| 5.4 Cửa sổ T [Mới] | T = 120/250/500, bản VS "đủ T" (Bước 2) | **Bảng 17** A: 12 phương pháp + 3 dòng VS "đủ T"; **Hình 9** heatmap cặp theo T (các cặp có VS dùng bản "đủ T"). Một câu nêu VS của thầy ở T = 120 ra sao và vì sao |
| 5.5 Tham số tự chọn từ quá khứ [Mới] | Các chuỗi lợi suất đã có: h = 30/60/120 và HL_VOL = 10/20/40 ở N = 100 | **Bảng 18** (xem Bước 4b): Vol ở tham số chuẩn và ở tham số tự chọn, số lần đổi tham số, kiểm định hai cặp "tự chọn với tự chọn" |
| Lưới N × h | Lưới N × h đầy đủ (cache) | **Hình 6** heatmap của v3, giữ nguyên (Vol EW-RIE\* và ΔVol so với EW-NL-LW); **Hình 7** cùng bố cục 2 × 2: ΔVol của EW-RIE\* so với VS-NL-LW (trái) và so với EW-WeSpeR (phải), đánh \* theo p Holm |

Thứ tự trong mục: 5.1 → Hình 6, Hình 7 → 5.2 → 5.3 → 5.3b → 5.4 → 5.5. HL_VOL chỉ ảnh hưởng ba bộ VS; các hàng khác để trống ở các cột HL_VOL của Bảng A. Ở các cột HL_VOL, heatmap cho biết: VS còn giúp không (cụm C), VS-EW-RIE\* so với VS-NL-LW và VS-RIE (cụm D), và EW-RIE\* (h = 60) so với VS-NL-LW ở từng HL_VOL (cụm E).

### 6. Việc của nhóm
Các ô gợi ý của thầy (`# ---- T2 ----`, `T3`, `T5`) giữ nguyên, code của nhóm ở ô ngay sau.

**T2. Độ vững** — kết luận còn đúng khi đổi cách thực thi?
| Mục | Đầu vào | Đầu ra |
|---|---|---|
| T2a Tái cân bằng, phí | REB = 5/21/63; COST = 0,15/0,25/0,40% | **Bảng 19** A theo REB; **Bảng 20** Sharpe sau phí của 12 bộ theo COST (REB = 21); **Hình 10** heatmap REB × COST của v3; **Hình 11** heatmap cặp theo REB |
| T2b Lọc đứng giá | Không lọc, 5%, 10%, 15%, 20%, 30% (chuẩn vẫn 20%) | **Bảng 21** A; **Hình 12** của v3 (Vol theo mức lọc); **Hình 13** heatmap cặp theo mức lọc |
| T2c Phí thực tế [v3] | Quy ước phí + thuế bán 0,1% | **Bảng 22** Sharpe của 12 bộ |
| T2d Hủy niêm yết [Mới] | Danh sách mã từng kỳ; ngày, lý do hủy; cú sốc 0% / −30% / −100% cho hủy bắt buộc và chưa rõ | **Bảng 23** số lượt hủy trong kỳ nắm giữ theo năm và lý do, kèm một dòng: trong 86 mã hủy có giá, bao nhiêu mã từng vào danh mục ít nhất một kỳ; **Bảng 24** A theo kịch bản. Một câu: thứ hạng có đổi không |

Ghi chú T2b: báo số kỳ và số phiên ngoài mẫu của từng mức lọc. Bảng A và heatmap tính trên **ngày chung** của các mức có ít nhất 60 kỳ; mức nào ít hơn 60 kỳ (có thể là 5%) thì báo riêng trên ngày của chính nó ở một dòng dưới bảng, ghi rõ số kỳ, không gộp vào ngày chung.

**T3. Đối chứng & kiểm định** — chênh lệch có thật không?
| Mục | Đầu vào | Đầu ra |
|---|---|---|
| T3a [v3] | — | Định nghĩa 1/N, PCA, DCC-GARCH |
| T3b [v3] | 15 bộ, cấu hình chuẩn | **Bảng 25**: Vol, Sharpe, Sharpe sau phí, turnover, **chi phí giao dịch %/năm** (= turnover × COST × 252/REB), **số mã hiệu dụng**, **tỷ trọng lớn nhất**, ms/lần (lấy từ Bảng 12) |
| T3c [v3 + Mới] | Lợi suất ngoài mẫu | **Bảng 26** (bán khống), **Bảng 27** (chỉ mua): `pair_table` 12 cặp (ΔVol, CI, p LW-HAC, p LW-boot, p Holm, p JKM, ΔTurnover + CI); **Bảng 28** EW-RIE\* so với 1/N, PCA-auto, DCC (phụ, không vào Holm); **Bảng 29** cặp E với độ dài khối 10/21/42; **Hình 14** ΔVol và CI của 12 cặp, xếp theo cụm, đường dọc tại 0 |

Câu Kết quả của T3c nêu riêng cặp E: ΔVol và p; ΔTurnover và CI; chênh lệch chi phí giao dịch mỗi năm, số mã hiệu dụng, tỷ trọng lớn nhất (lấy từ Bảng 25).

**T5. Vì sao VS giúp trên HOSE?**
| Mục | Đầu vào | Đầu ra |
|---|---|---|
| T5a Trước và sau VS | Cụm C, chia theo `PERIODS` | **Bảng 30** ΔVol và CI theo giai đoạn; **Hình 15** của v3 |
| T5b Dự báo biến động [v3] | Lợi suất từng mã | **Bảng 31**; **Hình 16** của v3 |
| T5c Họ VS và cặp chính [Mới] | Cụm D, E theo `PERIODS`; lợi suất ngoài mẫu hằng ngày | **Bảng 32** ΔVol và CI theo giai đoạn; **Hình 17** ΔVol trượt 1 năm (cửa sổ 252 phiên) của EW-RIE\* − VS-NL-LW theo thời gian, hai chế độ, đường ngang tại 0, tô nền các giai đoạn trong `PERIODS` |
| T5d VS giúp nhờ phần chung hay phần riêng? [Mới] (gợi ý (a) của thầy) | Hai biến thể VS mới, bộ làm sạch NL-LW, cấu hình chuẩn | **Bảng 33** (xem Bước 4b): Vol của NL-LW, VS chỉ phần chung, VS chỉ phần riêng, VS đầy đủ; toàn mẫu và theo `PERIODS`; hai chế độ |

Số theo giai đoạn và đường trượt là mô tả (CI bootstrap, không Holm); ghi rõ dưới bảng và hình.

**Tổng kết theo cụm [Mới]** — kết luận có đúng ngoài cấu hình chuẩn không?
| Mục | Đầu vào | Đầu ra |
|---|---|---|
| Tổng kết | Mọi ô (cấu hình × chế độ) của Hình 8, 9, 11, 13; cấu hình chuẩn chỉ đếm một lần | **Bảng 34**: hàng = 12 cặp theo cụm; cột = số ô, số ô ΔVol < 0, số ô âm có ý nghĩa, số ô dương có ý nghĩa, ΔVol trung vị |

Một câu Kết quả cho từng cụm A–E. Ghi dưới bảng: p-value mang tính mô tả, không hiệu chỉnh xuyên cấu hình. Không thêm bảng xếp hạng hay hình nào khác ở mục này.

### Ghi chú [Thầy] · Ghi chú của nhóm
Hạn chế: 19 mã hủy thiếu giá; chưa có VN30/HNX; vế "không trong GARCH" của T5 chưa mô phỏng; tình trạng đối chiếu Oriol; EW-RIE\* kém ổn định khi N > T_eff; bộ VS của thầy dùng T − HL_VOL phiên; T5d là cách nhóm hiểu gợi ý (a), cần thầy xác nhận; tham số tự chọn (5.5) chưa tính phí do đổi tham số. Trạng thái các việc T.

**Tổng: 34 bảng (7 là đầu ra ô của thầy), 17 hình** (9 hình của v3 và của thầy; 8 hình mới: Hình 5, 7, 8, 9, 11, 13, 14, 17).

### Những thứ của v5 KHÔNG đưa vào v6
§4.4 (15 cặp "nhóm dẫn đầu", ma trận 6 × 6); bảng tứ phân vị và bảng tách bước thời gian; các bảng "6 bộ đầu bảng"; bảng hậu kiểm HL_VOL; heatmap phụ; bảng phí hòa vốn; bảng tỷ trọng mã hủy; hình scatter ξ; Test 2b-30; mục Tổng kết độ vững kiểu v5 (bảng xếp hạng 15 bộ, ma trận số ô, hình hạng, hình Vol–turnover); các bảng chỉ có "phương pháp chính".

---

## Phụ lục A — hàm cặp và heatmap (đặt ở §3.3)

Cần sẵn `lw_var_test`, `jkm_test`, `block_bootstrap_ci`, `CONFIG`, `savefig`. `reb_dates` lấy từ log universe.

```python
M12 = ["Sample", "Ledoit-Wolf", "NL-LW", "MP-clip", "RIE", "VS-NL-LW", "VS-RIE", "EW-NL-LW", "EW-RIE (q_eff)", "EW-WeSpeR", "EW-RIE*", "VS-EW-RIE*"]
PAIRS12 = [("A. Làm sạch", "EW-RIE*", "EW-NL-LW"), ("A. Làm sạch", "EW-RIE*", "EW-RIE (q_eff)"), ("A. Làm sạch", "EW-RIE*", "EW-WeSpeR"),
           ("B. Trọng số mũ", "EW-NL-LW", "NL-LW"), ("B. Trọng số mũ", "EW-RIE*", "RIE"),
           ("C. Trước/sau VS", "VS-NL-LW", "NL-LW"), ("C. Trước/sau VS", "VS-RIE", "RIE"), ("C. Trước/sau VS", "VS-EW-RIE*", "EW-RIE*"),
           ("D. Trong họ VS", "VS-EW-RIE*", "VS-NL-LW"), ("D. Trong họ VS", "VS-EW-RIE*", "VS-RIE"), ("D. Trong họ VS", "VS-RIE", "VS-NL-LW"),
           ("E. EW hay VS", "EW-RIE*", "VS-NL-LW")]

def holm(p):
    p = np.asarray(p, float); o = np.argsort(p); adj = np.minimum(1, np.maximum.accumulate(p[o] * (len(p) - np.arange(len(p)))))
    out = np.empty(len(p)); out[o] = adj; return out

def turnover_series(o, reb_dates, cost=None):
    # turnover từng kỳ, khôi phục từ r − r_net tại các ngày tái cân bằng (kỳ đầu không có turnover)
    return ((o["r"] - o["r_net"]).reindex(reb_dates[1:]) / (cost or CONFIG["COST"])).values

def pair_table(out, pairs=PAIRS12, reb_dates=None, block=21, M=2000, B=2000, seed=0):
    # Bảng kiểm định chi tiết: mỗi cặp (a, b) chỉ khác một thành phần. ΔVol = Vol(a) − Vol(b); < 0 ⇒ a rủi ro thấp hơn.
    rows = []
    for g, a, b in pairs:
        assert out[a]["r"].index.equals(out[b]["r"].index), f"khác mẫu: {a}, {b}"
        ra, rb = out[a]["r"].values, out[b]["r"].values; lo, hi = block_bootstrap_ci(ra, rb, block=block)
        d, se, p_hac, p_bt = lw_var_test(ra, rb, block=block, M=M)
        row = {"Cụm": g, "Cặp": f"{a} − {b}", "ΔVol (pp)": (ra.std() - rb.std()) * np.sqrt(252) * 100, "CI lo": lo, "CI hi": hi,
               "p LW-HAC": p_hac, "p LW-boot": p_bt, "p JKM": jkm_test(ra, rb)[1]}
        if reb_dates is not None:                                   # chênh lệch turnover/kỳ + CI bootstrap theo kỳ (ghép cặp)
            dt = turnover_series(out[a], reb_dates) - turnover_series(out[b], reb_dates); dt = dt[~np.isnan(dt)]; rng = np.random.default_rng(seed)
            bs = dt[rng.integers(0, len(dt), (B, len(dt)))].mean(1)
            row.update({"ΔTurnover": dt.mean(), "Turn CI lo": np.percentile(bs, 2.5), "Turn CI hi": np.percentile(bs, 97.5)})
        rows.append(row)
    T = pd.DataFrame(rows); T.insert(T.columns.get_loc("p LW-boot") + 1, "p Holm", holm(T["p LW-boot"].values))   # Holm trên cả 12 cặp
    return T.set_index(["Cụm", "Cặp"])

def pair_grid(outs, **kw):
    # outs = {nhãn cột: out}. Trả về D (ΔVol, pp) và P (p Holm trên 12 cặp, riêng từng cột); hàng = 12 cặp theo cụm.
    D, P = {}, {}
    for lab, out in outs.items():
        T = pair_table(out, **kw); D[lab], P[lab] = T["ΔVol (pp)"], T["p Holm"]
    return pd.DataFrame(D), pd.DataFrame(P)

def pair_heatmap(grids, title, vmax=1.0, fname=None):
    # grids = {"Bán khống": (D, P), "Chỉ mua": (D, P)}. Mỗi ô ghi ΔVol; * nếu p Holm < 0,05. Xanh: bộ đứng trước rủi ro thấp hơn; đỏ: cao hơn.
    n = len(grids); D0 = next(iter(grids.values()))[0]
    fig, axes = plt.subplots(1, n, figsize=(2.6 + n * (1.6 + 0.75 * D0.shape[1]), 0.42 * len(D0) + 1.6), sharey=True)
    for ax, (mode, (D, P)) in zip(np.atleast_1d(axes), grids.items()):
        ax.imshow(D.values, cmap="RdYlGn_r", vmin=-vmax, vmax=vmax, aspect="auto")       # màu cắt ở ±vmax, số trong ô là giá trị thật
        for i in range(D.shape[0]):
            for j in range(D.shape[1]):
                v, p = D.values[i, j], P.values[i, j]
                if np.isnan(v): continue
                ax.text(j, i, f"{v:+.2f}".replace(".", ",").replace("-", "−") + ("*" if p < .05 else ""), ha="center", va="center", fontsize=8,
                        color="white" if abs(v) > .7 * vmax else "black", fontweight="bold" if p < .05 else "normal")
        ax.set_xticks(range(D.shape[1])); ax.set_xticklabels(D.columns, fontsize=8); ax.set_title(mode, fontsize=10)
        cl = D.index.get_level_values(0)
        for i in range(1, len(cl)):
            if cl[i] != cl[i - 1]: ax.axhline(i - .5, color="black", lw=1)                # vạch ngăn giữa các cụm
    a0 = np.atleast_1d(axes)[0]; a0.set_yticks(range(len(D0))); a0.set_yticklabels([f"{c[:1]} | {p}" for c, p in D0.index], fontsize=8)
    fig.suptitle(title + "  (ΔVol, pp; * = p Holm < 0,05)", fontsize=11); plt.tight_layout()
    if fname: savefig(fig, fname)
    return fig
```

Cách dùng: `g = {"Bán khống": pair_grid(outs_short), "Chỉ mua": pair_grid(outs_long)}` với `outs_* = {"N=50": out, "N=100": out, ...}`, rồi `pair_heatmap(g, "12 cặp theo N, h, HL_VOL", fname="fig_pairs_sens")`.

Đã chạy thử trên lợi suất giả lập với các hàm kiểm định của v3 (12 cặp ≈ 1,5 s với M = 500) và đã vẽ thử heatmap. Chưa chạy trên dữ liệu thật. Giữ M ≥ 2000: với 12 cặp, p Holm nhỏ nhất đạt được là 12/(M + 1).
