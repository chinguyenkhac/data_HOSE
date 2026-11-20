"""Dựng notebooks/EW_RIE_HOSE_v8.ipynb = notebook v7 ĐÃ CHẠY (giữ nguyên mã và kết quả phần 0–7) + phần 8 chèn trước "## Ghi chú",
rồi chạy RIÊNG các ô phần 8 trong kernel đã nạp ô định nghĩa của v6 và ô lõi §7 (đọc cache). Dùng: python scripts/build_v8.py [--no-exec]"""
import os, sys, copy, time
for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ[k] = "1"
import nbformat
from nbclient import NotebookClient
H = os.path.dirname(os.path.abspath(__file__)); NB = os.path.abspath(os.path.join(H, "..", "notebooks"))
sys.path.insert(0, H); from v7ns import BOOT

SW = [("HL_VOL", "Quét HL_VOL (half-life chuẩn hóa biến động của bộ VS)"), ("h", "Quét h (half-life trọng số mũ của bộ EW)"),
      ("T", "Quét cửa sổ T (bộ VS dùng bản \"đủ T\" của §5.4 vì bản gốc mất HL_VOL phiên khi T nhỏ)"), ("REB", "Quét chu kỳ tái cân bằng REB"), ("N", "Quét số mã N"), ("Lọc", "Quét ngưỡng lọc mã đứng giá")]
LAYOUT8 = [("m", "m8_intro.md"), ("m", "### 8.0 Lõi và kiểm hồi quy"), ("c", "c8_core.py"), ("c", "c8_tables.py"), ("c", "c8_check.py"),
           ("m", "### 8.1 Quét từng siêu tham số\nMỗi lần quét đổi MỘT tham số, giữ các tham số khác ở cấu hình chuẩn. Bảng: Vol của 8 bộ; hình: ΔVol 11 cặp; nhận xét ngay dưới.")]
for sw, t in SW: LAYOUT8 += [("m", f"#### {t}"), ("c", f"sweep_block({sw!r}, {t!r})")]
LAYOUT8 += [("m", "### 8.2 \"Gấp và nhanh\": h × HL_VOL ở REB 5 và 21 — và 8.3 Dài hạn: T × REB"), ("c", "c8_grids.py"),
            ("m", "### 8.4 Kiểm định chung và kết luận"), ("c", "c8_sum.py")]
TOC_ROW = ("| **8. Lưới siêu tham số** (v8) | 8.1 Quét từng tham số (HL_VOL, h, T, REB, N, lọc) với 11 cặp A1–E1 · 8.2 \"Gấp và nhanh\" h × HL_VOL ở REB 5, 21 · "
           "8.3 Dài hạn T × REB · 8.4 Kiểm định chung trên lưới, kết luận | Bảng 43 trở đi, Hình 29 trở đi |")

def build():
    nb = copy.deepcopy(nbformat.read(os.path.join(NB, "EW_RIE_HOSE_v7.ipynb"), 4))
    k = next(i for i, c in enumerate(nb.cells) if c.cell_type == "markdown" and c.source.startswith("## Ghi chú\n"))
    new = []
    for kind, x in LAYOUT8:
        src = open(os.path.join(H, "cells", x), encoding="utf-8").read().rstrip("\n") if x.endswith((".md", ".py")) else x
        c = nbformat.v4.new_markdown_cell(src) if kind == "m" else nbformat.v4.new_code_cell(src)
        c.metadata["tags"] = ["v8"]; new.append(c)
    nb.cells = nb.cells[:k] + new + nb.cells[k:]
    toc = nb.cells[2]
    if "**8. Lưới siêu tham số**" not in toc.source: toc.source = toc.source.replace("| **Ghi chú** |", TOC_ROW + "\n| **Ghi chú** |", 1)
    return nb

def execute(nb):
    client = NotebookClient(nb, timeout=14400, kernel_name="python3", resources={"metadata": {"path": NB}})
    idx = [i for i, c in enumerate(nb.cells) if c.cell_type == "code" and "v8" in c.metadata.get("tags", [])]
    core7 = next(i for i, c in enumerate(nb.cells) if "v7" in c.metadata.get("tags", []) and c.source.startswith("# ---- 7.0 Lõi"))
    with client.setup_kernel():
        for i in BOOT + [core7]: client.execute_cell(copy.deepcopy(nb.cells[i]), i)
        for i in idx:
            t = time.time(); client.execute_cell(nb.cells[i], i); print(f"ô {i}: {time.time() - t:.0f}s", flush=True)
    n0 = max(c.get("execution_count") or 0 for c in nb.cells if c.cell_type == "code" and "v8" not in c.metadata.get("tags", []))
    for j, i in enumerate(idx): nb.cells[i].execution_count = n0 + 1 + j
    return nb

if __name__ == "__main__":
    nb = build()
    if "--no-exec" not in sys.argv: nb = execute(nb)
    nbformat.write(nb, os.path.join(NB, "EW_RIE_HOSE_v8.ipynb")); print("đã ghi notebooks/EW_RIE_HOSE_v8.ipynb")
