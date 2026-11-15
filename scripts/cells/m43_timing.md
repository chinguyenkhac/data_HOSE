### 4.3 (bổ sung) Thời gian chạy

**Câu hỏi:** chi phí tính toán của từng bộ ước lượng khi N tăng (thầy nhận xét cột "giây/lần" cũ sai vì EW-WeSpeR trúng cache)?
**Làm gì:** đo một lần ước lượng ma trận N × N (ms, chưa gồm giải GMV) trên 12 cửa sổ HOSE thật, N ∈ {50, 100, 150, 200}, mỗi cửa sổ gọi 3 lần lấy nhỏ nhất, báo trung vị và [Q1; Q3]; mọi bộ trong `FULL`. EW-WeSpeR gọi thẳng (không qua cache), tách "nguội" (khởi tạo lại) và "ấm" (khởi tạo từ kỳ trước); DCC không qua `_DCC_CACHE`, chỉ 3 cửa sổ; EW-RIE\*: lần gọi đầu (gồm mô phỏng phổ null) và thời gian theo bước. Chạy một mình trên máy rảnh (1 luồng BLAS).
