# EW-RIE\*: Làm sạch ma trận tương quan có trọng số mũ bằng lý thuyết ma trận ngẫu nhiên

### Ứng dụng: danh mục phương sai nhỏ nhất trên HOSE

**Câu hỏi nghiên cứu.** Ở thị trường mới nổi (N cổ phiếu lớn so với số phiên T, biến động thay đổi theo chế độ, cấm bán khống), bộ ước lượng ma trận hiệp phương sai nào cho danh mục rủi ro thấp nhất ngoài mẫu?

**Phương pháp đề xuất: EW-RIE\***

1. Ước lượng tương quan có trọng số mũ (half-life *h*) để phản ứng nhanh với thay đổi chế độ:
   $E = \sum\_t w\_t x\_t x\_t^\top = C^{1/2} W C^{1/2}$, với $W = \sum\_t w\_t y\_t y\_t^\top$ là nhiễu.
2. R-transform của nhiễu (tổng tự do các ma trận hạng 1): $R\_W(g) = \sum\_t \dfrac{w\_t}{1 - N w\_t g}$.
3. Phép thế nhân (BBP 2016) cho trị riêng làm sạch:
   $\xi\_i = \lambda\_i\,\dfrac{\operatorname{Im}\gamma(z\_i)}{\operatorname{Im} t\_E(z\_i)}$, $z\_i = \lambda\_i - i\eta$, $t\_E = z g\_E(z) - 1$, với $\gamma$ là nghiệm của $\gamma\,R\_W(\gamma) = t\_E$.
   Trọng số đều ⇒ trùng công thức RIE cổ điển $\lambda/|1-q+qzg|^2$.
4. Ba chi tiết kỹ thuật (đóng góp của nhóm):
   - **Chọn đúng nhánh nghiệm** bằng tiếp tục giải tích: đi từ $t\approx 0$ (nơi $\gamma\approx t$) theo tia đến $t\_E$.
   - **Ngoại lai** (trị riêng cô lập, ví dụ mode thị trường): đánh giá trên trục thực với $g$ bỏ-một, $\xi = \lambda\,\gamma'(t)$. Công thức BBP gốc với $\eta = N^{-1/2}$ ước lượng sai mode thị trường.
   - **Hiệu chỉnh N hữu hạn**: so với cùng công thức trên phổ nhiễu thuần (khớp thang theo trung vị).

**Đối chứng:** ma trận mẫu, Ledoit–Wolf (2004), NL-LW (Ledoit–Wolf 2020), MP-clip (Laloux 1999), RIE (Bun–Bouchaud–Potters 2016/17), bản EW với $q\_{\text{eff}}$, EW-NL-LW, và biến thể VS (chuẩn hóa biến động EWMA).

**Kết quả hiện có (HOSE 2009–3/2020, N=100, T=250, h=60):**

|  | Bán khống | Chỉ mua |
| --- | --- | --- |
| NL-LW | 15,14% | 15,95% |
| EW-NL-LW | 14,43% | 15,28% |
| EW-RIE ($q\_{\text{eff}}$) | 15,97% | 16,41% |
| **EW-RIE\*** | **14,24%** | **15,21%** |

EW-RIE\* tốt hơn có ý nghĩa (bootstrap khối, 95%) so với mọi đối chứng, ở mọi half-life 30/60/120. Trên dữ liệu tổng hợp, EW-RIE\* chỉ cách oracle ≈1%.
Hạn chế: dữ liệu đến 3/2020; survivorship bias; VS **không** được xác nhận trong mô phỏng GARCH.

**Tài liệu chính:** Bun, Bouchaud & Potters (2016) *IEEE Trans. Inf. Theory* 62(12); (2017) *Physics Reports* 666; Ledoit & Wolf (2020) *Ann. Statist.*; Laloux et al. (1999) *PRL*; Jagannathan & Ma (2003) *J. Finance*.