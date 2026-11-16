### Đối chiếu EW-WeSpeR với mã gốc của Oriol (bổ sung)

**Nguồn.** Bài báo: Oriol, *WeSpeR*, arXiv:2410.14413. Mã PyTorch: `github.com/nlcvbo/wesper` (thư mục `code/`, commit `1df4890`, giấy phép MIT). **Chưa xác minh được đây là repo chính thức:** trang arXiv không mở được từ phiên chạy (mạng chặn), và trang GitHub của repo không có README hay liên kết tới bài báo. Cần người đọc kiểm lại liên kết trên trang arXiv.

**Cách chạy** (`scripts/wesper_check.py`, người giao việc đã cấp quyền chạy mã). Không sửa mã của tác giả; chỉ bọc hai chỗ tương thích với scipy mới (`minimize` nhận `x0` numpy, hàm mục tiêu trả `float` thay vì tensor torch). Quy đổi: bản nhóm Σw = 1 ⇒ trọng số của tác giả W = T·w (trung bình 1), S = XᵀWX/T, c = N/T, `weights='Ndiracs'` với d = các giá trị W, khối lượng 1/T, `Kd = 1, Kt = 30`; τ khởi tạo **đúng như mã thí nghiệm của tác giả** (trị riêng của bản co weighted-LWO `wLWO_estimator`, thêm điểm lấp đầy, chuẩn hóa trung bình), 50 epoch, lr = 5·10⁻². So: phổ quần thể τ (Wasserstein-1 chia trung bình), trị riêng sau co ξ (cùng chuẩn hóa vết), rủi ro GMV so với tối ưu, thời gian.

**Một lỗi của chính người chạy, đã sửa:** lần chạy đầu dùng khởi tạo mặc định của `fit_from_F` (chọn ngẫu nhiên có hoàn lại từ trị riêng thô); khi đó loss thành NaN sau ~25 epoch và ξ lệch ~25% so với bản nhóm. Đó là lỗi cách dùng, không phải so sánh có nghĩa; kết quả đó bỏ (lưu ở `results_v5/logs/old_badinit/`) và chạy lại với khởi tạo của tác giả. Kiểm nhỏ (N = 30, T = 100, trọng số đều): bản nhóm lệch NL-LW 4,3%, bản gốc lệch NL-LW 5,8%, hai bản lệch nhau 2,7% (30 epoch).

Đọc tĩnh `nl_formulas.py`: công thức co `h(λ) = Σ w_j τ_j² / |τ_j X + 1|² ÷ Σ w_j τ_j / |τ_j X + 1|²` cùng dạng oracle d(λ) = Im e / Im m của bản nhóm (đọc mã, không phải kiểm chứng số).
