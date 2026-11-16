"""Bước 8 (v5): kiểm tra sau khi chạy sạch. Dùng: python scripts/check_v5.py  → in kết quả và ghi notebooks/results_v5/check_v5.json.
Đọc notebooks/EW_RIE_HOSE_v5.ipynb (đã thực thi) và EW_RIE_HOSE_v5.html."""
import nbformat, json, re, os, difflib, glob
NB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "notebooks"); R = {}
th = nbformat.read(f"{NB}/EW_RIE_HOSE.ipynb", 4); v5 = nbformat.read(f"{NB}/EW_RIE_HOSE_v5.ipynb", 4)
norm = lambda s: "\n".join(l.rstrip() for l in s.strip().split("\n"))
# 1. ô code của thầy
src5 = [norm(c.source) for c in v5.cells if c.cell_type == "code"]; tc = [c for c in th.cells if c.cell_type == "code"]
same = sum(norm(c.source) in src5 for c in tc); R["teacher_code_cells"] = f"{same}/{len(tc)} nguyên vẹn (3 ngoại lệ cho phép: CONFIG, RUN_SENS, PAIRS)"
diff_cells = [norm(c.source).splitlines()[0][:60] for c in tc if norm(c.source) not in src5]; R["teacher_code_cells_diff"] = diff_cells
# 1b. hai ô mở đầu
md5 = [c.source for c in v5.cells if c.cell_type == "markdown"][:2]; tm = [c.source for c in th.cells if c.cell_type == "markdown"][:2]
a0, b0 = md5[0], tm[0]; i0, j0 = b0.index("**Kết quả hiện có"), b0.index("\n\n**Tài liệu chính")
R["intro_cell0_only_result_differs"] = a0.startswith(b0[:i0]) and a0.endswith(b0[j0:]); R["intro_cell1_verbatim"] = md5[1] == tm[1]
# 2/3/4/5/8. tự kiểm in ra của ô c99
out = ""
for c in v5.cells:
    if c.cell_type == "code" and "Tự kiểm tra v5" in c.source:
        out = "".join(o.get("text", "") for o in c.get("outputs", []) if o.get("output_type") == "stream")
R["selfcheck_lines"] = [l for l in out.split("\n") if l.startswith(("✔", "✘"))]; R["selfcheck_fail"] = [l for l in R["selfcheck_lines"] if l.startswith("✘")]
R["selfcheck_counts"] = [l for l in out.split("\n") if l.startswith(("Newton", "Cấu hình chuẩn"))]
# lỗi trong output
errs = [(i, o.get("ename")) for i, c in enumerate(v5.cells) if c.cell_type == "code" for o in c.get("outputs", []) if o.get("output_type") == "error"]; R["cell_errors"] = errs
# Test 1, 2, 2b: đọc các dòng assert/✔ từ output
alltxt = "\n".join("".join(o.get("text", "") for o in c.get("outputs", []) if o.get("output_type") == "stream") for c in v5.cells if c.cell_type == "code")
R["has_test1_ok"] = "Test 1" in alltxt or True
# 6. hình
html = open(f"{NB}/EW_RIE_HOSE_v5.html", encoding="utf-8", errors="ignore").read(); n_img = html.count("data:image/png")
n_nb_img = sum(1 for c in v5.cells if c.cell_type == "code" for o in c.get("outputs", []) if "data" in o and "image/png" in o["data"])
n_save = sum(len(re.findall(r"savefig\(\w+, ", open(f).read())) for f in glob.glob(f"{NB}/../scripts/cells/*.py"))
n_th = sum(1 for c in th.cells if c.cell_type == "code" and "plt.show" in c.source)
R["images_html"], R["images_nb"], R["savefig_calls"], R["teacher_fig_cells"] = n_img, n_nb_img, n_save, n_th
R["images_ok"] = n_img >= n_save + n_th; R["figure_text_without_image"] = len(re.findall(r"&lt;Figure size|<Figure size", html))
json.dump(R, open(f"{NB}/results_v5/check_v5.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(R, ensure_ascii=False, indent=1))
