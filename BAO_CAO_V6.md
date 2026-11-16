# BAO_CAO_V6 — EW-RIE\* trên HOSE (bản gọn theo khuôn của thầy)

Notebook `notebooks/EW_RIE_HOSE_v6.ipynb` (+ `EW_RIE_HOSE_v6.html` đủ code, `EW_RIE_HOSE_v6_gon.html` không code). HOSE 12/2016–11/2026, 118 kỳ, 2 475 phiên ngoài mẫu; N = 100, T = 250, h = 60, HL_VOL = 20, REB = 21, COST = 0,25%. Mọi số lấy từ `notebooks/results_v6/*.csv`. ΔVol = Vol(bộ trước) − Vol(bộ sau), pp/năm; hai số = bán khống / chỉ mua.

## 1. Bốn ý trả lời thầy

**(1) Cặp EW-RIE\* vs VS-NL-LW** (T3c: Bảng 26–27, 29, Hình 14; Tổng kết: Bảng 34). ΔVol +0,07 / +0,13 pp, p bootstrap 0,755 / 0,573, p Holm (12 cặp) 1,00 / 1,00: **ngang về rủi ro**. Trên 32 ô độ nhạy/độ vững (N, h, HL_VOL, T, REB, lọc đứng giá), cặp này có ý nghĩa ở 0 ô (ΔVol < 0 ở 13 ô, trung vị +0,07). EW-RIE\* giao dịch ít hơn có ý nghĩa: ΔTurnover −0,47 / −0,27 mỗi kỳ (CI [−0,52; −0,41] / [−0,30; −0,24]).

**(2) Thời gian chạy** (§4.3, Bảng 12; N = 100, ms mỗi lần ước lượng, trung vị 12 cửa sổ HOSE, 1 luồng BLAS). NL-LW 1,4, EW-NL-LW 1,6, VS-NL-LW 2,6, **EW-RIE\* 155**, **EW-WeSpeR 1211** (gọi thẳng, khởi tạo lại mỗi lần, không qua cache), DCC-GARCH 1927. EW-RIE\* nhanh hơn EW-WeSpeR 7,8 lần, chậm hơn NL-LW 113 lần.

**(3) Lợi suất ngày hủy niêm yết** (T2d: Bảng 23–24). 6 lượt mã trong universe bị hủy trong kỳ nắm giữ. Cú sốc 0% / −30% / −100% (và −30% mọi lý do) làm Vol đổi tối đa 0,093 pp; thứ hạng 12 bộ không đổi. Hạn chế: 19 mã hủy thiếu giá không bao giờ vào universe.

**(4) Đối chiếu EW-WeSpeR với mã gốc** (§1b, Bảng 2). Repo `nlcvbo/wesper` **chưa xác minh được là repo chính thức** (người giao việc tự kiểm). Rủi ro GMV khớp: chênh trung bình h = 15: +0,03%, h = 30: +0,44%, h = 60: +0,04%. Trị riêng sau co ξ lệch trung vị (50 epoch): h = 15: 12,2%, h = 30: 11,5%, h = 60: 3,2%, HOSE (h = 60): 4,4%. Chạy tiếp 3 mẫu đến 200 epoch: h = 15: 8,5% → 3,6% → 5,2%; h = 30: 14,0% → 7,5% → 4,4% (một phần độ lệch do mã gốc chưa hội tụ ở 50 epoch). Mã gốc không hội tụ (NaN) ở 7/12 cửa sổ HOSE.

## 2. EW-RIE\* so với VS-NL-LW: hơn / ngang / kém

Chỉ ghi "hơn" hoặc "kém" khi có kiểm định hoặc CI ủng hộ (riêng thời gian chạy: đo trực tiếp).

| Tiêu chí | Hơn | Ngang | Kém | Nguồn |
|---|---|---|---|---|
| Rủi ro, cấu hình chuẩn |  | ΔVol +0,07 / +0,13 pp, p Holm 1,00 / 1,00 |  | Bảng 26–27 |
| Rủi ro theo N, h, HL_VOL, T, REB, lọc đứng giá |  | có ý nghĩa ở 0/32 ô; ΔVol < 0 ở 13 ô; trung vị +0,07 pp (mô tả) |  | Hình 8, 9, 11, 13; Bảng 34 |
| Rủi ro theo giai đoạn | 2022 Sụt giảm (chỉ mua, −1,02) | các giai đoạn còn lại (CI chứa 0) | 2020Q1 COVID (bán khống, +1,79); 2020Q1 COVID (chỉ mua, +1,97) | Bảng 32, Hình 17 (CI bootstrap, mô tả) |
| Turnover và chi phí giao dịch | ΔTurnover −0,47 / −0,27/kỳ (CI không chứa 0); chi phí GD 2,83 / 1,43 so với 4,22 / 2,23 %/năm |  |  | Bảng 25–27 |
| Mức tập trung danh mục |  | số mã hiệu dụng 8,5 / 9,5 so với 7,7 / 8,1; tỷ trọng max 22,2 / 25,6% so với 25,7 / 30,7% (chưa kiểm định) |  | Bảng 25 |
| Thời gian chạy |  |  | 155 ms so với 2,6 ms mỗi lần (N = 100; đo trực tiếp, chênh ~60 lần, không cần kiểm định) | Bảng 12 |
| Lợi nhuận và Sharpe |  | Sharpe gộp 0,08 / 0,10 so với 0,25 / 0,33; sau phí -0,14 / -0,01 so với -0,08 / 0,16; p JKM 0,265 / 0,052 (không có ý nghĩa) |  | Bảng 22, 25–27 |

