# EW-RIE\*: Làm sạch ma trận tương quan có trọng số mũ bằng lý thuyết ma trận ngẫu nhiên
### Ứng dụng: danh mục phương sai nhỏ nhất trên HOSE — **phiên bản v4** (dữ liệu HOSE 2015–11/2026, gồm mã hủy niêm yết)

**Câu hỏi.** Trên HOSE, EW-RIE\* có cho danh mục phương sai nhỏ nhất (GMV) rủi ro ngoài mẫu thấp hơn các bộ ước lượng khác không, và ở điều kiện nào?

**Phương pháp.** Tương quan có trọng số mũ (half-life *h*), làm sạch trị riêng bằng phép thế nhân cho nhiễu có trọng số (R-transform của tổng tự do các ma trận hạng 1): chọn đúng nhánh nghiệm bằng tiếp tục giải tích, ngoại lai trên trục thực, hiệu chỉnh N hữu hạn; trọng số đều ⇒ trùng RIE cổ điển.

**Đối chứng.** 15 phương pháp (`FULL`): ma trận mẫu, Ledoit–Wolf, NL-LW, MP-clip, RIE, EW-RIE (q$_{\text{eff}}$), EW-NL-LW, **EW-WeSpeR** (Oriol 2024), VS-NL-LW, VS-RIE, **VS-EW-RIE\***, PCA, DCC-GARCH, 1/N. Họ kiểm định chính định trước (`CORE5`): EW-RIE\* so với NL-LW, EW-NL-LW, EW-WeSpeR, **VS-NL-LW**; ΔVol, CI bootstrap khối, kiểm định phương sai Ledoit–Wolf (2011), Holm, Jobson–Korkie, ΔTurnover.

**Kết quả** (HOSE 12/2016–11/2026, 118 kỳ, N = 100, T = 250, h = 60, REB = 21, COST = 0,25%, lọc đứng giá 20%; Vol ngoài mẫu %/năm):

| | Bán khống | Chỉ mua |
|---|---|---|
| NL-LW | 13,10 | 13,72 |
| EW-NL-LW | 12,72 | 13,12 |
| EW-RIE (q$_{\text{eff}}$) | 14,30 | 14,76 |
| EW-WeSpeR | 12,57 | 13,05 |
| **EW-RIE\*** | 12,56 | 13,07 |
| VS-NL-LW | 12,49 | 12,93 |

- **EW-RIE\* vs VS-NL-LW (cặp quan trọng nhất): ngang nhau về rủi ro.** ΔVol = +0,13 [-0,32; +0,63] pp (chỉ mua), +0,07 [-0,31; +0,53] pp (bán khống); p Holm 0,997 / 1,000. VS-NL-LW có Vol thấp nhất nhưng chênh lệch không có ý nghĩa. Khác biệt nằm ở **turnover**: EW-RIE\* giao dịch ít hơn -0,27 (chỉ mua) và -0,47 (bán khống) mỗi kỳ (CI 95% không chứa 0), và ở **thời gian chạy** (EW-RIE\* 154 ms so với VS-NL-LW 2,5 ms mỗi lần ước lượng ở N = 100).
- EW-RIE\* thấp hơn có ý nghĩa (p Holm < 0,05) so với EW-NL-LW ở cả hai chế độ (-0,06 [-0,09; -0,03] / -0,16 [-0,24; -0,09] pp) và so với NL-LW ở chế độ chỉ mua (-0,65 [-1,03; -0,28] pp; bán khống p Holm 0,070); **ngang EW-WeSpeR** (+0,01 / -0,01 pp) nhưng nhanh hơn ≈ 8 lần.
- **Độ vững** (19 cấu hình × 2 chế độ; N × h, HL\_VOL, REB, lọc đứng giá, kịch bản hủy niêm yết): EW-RIE\* thấp hơn VS-NL-LW ở 14/38 ô, thấp hơn có ý nghĩa 0 ô, cao hơn có ý nghĩa 0 ô (p-value mô tả, không hiệu chỉnh xuyên lưới); hạng TB trong 15 phương pháp: VS-EW-RIE\* 2,79, EW-RIE\* 2,95, VS-NL-LW 3,05.

**Hạn chế.** 19 mã hủy niêm yết thiếu giá (không bao giờ vào universe); lợi suất ngày hủy niêm yết (T2d: 6 lượt trong kỳ nắm giữ, kết quả không đổi với cú sốc −30%/−100%, kịch bản quy ước); **EW-WeSpeR chưa đối chiếu được với mã gốc** (bị chặn quyền chạy mã ngoài trong phiên chạy đêm; còn Test 2b 30 lần lặp); EW-RIE\* kém ổn định khi N > T$_{\text{eff}}$ (h = 15); N = 200 không đưa vào lưới (chỉ 74/129 kỳ đủ mã); T4 (lý thuyết), cửa sổ T, VN30/HNX để sau.

**Tài liệu chính:** Bun, Bouchaud & Potters (2016) *IEEE Trans. Inf. Theory* 62(12); (2017) *Physics Reports* 666; Ledoit & Wolf (2011) và (2020) *Ann. Statist.*; Oriol (2024) *WeSpeR*, arXiv:2410.14413; Laloux et al. (1999) *PRL*; Jagannathan & Ma (2003) *J. Finance*; Shumway (1997) *J. Finance*.
