# Đối chiếu EW-WeSpeR (bản numpy của nhóm) với mã gốc PyTorch (nlcvbo/wesper): đọc kết quả của scripts/wesper_check.py (50 epoch) và scripts/wesper_epochs.py (200 epoch)
import glob
OSall, OH = pd.read_csv(f"{RESULTS_DIR}/T1b_oriol_check_sim.csv"), pd.read_csv(f"{RESULTS_DIR}/T1b_oriol_check_hose.csv")
ok_ = lambda d: d["loss_finite"].astype(bool) & d["xi_med"].notna()
EP = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(f"{RESULTS_DIR}/T1b_oriol_epochs_h*_r*.csv"))], ignore_index=True)
rows = {}
for h_, g in list(OSall.groupby("h")) + [("HOSE", OH)]:
    f_ = g[ok_(g)]; e_ = EP[EP.h == h_] if h_ != "HOSE" else EP.iloc[:0]
    r = {"số mẫu": len(g), "mã gốc không hội tụ (NaN)": int((~ok_(g)).sum()), "ξ lệch, trung vị (50 epoch)": 100 * f_.xi_med.median()}
    for ep_ in (50, 100, 200):
        x = e_[(e_.epoch == ep_) & e_.loss_finite.astype(bool)]
        r[f"ξ lệch, 3 mẫu ({ep_} epoch)"] = 100 * x.xi_med.median() if len(x) else np.nan
    r["chênh rủi ro GMV (gốc/nhóm − 1), TB %"] = 100 * f_.risk_diff.mean() if "risk_diff" in f_ else np.nan
    r["chênh rủi ro GMV, |lớn nhất| %"] = 100 * f_.risk_diff.abs().max() if "risk_diff" in f_ else np.nan
    r["giây/lần, mã gốc (50 epoch)"] = f_.sec_oriol.mean(); r["giây/lần, bản nhóm"] = f_.sec_nhom.mean()
    rows["h = " + str(h_) if h_ != "HOSE" else "HOSE (h = 60)"] = r
T1O = pd.DataFrame(rows).T; save(T1O.reset_index(), "T1b_oriol_summary"); save(EP, "T1b_oriol_epochs")
cap("Bảng", "Đối chiếu EW-WeSpeR của nhóm với mã gốc (nlcvbo/wesper). ξ lệch = sai lệch tương đối trung vị của trị riêng sau co (cùng chuẩn hóa vết), %; mẫu mã gốc trả NaN bị loại khỏi thống kê. "
    "Cột 100/200 epoch: 3 mẫu đầu, chạy tiếp từ τ của giai đoạn trước. Rủi ro GMV chia cho tối ưu của ma trận thật (chỉ có ở giả lập). Thời gian đo khi nhiều tiến trình chạy song song.")
show(T1O, 2)
_r = lambda h_, c: T1O.loc[f"h = {h_}", c]
_cr = "chênh rủi ro GMV (gốc/nhóm − 1), TB %"
md(f"**Kết quả.** Rủi ro GMV của hai bản gần như trùng: chênh trung bình {', '.join(f'h = {h_}: {f2(_r(h_, _cr), 2)}%' for h_ in (15, 30, 60))}. "
   f"ξ lệch trung vị (50 epoch): h = 15: {f2(_r(15, 'ξ lệch, trung vị (50 epoch)'), 1)}%, h = 30: {f2(_r(30, 'ξ lệch, trung vị (50 epoch)'), 1)}%, h = 60: {f2(_r(60, 'ξ lệch, trung vị (50 epoch)'), 1)}%; "
   f"chạy tiếp 3 mẫu đến 200 epoch: h = 15: " + " → ".join(f2(_r(15, f'ξ lệch, 3 mẫu ({e} epoch)'), 1) + "%" for e in (50, 100, 200)) + ", h = 30: " + " → ".join(f2(_r(30, f'ξ lệch, 3 mẫu ({e} epoch)'), 1) + "%" for e in (50, 100, 200)) + ". "
   f"Mã gốc không hội tụ (NaN) ở {int(T1O.loc['HOSE (h = 60)', 'mã gốc không hội tụ (NaN)'])}/{int(T1O.loc['HOSE (h = 60)', 'số mẫu'])} cửa sổ HOSE và {int(T1O.drop(index='HOSE (h = 60)')['mã gốc không hội tụ (NaN)'].sum())}/{int(T1O.drop(index='HOSE (h = 60)')['số mẫu'].sum())} mẫu giả lập.")
_dec = all(_r(h_, "ξ lệch, 3 mẫu (200 epoch)") < _r(h_, "ξ lệch, 3 mẫu (50 epoch)") for h_ in (15, 30))
md(f"**Kết luận.** Hai bản khớp về rủi ro GMV; trị riêng sau co khớp ở h = 60 (< 5%) nhưng lệch ~10% ở h = 15–30, "
   + ("và độ lệch giảm khi chạy thêm epoch (một phần do mã gốc chưa hội tụ)." if _dec else "và độ lệch không giảm khi chạy thêm epoch (không phải do chưa hội tụ).")
   + " Repo `nlcvbo/wesper` chưa xác minh được là repo chính thức của tác giả.")
