"""Kiểm notebook v7: (1) mọi ô v6 giữ nguyên mã VÀ kết quả (trừ ô Mục lục chỉ thêm một dòng); (2) các ô phần 7 không lỗi;
(3) đủ Bảng 35–42, Hình 18–28 theo thứ tự, 11 ảnh; (4) kiểm hồi quy với v6 đạt; (5) HTML có đủ ảnh. Ghi results_v7/check_v7.json."""
import os, re, json, nbformat
H = os.path.dirname(os.path.abspath(__file__)); NB = os.path.join(H, "..", "notebooks")
v6 = nbformat.read(os.path.join(NB, "EW_RIE_HOSE_v6.ipynb"), 4); v7 = nbformat.read(os.path.join(NB, "EW_RIE_HOSE_v7.ipynb"), 4)
new = [i for i, c in enumerate(v7.cells) if "v7" in c.metadata.get("tags", [])]; k = new[0]; n = len(new)
assert new == list(range(k, k + n)), "các ô v7 phải liền nhau"
out = {"so_o_v6": len(v6.cells), "so_o_v7": len(v7.cells), "so_o_moi": n}
same = []
for j, c6 in enumerate(v6.cells):
    c7 = v7.cells[j if j < k else j + n]
    if j == 2:      # Mục lục: chỉ thêm một dòng cho phần 7
        ok = c7.source.replace(next(l for l in c7.source.split("\n") if "**7. Nhà đầu tư dài hạn**" in l) + "\n", "") == c6.source
    else:
        ok = c6.cell_type == c7.cell_type and c6.source == c7.source and json.dumps(c6.get("outputs", []), sort_keys=True) == json.dumps(c7.get("outputs", []), sort_keys=True)
    same.append(ok)
out["v6_giu_nguyen"] = f"{sum(same)}/{len(same)}"
errs, caps, imgs, texts = [], [], 0, []
for i in new:
    for o in v7.cells[i].get("outputs", []):
        if o.output_type == "error": errs.append((i, o.ename))
        if o.output_type == "stream" and "Traceback" in o.text: errs.append((i, "stderr"))
        d = o.get("data", {})
        if "image/png" in d: imgs += 1
        t = d.get("text/markdown", "") + (o.text if o.output_type == "stream" else "")
        texts.append(t); caps += re.findall(r"\*\*(Bảng|Hình) (\d+)\.\*\*", t)
out["loi"] = errs
B = [int(x) for kd, x in caps if kd == "Bảng"]; F = [int(x) for kd, x in caps if kd == "Hình"]
out["bang"], out["hinh"], out["anh"] = B, F, imgs
out["bang_ok"], out["hinh_ok"], out["anh_ok"] = B == list(range(35, 43)), F == list(range(18, 29)), imgs == 11
out["hoi_quy_v6"] = any("✔ khớp v6" in t for t in texts)
for f in ("EW_RIE_HOSE_v7.html", "EW_RIE_HOSE_v7_gon.html"):
    p = os.path.join(NB, f)
    if os.path.exists(p):
        h = open(p, encoding="utf-8").read(); out[f] = {"anh": h.count("data:image/png"), "loi": h.count("Traceback (most recent")}
out["dat"] = bool(sum(same) == len(same) and not errs and out["bang_ok"] and out["hinh_ok"] and out["anh_ok"] and out["hoi_quy_v6"])
json.dump(out, open(os.path.join(NB, "results_v7", "check_v7.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