## 3. Tự kiểm (Bước 7)

1. Ô code của thầy: 15/18 nguyên vẹn; khác (đúng 3 ngoại lệ cho phép: CONFIG, `RUN_SENS = True`, `PAIRS`): ['# ======================= CONFIG =======================', 'ESTIMATORS = build_estimators(CONFIG)', 'RUN_SENS = False   # đặt True để chạy (~10–20 phút)']. Ô mở đầu chỉ khác ở đoạn Kết quả/Hạn chế: **đạt**; ô Phân công nhóm nguyên văn: **đạt**.
2. Test 1, 2, 2b và mọi assert: lỗi thực thi 0 → **đạt**.
3. Hồi quy Bước 0: ✔ Hồi quy Bước 0: Vol 12 phương pháp khớp đến 0,01 (cache run_full); ✔ Hồi quy Bước 0: §4 của thầy (tính lại) khớp đến 0,01 cho 11 bộ.
4. Số bảng 34/34, số hình 17/17 (**đạt**); ảnh nhúng: notebook 17, HTML đủ code 18, HTML gọn 18.
5. ✔ Mọi heatmap cặp đủ 12 cặp và có CSV; ✔ Mọi Bảng A đủ 12 hàng.
6. Số trong chữ: mọi câu Kết quả/Kết luận sinh từ code bằng số của bảng ngay trên (không gõ tay); ô mở đầu sinh từ CSV của T3c/T3b sau khi chạy (`scripts/make_intro6.py`).
7. Newton thất bại: {'fail': 0, 'total': 60682}; Đếm lỗi số — Newton thất bại (EW-RIE*, §4 và các ô tính lại): 0/200236 | EW-WeSpeR dùng dự phòng: 0/118.

Các dòng tự kiểm trong notebook:

- ✔ Hồi quy Bước 0: Vol 12 phương pháp khớp đến 0,01 (cache run_full)
- ✔ Hồi quy Bước 0: §4 của thầy (tính lại) khớp đến 0,01 cho 11 bộ
- ✔ Mẫu ngoài mẫu: 118 kỳ, 2 475 phiên
- ✔ Bước 1: EW-RIE* − VS-NL-LW ≈ +0,07 / +0,13; EW-RIE* − EW-NL-LW ≈ −0,16 / −0,06
- ✔ Bước 2: bộ không phải VS ở mọi T trùng hệt lần chạy thường; cùng ngày ngoài mẫu (assert ở §5.4)
- ✔ Bước 2: không kỳ nào thiếu phiên trước cửa sổ cho bộ VS "đủ T"
- ✔ T5d: VS đầy đủ trùng VS-NL-LW cấu hình chuẩn (assert)
- ✔ Số bảng = 34, số hình = 17
- ✔ Mọi heatmap cặp đủ 12 cặp và có CSV
- ✔ Mọi Bảng A đủ 12 hàng

## 4. Việc chưa xong, quyết định đã tự chọn, đề xuất

- **Chưa xong:** xác minh repo gốc của EW-WeSpeR (arXiv bị chặn từ phiên chạy); T4 (lý thuyết), VN30/HNX, vế "không giúp trong GARCH" của T5; 19 mã hủy thiếu giá.
- **Tự chọn:** (i) bộ VS "đủ T": mã không có đủ HL_VOL phiên trước cửa sổ (chưa niêm yết hoặc toàn 0) khởi động EWMA trên đầu cửa sổ như `make_vs` (số lượt ghi ở §5.4); lần cài đầu không xử lý điều này và cho VS-NL-LW 18% ở T = 250, đã sửa. (ii) Xóa trạng thái khởi tạo ấm của EW-WeSpeR sau Test 2b, vì Test 2b 20 lần lặp làm EW-WeSpeR bán khống ở §4 thành 13,33% (thay vì 12,57%) — EW-WeSpeR nhạy với khởi tạo. (iii) Lọc đứng giá 5%: không kỳ nào đủ 100 mã ⇒ báo riêng. (iv) Bảng 21 xếp hai chế độ theo hàng để giữ một số bảng. (v) Tổng kết (Bảng 34) bỏ các cột trùng cấu hình chuẩn (h = 60, HL_VOL = 20, REB = 21, T = 250). (vi) Test 2b dùng 20 lần lặp (v3: 6).
- **Đề xuất (không thêm vào notebook):** kiểm định chênh lệch số mã hiệu dụng/tỷ trọng max (bootstrap theo kỳ) để biến dòng "mức tập trung" ở mục 2 thành hơn/kém có căn cứ; đo thời gian kèm khoảng tứ phân vị; thử EW-WeSpeR với khởi tạo nguội ở mọi kỳ để đo độ nhạy khởi tạo.
