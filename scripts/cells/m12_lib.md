### 1.2 (bổ sung) EW-NL-LW khi N > T\_eff, EW-WeSpeR, VS-EW-RIE\*

- **Sửa EW-NL-LW khi N > T\_eff:** `nl_lw_S` được định nghĩa lại (nhánh p > n của Ledoit–Wolf 2020); bản của thầy giữ làm `nl_lw_S_v2`. Khi N ≤ T\_eff kết quả trùng hệt.
- **Đối chứng EW-WeSpeR** (Oriol 2024, arXiv:2410.14413): khôi phục phổ quần thể của hiệp phương sai có trọng số rồi co phi tuyến (kiểu QuEST). Cài lại bằng numpy; `build_estimators` được bọc để thêm "EW-WeSpeR". Đối chiếu với mã gốc: xem ngay dưới Test 2b.
- **VS-EW-RIE\*** (chuẩn hóa biến động EWMA rồi EW-RIE\* trên tương quan có trọng số mũ của chuỗi đã chuẩn hóa): định nghĩa ở §3.3 (`make_vs_ew_rie`).
