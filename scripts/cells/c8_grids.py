# ---- 8.2 / 8.3 Lưới hai chiều: "gấp và nhanh" (h × HL_VOL, REB 5 và 21) và dài hạn (T × REB); cặp E1, D1, C3 ----
def grid_heat(tier, sw, rows, cols, rlab, clab, title):
    d = T8[(T8.tier == tier) & (T8.sweep == sw)].copy(); d["rc"] = d["label"]
    fig, axs = plt.subplots(2, 3, figsize=(15, 7.4))
    for i, m in enumerate(("so", "lo")):
        for j, pk in enumerate(FOCUS8):
            x = d[(d.pair == pk) & (d["mode"] == m)].set_index("label"); a = axs[i, j]
            D = np.array([[x.loc[str((r, c)), "dvol"] for c in cols] for r in rows]); Pm = np.array([[x.loc[str((r, c)), "p Holm"] for c in cols] for r in rows])
            a.imshow(D, cmap="RdBu_r", vmin=-1.2, vmax=1.2, aspect="auto")
            for u in range(len(rows)):
                for v in range(len(cols)):
                    a.text(v, u, dv(D[u, v]) + ("*" if Pm[u, v] < .05 else ""), ha="center", va="center", fontsize=8, color="white" if abs(D[u, v]) > .7 else "#202124")
            a.set_xticks(range(len(cols))); a.set_xticklabels(cols, fontsize=8); a.set_yticks(range(len(rows))); a.set_yticklabels(rows, fontsize=8)
            a.set_xlabel(clab, fontsize=8); a.set_ylabel(rlab, fontsize=8); a.set_title(f"{MODES8[m]} — {PLAB8[pk]}", fontsize=9)
    plt.tight_layout(); savefig8(fig, f"grid_{sw.replace(' ', '_').replace('×', 'x')}")
    cap("Hình", title)
    return d

def grid_note(d, cond=None, cond_lab=""):
    out = []
    for pk in FOCUS8:
        for m in ("so", "lo"):
            x = d[(d.pair == pk) & (d["mode"] == m)]; sg = x[x["p Holm"] < .05]
            s_ = f"{pk} {MODES8[m].lower()}: âm ở {int((x.dvol < 0).sum())}/{len(x)} ô, có ý nghĩa {len(sg)} ô"
            if len(sg): s_ += f" (âm {int((sg.dvol < 0).sum())}, dương {int((sg.dvol > 0).sum())})"
            if cond is not None:
                y = x[x.label.map(cond)]; s_ += f"; {cond_lab}: ΔVol TB {dv(y.dvol.mean())} pp"
            out.append(s_)
    return "; ".join(out)

H8_ROWS, H8_COLS = (15, 30, 60, 120), (5, 10, 20, 30, 40, 60)
FAST = lambda lab: eval(lab)[0] <= 30 and eval(lab)[1] <= 10
GD = {}
for reb in (5, 21):
    GD[reb] = grid_heat("T2", f"h×HL REB {reb}", H8_ROWS, H8_COLS, "h (EW)", "HL_VOL (VS)",
                        f"Lưới \"gấp và nhanh\" h × HL_VOL ở REB = {reb}: ΔVol (pp/năm) của E1 (EW-RIE\\* − VS-NL-LW), D1 (VS-EW-RIE\\* − VS-NL-LW, cùng HL_VOL: chỉ khác bộ làm sạch), "
                        f"C3 (VS-EW-RIE\\* − EW-RIE\\*, cùng h: có/không VS); * = p Holm < 0,05 (Holm trên 24 ô của mỗi cặp × chế độ).")
    md(f"*Nhận xét (REB = {reb}).* " + grid_note(GD[reb], FAST, "vùng nhanh h ≤ 30, HL_VOL ≤ 10")
       + ". E1 chỉ phụ thuộc h theo hàng và HL_VOL theo cột; D1 cho biết bộ làm sạch RIE\\* có thêm gì khi đã chuẩn hóa biến động; C3 cho biết VS có giúp EW-RIE\\* không.")

