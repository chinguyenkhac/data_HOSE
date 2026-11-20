# EW_RIE_HOSE — pipeline v4 (chạy qua đêm)

Giao việc cho Claude Code. Đọc hết một lượt, làm lần lượt Bước 0 → 11. Người giao việc ngủ, không trả lời được: gặp chỗ chưa rõ thì chọn phương án hợp lý nhất, ghi vào `BAO_CAO_V4.md` rồi làm tiếp.

---

## 1. Bối cảnh

**Câu hỏi của cả notebook.** Trên HOSE, EW-RIE\* có cho danh mục phương sai nhỏ nhất (GMV) rủi ro ngoài mẫu thấp hơn các bộ ước lượng khác không, và ở điều kiện nào?

**Hai file nguồn người dùng gửi lại:**

| File | Vai trò |
|---|---|
| `EW_RIE_HOSE.ipynb` | **Bản mẫu của thầy.** Khuôn trình bày: §0 Cài đặt · §1 Thư viện · §1b Kiểm thử · §2 Dữ liệu · §3 Backtest · §4 Chạy chính · §5 Độ nhạy · §6 Việc của nhóm (T2, T3, T5) · Ghi chú |
| `EW_RIE_HOSE_v3_nho.ipynb` | **Bản nhóm đang làm, thầy đã khá ưng.** Tái sử dụng toàn bộ: code, dữ liệu `data_hose/`, cache, kết quả. Chỉ chỉnh tiếp theo khuôn của thầy, không viết lại từ đầu. Nếu trên nhánh có bản mới hơn thì dùng bản đó |

**Cấu hình chuẩn (không đổi):** N = 100, WINDOW = 250, REB = 21, COST = 0,25%, HL_EW = 60, HL_VOL = 20, ZERO_MAX = 20%. Mỗi thí nghiệm chỉ đổi đúng một tham số.

**Các việc T hỏi gì:**

| Việc | Câu hỏi | Đổi gì |
|---|---|---|
| §4 | Ở cấu hình chuẩn, ai rủi ro thấp nhất? | không đổi |
| T3 | Có hơn đối thủ mạnh không, chênh lệch có thật không? | thêm đối thủ, kiểm định |
| T2 | Còn đúng khi đổi cách thực thi? | REB, COST, lọc đứng giá, lợi suất ngày hủy niêm yết |
| T6 (§5) | Còn đúng khi đổi thiết lập ước lượng? | N, h, HL_VOL |
| T5 | Vì sao chuẩn hóa biến động (VS) giúp? | tách tác động VS |

**v3 còn thiếu:** (1) T2, T6 chỉ so 3 bộ, vắng VS-NL-LW; (2) kiểm định phương sai Ledoit–Wolf chỉ có ở T3; (3) cặp EW-RIE\* vs VS-NL-LW nằm riêng ở T3d, không có trong bảng chính (thầy nhận xét); (4) thời gian chạy đo sai, EW-WeSpeR ghi 0,001 s do trúng cache (thầy nhận xét); (5) chưa đối chiếu WeSpeR với code gốc (thầy gợi ý); (6) lợi suất sau hủy niêm yết đặt 0, chưa thử độ nhạy (thầy gợi ý); (7) trình bày: đánh số lẫn lộn, T6 sai mục, hình chưa có số.

---

## 2. Quy tắc

1. **Không sửa ô của thầy.** Mã các ô trong `EW_RIE_HOSE.ipynb` giữ nguyên từng ký tự. Ngoại lệ đã có ở v3: ô CONFIG, cờ `RUN_SENS`. Ngoại lệ mới duy nhất: thêm cặp vào `PAIRS` (Bước 1). Phần nhóm đặt ở ô mới.
2. **Trung thực.** Không chỉnh tham số để EW-RIE\* thắng. Cặp so sánh chính định trước (mục 3).
3. **Không nhìn trước tương lai.** Lọc và chọn mã chỉ dùng cửa sổ quá khứ. Lưới tham số chỉ là phân tích độ nhạy.
4. **Cùng mẫu.** Trong một bảng mọi phương pháp dùng đúng cùng ngày; giữ assert của `run()`.
5. **Không tự sửa cho khớp.** Kiểm thử hay đối chiếu không đạt thì ghi nguyên số, làm tiếp.

---

## 3. Vận hành

