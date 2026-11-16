# ---- T5d: Bảng 33 — NL-LW, VS chỉ phần chung, VS chỉ phần riêng, VS đầy đủ (= VS-NL-LW); cấu hình chuẩn, hai chế độ ----
K5D = ["NL-LW", "VS chỉ phần chung", "VS chỉ phần riêng", "VS-NL-LW"]
T5D = {m: run_full(CONFIG, lo, K5D) for m, lo in MODES.items()}
for m in MODES: assert np.array_equal(T5D[m]["out"]["VS-NL-LW"]["r"].values, OUT0[m]["VS-NL-LW"]["r"].values)      # VS đầy đủ trùng số cấu hình chuẩn
rows = []
for m in ("short_ok", "long_only"):
    out = T5D[m]["out"]; tt = pair_table(out, [("T5d", k, "NL-LW") for k in K5D[1:]])
    for k in K5D:
        r = out[k]["r"]; row = {"Chế độ": VN[m], "Bộ": "VS đầy đủ (VS-NL-LW)" if k == "VS-NL-LW" else k, "Vol toàn mẫu": r.std() * np.sqrt(252) * 100}
        row.update({p: r[s0:s1].std() * np.sqrt(252) * 100 for p, s0, s1 in PERIODS if len(r[s0:s1]) > 21})
        if k != "NL-LW":
            t = tt.xs(f"{k} − NL-LW", level=1).iloc[0]
            row.update({"ΔVol vs NL-LW [CI]": f"{dv(t['ΔVol (pp)'])} [{dv(t['CI lo'])}; {dv(t['CI hi'])}]", "p LW-boot": t["p LW-boot"], "p Holm (3 cặp)": t["p Holm"]})
        rows.append(row)
T33 = pd.DataFrame(rows).set_index(["Chế độ", "Bộ"]); save(T33, "T5d_vs_split")
cap("Bảng", "VS nhờ phần chung hay phần riêng: Vol (%/năm) toàn mẫu và theo giai đoạn; ΔVol so với NL-LW [CI 95% bootstrap khối], p kiểm định phương sai (Holm trên 3 cặp, riêng từng chế độ). Cùng bộ làm sạch NL-LW.")
show(T33, 2)
v33 = lambda m, k, c: T33.loc[(VN[m], k), c]
gain = {m: {k: v33(m, "NL-LW", "Vol toàn mẫu") - v33(m, k, "Vol toàn mẫu") for k in ("VS chỉ phần chung", "VS chỉ phần riêng", "VS đầy đủ (VS-NL-LW)")} for m in MODES}
gcv = {m: {k: v33(m, "NL-LW", "2020Q1 COVID") - v33(m, k, "2020Q1 COVID") for k in ("VS chỉ phần chung", "VS chỉ phần riêng", "VS đầy đủ (VS-NL-LW)")} for m in MODES}
main_ = {m: max(("VS chỉ phần chung", "VS chỉ phần riêng"), key=lambda k: gain[m][k]) for m in MODES}
md("**Kết quả.** Mức giảm Vol so với NL-LW (toàn mẫu, pp): " + "; ".join(f"{VN[m]}: phần chung {f2(gain[m]['VS chỉ phần chung'])}, phần riêng {f2(gain[m]['VS chỉ phần riêng'])}, đầy đủ {f2(gain[m]['VS đầy đủ (VS-NL-LW)'])}" for m in ("short_ok", "long_only"))
   + ". Ở 2020Q1 COVID: " + "; ".join(f"{VN[m]}: phần chung {f2(gcv[m]['VS chỉ phần chung'])}, phần riêng {f2(gcv[m]['VS chỉ phần riêng'])}, đầy đủ {f2(gcv[m]['VS đầy đủ (VS-NL-LW)'])}" for m in ("short_ok", "long_only")) + ".\n\n"
   f"**Kết luận.** Đóng góp chính đến từ **{main_['long_only'].replace('VS chỉ ', '')}** (chỉ mua) và **{main_['short_ok'].replace('VS chỉ ', '')}** (bán khống); đây là cách nhóm hiểu gợi ý (a), cần thầy xác nhận.")
