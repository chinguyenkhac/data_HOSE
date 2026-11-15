**Làm gì trong bản v4 (ngắn gọn):** các ô của thầy giữ nguyên (chỉ ô CONFIG, cờ `RUN_SENS` và thêm ba cặp vào `PAIRS` ở §4); phần nhóm thêm ghi "(bổ sung)" trong tiêu đề.

1. **So sánh đầy đủ ở mọi mục:** mỗi thí nghiệm chạy đủ 15 phương pháp (`FULL`) và kiểm định bằng một hàm chung `compare_to` (§3.3): ΔVol, CI bootstrap khối, kiểm định phương sai Ledoit–Wolf (2011), Holm trên họ lõi `CORE5` (EW-RIE\* vs NL-LW, EW-NL-LW, EW-WeSpeR, **VS-NL-LW**), Jobson–Korkie, ΔTurnover.
2. **Mới:** thời gian chạy đo đúng (§4.3), đối chiếu EW-WeSpeR với mã gốc của tác giả (§1b), độ nhạy lợi suất ngày hủy niêm yết (T2d), lưới N × h và HL\_VOL (§5), ΔVol theo giai đoạn (T5), bảng tổng kết độ vững (cuối §6).
3. Mọi bảng/hình đánh số "Bảng n"/"Hình n"; bảng chính chỉ hiện `CORE5` + EW-RIE\*, bảng đủ `FULL` lưu CSV ở `results_v4/`.