**Ghi tiến độ.** Sau **mỗi bước** cập nhật `PROGRESS.md`: bước đã xong · bước đang làm · quyết định đã tự chọn · lệnh nào đang chạy nền · việc tiếp theo. Đầu mỗi lượt làm việc, đọc `PROGRESS.md` trước rồi làm tiếp từ đó. Nhờ vậy bị ngắt do hết hạn mức thì lần sau nhặt lại đúng chỗ.

**Tự tiếp tục.** Ghi `RUNNING.lock` (thời điểm) mỗi 10 phút khi đang làm. Nếu thấy `RUNNING.lock` mới (dưới 20 phút) mà không phải do chính mình thì thoát, tránh hai phiên chạy chồng. Nếu phiên có tính năng tác vụ định kỳ, tạo một tác vụ chạy mỗi giờ với nội dung "đọc `PROGRESS.md`, kiểm tra khóa, làm tiếp bước dở"; nếu không có thì bỏ qua.

**Chạy nặng.**
- `run()` có cache. Gọi theo từng phương pháp một rồi ghép kết quả, để thêm phương pháp không làm tính lại phương pháp khác.
- Bộ không dùng trọng số mũ không phụ thuộc h: trong lưới N × h chỉ tính một lần cho mỗi N.
- Dùng `tag` cho mọi biến thể dữ liệu (kịch bản hủy niêm yết) để không trúng nhầm cache.
- Phần nặng viết thành script (`scripts/run_grid.py`) dùng đúng các hàm của notebook, chạy nền, ghi log vào `results_v4/logs/`, mỗi tiến trình `OMP_NUM_THREADS=1`.
- Khi chờ: `sleep` 5–10 phút, xem 20 dòng cuối log. **Không kết thúc lượt khi job còn chạy.**
- DCC-GARCH chậm: cấu hình nào mất quá 45 phút vì DCC thì bỏ DCC khỏi cấu hình đó và ghi rõ. Ở cấu hình chuẩn luôn có DCC.
- Một bước lỗi không gỡ được trong 30 phút: ghi vào báo cáo, sang bước sau.

**Mốc giờ.** Nhóm A (Bước 1–4) và `BAO_CAO_V4.md` bản tạm xong trước 3h sáng. Nhóm B làm tiếp theo thứ tự. Đến 7h30 dừng làm mới: chạy sạch, xuất file, viết báo cáo cuối.

**Giao kết quả.**
- Commit sau mỗi bước, push lên **nhánh hiện tại**. **Không merge, không đẩy lên `main`**: người giao việc sẽ duyệt.
- Khi xong (hoặc đến 7h30), **gửi trực tiếp trong phiên chat** (đính kèm): `EW_RIE_HOSE_v4.ipynb`, `EW_RIE_HOSE_v4.html`, `BAO_CAO_V4.md`. Nếu không đính kèm được thì để ở thư mục gốc repo và nêu đường dẫn.

---

## 4. Bước 0 — chuẩn bị

- Sao `EW_RIE_HOSE_v3_nho.ipynb` thành `EW_RIE_HOSE_v4.ipynb`; v3 để nguyên. Kết quả vào `results_v4/`, hình `figs_v4/`, cache `results_v4/cache/` (chép cache cũ sang).
- Chạy v4 chưa sửa gì, so **bảng hồi quy** (Vol %/năm, cấu hình chuẩn). Lệch quá 0,01 thì dừng tìm nguyên nhân.

| Phương pháp | Bán khống | Chỉ mua |
|---|---|---|
| NL-LW | 13,10 | 13,72 |
| EW-NL-LW | 12,72 | 13,12 |
| EW-RIE (q_eff) | 14,30 | 14,76 |
| EW-WeSpeR | 12,57 | 13,05 |
| EW-RIE\* | 12,56 | 13,07 |
| VS-NL-LW | 12,49 | 12,93 |

OOS: 118 kỳ, 12/2016–11/2026. EW-RIE\* − VS-NL-LW ở v3: +0,07 / +0,13 pp, p Holm = 1.

