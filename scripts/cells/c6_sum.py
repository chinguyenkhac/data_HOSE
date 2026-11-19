# ---- Tổng kết: Bảng 34 — 12 cặp × (số ô, ΔVol < 0, âm có ý nghĩa, dương có ý nghĩa, ΔVol trung vị) ----
DROP = {"h = 60", "HL_VOL = 20", "REB = 21", "T = 250"}
Dall, Pall = [], []
for G in (G53, G54, G2A, G2B):
    for m, (D, Pm) in G.items():
        keep = [c for c in D.columns if c not in DROP]; Dall.append(D[keep].add_prefix(f"{m}|")); Pall.append(Pm[keep].add_prefix(f"{m}|"))
Dall, Pall = pd.concat(Dall, axis=1), pd.concat(Pall, axis=1)
T34 = pd.DataFrame({"Số ô": Dall.notna().sum(1), "ΔVol < 0": (Dall < 0).sum(1), "Âm có ý nghĩa": ((Dall < 0) & (Pall < .05)).sum(1),
                    "Dương có ý nghĩa": ((Dall > 0) & (Pall < .05)).sum(1), "ΔVol trung vị (pp)": Dall.median(1)})
save(T34, "T_summary_clusters")
cap("Bảng", f"Tổng kết 12 cặp trên mọi ô (cấu hình × chế độ) của Hình 8, 9, 11, 13 ({Dall.shape[1]} cột; cụm A, B không có ở các cột HL\\_VOL). "
    "Có ý nghĩa = p Holm < 0,05 trong từng cột; p-value mang tính mô tả, không hiệu chỉnh xuyên cấu hình.")
show(T34, 2)
def clus(c):
    t = T34[T34.index.get_level_values(0).str.startswith(c)]
    return "; ".join(f"{e_(p)}: âm {int(r['ΔVol < 0'])}/{int(r['Số ô'])} ô ({int(r['Âm có ý nghĩa'])} có ý nghĩa, {int(r['Dương có ý nghĩa'])} dương có ý nghĩa), trung vị {dv(r['ΔVol trung vị (pp)'])}" for (_, p), r in t.iterrows())
md("**Kết quả.**\n\n" + "\n".join(f"- **{c}.** {clus(c)}." for c in "ABCDE"))
_r34 = lambda p: T34.xs(p, level=1).iloc[0]
md(f"**Kết luận.** Cụm A: EW-RIE\\* thấp hơn EW-NL-LW ở {int(_r34('EW-RIE* − EW-NL-LW')['ΔVol < 0'])}/{int(_r34('EW-RIE* − EW-NL-LW')['Số ô'])} ô; "
   f"cụm E (EW-RIE\\* − VS-NL-LW) có ý nghĩa ở {int(_r34('EW-RIE* − VS-NL-LW')['Âm có ý nghĩa'] + _r34('EW-RIE* − VS-NL-LW')['Dương có ý nghĩa'])}/{int(_r34('EW-RIE* − VS-NL-LW')['Số ô'])} ô.")
