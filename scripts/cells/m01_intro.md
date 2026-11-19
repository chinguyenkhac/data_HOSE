## Phân công nhóm

| Mã | Việc | Đầu ra | Mục trong notebook |
| --- | --- | --- | --- |
| **T1** | Dữ liệu 2020–2025 (vnstock/nguồn trả phí) + **mã đã hủy niêm yết** để loại survivorship bias | `prices.csv`, `values.csv` | §2, ô T1 |
| **T2** | Độ vững: chi phí GD thực tế (phí + thuế 0,1%), tần suất tái cân bằng 5/21/63 phiên, xử lý phiên không giao dịch (~18%) | Bảng độ vững | §6, ô T2 |
| **T3** | Đối chứng & kiểm định chuẩn: danh mục 1/N, mô hình nhân tố, DCC-GARCH; kiểm định chênh lệch phương sai Ledoit–Wolf (2011, HAC), Sharpe (Jobson–Korkie/Memmel) | Bảng kiểm định | §6, ô T3 |
| **T4** | Lý thuyết: chứng minh tính đúng của việc chọn nhánh, điều kiện ngoại lai, hiệu chỉnh N hữu hạn; **rà soát tính mới** (đọc toàn văn BBP 2016 §III và Phys. Rep. 2017) | Mục Methodology (LaTeX) | — |
| **T5** | Vì sao VS giúp trên HOSE nhưng không trong GARCH? (biến động riêng lẻ, tương quan đổi theo chế độ…) | Ghi chú + thí nghiệm | §6, ô T5 |
| **T6** | Mở rộng: N = 50/150, cửa sổ T, VN30/HNX | Bảng phụ lục | §5 (đổi CONFIG) |
| **T7** | Viết bài, nhắm tạp chí (kiểm tra hạng Q trên Scimago) | Bản thảo | — |

**Quy ước:** mỗi người làm trên bản sao notebook (`File → Save a copy in Drive`), ghi kết quả vào thư mục chung. Đổi tham số ở ô CONFIG, không sửa thư viện ở §1 trừ khi đã thống nhất.