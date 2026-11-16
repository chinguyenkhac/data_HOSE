### 4.3 Thời gian chạy

**Câu hỏi:** chi phí tính toán của từng bộ ước lượng khi N tăng?
Đo một lần ước lượng ma trận N × N (ms, chưa gồm giải GMV) trên 12 cửa sổ tái cân bằng HOSE thật, N ∈ {50, 100, 150}; mỗi cửa sổ gọi 3 lần lấy nhỏ nhất, báo trung vị qua 12 cửa sổ. EW-WeSpeR gọi thẳng, khởi tạo lại mỗi lần (không qua cache, không khởi tạo ấm); DCC không qua cache, chỉ 3 cửa sổ; EW-RIE\*: bỏ lần gọi đầu (mô phỏng phổ null một lần cho mỗi N).
