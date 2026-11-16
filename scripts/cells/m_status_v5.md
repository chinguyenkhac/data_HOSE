### Trạng thái từng việc T (ghi chú v4/v5)

| Mã | Việc | Đầu ra | Mục trong notebook | Trạng thái (v4) |
| --- | --- | --- | --- | --- |
| **T1** ✔ | Dữ liệu 2020–2025 (vnstock/nguồn trả phí) + **mã đã hủy niêm yết** để loại survivorship bias — *đã làm: HOSE 2015–11/2026* | `prices.csv`, `values.csv` | §2 | xong; còn 19 mã hủy thiếu giá |
| **T2** ✔ | Độ vững: chi phí GD thực tế (phí + thuế 0,1%), tần suất tái cân bằng 5/21/63 phiên, xử lý phiên không giao dịch (~18%), **lợi suất ngày hủy niêm yết (T2d, mới)** | Bảng độ vững | §6, ô T2 | xong, đủ 15 phương pháp |
| **T3** ✔ | Đối chứng & kiểm định chuẩn: danh mục 1/N, mô hình nhân tố, DCC-GARCH; kiểm định chênh lệch phương sai Ledoit–Wolf (2011, HAC), Sharpe (Jobson–Korkie/Memmel); **đối chứng EW-RIE\* vs VS-NL-LW** | Bảng kiểm định | §6, ô T3 | xong, một bảng duy nhất |
| **T4** (để sau) | Lý thuyết: chứng minh tính đúng của việc chọn nhánh, điều kiện ngoại lai, hiệu chỉnh N hữu hạn; **rà soát tính mới** (đọc toàn văn BBP 2016 §III và Phys. Rep. 2017) | Mục Methodology (LaTeX) | — | chưa làm |
| **T5** ✔ | Vì sao VS giúp trên HOSE nhưng không trong GARCH? (biến động riêng lẻ, tương quan đổi theo chế độ…) | Ghi chú + thí nghiệm | §6, ô T5 | xong, thêm ΔVol theo giai đoạn |
| **T6** ◐ | Mở rộng: N = 50/150 và half-life h = 30/60/120, HL\_VOL = 10/20/40 *(đã làm, §5)*; cửa sổ T, VN30/HNX *(để sau)* | Bảng phụ lục | §5 | N × h, HL\_VOL xong |
| **T7** | Viết bài, nhắm tạp chí (kiểm tra hạng Q trên Scimago) | Bản thảo | — | chưa làm |

**Quy ước:** mỗi người làm trên bản sao notebook (`File → Save a copy in Drive`), ghi kết quả vào thư mục chung. Đổi tham số ở ô CONFIG, không sửa thư viện ở §1 trừ khi đã thống nhất.
