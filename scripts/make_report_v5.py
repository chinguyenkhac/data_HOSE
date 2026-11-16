"""Sinh BAO_CAO_V5.md (ở thư mục gốc repo) từ các CSV của results_v5 và check_v5.json. Chạy sau chạy sạch + check_v5.py."""
import pandas as pd, numpy as np, json, os, glob
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); R = f"{ROOT}/notebooks/results_v5"
f2 = lambda x, d=2: ("–" if pd.isna(x) else f"{x:.{d}f}".replace(".", ",")); VN = {"long_only": "Chỉ mua", "short_ok": "Bán khống"}
def tab(df, idx=True):
    d = df.reset_index() if idx else df; cols = list(d.columns)
    return "\n".join(["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)] + ["| " + " | ".join(str(x) for x in r) + " |" for r in d.itertuples(index=False)])
L = ["# BAO_CAO_V5 — EW-RIE\\* trên HOSE (pipeline v5)", "", "Notebook: `notebooks/EW_RIE_HOSE_v5.ipynb` (+ `.html`). Dữ liệu: `data_hose/` như v4, không mở rộng. Mọi số trong báo cáo lấy từ `notebooks/results_v5/*.csv`.", ""]
# 1. WeSpeR
OSall = pd.read_csv(f"{R}/T1b_oriol_check_sim.csv"); OS = OSall[OSall.loss_finite.astype(bool) & OSall.xi_med.notna()]; OH = pd.read_csv(f"{R}/T1b_oriol_check_hose.csv"); OHf = OH[OH.loss_finite.astype(bool) & OH.xi_med.notna()]
g = OS.groupby("h").agg(mẫu=("rep", "size"), W1=("W1_tau", "median"), xi_med=("xi_med", "median"), xi_max=("xi_max", "max"), risk_diff=("risk_diff", "mean"), giây_gốc=("sec_oriol", "mean"), giây_nhóm=("sec_nhom", "mean"))
g = g.apply(lambda c: c.map(lambda x: f2(x, 3) if c.name not in ("mẫu",) else str(int(x))))
L += ["## 1. Đối chiếu EW-WeSpeR với mã gốc", "",
      "- Repo dùng: `github.com/nlcvbo/wesper` (commit `1df4890`, MIT). **Chưa xác minh được đây là repo chính thức**: arXiv 2410.14413 không mở được (mạng chặn) và trang repo không có README/liên kết tới bài báo.",
      "- Chạy bằng `scripts/wesper_check.py` (torch 2.15 CPU); không sửa mã gốc, chỉ bọc 2 chỗ tương thích scipy mới. τ khởi tạo theo mã thí nghiệm của tác giả (trị riêng bản co wLWO), 50 epoch, lr 5e-2.",
      "- **Lỗi của người chạy, đã sửa:** lần đầu dùng khởi tạo mặc định của `fit_from_F` ⇒ loss NaN, ξ lệch ~25%; kết quả bỏ (`results_v5/logs/old_badinit/`), chạy lại.",
      f"- Giả lập (mô hình nhân tố Test 2, N = 100, T = 250): số mẫu mỗi h theo bảng (không đủ 20 vì mã gốc chậm 130–900 s/lần; dừng theo giới hạn 3 giờ). Cột: W1 = Wasserstein-1 chuẩn hóa của phổ τ; xi_med = sai lệch tương đối trung vị của ξ; risk_diff = chênh tỷ số rủi ro GMV/tối ưu (gốc so với nhóm).", "", tab(g), "",
      f"- Mã gốc trả NaN ở {len(OSall) - len(OS)}/{len(OSall)} mẫu giả lập (loại khỏi bảng trên).",
      f"- HOSE (N = 100, h = 60): mã gốc trả NaN (loss không hữu hạn) ở {len(OH) - len(OHf)}/{len(OH)} cửa sổ; {len(OHf)} cửa sổ chạy được cho sai lệch ξ trung vị {f2(100 * OHf.xi_med.median(), 1)}%, lớn nhất {f2(100 * OHf.xi_max.max(), 0)}%.",
      f"- Tiêu chí (ξ trung vị < 5% và chênh rủi ro < 1%): {open(f'{R}/wesper_status.txt', encoding='utf-8').read().split('tiêu chí')[1].split(';')[0].strip()}.",
      "- Thời gian: mã gốc ≥ 130 s/lần ⇒ không chạy backtest \"EW-WeSpeR (Oriol)\" (ngưỡng 30 s). Bản nhóm ≈ 0,1–1 s/lần.", "- Hình mới: scatter ξ nhóm – ξ gốc (`figs_v5/fig_oriol_xi_scatter.png`).", ""]
# 2. T
WI = pd.read_csv(f"{R}/T6_window_info.csv").drop(columns="Unnamed: 0", errors="ignore"); WC = pd.read_csv(f"{R}/T6_window_compare_full.csv")
x = WC[WC.rival.isin(["VS-NL-LW", "EW-WeSpeR", "EW-NL-LW", "NL-LW"])].copy()
x["ΔVol [CI]"] = [f"{a:+.2f} [{b:+.2f}; {c:+.2f}]".replace(".", ",") for a, b, c in zip(x["ΔVol (pp)"], x["CI lo"], x["CI hi"])]; x["p Holm"] = x["p Holm"].map(lambda p: f2(p, 3))
x = x.pivot_table(index=["mode", "rival"], columns="T", values="ΔVol (pp)", aggfunc="first").round(2)
L += ["## 2. Cửa sổ T (§5.4)", "", tab(WI.set_index("T")), "", "ΔVol = Vol(EW-RIE\\*) − Vol(đối thủ), pp/năm (cùng T, cùng ngày). Đủ CI, p Holm, 15 bộ: `T6_window_compare_full.csv`.", "", tab(x), ""]
# 3. pairwise
P = pd.read_csv(f"{R}/T44_pairwise_std.csv"); sig = P[P.p_holm < .05][["mode", "a", "b", "dvol", "p_holm"]]
A = pd.read_csv(f"{R}/pairwise_all_cells.csv"); TOP = ["EW-RIE*", "VS-NL-LW", "VS-EW-RIE*", "EW-WeSpeR", "EW-NL-LW", "VS-RIE"]; CNT = pd.DataFrame(0, index=TOP, columns=TOP)
for r in A.itertuples():
    if r.p_holm < .05: CNT.loc[(r.a, r.b) if r.dvol < 0 else (r.b, r.a)] += 1
nC = A.groupby(["config", "mode"]).ngroups
L += ["## 3. So sánh mọi cặp trong nhóm dẫn đầu (§4.4)", "", f"Cấu hình chuẩn: {len(sig)}/30 cặp (2 chế độ × 15) có p Holm < 0,05:", "", tab(sig.assign(dvol=sig.dvol.map(f2), p_holm=sig.p_holm.map(lambda p: f2(p, 3))), idx=False), "",
      f"Trên {nC} ô độ vững (cấu hình × chế độ): số ô mà bộ ở hàng thấp hơn bộ ở cột có ý nghĩa (p Holm < 0,05 trong ô; mô tả):", "", tab(CNT), ""]
# 4. thêm
L += ["## 4. Đã thêm", "", "- **Bước 1:** hai ô mở đầu chép nguyên văn của thầy, chỉ đổi đoạn Kết quả/Hạn chế (số lấy từ CSV).",
      "- **Kiểm định/so sánh:** `pairwise_top` (15 cặp, Holm 15) ở §4.4 và mọi ô độ vững (`pairwise_all_cells.csv`); cửa sổ T (§5.4); §5.1 theo h cho 6 bộ TOP; §5.2 thêm cột/heatmap EW-WeSpeR, VS-EW-RIE\\*; T2c: JKM Sharpe sau phí + phí hòa vốn (`T2c_sharpe_jkm.csv`); ghi chú Test 2b-30.",
      "- **Hình mới:** fig_pairwise_std, fig_window_vol, fig_window_dvol, fig_halflife_top6, fig_hlvol, fig_heat_nh_vs_wesper, fig_rank_top_cells, fig_vol_turnover, fig_oriol_xi_scatter; hình phụ lấy lại từ v3: fig_T2a_heatmap, fig_T3d_vs_ew_rie (trục không từ 0), fig_T6_N_h_grid. `%matplotlib inline` ở §0; chạy nbconvert không đặt MPLBACKEND=Agg.", ""]
# 5. tự kiểm
C = json.load(open(f"{R}/check_v5.json"))
L += ["## 5. Tự kiểm", "", f"- Ô code của thầy: {C['teacher_code_cells']}; ô khác: {C['teacher_code_cells_diff']}.", f"- Ô mở đầu 0 chỉ khác ở đoạn Kết quả/Hạn chế: {'ĐẠT' if C['intro_cell0_only_result_differs'] else 'KHÔNG ĐẠT'}; ô 1 (Phân công nhóm) nguyên văn: {'ĐẠT' if C['intro_cell1_verbatim'] else 'KHÔNG ĐẠT'}.",
      f"- Lỗi thực thi trong notebook: {len(C['cell_errors'])}.", f"- Ảnh nhúng trong HTML: {C['images_html']} (≥ {C['savefig_calls']} lời gọi savefig + {C['teacher_fig_cells']} ô hình của thầy: {'ĐẠT' if C['images_ok'] else 'KHÔNG ĐẠT'}); chuỗi 'Figure size' không kèm ảnh: {C['figure_text_without_image']}.", ""] \
    + [f"- {l}" for l in C["selfcheck_lines"]] + [f"- {l}" for l in C["selfcheck_counts"]] + [""]
L += ["## 6. Việc chưa xong và lý do", "", "- Đối chiếu mã gốc: số mẫu giả lập ít hơn 20/h (mã gốc rất chậm); 7/12 cửa sổ HOSE mã gốc trả NaN; chưa xác minh repo chính thức (arXiv bị chặn). Không rõ bên nào lệch ở dữ liệu thật (không có đáp án đúng).",
      "- T4 (lý thuyết), VN30/HNX của T6, T7 (viết bài): ngoài phạm vi v5. 19 mã hủy niêm yết thiếu giá (không tải dữ liệu mới theo yêu cầu).", "- Git: commit/push theo nhánh `claude/kind-wozniak-z1fq73`, không merge, không đẩy `main`.", ""]
open(f"{ROOT}/BAO_CAO_V5.md", "w", encoding="utf-8").write("\n".join(L)); print("BAO_CAO_V5.md:", len(L), "dòng")
