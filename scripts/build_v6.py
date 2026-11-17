"""Dựng notebooks/EW_RIE_HOSE_v6.ipynb từ: ô của bản nhóm v3_nho (chỉ số 'n<i>'), ô mới trong scripts/cells (tên file) và markdown.
Mỗi mục LAYOUT: ('n', i, tags) | ('f', 'file.py', tags) | ('m', 'file.md') | ('mt', 'text')."""
import os, nbformat, copy, sys
HERE = os.path.dirname(os.path.abspath(__file__)); NB = os.path.join(HERE, "..", "notebooks")
nho = nbformat.read(f"{NB}/EW_RIE_HOSE_v3_nho.ipynb", 4); thay = nbformat.read(f"{NB}/EW_RIE_HOSE.ipynb", 4)
sys.path.insert(0, HERE); from layout_v6 import LAYOUT

def build(out=f"{NB}/EW_RIE_HOSE_v6.ipynb"):
    cells = []
    for it in LAYOUT:
        kind = it[0]
        if kind == "t":
            c = copy.deepcopy(thay.cells[it[1]]); c.pop("id", None)
        elif kind == "n":
            c = copy.deepcopy(nho.cells[it[1]]); c.pop("id", None)
            if len(it) > 2 and it[2]: c.metadata["tags"] = list(it[2])
        elif kind == "ne":     # ô của bản nhóm với vài thay thế văn bản (it[2] = [(cũ, mới), ...]); mỗi cặp phải khớp đúng 1 lần
            c = copy.deepcopy(nho.cells[it[1]]); c.pop("id", None); src = c.source
            for old, new in it[2]:
                assert src.count(old) == 1, (it[1], old); src = src.replace(old, new)
            c.source = src
            if len(it) > 3 and it[3]: c.metadata["tags"] = list(it[3])
        elif kind == "f":
            fp = f"{HERE}/cells/{it[1]}"
            if not os.path.exists(fp): c = nbformat.v4.new_markdown_cell(f"**TODO** ô `{it[1]}` chưa viết"); cells.append(c); continue
            c = nbformat.v4.new_code_cell(open(fp, encoding="utf-8").read().rstrip("\n").replace("results_v4", "results_v6").replace("figs_v4", "figs_v6").replace("results_v5", "results_v6").replace("figs_v5", "figs_v6"))
            if len(it) > 2 and it[2]: c.metadata["tags"] = list(it[2])
        elif kind == "m":
            fp = f"{HERE}/cells/{it[1]}"
            c = nbformat.v4.new_markdown_cell(open(fp, encoding="utf-8").read().rstrip("\n") if os.path.exists(fp) else f"**TODO** `{it[1]}`")
        else:
            c = nbformat.v4.new_markdown_cell(it[1])
        cells.append(c)
    nb = nbformat.v4.new_notebook(cells=cells, metadata=nho.metadata)
    for c in nb.cells: c.pop("outputs", None) if c.cell_type != "code" else (c.__setitem__("outputs", []), c.__setitem__("execution_count", None))
    nbformat.validator.normalize(nb); nbformat.write(nb, out); print("v6:", len(cells), "ô ->", out)
if __name__ == "__main__": build()
