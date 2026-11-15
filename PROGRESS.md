# PROGRESS (pipeline v4)
Cập nhật: 2026-11-15 ~17:00 UTC (00:00 VN). Người duyệt kiểm tra lúc 8:00 VN (01:00 UTC 16/11).

## Đã xong
- Đọc pipeline + v3 + HTML. Khôi phục `notebooks/EW_RIE_HOSE_v3_nho.ipynb` (bản nhóm mới nhất, có T3d/VS-EW-RIE*) và `notebooks/EW_RIE_HOSE.ipynb` (bản thầy) từ HTML bằng `scripts/html_to_nb.py`.
- **Bước 0 ✔**: bảng hồi quy khớp đúng 2 chữ số cả 12 số (xem `notebooks/results_v4/step0_regression.csv`). Nạp 17 ô `defs` chạy được; `d = 0` trùng hệt.
- Viết xong: `scripts/hose_ns.py`, `scripts/run_grid.py`, `scripts/build_v4.py`, `scripts/layout.py`, các ô trong `scripts/cells/` (§3.2 ADJ, §3.3 utils/tests/full, T2d defs, 4.3 timing).

## Quyết định tự chọn
- Nền = v3_nho (khôi phục từ HTML) vì repo chỉ có v3 cũ; bản thầy cũng khôi phục từ HTML để so ô.
- Repo không có cache/`results/` → tính lại mọi thứ; cache ở `notebooks/results_v4/cache`, log ở `notebooks/results_v4/logs`.
- Cache theo từng phương pháp (`run_full`), tham số không dùng (HL_EW/HL_VOL) chuẩn hóa để dùng chung giữa các cấu hình.

## Đang chạy nền (xem results_v4/logs/)
- std, delist S1, delist S2 (đã khởi động ~17:00 UTC)

## Việc tiếp theo
- Hàng đợi: delist S1-mọi-lý-do, nh (N×h), hlv, zero, reb → rồi Bước 2 (timing, cần máy rảnh), 3 (WeSpeR gốc), viết ô notebook, build, nbconvert, báo cáo.

## Cập nhật 16:55 UTC
- std (FULL, 2 chế độ) xong. delist S1/S2/S1-mọi-lý-do đang chạy; hàng đợi nh/hlv/zero/reb chạy theo `scripts/queue.sh` (log `results_v4/logs/queue.log`).
- Viết xong mọi ô v4 (scripts/cells/*) + `layout.py` + `build_v4.py` (notebook dựng từ layout). Còn: chạy thử từng ô (dev_exec.py), md còn thiếu (m00_summary, m43_timing, m_notes_v4), BAO_CAO_V4.md, nbconvert, so ô thầy.
- **Bước 3 (đối chiếu WeSpeR gốc): bị chặn** — trình phân loại quyền từ chối chạy mã repo ngoài (`nlcvbo/wesper`, commit 1df4890); đã `add_repo` + clone + `torch` 2.15 cài được; viết sẵn `scripts/wesper_check.py` cho người duyệt chạy; fallback = Test 2b 30 lần lặp (cell c1b_oriol_view.py).
- Timing sơ bộ (máy đang tải) chạy bằng `scripts/run_timing.py`; số chính thức đo lại khi máy rảnh.
- Đã tạo tác vụ định kỳ hằng giờ (:38) fire vào phiên này; pipeline gốc chép ở PIPELINE_V4_2.md; RUNNING.lock ghi id phiên + giờ.
