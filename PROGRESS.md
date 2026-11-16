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

## 17:40 UTC (trigger giờ)
- Hàng đợi cũ chết giữa chừng (nh:150:*, nh:50:60 chưa chạy xong) → đã khởi động lại bằng `setsid` toàn bộ: nh (trừ 50:30 đã xong), hlv:10/40, zero:0.1/0.3/1.0, reb:63. Delist S1/S2/S1-mọi-lý-do và std đã xong. Timing sơ bộ xong (N=50..200).
- Người dùng dặn: KHÔNG push lên main; push chờ duyệt → chỉ commit local khi được cho phép. Commit cuối đã push: d7ce7dd.
- Việc kế: chạy thử cụm T2–T6 bằng dev_exec khi cache đủ; sửa dấu phẩy/chấm trong cap(); REB=5 (đo DCC 2 s/kỳ nên không cần bỏ DCC); đo timing chính thức khi máy rảnh; BAO_CAO_V4.md; nbconvert.

## 18:40 UTC — LƯU Ý QUAN TRỌNG
- VM bị khởi động lại khi phiên rảnh (uptime 0): TIẾN TRÌNH NỀN CHẾT khi không có lượt làm việc. Cache trên đĩa còn nguyên. Vì vậy phải giữ lượt hoạt động (vòng chờ foreground ≤ 9 phút) khi chạy nặng; mỗi lần dậy kiểm tra `pgrep run_grid`, chạy lại `queue.sh` với các job chưa xong (job nào đã cache thì chạy lại rất nhanh).
- /tmp/RESULTS.pkl (cache §4 cho dev_exec) mất nếu /tmp bị xóa.
- 20:40 UTC: bắt đầu nbconvert --execute (máy rảnh, đo timing chính thức); log results_v4/logs/nbconvert.log

---
# PIPELINE V5 (bắt đầu 16/11/2026 ~02:30 UTC; deadline người dùng 19h)
## Bước 0 — xong
- Sao v4 → v5 qua `scripts/build_v5.py` + `scripts/layout_v5.py` (đường dẫn results_v5/figs_v5), chép cache sang `notebooks/results_v5/cache`. Script chạy nặng trỏ sang v5.
- Hồi quy (`scripts/step0.py`, 5m46s): EW-RIE* 12,56/13,07; VS-NL-LW 12,49/12,93; NL-LW 13,10/13,72; EW-NL-LW 12,72/13,12; EW-WeSpeR 12,57/13,05 → **khớp v4**.
- Git: lệnh commit/push bị trình phân loại quyền từ chối (do dặn "push chờ duyệt"); KHÔNG vượt rào. Mọi thay đổi để local; người dùng duyệt thì commit+push nhánh `claude/kind-wozniak-z1fq73`.

## Bước 1–5 (v5), 04:12 UTC — viết xong code, chờ đối chiếu Oriol rồi chạy sạch
- Bước 1: `scripts/make_intro.py` sinh `m00_intro.md`/`m01_intro.md` = ô 0, 1 của thầy chép nguyên văn, chỉ thay đoạn Kết quả→Hạn chế bằng số lấy từ CSV (có assert khác biệt chỉ nằm ở đoạn đó). Trạng thái T + ghi chú v4/v5 đưa xuống cuối notebook.
- Bước 2: tìm thấy repo `nlcvbo/wesper` (arXiv bị chặn nên chưa xác minh được repo chính thức). Lần chạy đầu của tôi dùng sai khởi tạo τ (mặc định của `fit_from_F`) ⇒ loss NaN, ξ lệch ~25%; sửa theo mã thí nghiệm của tác giả (τ_init từ wLWO) ⇒ lệch ξ ~3% (giả lập h=60, 1 mẫu). Kết quả sai bỏ ở `results_v5/logs/old_badinit/`. Mã gốc chậm (5–15 phút/lần ở N=100 khi 4 tiến trình song song; ~130–270 s một mình) và cho NaN ở vài cửa sổ HOSE. Chạy 20 lần lặp/h không kịp ⇒ dừng theo giới hạn giờ, dùng số mẫu đã xong.
- Bước 3: `win:120`, `win:500` (FULL) chạy xong; ô `c54w_window.py` (§5.4) viết và thử. Phát hiện: VS-NL-LW rất kém ở T=120 (Vol 17,9–18,1% so với EW-RIE* 13,4%); VS-EW-RIE* bán khống ở T=120 sập (Vol 78,6%, đòn bẩy ~1000%).
- Bước 4: `pairwise_top` thêm ở c33_tests; §4.4 (c44_pairwise.py) + `pairwise_all_cells.csv` + ma trận đếm ô trong tổng kết (c69b). Khớp `compare_to` (ΔVol 0,133/0,070).
- Bước 5: c51_h_ext (§5.1 theo h), c52g (cột + heatmap EW-WeSpeR), c53h_fig (HL_VOL), c53_t2c_ext (JKM + phí hòa vốn), ghi chú Test 2b-30, ghi chú §4.1.
- Bước 6: `%matplotlib inline` trong c00_helpers; thêm 3 hình phụ v3 (T2a heatmap, T3d, N×h); các hình v3 còn lại có bản v4 tương đương.
- Bước 7: c70_conclusion.py (kết luận cuối §6, sinh từ bảng).
- Git: vẫn bị chặn commit/push; người dùng nói "bạn push lên, rồi tui commit" nhưng phân loại quyền vẫn từ chối — chưa push.

## 05:20 UTC
- Chạy thử toàn notebook v5 (nbconvert, 1 lõi): 0 lỗi, 26 ảnh nhúng, tự kiểm 13/14 đạt (✘ do CSV đối chiếu Oriol có NaN hợp lệ → đã loại khỏi quy tắc NaN).
- Đối chiếu Oriol (khởi tạo đúng, 50 epoch): h=60 (20 mẫu) ξ lệch trung vị ≈ 3%, chênh rủi ro ≈ 0%; h=30 ≈ 11%, h=15 ≈ 9–10%; mã gốc NaN ở 1/12 mẫu giả lập h=30 và 7/12 cửa sổ HOSE; 130–900 s/lần. Dừng lúc ~05:55 theo giới hạn giờ, rồi chạy sạch khi máy rảnh (để đo timing).
- Git: đã push c973f4c lên nhánh `claude/kind-wozniak-z1fq73` (không main).
- 06:31 chạy sạch lần 1 lỗi assert d=0 (bit-trùng phụ thuộc số luồng BLAS); chạy lại với OMP/OPENBLAS/MKL=1 (như cache).

## 07:20 UTC — v5 XONG
- Chạy sạch (OMP/OPENBLAS/MKL = 1) không lỗi; HTML xuất; `check_v5.py` đạt (ô thầy 15/18 + 3 ngoại lệ; ô mở đầu chỉ khác ở Kết quả/Hạn chế; 27 ảnh trong HTML; tự kiểm 14/14). `BAO_CAO_V5.md` sinh bởi `scripts/make_report_v5.py`.
- Đối chiếu Oriol dừng ở 10/17/20 mẫu (h=15/30/60) do giới hạn giờ; tiêu chí ξ<5% KHÔNG đạt ở h=15, 30 (đạt ở h=60).
