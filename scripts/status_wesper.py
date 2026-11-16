"""Ghi results_v5/wesper_status.txt (dùng cho ô mở đầu) từ các CSV đối chiếu; gộp T1b_oriol_check_sim_h*.csv → T1b_oriol_check_sim.csv."""
import pandas as pd, glob, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "notebooks", "results_v5")
OS = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(f"{R}/T1b_oriol_check_sim_h*.csv"))], ignore_index=True); OS.to_csv(f"{R}/T1b_oriol_check_sim.csv", index=False)
OH = pd.read_csv(f"{R}/T1b_oriol_check_hose.csv"); OHf = OH[OH.loss_finite.astype(bool) & OH.xi_med.notna()]; nfail = len(OH) - len(OHf)
gx, gr = OS.groupby("h").xi_med.median(), OS.groupby("h").risk_diff.mean()
ok = bool((gx < .05).all() and OHf.xi_med.median() < .05 and (gr.abs() < .01).all()); f2 = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")
txt = f"EW-WeSpeR đã đối chiếu với mã gốc nlcvbo/wesper (repo chính thức chưa xác minh được): sai lệch ξ trung vị {f2(100 * float(gx.min()))}–{f2(100 * float(gx.max()))}% (giả lập, theo h), tiêu chí < 5% **{'đạt' if ok else 'không đạt'}**; mã gốc trả NaN ở {nfail}/{len(OH)} cửa sổ HOSE (§1b)"
open(f"{R}/wesper_status.txt", "w", encoding="utf-8").write(txt); print(txt); print(len(OS), "mẫu giả lập")
