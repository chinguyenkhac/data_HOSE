"""v6 Bước 7: kiểm tra notebook đã thực thi + 2 HTML. Ghi notebooks/results_v6/check_v6.json."""
import nbformat, json, re, os
NB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "notebooks"); R = {}
th = nbformat.read(f"{NB}/EW_RIE_HOSE.ipynb", 4); v6 = nbformat.read(f"{NB}/EW_RIE_HOSE_v6.ipynb", 4)
norm = lambda s: "\n".join(l.rstrip() for l in s.strip().split("\n"))
src6 = [norm(c.source) for c in v6.cells if c.cell_type == "code"]; tc = [c for c in th.cells if c.cell_type == "code"]
R["teacher_code_cells"] = f"{sum(norm(c.source) in src6 for c in tc)}/{len(tc)}"
R["teacher_code_cells_diff"] = [norm(c.source).splitlines()[0][:70] for c in tc if norm(c.source) not in src6]
a0, b0 = v6.cells[0].source, th.cells[0].source; i0, j0 = b0.index("**Kết quả hiện có"), b0.index("\n\n**Tài liệu chính")
R["intro0_only_result_block_differs"] = a0.startswith(b0[:i0]) and a0.endswith(b0[j0:]); R["intro1_verbatim"] = v6.cells[1].source == th.cells[1].source
R["cell_errors"] = [(i, o.get("ename"), o.get("evalue", "")[:120]) for i, c in enumerate(v6.cells) if c.cell_type == "code" for o in c.get("outputs", []) if o.get("output_type") == "error"]
md_out = "\n".join(o.get("data", {}).get("text/markdown", "") for c in v6.cells if c.cell_type == "code" for o in c.get("outputs", []) if "data" in o)
R["bang"] = sorted({int(x) for x in re.findall(r"\*\*Bảng (\d+)[\.–]", md_out)} | {n for a, b in re.findall(r"\*\*Bảng (\d+)–(\d+)\.", md_out) for n in range(int(a), int(b) + 1)})
R["hinh"] = sorted({int(x) for x in re.findall(r"\*\*Hình (\d+)\.", md_out)})
R["bang_ok"] = R["bang"] == list(range(1, 35)); R["hinh_ok"] = R["hinh"] == list(range(1, 18))
R["images_nb"] = sum(1 for c in v6.cells if c.cell_type == "code" for o in c.get("outputs", []) if "data" in o and "image/png" in o["data"])
for h in ("EW_RIE_HOSE_v6.html", "EW_RIE_HOSE_v6_gon.html"):
    p = f"{NB}/{h}"; R[f"images_{h}"] = open(p, encoding="utf-8", errors="ignore").read().count("data:image/png") if os.path.exists(p) else None
txt = "\n".join("".join(o.get("text", "") for o in c.get("outputs", []) if o.get("output_type") == "stream") for c in v6.cells if c.cell_type == "code")
R["selfcheck"] = [l for l in txt.split("\n") if l.startswith(("✔", "✘"))]; R["selfcheck_fail"] = [l for l in R["selfcheck"] if l.startswith("✘")]
R["counts"] = [l for l in txt.split("\n") if l.startswith(("Đếm lỗi số", "Newton thất bại"))]
R["test_lines"] = [l for l in txt.split("\n") if "Test" in l or "✔" in l][:6]
json.dump(R, open(f"{NB}/results_v6/check_v6.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(R, ensure_ascii=False, indent=1))