- Khai báo ở §3.3 (tiện ích chung):
  - **`FULL`** (chạy ở mọi thí nghiệm): Sample, Ledoit-Wolf, NL-LW, MP-clip, RIE, VS-NL-LW, VS-RIE, EW-NL-LW, EW-RIE (q_eff), EW-WeSpeR, EW-RIE\*, PCA-auto, DCC-GARCH, 1/N, thêm biến thể VS-EW-RIE\* (hàm `est_vs_ew_rie` của T3d).
  - **`CORE5`** (họ kiểm định chính, định trước): EW-RIE\* so với NL-LW, EW-NL-LW, EW-WeSpeR, VS-NL-LW. **Cặp quan trọng nhất: EW-RIE\* vs VS-NL-LW.**
  - **`compare_to`** (Phụ lục A): mỗi cặp báo ΔVol (pp), CI 95% bootstrap khối, kiểm định phương sai Ledoit–Wolf 2011 (p HAC, **p bootstrap = kết quả chính**), p Holm (chỉ trên `CORE5`), p Jobson–Korkie, ΔTurnover kèm CI. ΔVol < 0 là EW-RIE\* rủi ro thấp hơn.
  - Chuyển `hac`, `lw_var_test`, `jkm_test` từ T3c lên §3.3 để mọi mục dùng.

---

## 5. Nhóm A — bốn việc thầy yêu cầu

**Bước 1. Cặp EW-RIE\* vs VS-NL-LW vào bảng chính** (§4, T3c)
- §4: thêm vào `PAIRS` ba cặp `("EW-RIE*","VS-NL-LW")`, `("EW-RIE*","EW-WeSpeR")`, `("EW-RIE*","VS-RIE")`. Không sửa gì khác trong ô.
- T3b: thêm các bộ còn thiếu để T3 có đủ `FULL`. T3c: thay vòng lặp bằng `compare_to` trên `FULL`, một bảng duy nhất, dòng `CORE5` in đậm.
- Gộp T3d vào T3c; hai cặp VS-EW-RIE\* thành bảng phụ ngay dưới. Sửa các câu tóm tắt tự sinh và chú thích "Holm cho 4 so sánh".
- Thay hình cột T3d bằng hình ΔVol kèm CI 95% (điểm + thanh sai số, đường dọc tại 0).
- *Đạt khi:* có dòng EW-RIE\* vs VS-NL-LW, ΔVol ≈ +0,07 / +0,13 pp; số cũ ở T3c không đổi (trừ p Holm, vì họ kiểm định còn 4 cặp; ghi chú).

**Bước 2. Thời gian chạy (§4.3, mới)** — code ở Phụ lục B
- Đo một lần ước lượng ma trận N×N (ms, không gồm giải GMV): 12 cửa sổ HOSE thật, N ∈ {50, 100, 150, 200}, mỗi lần gọi 3 lần lấy nhỏ nhất, báo trung vị và [Q1; Q3].
- Mọi bộ trong `FULL`. EW-WeSpeR gọi thẳng, không qua cache, tách "nguội" và "ấm". DCC không qua `_DCC_CACHE`, chỉ đo 3 cửa sổ. EW-RIE\*: báo "lần đầu" riêng, và bảng phụ tách thời gian theo bước (N = 100).
- Đầu ra: bảng (hàng = phương pháp, cột = N, bội số so với NL-LW, độ dốc log–log), một hình log–log, ghi CPU và số luồng BLAS. Sửa cột "Giây/lần ước lượng" ở T3b lấy từ bảng này.
- *Đạt khi:* EW-WeSpeR chậm hơn EW-NL-LW rõ rệt; EW-RIE\* ở N = 100 cỡ ≈ 0,12 s.

**Bước 3. Đối chiếu EW-WeSpeR với code gốc của Oriol (§1b, bổ sung)**
- Bài báo: Oriol, *WeSpeR*, arXiv:2410.14413, kèm bản PyTorch trên GitHub của tác giả. Tìm repo, ghi URL và commit đã dùng; cài `torch` bản CPU.
- Quy đổi quy ước trọng số trước khi so (bản nhóm dùng Σw = 1), ghi rõ phép quy đổi.
- Đầu vào chung (C, w): giả lập mô hình nhân tố của Test 2 (N = 100, T = 250, h ∈ {15, 30, 60}, 20 lần lặp, biết ma trận thật) và 12 cửa sổ HOSE.
- So: phổ quần thể τ (khoảng cách Wasserstein-1 chuẩn hóa), trị riêng sau co ξ (sai lệch tương đối trung vị và lớn nhất), rủi ro GMV so với tối ưu (chỉ giả lập).
- *Đạt khi:* sai lệch tương đối trung vị của ξ < 5% và chênh tỷ số rủi ro GMV < 1%. Không đạt thì báo nguyên số, không sửa bản nhóm.
- Nếu bản gốc chạy dưới 30 s/lần: thêm dòng "EW-WeSpeR (Oriol)" vào bảng T3 và bảng thời gian chạy. Nếu không tìm hoặc không chạy được: ghi đã thử gì, lỗi gì; thay bằng Test 2b với 30 lần lặp có sai số chuẩn, giữ câu "chưa đối chiếu mã gốc" ở Ghi chú.

