"""Dựng notebooks/EW_RIE_HOSE_v7.ipynb = notebook v6 ĐÃ CHẠY (giữ nguyên mã và kết quả) + phần 7 chèn trước "## Ghi chú",
rồi chạy RIÊNG các ô phần 7 trong một kernel đã nạp lại các ô định nghĩa/dữ liệu của v6 (đọc cache, không chạy lại phần cũ).
Dùng: python scripts/build_v7.py [--no-exec]"""
import os, sys, copy, time
for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ[k] = "1"      # như khi tạo cache v6 (khớp bit)
import nbformat
from nbclient import NotebookClient
H = os.path.dirname(os.path.abspath(__file__)); NB = os.path.abspath(os.path.join(H, "..", "notebooks"))
sys.path.insert(0, H); from v7ns import BOOT

LAYOUT7 = [("m", "m7_intro.md"), ("m", "### 7.0 Lõi: tỷ trọng đích, mô phỏng NAV có trôi, kiểm hồi quy với v6"), ("c", "c7_core.py"), ("c", "c7_check.py"),
           ("m", "m7_h1.md"), ("c", "c7_h1_tab.py"), ("c", "c7_h1_fig.py"), ("m", "m7_h2.md"), ("c", "c7_h2.py"),
           ("m", "m7_h3.md"), ("c", "c7_h3.py"), ("m", "m7_h4.md"), ("c", "c7_h4.py"),
           ("m", "### 7.5 Tổng kết phần 7"), ("c", "c7_sum.py")]
TOC_ROW = ("| **7. Nhà đầu tư dài hạn** (v7) | 7.0 Lõi và kiểm hồi quy với v6 · 7.1 Tăng trưởng tài sản: NAV có trôi tỷ trọng, phí và thuế thật, CAGR, MDD, hồi phục, "
           "CVaR, phí Fleming–Kirby–Ostdiek, cổ phiếu ít biến động · 7.2 Tái cân bằng thưa: REB 21–252 × vùng không giao dịch · 7.3 Khủng hoảng: COVID 2020, 2022, "
           "thuế quan 4/2025, cầu chì · 7.4 Thực thi được: trần tỷ trọng, trần turnover, sức chứa vốn · 7.5 Tổng kết | Bảng 35–42, Hình 18–28 |")

def build():
    v6 = nbformat.read(os.path.join(NB, "EW_RIE_HOSE_v6.ipynb"), 4); nb = copy.deepcopy(v6)
    k = next(i for i, c in enumerate(nb.cells) if c.cell_type == "markdown" and c.source.startswith("## Ghi chú\n"))
    new = []
    for kind, x in LAYOUT7:
        src = open(os.path.join(H, "cells", x), encoding="utf-8").read().rstrip("\n") if x.endswith((".md", ".py")) else x
        c = nbformat.v4.new_markdown_cell(src) if kind == "m" else nbformat.v4.new_code_cell(src)
        c.metadata["tags"] = ["v7"]; new.append(c)
    nb.cells = nb.cells[:k] + new + nb.cells[k:]
    toc = nb.cells[2]; assert toc.source.startswith("## Mục lục")
    if "**7. Nhà đầu tư dài hạn**" not in toc.source:
        toc.source = toc.source.replace("| **Ghi chú** |", TOC_ROW + "\n| **Ghi chú** |", 1)
    return nb

def execute(nb):
    client = NotebookClient(nb, timeout=7200, kernel_name="python3", resources={"metadata": {"path": NB}})
    idx = [i for i, c in enumerate(nb.cells) if c.cell_type == "code" and "v7" in c.metadata.get("tags", [])]
    t0 = time.time()
    with client.setup_kernel():
        for i in BOOT:                                       # ô định nghĩa/dữ liệu của v6: chạy trên BẢN SAO, không đổi output v6 trong notebook
            assert "v7" not in nb.cells[i].metadata.get("tags", []); client.execute_cell(copy.deepcopy(nb.cells[i]), i)
        print(f"nạp v6: {time.time() - t0:.0f}s", flush=True)
        for i in idx:
            t = time.time(); client.execute_cell(nb.cells[i], i); print(f"ô {i}: {time.time() - t:.0f}s", flush=True)
    n0 = max(c.get("execution_count") or 0 for c in nb.cells if c.cell_type == "code" and "v7" not in c.metadata.get("tags", []))
    for j, i in enumerate(idx): nb.cells[i].execution_count = n0 + 1 + j
    return nb

if __name__ == "__main__":
    nb = build()
    if "--no-exec" not in sys.argv: nb = execute(nb)
    nbformat.write(nb, os.path.join(NB, "EW_RIE_HOSE_v7.ipynb")); print("đã ghi notebooks/EW_RIE_HOSE_v7.ipynb")
