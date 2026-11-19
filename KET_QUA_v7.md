# Kết quả v7 — Nhà đầu tư dài hạn

Notebook: `EW_RIE_HOSE_v7.ipynb` (+ `EW_RIE_HOSE_v7.html` có code, `EW_RIE_HOSE_v7_gon.html` ẩn code). Nhánh `v7`, không merge vào main.

## 1. Đã làm gì

- **Giữ nguyên v6.** Notebook v7 = notebook v6 đã chạy (mã và kết quả không đổi) + phần **7. Nhà đầu tư dài hạn** chèn trước "Ghi chú"; mục lục thêm một dòng. Chỉ các ô phần 7 được chạy mới, trong một kernel đã nạp lại các ô định nghĩa/dữ liệu của v6 (đọc cache, không chạy lại phần cũ): `scripts/build_v7.py`.
- **Kiểm tra** (`scripts/check_v7.py` → `notebooks/results_v7/check_v7.json`): 118/118 ô v6 trùng hệt (mã + output); phần 7 không lỗi; đủ Bảng 35–42, Hình 18–28 (8 bảng, 11 hình; mỗi hướng ≤ 2 bảng, ≤ 3 hình); HTML có 29 ảnh.
- **Kiểm hồi quy với v6:** tỷ trọng đích tính lại (cùng universe, cùng bộ ước lượng, cùng GMV) cho lợi suất Y·w trùng cache v6 **tuyệt đối (lệch 0,0)** ở cả 8 bộ, kể cả EW-WeSpeR và VS HL_VOL 10/40.
- **Đăng ký trước:** giả thuyết và ngưỡng của cả 4 hướng ghi vào `PROGRESS.md` (commit `c148e9e`) **trước khi chạy**; không chỉnh tham số sau khi thấy kết quả. Đoạn "Đào sâu" trong notebook là khám phá sau đó, chỉ mô tả.
- Quy ước: chỉ mua là chính (bán khống chỉ tham khảo); NAV có trôi tỷ trọng giữa hai lần tái cân bằng; phí mua 0,15%, bán 0,15% + thuế 0,1%; mốc tiết kiệm 5%/năm (giả định); kiểm định Ledoit–Wolf (2011) bootstrap khối như v6, Holm trong từng họ. Mẫu: 12/2016–11/2026 (9,8 năm, 2 475 phiên, 118 kỳ).
- **VN-Index: không lấy được.** `vnstock` không còn trên PyPI; bản 6.0.1 cài từ kho chính thức (vnstocks.com) bỏ nguồn VCI, mọi nguồn còn lại cần khóa API của công ty chứng khoán. Thay bằng **Thị trường EW** (mọi mã đủ điều kiện, chia đều, tái cân bằng 21 phiên, không phí) — khác VN-Index vì nghiêng về mã nhỏ.

## 2. Kết quả từng hướng (chỉ mua, sau phí và thuế)

### Hướng 1 – Tăng trưởng tài sản (Bảng 35–36, Hình 18–20)
| | CAGR | Vol | MDD | Calmar | Chi phí/năm |
|---|---|---|---|---|---|
| EW-RIE\* | 1,56% | 12,97% | −41,3% | 0,04 | 1,16% |
| VS-NL-LW | 3,39% | 12,84% | −40,8% | 0,08 | 1,81% |
| NL-LW | 2,36% | 13,67% | −47,2% | 0,05 | 0,85% |
| EW-WeSpeR | 1,61% | 12,96% | −41,1% | 0,04 | 1,16% |
| 1/N (top-100) | 8,30% | 22,60% | −60,1% | 0,14 | 0,31% |
| Thị trường EW | 9,43% | 18,55% | −57,0% | 0,17 | – |
| Q1 ít biến động (mọi mã) | 12,48% | 12,55% | −32,2% | 0,39 | – |
| Tiết kiệm (giả định) | 5,00% | – | – | – | – |

- **H1a** (EW-RIE\* Vol thấp hơn VS-NL-LW): **không đạt** — ΔVol +0,13 pp, p 0,59.
- **H1b** (giá trị kinh tế ≥ 25 bps/năm): **không đạt** — phí FKO γ = 5, cùng kỳ vọng: −8,3 bps/năm, CI 95% [−41,7; 21,0]. Bản lợi suất thực −186 bps/năm chủ yếu là chênh lợi suất trung bình (CI [−504; 114]).
- **H1c** (cổ phiếu ít biến động tăng kém thị trường): **chưa đủ bằng chứng** — Q1 còn tăng hơn (+1,8 pp/năm, p 0,64).
- GMV chưa hồi phục đỉnh 2022 (dưới đỉnh ~55 tháng).