**Bước 4. T2d (mới): độ nhạy lợi suất ngày hủy niêm yết**
- Hiện trạng: mã hủy trong kỳ nắm giữ có lợi suất 0 các ngày còn lại (giả định bán đúng giá cuối).
- 4a. Đếm (log universe + `security_master.csv`): bao nhiêu lượt mã trong universe bị hủy **trong kỳ nắm giữ**, theo lý do (`bat_buoc`, `hop_nhat`, `tu_nguyen`, `chuyen_san`, `chua_ro`) và năm, kèm tỷ trọng của từng phương pháp. Nếu bằng 0, ghi rõ và chỉ làm 4d.
- 4b. Cài đặt: không sửa `run_backtest` của thầy. Dùng kỹ thuật `inspect.getsource` của v3 (§3.2): sau dòng tính `Y`, cộng ma trận điều chỉnh `d` tại (ngày giao dịch đầu tiên sau ngày có giá cuối, mã bị hủy). Không đưa cú sốc vào `P` (bộ lọc `MAX_ABS_RET` sẽ xóa nó và làm bẩn cửa sổ ước lượng sau). Kiểm tra: `d = 0` trùng hệt bản chuẩn.
- 4c. Kịch bản (áp cho `bat_buoc` và `chua_ro`; lý do khác giữ 0): S0 = 0% (như hiện tại) · S1 = −30% (mức quy ước hủy do hoạt động kém, Shumway 1997) · S2 = −100% (cận xấu nhất). Thêm một dòng S1 áp cho mọi lý do.
- 4d. Giới hạn: 19 mã hủy thiếu giá không bao giờ vào universe; báo bao nhiêu mã hủy từ 12/2016, ghi là hạn chế còn lại.
- Đầu ra: bảng số lượt hủy; Vol của `FULL` theo kịch bản; `compare_to` mỗi kịch bản (ít nhất `CORE5`); một hình ΔVol (EW-RIE\* − VS-NL-LW) theo kịch bản. Nêu rõ thứ hạng và kết luận kiểm định có đổi không.

**Sau Bước 4:** commit, cập nhật `PROGRESS.md`, viết `BAO_CAO_V4.md` bản tạm.

---

## 6. Nhóm B — so sánh đầy đủ ở mọi mục

**Bước 5. §5.1, §5.2 (T6): half-life h và lưới N × h**
- Ô `RUN_SENS` của thầy giữ nguyên (mục 5.1). Chuyển T6 về §5.2 (đúng bảng phân công của thầy).
- Lưới N ∈ {50, 100, 150} × h ∈ {30, 60, 120}, hai chế độ, chạy `FULL`. Thêm N = 200 nếu mọi kỳ còn đủ mã (không thì bỏ, ghi số kỳ).
- Mỗi ô lưới: Vol mọi phương pháp, **xếp hạng**, `compare_to`. Bảng chính: Vol EW-RIE\*, phương pháp đứng đầu, ΔVol so với VS-NL-LW kèm CI và p. Ghi q_eff của từng (N, h).
- Hình: heatmap ΔVol (EW-RIE\* − VS-NL-LW) theo N × h, hai chế độ, đánh \* ô có p Holm < 0,05. Heatmap cũ (so với EW-NL-LW) giữ làm hình phụ.
- Viết lại câu "thấp nhất ở 18/18 tổ hợp". Không so Vol tuyệt đối giữa các N (mỗi N có tập kỳ OOS riêng).

**Bước 6. §5.3 (mới): HL_VOL**
- VS-NL-LW, VS-RIE, VS-EW-RIE\* với HL_VOL ∈ {10, 20, 40}, cấu hình chuẩn, hai chế độ.
- Bảng: Vol theo HL_VOL; ΔVol của EW-RIE\* (h = 60) so với VS-NL-LW ở từng HL_VOL kèm CI và p. Thêm một dòng "mỗi bên ở tham số tốt nhất", ghi rõ là hậu kiểm, chỉ để tham khảo.

