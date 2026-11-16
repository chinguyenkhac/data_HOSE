# ---- 4.4 So sánh mọi cặp trong nhóm dẫn đầu, cấu hình chuẩn (cần STD/OUT0/REB_DATES từ ô ngay trên) ----
PWS = {m: pairwise_top(OUT0[m], TOP, REB_DATES) for m in MODES}
save(pd.concat({m: PWS[m][0] for m in MODES}, names=["mode", "i"]).reset_index().drop(columns="i"), "T44_pairwise_std")
for m in MODES:
    PW = PWS[m][0].rename(columns=dict(a="A", b="B", dvol="ΔVol (A−B), pp", p_hac="p LW-HAC", p_boot="p LW-boot", p_jkm="p JKM", dturn="ΔTurnover (A−B)", p_holm="p Holm (15 cặp)"))
    cap("Bảng", f"{VN[m]}: 15 cặp trong nhóm dẫn đầu, {th(len(OUT0[m]['EW-RIE*']['r']))} phiên OOS chung. ΔVol = Vol(A) − Vol(B) (< 0: A rủi ro thấp hơn); p Holm hiệu chỉnh trên cả 15 cặp. Đủ cột: `{RESULTS_DIR}/T44_pairwise_std.csv`.")
    show(PW.set_index(["A", "B"]).sort_values("p Holm (15 cặp)"), 3)
def pw_heatmap(PWD, title_fn, fname, capt):
    fig, ax = plt.subplots(1, 2, figsize=(13, 5.4))
    for a, m in zip(ax, MODES):
        _, D, S = PWD[m]; ms = list(D.index); M_ = D.values.copy(); vm = np.nanmax(np.abs(M_))
        im = a.imshow(M_, cmap="RdBu_r", vmin=-vm, vmax=vm)
        for i in range(len(ms)):
            for j in range(len(ms)):
                if i != j: a.text(j, i, f"{M_[i, j]:+.2f}{S.iloc[i, j]}", ha="center", va="center", fontsize=8, color="white" if abs(M_[i, j]) > .6 * vm else "black")
        a.set_xticks(range(len(ms)), ms, rotation=35, ha="right", fontsize=8); a.set_yticks(range(len(ms)), ms, fontsize=8); a.set_title(title_fn(m), fontsize=10)
        plt.colorbar(im, ax=a, fraction=.046, label="ΔVol (hàng − cột), pp/năm")
    plt.tight_layout(); savefig(fig, fname); cap("Hình", capt)
pw_heatmap(PWS, lambda m: VN[m], "fig_pairwise_std",
           "Ma trận ΔVol = Vol(hàng) − Vol(cột) giữa 6 bộ đầu bảng, cấu hình chuẩn (đỏ: hàng có rủi ro cao hơn; xanh: thấp hơn). Dấu \\* = p Holm < 0,05 trên 15 cặp.")
_e = lambda s: s.replace("*", "\\*"); _dv = lambda x: f"{x:+.2f}".replace(".", ",").replace("-", "−")
_pH = lambda p: "< 0,01" if p < .01 else f"= {p:.2f}".replace(".", ",")
def pw_text(PWD, scope=""):
    t = []
    for m in MODES:
        PW = PWD[m][0]; sig = PW[PW["p_holm"] < .05]; ns_ = PW[PW["p_holm"] >= .05]
        s = ", ".join(f"{_e(r.a)} {'<' if r.dvol < 0 else '>'} {_e(r.b)} (ΔVol {_dv(r.dvol)} pp, p Holm {_pH(r.p_holm)})" for r in sig.itertuples())
        t.append(f"**{VN[m]}:** {len(sig)}/{len(PW)} cặp phân biệt được (p Holm < 0,05)" + (f": {s}." if len(sig) else ".") + f" {len(ns_)} cặp còn lại không phân biệt được rủi ro.")
    return " ".join(t)
md(f"**Kết quả.** {pw_text(PWS)}")
_sig = lambda m: {frozenset((r.a, r.b)) for r in PWS[m][0].itertuples() if r.p_holm < .05}
_eqv = [k for k in TOP if k != "EW-NL-LW" and all(frozenset(("EW-RIE*", k)) not in _sig(m) for m in MODES)]
md(f"**Kết luận.** EW-RIE\\* không phân biệt được về rủi ro với {', '.join(_e(k) for k in _eqv)} ở cả hai chế độ (p Holm ≥ 0,05); "
   f"riêng EW-NL-LW {'khác' if all(frozenset(('EW-RIE*', 'EW-NL-LW')) in _sig(m) for m in MODES) else 'không khác ở mọi chế độ so với'} EW-RIE\\* có ý nghĩa. Xem ΔTurnover trong bảng: cùng rủi ro nhưng turnover khác nhau là chỗ các bộ này thật sự khác nhau.")
open(f"{RESULTS_DIR}/pairwise_sentence.txt", "w", encoding="utf-8").write(f"Trong nhóm dẫn đầu (15 cặp, Holm): " + pw_text(PWS).replace("**", ""))