### Hướng 2 – Tái cân bằng thưa (Bảng 37–38, Hình 21–23)
- ΔVol EW-RIE\* − VS-NL-LW (vùng 0) theo REB 21/63/126/252: **+0,13 / −0,37 / −0,84 / −1,19 pp**; 6/12 ô p Holm < 0,05 (tất cả ở REB 126, 252).
- **H2: ủng hộ mạnh** theo ngưỡng đăng ký trước.
- Chi phí EW-RIE\* giảm 1,16 → 0,27 %/năm (REB 21 → 252); Vol tăng 12,97 → 15,57%.

### Hướng 3 – Khủng hoảng (Bảng 39–40, Hình 24–26)
- Đỉnh → đáy (Thị trường EW): COVID 02/01/20 → 31/03/20; 2022: 29/03/22 → 15/11/22; thuế quan 17/03/25 → 09/04/25.
- Mức sụt EW-RIE\* / VS-NL-LW / Thị trường EW: −26,5 / −24,1 / −29,1%; −36,3 / −39,5 / −57,0%; −17,7 / −20,3 / −19,8%. **H3a: đạt** (2/3, chỉ mô tả).
- Cầu chì: 11 lần kích hoạt (13 lần cắt ngưỡng bị bỏ vì sát kỳ đều). EW-RIE\*: ΔVol −0,10 pp (p 0,21), MDD −41,3 → −38,1%, CAGR +0,7 pp, chi phí +0,03 %/năm. **H3b: đạt** (nhờ tiêu chí MDD ≥ 2 pp; Vol không đổi có ý nghĩa ở phương pháp nào).

### Hướng 4 – Danh mục thực thi được (Bảng 41–42, Hình 27–28)
- Thứ hạng theo Vol **giữ** (Kendall τ ≥ 0,87 ở mọi cấu hình; dấu ΔVol EW-RIE\* − VS-NL-LW luôn dương, không có ý nghĩa).
- Trần 10%: Vol EW-RIE\* 12,97 → 13,67%, CAGR 1,56 → 4,15%. Trần turnover 10%: Vol 13,51%, CAGR 5,79%.
- Sức chứa **không đạt**: % NAV bán được trong 5 phiên (10% ADV20), trung bình: EW-RIE\* 70% (quỹ 100 tỷ), 26% (1 000 tỷ); 1/N 96% / 75%.

## 3. Tự phản biện và phát hiện khi đào sâu (không đăng ký trước)

1. **GMV chỉ mua tăng chậm do tập trung, không phải do "cổ phiếu ít biến động tăng chậm".** 12 mã chiếm ~59% danh mục EW-RIE\* (VPI trung bình 15,5%; ở đáy 3/2020: 58% VPI + 17% NVL, số mã hiệu dụng 2,6). NVL kéo lùi −1,8 %/năm. Cùng universe, Q1 top-100 (20 mã chia đều) tăng 13,1%/năm với Vol 16,7%: GMV giảm thêm ~3,7 pp Vol nhưng mất ~11,5 pp CAGR mỗi năm.
2. **Kết quả Hướng 2 phụ thuộc pha lịch.** Ở REB 252, ΔVol trung bình qua 12 pha chỉ −0,64 pp (khoảng [−1,70; +0,09]); 6/12 pha có ý nghĩa. CAGR 11,65% của pha 0 là pha may (trung bình 7,11%, khoảng [2,29; 11,65]).
3. **Lợi thế ở REB dài phần lớn là do VS yếu đi, không phải EW-RIE\* mạnh lên.** So với VS-NL-LW HL_VOL 40, lợi thế còn −0,17 (p 0,065) / −0,59 pp (REB 126/252). Ở REB 252, NL-LW, EW-NL-LW, EW-WeSpeR có Vol ≈ EW-RIE\* (15,5–15,6%).
4. **Cầu chì: thời điểm có vai trò nhưng chỉ dựa trên một đợt.** Giả dược (30 bộ, mỗi bộ 11 ngày ngẫu nhiên): MDD cải thiện trung bình +0,1 pp, chỉ 1/30 bộ bằng cầu chì (p hoán vị ≈ 0,06). Nhưng MDD là một đợt sụt (2022; 4/11 lần kích hoạt rơi vào 2022). Ở COVID và thuế quan 4/2025, lần cắt ngưỡng trùng kỳ đều nên cầu chì không thêm gì.
5. **Điều chỉnh chậm cho lợi suất cao hơn.** Trần turnover 10% làm lợi suất trung bình của EW-RIE\* cao hơn +4,2 pp/năm (p NW 0,011; Holm trên 4 cấu hình 0,043), cùng chiều với REB dài ở Hướng 2. Thử giải thích bằng lợi suất của chính lệnh về đích: âm nhẹ (−0,08% / −0,42% / −0,50% mỗi lệnh ở h = 21/63/126) nhưng **không có ý nghĩa**.
6. **Sức chứa bị đánh giá quá bi quan ở những năm đầu.** `values.csv` = giá điều chỉnh × khối lượng khớp lệnh (ví dụ HPG 2017 giá điều chỉnh ~5 500 đồng). Chỉ tính từ 2024: EW-RIE\* bán được 91,6% NAV trong 5 phiên (quỹ 100 tỷ), trần 10% đạt 99,3%; quỹ 1 000 tỷ chỉ 37,9% / 53,4%. GMV chỉ hơi nghiêng về mã kém thanh khoản (hạng trung bình 55,8/100), nên nguyên nhân chính là độ tập trung.