**Bước 7. T2a, T2b: độ vững với đủ phương pháp**
- T2a: REB ∈ {5, 21, 63} × COST ∈ {0,15%; 0,25%; 0,40%}, `FULL` (DCC có thể bỏ ở REB = 5 theo quy tắc 45 phút). Vol chỉ phụ thuộc REB; Sharpe sau phí theo REB × COST; `compare_to` mỗi REB kèm ΔTurnover. Thay heatmap cũ (ba cột Vol trùng nhau) bằng đường Vol theo REB và đường Sharpe sau phí theo COST.
- Kiểm định turnover: ở v3 EW-RIE\* có turnover/kỳ 0,48 so với 0,75 của VS-NL-LW (chỉ mua), 0,94 so với 1,41 (bán khống). Báo chênh lệch có ý nghĩa không và mức COST hòa vốn Sharpe sau phí.
- T2b: ba mức lọc (không lọc, 20%, 10%), thêm 30%; `FULL`; so trên ngày chung; `compare_to` mỗi mức. Chuẩn vẫn 20%. Dời chú giải hình khỏi vùng che số.
- T2c: giữ nguyên, mở rộng bảng Sharpe cho `CORE5` và EW-RIE\*.

**Bước 8. T5: bổ sung**
- Giữ T5a, T5b. T5a dùng `compare_to` thay CI đơn lẻ.
- Thêm bảng và hình ΔVol (EW-RIE\* − VS-NL-LW) theo từng giai đoạn trong `PERIODS`, hai chế độ, kèm CI. Nêu: VS-NL-LW hơn EW-RIE\* ở giai đoạn nào, kém ở giai đoạn nào.

**Bước 9. Bảng tổng kết độ vững (mới, cuối §6)**
- Gom mọi cấu hình đã chạy (chuẩn, N × h, HL_VOL, REB, lọc đứng giá, kịch bản hủy niêm yết) × hai chế độ: mỗi phương pháp trong `FULL` đứng đầu bao nhiêu ô, thứ hạng trung bình và xấu nhất.
- Riêng EW-RIE\* vs VS-NL-LW: số ô ΔVol < 0; số ô thấp hơn / cao hơn có ý nghĩa (p Holm < 0,05); ΔTurnover trung bình.
- Ghi chú: p-value trong lưới mang tính mô tả (không hiệu chỉnh xuyên lưới); kết luận chính dựa vào cấu hình chuẩn và xu hướng nhất quán theo N, h.

---

## 7. Nhóm C — trình bày theo khuôn của thầy

**Bước 10. Sắp lại notebook**

Giữ khung và số mục của thầy. Phần nhóm thêm ghi "(bổ sung)" trong tiêu đề; bỏ dấu ▶ và các mã §1c, §3b, T1.0, T1.1.

- **Mở đầu:** tóm tắt đúng khuôn thầy (Câu hỏi → Phương pháp → Đối chứng → Kết quả → Hạn chế → Tài liệu), bảng Phân công thêm cột trạng thái
- **0** Cài đặt & cấu hình
- **1** Thư viện: 1.1 bộ của thầy · 1.2 (bổ sung) EW-NL-LW khi N > T_eff, EW-WeSpeR, VS-EW-RIE\* · **1b** Kiểm thử: Test 1, 2 của thầy, Test 2b, đối chiếu WeSpeR
- **2** Dữ liệu (T1): nạp và lọc khoảng niêm yết · chất lượng · lịch sử niêm yết/hủy · chọn ngưỡng lọc đứng giá
- **3** Backtest: 3.1 của thầy · 3.2 lọc đứng giá · 3.3 tiện ích chung (`FULL`, `CORE5`, `compare_to`, hàm kiểm định)
- **4** Chạy chính: 4.1 bảng · 4.2 hình · 4.3 thời gian chạy
- **5** Độ nhạy (T6): 5.1 h · 5.2 N × h · 5.3 HL_VOL
- **6** Việc của nhóm: T2 (a, b, c, d) · T3 (a, b, c) · T5 (a, b, giai đoạn) · Tổng kết độ vững
- **Ghi chú** của thầy + Ghi chú v4