# bảng: cấu hình tốt nhất của từng bộ chính trên lưới nhanh (Vol thấp nhất) so với cấu hình chuẩn
rows = []
for reb in (5, 21):
    for m in ("so", "lo"):
        for nm, grid in (("EW-RIE*", [(h, 20) for h in H8_ROWS]), ("VS-NL-LW", [(60, hv) for hv in H8_COLS]), ("VS-EW-RIE*", [(h, hv) for h in H8_ROWS for hv in H8_COLS])):
            v = {g: returns8(nm, C(h=g[0], hv=g[1]), reb)[m][0].std() * np.sqrt(252) * 100 for g in grid}; b = min(v, key=v.get)
            par = f"h = {b[0]}" if nm == "EW-RIE*" else (f"HL_VOL = {b[1]}" if nm == "VS-NL-LW" else f"h = {b[0]}, HL_VOL = {b[1]}")
            rows.append({"REB": reb, "Chế độ": MODES8[m], "Bộ": nm, "Vol chuẩn %": returns8(nm, STD8, reb)[m][0].std() * np.sqrt(252) * 100,
                         "Vol tốt nhất %": v[b], "Tham số tốt nhất": par, "Vol xấu nhất %": max(v.values())})
TB8F = pd.DataFrame(rows).set_index(["REB", "Chế độ", "Bộ"]); save8(TB8F, "tot_nhat_luoi_nhanh")
cap("Bảng", "Lưới \"gấp và nhanh\": Vol (%/năm) ở cấu hình chuẩn (h = 60, HL_VOL = 20) và ở tham số tốt nhất/xấu nhất trên lưới (chọn SAU khi thấy kết quả ⇒ lạc quan, chỉ để so biên độ), "
    "ba bộ chính, REB 5 và 21, hai chế độ.")
show(TB8F)
gain = TB8F["Vol chuẩn %"] - TB8F["Vol tốt nhất %"]
md(f"*Nhận xét.* Chỉnh tham số tốt nhất (nhìn trước) giảm Vol tối đa: " + "; ".join(f"{r[2]} REB {r[0]} {r[1].lower()} {f2(g)} pp" for r, g in gain.items())
   + ". Sau khi mỗi bộ đã được chỉnh tốt nhất, bộ thấp nhất mỗi dòng (REB × chế độ): "
   + "; ".join(f"REB {k[0]} {k[1].lower()}: {TB8F.loc[k, 'Vol tốt nhất %'].idxmin()}" for k in TB8F.index.droplevel(2).unique()) + ".")

# ---- 8.3 dài hạn: T × REB ----
GT8 = grid_heat("T3", "T×REB", (120, 250, 500, 750), (5, 21, 63, 252), "T (cửa sổ)", "REB (phiên)",
                "Lưới dài hạn T × REB: ΔVol (pp/năm) của E1, D1, C3; * = p Holm < 0,05 (Holm trên 16 ô của mỗi cặp × chế độ). Mỗi T có mẫu ngoài mẫu riêng (T dài ⇒ bắt đầu muộn hơn).")
LONG = lambda lab: eval(lab)[0] >= 500 and eval(lab)[1] >= 63
md("*Nhận xét.* " + grid_note(GT8, LONG, "vùng dài T ≥ 500, REB ≥ 63") + ".")
rows = []
for W in (120, 250, 500, 750):
    for reb in (5, 21, 63, 252):
        rows.append({"T": W, "REB": reb, **{f"{nm} ({MODES8[m]})": returns8(nm, C(W=W, full=True), reb)[m][0].std() * np.sqrt(252) * 100
                                            for m in ("lo", "so") for nm in ("EW-RIE*", "VS-EW-RIE*", "VS-NL-LW")},
                     "Bắt đầu": returns8("EW-RIE*", C(W=W, full=True), reb)["lo"][0].index[0].strftime("%m/%Y")})
TB8T = pd.DataFrame(rows).set_index(["T", "REB"]); save8(TB8T, "vol_T_REB")
cap("Bảng", "Lưới dài hạn T × REB: Vol (%/năm) của ba bộ chính, chỉ mua và bán khống; cột cuối: tháng bắt đầu mẫu ngoài mẫu.")
show(TB8T)
bl = {m: TB8T[[f"{nm} ({MODES8[m]})" for nm in ("EW-RIE*", "VS-EW-RIE*", "VS-NL-LW")]].idxmin(1).str.replace(f" ({MODES8[m]})", "", regex=False) for m in ("lo", "so")}
md("*Nhận xét.* Số ô mỗi bộ có Vol thấp nhất — chỉ mua: " + ", ".join(f"{k} {v}" for k, v in bl['lo'].value_counts().items())
   + "; bán khống: " + ", ".join(f"{k} {v}" for k, v in bl['so'].value_counts().items())
   + ". Vol của EW-RIE\\* (chỉ mua) thấp nhất ở " + ", ".join(f"T = {i[0]}, REB = {i[1]}" for i in [TB8T["EW-RIE* (Chỉ mua)"].idxmin()]) + ".")
