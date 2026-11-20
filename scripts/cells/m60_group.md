## 6. Việc của nhóm

Dữ liệu: HOSE 2015-01 → 2026-11 (`data_hose/`, gồm mã hủy niêm yết); cấu hình chuẩn ở ô CONFIG (N = 100, T = 250, REB = 21, COST = 0,25% một chiều, HL\_EW = 60, HL\_VOL = 20, ZERO\_MAX = 20%), SEED = 0.

**Quy ước chung cho T2–T5**
- So sánh công bằng: trong mỗi bảng mọi phương pháp dùng **cùng ngày ngoài mẫu, cùng universe, cùng REB/COST/chế độ** (assert trong `run`, `run_full`, `compare_to`). Khi các cấu hình có số kỳ khác nhau, so trên **ngày chung**.
- *Gộp* = trước phí; *sau phí* = trừ COST × Σ|Δw| tại ngày tái cân bằng. *Chỉ mua* = `long_only`, *bán khống* = `short_ok`. Mỗi thí nghiệm chạy đủ `FULL` (15 phương pháp); bảng chính chỉ hiện `CORE5` + EW-RIE\*, bảng đủ lưu CSV ở `results_v4/`.
- Mỗi mục: **Câu hỏi → Làm gì → Bảng/Hình → Kết quả → Kết luận**; câu "Kết quả/Kết luận" sinh từ code, lấy số từ bảng ngay trên. Phần nặng chạy bằng `scripts/run_grid.py` (cache theo từng phương pháp ở `results_v4/cache`).
- Kiểm định: ΔVol = Vol(EW-RIE\*) − Vol(đối thủ), CI 95% block bootstrap (b = 21), p = kiểm định phương sai Ledoit–Wolf (2011) bootstrap, p Holm trên 4 đối thủ lõi (định trước), p Jobson–Korkie cho Sharpe.