Các ô gợi ý của thầy ở §6 (`# ---- T2 ----`, `T3`, `T5`) giữ nguyên, code nhóm ở ô ngay sau.

**Khuôn mỗi mục T** (chữ tối đa 5 dòng): Câu hỏi → Làm gì → Bảng/Hình → Kết quả → Kết luận.

**Bảng, hình:**
- Đánh số "Bảng n", "Hình n" xuyên suốt, mỗi cái một dòng chú thích (mẫu, cấu hình, đơn vị); tiêu đề hình không chứa mã T.
- Bảng chính chỉ hiện `CORE5` + EW-RIE\*; bảng đủ `FULL` lưu CSV và nhắc tên file trong chú thích.
- Vol 2 chữ số thập phân, p 3 chữ số.
- Màu cố định ở mọi hình: EW-RIE\* `#1baf7a`, NL-LW `#2a78d6`, EW-NL-LW `#eb6834`, EW-WeSpeR `#8e44ad`, VS-NL-LW `#e0a800`; bộ còn lại xám `#9aa0a6`. Một cách viết tên: "VS-EW-RIE\*".
- Hình cột của thầy ở §4 giữ nguyên. Ẩn log tiến độ (đưa vào file log), mỗi ô chỉ còn bảng và hình cần đọc.

**Bước 11. Chạy sạch, xuất file, viết tóm tắt**
- Khởi động lại kernel, chạy từ trên xuống (`jupyter nbconvert --to notebook --execute`) không lỗi; xuất `EW_RIE_HOSE_v4.html`.
- Viết lại phần tóm tắt đầu notebook theo khuôn thầy, số lấy từ kết quả mới: bảng Kết quả (NL-LW, EW-NL-LW, EW-RIE (q_eff), EW-WeSpeR, VS-NL-LW, EW-RIE\*); một đoạn nói thẳng EW-RIE\* hơn, ngang hay kém VS-NL-LW, ở N, h nào, khác biệt nằm ở rủi ro, turnover hay thời gian chạy; hạn chế (19 mã hủy thiếu giá, kết quả T2d, tình trạng đối chiếu WeSpeR, EW-RIE\* khi N > T_eff, T4 và phần còn lại của T6 để sau).
- Mọi con số trong ô Kết quả, Kết luận phải khớp bảng ngay trên; ưu tiên sinh câu từ code như v3.

---

## 8. Kiểm thử và báo cáo

**Kiểm thử** (ghi đạt / không đạt vào `BAO_CAO_V4.md`):
1. Ô của thầy nguyên vẹn (so từng ô với `EW_RIE_HOSE.ipynb`, in ô khác và lý do).
2. Test 1, 2, 2b và các assert sẵn có đều qua.
3. Bảng hồi quy (Bước 0) khớp đến 0,01.
4. Mọi bảng so sánh cùng ngày; in số kỳ, số ngày.
5. `compare_to` cho EW-RIE\* vs NL-LW ở cấu hình chuẩn trùng số cũ của T3c (ΔVol −0,54 / −0,65 pp).
6. T2d với `d = 0` trùng hệt bản chuẩn.
7. EW-WeSpeR không còn 0,001 s.
8. Báo số lần Newton thất bại (`_STATS`), EW-WeSpeR dùng dự phòng (`_WSP_SAFE`), GARCH dùng dự phòng (`DCC_LOG`).
9. Chạy sạch từ đầu không lỗi; HTML xuất được.
10. Chữ khớp số.

**`BAO_CAO_V4.md`** (người dùng gửi thầy sáng hôm sau), ngắn:
1. Trả lời bốn ý của thầy, mỗi ý 2–4 dòng kèm số: (a) EW-RIE\* vs VS-NL-LW · (b) thời gian chạy · (c) đối chiếu WeSpeR · (d) độ nhạy hủy niêm yết.
2. Bảng kiểm định chính ở cấu hình chuẩn (`CORE5`, hai chế độ).
3. Bảng tổng kết độ vững.
4. Đoạn 3–5 câu: EW-RIE\* hơn, ngang, kém VS-NL-LW ở đâu.
5. Việc đã xong / chưa xong và lý do; quyết định đã tự chọn; tổng thời gian chạy; chỗ repo khác với mô tả ở đây.

---

## Phụ lục A — hàm so sánh chung

Đặt ở §3.3, sau `hac`, `lw_var_test`, `jkm_test`, `block_bootstrap_ci`. `reb_dates` lấy từ log universe: `[u["date"] for u in d["ulog"]]`.

