## 7. Nhà đầu tư dài hạn (v7)

Góc nhìn: đầu tư **dài hạn, giao dịch thưa, không đầu cơ**. Phần 0–6 giữ nguyên v6 (mã và kết quả không đổi). Phần 7 dùng lại đúng universe, bộ ước lượng và GMV của v6; ô 7.0 kiểm hồi quy: lợi suất tính lại từ tỷ trọng mới phải trùng cache v6.

**Quy ước chung**
- Phương pháp: EW-RIE\*, VS-NL-LW (HL_VOL = 20; mỗi lần chạy VS thêm HL_VOL 10 và 40), NL-LW, EW-NL-LW, EW-WeSpeR, 1/N. **Chỉ mua** là chính; bán khống chỉ để tham khảo (thực tế HOSE không cho bán khống kiểu này).
- NAV 1 đồng, **tỷ trọng trôi theo giá** giữa hai lần tái cân bằng (khác `run_backtest` giữ tỷ trọng cố định); phí **mua 0,15%**, **bán 0,15% + thuế 0,1%**, áp cho mọi giao dịch kể cả lần mua đầu.
- Mốc: **tiết kiệm 5%/năm (giả định)**. **VN-Index: không lấy được** — thư viện vnstock không còn trên PyPI; bản 6.0.1 cài từ kho chính thức bỏ nguồn VCI và mọi nguồn còn lại cần khóa API của công ty chứng khoán. Thay bằng **Thị trường EW**: danh mục đều mọi mã đủ điều kiện (cùng bộ lọc universe, không cắt top-N), tái cân bằng 21 phiên, không phí. Khác VN-Index (trọng số vốn hóa): nghiêng về mã nhỏ.
- Kiểm định chênh lệch Vol: Ledoit–Wolf (2011) bootstrap khối như v6 (b = 21, M = 2 000), Holm trong từng họ.
- **Giả thuyết và ngưỡng ghi trước khi chạy** (`PROGRESS.md`, mục v7), không chỉnh tham số sau khi thấy kết quả. Câu "Kết luận" so với ngưỡng đó. Đoạn **"Đào sâu"** là khám phá sau khi thấy kết quả, chỉ mang tính mô tả.

| Mục | Câu hỏi | Đầu ra |
|---|---|---|
| 7.0 Lõi | Tỷ trọng đích, mô phỏng NAV, kiểm hồi quy với v6 | — |
| 7.1 Tăng trưởng tài sản | 1 đồng thành bao nhiêu sau phí, thuế? Sụt sâu, hồi phục lâu cỡ nào? Đáng bao nhiêu bps/năm? Cổ phiếu ít biến động có tăng kém thị trường? | Bảng 35–36, Hình 18–20 |
| 7.2 Tái cân bằng thưa | REB 21–252 phiên × vùng không giao dịch: rủi ro, lợi suất, chi phí; EW-RIE\* có lợi hơn khi REB dài? | Bảng 37–38, Hình 21–23 |
| 7.3 Khủng hoảng | COVID 2020, năm 2022, thuế quan 4/2025; "cầu chì" tái cân bằng sớm | Bảng 39–40, Hình 24–26 |
| 7.4 Thực thi được | Trần tỷ trọng, trần turnover, sức chứa quỹ 100 và 1 000 tỷ đồng; thứ hạng có giữ? | Bảng 41–42, Hình 27–28 |
| 7.5 Tổng kết | Phân tích chéo và bảng tổng kết bốn hướng | — |
