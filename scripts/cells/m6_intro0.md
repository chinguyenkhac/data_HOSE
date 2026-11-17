# EW-RIE\*: Làm sạch ma trận tương quan có trọng số mũ bằng lý thuyết ma trận ngẫu nhiên

### Ứng dụng: danh mục phương sai nhỏ nhất trên HOSE

**Câu hỏi nghiên cứu.** Ở thị trường mới nổi (N cổ phiếu lớn so với số phiên T, biến động thay đổi theo chế độ, cấm bán khống), bộ ước lượng ma trận hiệp phương sai nào cho danh mục rủi ro thấp nhất ngoài mẫu?

**Phương pháp đề xuất: EW-RIE\***

1. Ước lượng tương quan có trọng số mũ (half-life *h*) để phản ứng nhanh với thay đổi chế độ:
   $E = \sum_t w_t x_t x_t^\top = C^{1/2} W C^{1/2}$, với $W = \sum_t w_t y_t y_t^\top$ là nhiễu.
2. R-transform của nhiễu (tổng tự do các ma trận hạng 1): $R_W(g) = \sum_t \dfrac{w_t}{1 - N w_t g}$.
3. Phép thế nhân (BBP 2016) cho trị riêng làm sạch:
   $\xi_i = \lambda_i\,\dfrac{\operatorname{Im}\gamma(z_i)}{\operatorname{Im} t_E(z_i)}$, $z_i = \lambda_i - i\eta$, $t_E = z g_E(z) - 1$, với $\gamma$ là nghiệm của $\gamma\,R_W(\gamma) = t_E$.
   Trọng số đều ⇒ trùng công thức RIE cổ điển $\lambda/|1-q+qzg|^2$.
4. Ba chi tiết kỹ thuật (đóng góp của nhóm):
   - **Chọn đúng nhánh nghiệm** bằng tiếp tục giải tích: đi từ $t\approx 0$ (nơi $\gamma\approx t$) theo tia đến $t_E$.
   - **Ngoại lai** (trị riêng cô lập, ví dụ mode thị trường): đánh giá trên trục thực với $g$ bỏ-một, $\xi = \lambda\,\gamma'(t)$. Công thức BBP gốc với $\eta = N^{-1/2}$ ước lượng sai mode thị trường.
   - **Hiệu chỉnh N hữu hạn**: so với cùng công thức trên phổ nhiễu thuần (khớp thang theo trung vị).

**Đối chứng:** ma trận mẫu, Ledoit–Wolf (2004), NL-LW (Ledoit–Wolf 2020), MP-clip (Laloux 1999), RIE (Bun–Bouchaud–Potters 2016/17), bản EW với $q_{\text{eff}}$, EW-NL-LW, và biến thể VS (chuẩn hóa biến động EWMA).

**Kết quả hiện có (HOSE 12/2016–11/2026, N=100, T=250, h=60):**

|  | Bán khống | Chỉ mua |
| --- | --- | --- |
| NL-LW | 13,10% | 13,72% |
| EW-NL-LW | 12,72% | 13,12% |
| EW-RIE ($q_{\text{eff}}$) | 14,30% | 14,76% |
| EW-WeSpeR | 12,57% | 13,05% |
| VS-NL-LW | 12,49% | 12,93% |
| **EW-RIE\*** | **12,56%** | **13,07%** |

EW-RIE\* có rủi ro thấp hơn EW-NL-LW có ý nghĩa (ΔVol −0,16 / −0,06 điểm %, bán khống / chỉ mua; p Holm < 0,01 / < 0,01) và thấp hơn NL-LW (−0,54 / −0,65 điểm %; CI 95% bootstrap khối của thầy không chứa 0 ở cả hai chế độ). So với VS-NL-LW và EW-WeSpeR, chênh lệch rủi ro không có ý nghĩa (ΔVol +0,07 / +0,13 và −0,01 / +0,01 điểm %; p Holm = 1,00 / = 1,00 và = 1,00 / = 1,00). Turnover mỗi kỳ của EW-RIE\* thấp hơn VS-NL-LW (−0,47 / −0,27; CI 95% không chứa 0).
Hạn chế: 19 mã hủy niêm yết thiếu giá; chưa có VN30/HNX; EW-RIE\* kém ổn định khi N > T\_eff; EW-WeSpeR khớp mã gốc về rủi ro GMV nhưng trị riêng sau co lệch ~10% ở h = 15–30 (repo gốc chưa xác minh).

**Tài liệu chính:** Bun, Bouchaud & Potters (2016) *IEEE Trans. Inf. Theory* 62(12); (2017) *Physics Reports* 666; Ledoit & Wolf (2020) *Ann. Statist.*; Laloux et al. (1999) *PRL*; Jagannathan & Ma (2003) *J. Finance*.