```python
CORE5 = ["NL-LW", "EW-NL-LW", "EW-WeSpeR", "VS-NL-LW"]            # đối thủ lõi của EW-RIE* (họ Holm chính, định trước)

def holm(p):
    p = np.asarray(p, float); o = np.argsort(p); adj = np.minimum(1, np.maximum.accumulate(p[o] * (len(p) - np.arange(len(p)))))
    out = np.empty(len(p)); out[o] = adj; return out

def turnover_series(o, reb_dates, cost=None):
    # turnover từng kỳ, khôi phục từ r − r_net tại các ngày tái cân bằng (kỳ đầu không có turnover)
    return ((o["r"] - o["r_net"]).reindex(reb_dates[1:]) / (cost or CONFIG["COST"])).values

def compare_to(out, target="EW-RIE*", rivals=None, reb_dates=None, block=21, M=2000, B=2000, seed=0):
    # So target với từng đối thủ trên CÙNG chuỗi ngày. ΔVol < 0 ⇒ target rủi ro thấp hơn.
    rivals = rivals or [k for k in out if k != target]; ra = out[target]["r"].values; rows = {}
    for b in rivals:
        assert out[b]["r"].index.equals(out[target]["r"].index), f"khác mẫu: {b}"
        rb = out[b]["r"].values; lo, hi = block_bootstrap_ci(ra, rb, block=block)
        d, se, p_hac, p_bt = lw_var_test(ra, rb, block=block, M=M)
        row = {"Vol": rb.std() * np.sqrt(252) * 100, "ΔVol (pp)": (ra.std() - rb.std()) * np.sqrt(252) * 100, "CI lo": lo, "CI hi": hi,
               "Δlog σ²": d, "p LW-HAC": p_hac, "p LW-boot": p_bt, "p JKM": jkm_test(ra, rb)[1], "lõi": b in CORE5}
        if reb_dates is not None:                                   # chênh lệch turnover/kỳ + CI bootstrap theo kỳ (ghép cặp)
            dt = turnover_series(out[target], reb_dates) - turnover_series(out[b], reb_dates); rng = np.random.default_rng(seed)
            bs = dt[rng.integers(0, len(dt), (B, len(dt)))].mean(1)
            row.update({"ΔTurnover": dt.mean(), "Turn CI lo": np.percentile(bs, 2.5), "Turn CI hi": np.percentile(bs, 97.5)})
        rows[b] = row
    C = pd.DataFrame(rows).T.infer_objects(); C["p Holm"] = np.nan
    core = C.index[C["lõi"].astype(bool)]
    if len(core): C.loc[core, "p Holm"] = holm(C.loc[core, "p LW-boot"].values.astype(float))   # Holm chỉ trên họ lõi
    return C
```

Đã chạy thử trên chuỗi lợi suất giả lập với các hàm kiểm định của v3 (khoảng 0,4 s mỗi cặp). Chưa chạy trên dữ liệu thật.

## Phụ lục B — đo thời gian chạy (§4.3)

Cần sẵn `P`, `V`, `CONFIG`, `ESTIMATORS`, `make_ew`, `ew_weights`, `ew_corr`, `ew_wesper_corr`, `_WSP`, `_NULL_CACHE`, `_STATS`, `_xi`, `_xi_outliers`, `_null_spectrum`. Bổ sung các bộ T3 (PCA-auto, DCC, 1/N) vào `TIME_EST`; DCC phải gọi không qua `_DCC_CACHE`.