## 4. Điều gì chưa chứng minh được

- **EW-RIE\* tốt hơn VS-NL-LW cho nhà đầu tư dài hạn ở REB = 21:** không (ΔVol +0,13 pp, p 0,59; phí FKO cùng kỳ vọng có CI chứa 0).
- **EW-RIE\* vượt trội ở REB dài:** chỉ đúng khi so với VS HL_VOL 20 ở pha 0. Trung bình theo pha lợi thế nhỏ hơn một nửa. So với VS HL_VOL 40 thì nhỏ hơn nữa (REB 126: p 0,065). Các bộ không chuẩn hóa biến động khác cũng cho kết quả như vậy.
- **Cầu chì giảm rủi ro:** Vol không giảm có ý nghĩa ở phương pháp nào. Cải thiện MDD dựa trên một đợt sụt (2022). Chưa kiểm được ngoài mẫu.
- **Cơ chế "điều chỉnh chậm ⇒ lợi suất cao hơn":** mới thấy ở trần turnover (có ý nghĩa sau Holm) và REB dài (phụ thuộc pha). Phép thử lợi suất của lệnh về đích không có ý nghĩa, nên cơ chế chưa rõ. Đây là phát hiện khám phá, cần đăng ký trước và kiểm trên dữ liệu khác.
- **So với VN-Index:** chưa làm được (không có dữ liệu); Thị trường EW nghiêng về mã nhỏ nên không thay thế hoàn toàn.
- **Sức chứa thực tế:** dữ liệu giá trị giao dịch xấp xỉ (giá điều chỉnh, không gồm thỏa thuận). Chưa mô hình hóa tác động giá, giá trần/sàn, room ngoại hay lô tối thiểu.
- **Bán khống:** chỉ báo Vol tham khảo; HOSE không cho bán khống kiểu này, chưa tính chi phí vay.
- **Thuế cổ tức và lãi tiền mặt:** chưa tính. Giá điều chỉnh đã ngầm tái đầu tư cổ tức, chưa trừ thuế 5%. Mã hủy niêm yết lấy lợi suất 0 như v6.

## 5. Quyết định tự chọn (ghi trong PROGRESS.md)
- REB dài dùng lại tỷ trọng đích của lịch 21 (mỗi REB/21 kỳ, pha 0 = kỳ đầu, cùng mẫu ngày); có kiểm mọi pha.
- Vùng không giao dịch theo từng mã; mã mất giá luôn bán; phần còn lại về đích rồi co giãn cho tổng = 1.
- Cầu chì bỏ lần kích hoạt cách kỳ đều ≤ 5 phiên; lịch đều giữ nguyên; EW-WeSpeR ở phiên thêm khởi tạo lạnh.
- GMV có trần giải bằng FISTA của thầy với phép chiếu lên đơn hình có trần (kiểm: trần 100% trùng GMV chỉ mua).
- Sức chứa tính trên tỷ trọng đích; quỹ cố định danh nghĩa (100 và 1 000 tỷ đồng).

## 6. Đề xuất bước tiếp
- Lấy VN-Index (cần khóa API một nguồn trong vnstock 6, hoặc tệp CSV) để thay Thị trường EW ở Hình 18–19 và cầu chì.
- Đăng ký trước rồi kiểm giả thuyết "điều chỉnh chậm có lợi" với nhiều mức trần turnover (5–30%) và trên VN30/HNX.
- GMV có trần 10% + trần turnover là cấu hình thực tế hơn cho nhà đầu tư dài hạn: CAGR 6,8%, Vol 13,9%. Nên đưa vào bản chính khi so EW-RIE\* với VS-NL-LW.

## 7. Cách chạy lại
```
python scripts/targets7_job.py "EW-RIE*"        # tỷ trọng đích (đã cache ở notebooks/results_v7/cache)
python scripts/build_v7.py                       # dựng + chạy riêng phần 7
python scripts/check_v7.py
```