```python
N_GRID, K_WIN, REPS = (50, 100, 150, 200), 12, 3

def timing_windows(N, K=K_WIN, cfg=CONFIG):
    W = cfg["WINDOW"]; R = np.log(P).diff(); R = np.expm1(R.mask(R.abs() > cfg["MAX_ABS_RET"], 0.0)); Xs = []
    for s in range(W + 1, len(R) - 1, cfg["REB"]):
        win = R.iloc[s - W:s]; ok = (win.notna().mean() >= .95) & P.iloc[s - 1].notna()
        ok &= (win == 0).mean() <= cfg.get("ZERO_MAX", 1.0)
        if ok.sum() < N: continue
        tick = V.iloc[s - W:s].loc[:, ok].median().sort_values(ascending=False).index[:N]
        Xs.append(win[tick].fillna(0).values)
    return [Xs[i] for i in np.linspace(0, len(Xs) - 1, min(K, len(Xs))).astype(int)]     # theo thứ tự thời gian

def _ms(f, X, reps):
    best = np.inf
    for _ in range(reps):
        t = time.perf_counter(); f(X); best = min(best, time.perf_counter() - t)
    return best * 1e3

def _wsp_cold_call(C, w):
    _WSP["warm"].clear(); return ew_wesper_corr(C, w)

hl = CONFIG["HL_EW"]
TIME_EST = {k: f for k, f in ESTIMATORS.items() if k != "EW-WeSpeR"}
TIME_EST["EW-WeSpeR (nguội)"] = make_ew(_wsp_cold_call, hl)
TIME_EST["EW-WeSpeR (ấm)"] = make_ew(ew_wesper_corr, hl)

rows = []
for N_ in N_GRID:
    Xs = timing_windows(N_)
    if not Xs: continue
    _NULL_CACHE.clear(); t = time.perf_counter(); ESTIMATORS["EW-RIE*"](Xs[0])         # lần đầu: gồm cả mô phỏng phổ null
    rows.append(dict(N=N_, method="EW-RIE* (lần đầu)", ms=(time.perf_counter() - t) * 1e3, q1=np.nan, q3=np.nan, K=1))
    for k, f in TIME_EST.items():
        warm = k.endswith("(ấm)")
        if warm: _WSP["warm"].clear(); f(Xs[0])                                          # kỳ 0 chỉ để tạo khởi tạo ấm
        v = np.array([_ms(f, X, 1 if warm else REPS) for X in (Xs[1:] if warm else Xs)])
        rows.append(dict(N=N_, method=k, ms=np.median(v), q1=np.percentile(v, 25), q3=np.percentile(v, 75), K=len(v)))
TIMING = pd.DataFrame(rows)
TT = TIMING.pivot(index="method", columns="N", values="ms")
nref = 100 if 100 in TT else TT.columns[0]; TT = TT.loc[TT[nref].sort_values().index]
TT[f"× NL-LW (N={nref})"] = TT[nref] / TT.loc["NL-LW", nref]
n0, n1 = TIMING.N.min(), TIMING.N.max()
TT["bậc theo N"] = np.log(TT[n1] / TT[n0]) / np.log(n1 / n0)                                # độ dốc log–log
display(TT.round(2))

def profile_ew_rie(X, hl=hl):                                                               # EW-RIE* tốn thời gian ở bước nào
    w = ew_weights(len(X), hl); C, _ = ew_corr(X, w); N = len(C); eta = 1 / np.sqrt(N); T = {}
    t = time.perf_counter(); lam, Vv = np.linalg.eigh(C); lam = np.maximum(lam, 1e-10); T["phân rã riêng (eigh)"] = time.perf_counter() - t
    null = _null_spectrum(N, w); s2 = np.median(lam) / np.median(null); D = lam[:, None] - lam[None, :]
    dens = (eta / (D**2 + eta**2)).sum(1) - 1 / eta; out = np.where(dens < 0.1 / eta)[0]; bulk = np.setdiff1d(np.arange(N), out)
    t = time.perf_counter(); _xi(lam, lam[bulk], w, N, eta); T["Newton – phần khối"] = time.perf_counter() - t
    t = time.perf_counter(); _xi_outliers(lam, out, w, N) if len(out) else None; T["Newton – ngoại lai"] = time.perf_counter() - t
    t = time.perf_counter(); _xi(null, lam[bulk] / s2, w, N, eta); T["hiệu chỉnh N hữu hạn"] = time.perf_counter() - t
    return T
_s0 = dict(_STATS)                                                                           # không làm bẩn bộ đếm Newton
prof = pd.DataFrame([profile_ew_rie(X) for X in timing_windows(100)]).median() * 1e3
_STATS.update(_s0)
display(pd.DataFrame({"ms": prof, "%": prof / prof.sum() * 100}).round(1))
```

Đã chạy thử trên dữ liệu giả lập, chưa chạy trên `data_hose`. Số tham khảo cỡ độ lớn ở N = 100 (không dùng trong báo cáo): NL-LW ≈ 1,5 ms; EW-RIE\* ≈ 135 ms; EW-WeSpeR bản numpy ≈ 800–1.100 ms.
