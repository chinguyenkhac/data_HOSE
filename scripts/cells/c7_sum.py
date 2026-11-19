# ---- 7.5 Tổng kết phần 7 + phân tích chéo (mô tả): vì sao điều chỉnh CHẬM về danh mục đích lại cho lợi suất cao hơn? ----
def trade_returns(nm, H=(21, 63, 126)):
    # lệnh tái cân bằng ở kỳ s (lịch 21, không vùng): Δw = w_đích(s) − w_hiện(s) (w_hiện = đích kỳ trước trôi theo giá); lợi suất của Δw nếu giữ h phiên
    out = {h: [] for h in H}; n = len(TICK7)
    for i in range(1, len(S_REG)):
        s0, s = S_REG[i - 1], S_REG[i]; ix0, W0 = TG[nm][s0]; wc = np.zeros(n); wc[ix0] = W0[0]
        wc *= np.prod(1 + RH[s0:s], axis=0); wc /= wc.sum(); wc[~PX_OK[s - 1]] = 0.0
        ix, Wm = TG[nm][s]; wt = np.zeros(n); wt[ix] = Wm[0]; dw = wt - wc
        for h in H:
            if s + h <= END7: out[h].append(dw @ (np.prod(1 + RH[s:s + h], axis=0) - 1))
    return {h: np.array(v) for h, v in out.items()}
TRD = {nm: trade_returns(nm) for nm in ("EW-RIE*", "VS-NL-LW", "NL-LW")}
def _nw_lag(x, lag):
    # trung bình và p với Newey–West, số trễ = max(L mặc định, số kỳ chồng lấn) (h > 21 ⇒ các quan sát chồng lấn)
    x = np.asarray(x, float); T = len(x); u = (x - x.mean())[:, None]; L = max(int(4 * (T / 100) ** (2 / 9)), lag)
    se = np.sqrt(hac(u, L)[0, 0] / T); return x.mean(), 2 * norm.sf(abs(x.mean() / se))
rows = []
for nm, d in TRD.items():
    for h, x in d.items():
        m, p = _nw_lag(x, h // 21); rows.append({"Phương pháp": nm, "h (phiên)": h, "TB mỗi lệnh %": m * 100, "quy %/năm (×12)": m * 12 * 100, "p NW": p, "số lệnh": len(x)})
TRT = pd.DataFrame(rows); save7(TRT, "S_lenh_tai_can_bang")
E_T = TRT[TRT["Phương pháp"] == "EW-RIE*"]; sig_h = [int(r["h (phiên)"]) for _, r in E_T.iterrows() if r["TB mỗi lệnh %"] < 0 and r["p NW"] < .05]
md("**Phân tích chéo (mô tả, không đăng ký trước).** Lợi suất của chính lệnh tái cân bằng (mua phần đích tăng, bán phần đích giảm so với danh mục đang trôi) nếu giữ h phiên, "
   "trung bình mỗi lệnh (p Newey–West có tính chồng lấn): " + "; ".join(
       f"{nm}: " + ", ".join(f"h = {r['h (phiên)']} → {dv(r['TB mỗi lệnh %'])}% (p {pv(r['p NW'])})" for _, r in TRT[TRT['Phương pháp'] == nm].iterrows()) for nm in TRD)
   + (". Lệnh về đích của EW-RIE\\* có lợi suất trung bình âm và **có ý nghĩa** ở h = " + ", ".join(str(h) for h in sig_h)
      + " phiên ⇒ mỗi lần tái cân bằng, GMV mua các mã sắp kém hơn; điều chỉnh chậm làm lệnh nhỏ đi nên lỗ ít hơn — khớp Hướng 2 và 4." if sig_h else
      ". Với EW-RIE\\*, lợi suất của lệnh về đích âm nhẹ nhưng **không có ý nghĩa** ở mọi h (độ lớn ~1–2 %/năm, nhỏ hơn chênh CAGR 4–5 pp của Hướng 2, 4) "
      "⇒ cơ chế \"lệnh về đích mua mã sắp kém\" **chưa được chứng minh**; chênh CAGR khi điều chỉnh chậm có thể đến từ việc để mã thắng tiếp tục trôi lên, chưa tách được."))

V = {"H1a": T36.loc["VS-NL-LW", "ΔVol (pp)"] < 0 and T36.loc["VS-NL-LW", "p LW-boot"] < .05}
md(f"**Tổng kết phần 7 (nhà đầu tư dài hạn, chỉ mua, sau phí và thuế thật).**\n\n"
   f"| Hướng | Câu hỏi | Kết quả chính | Theo ngưỡng đăng ký trước |\n|---|---|---|---|\n"
   f"| 1 | Tài sản tăng thế nào? | CAGR EW-RIE\\* {f2(T35.loc['EW-RIE*', 'CAGR %'])}%, VS-NL-LW {f2(T35.loc['VS-NL-LW', 'CAGR %'])}%, Thị trường EW {f2(T35.loc['Thị trường EW', 'CAGR %'])}%, "
   f"tiết kiệm 5%; MDD GMV ≈ {f2(T35.loc['EW-RIE*', 'MDD %'], 0)}% | H1a {'đạt' if V['H1a'] else 'không đạt'}; H1b không đạt; H1c: Q1 {_h1c('mọi mã đủ điều kiện')[0].replace('**', '')} |\n"
   f"| 2 | Tái cân bằng thưa? | ΔVol EW-RIE\\* − VS-NL-LW: {' / '.join(dv(x) for x in T38.xs(0.0, level='Vùng %')['ΔVol (pp)'].values)} pp (REB 21/63/126/252) | H2 {H2V}; nhưng phụ thuộc pha và HL_VOL |\n"
   f"| 3 | Khủng hoảng? | Sụt EW-RIE\\* nhỏ hơn VS-NL-LW ở {n_less}/3 đợt; cầu chì: MDD EW-RIE\\* {f2(fE['MDD không %'], 1)} → {f2(fE['MDD có %'], 1)}% | H3a {'đạt' if n_less >= 2 else 'không đạt'}; H3b {'đạt' if H3B else 'không đạt'} (một đợt sụt) |\n"
   f"| 4 | Thực thi được? | Thứ hạng giữ (τ ≥ {f2(min(tau.values()))}); quỹ 100 tỷ bán được {f2(liq['100 tỷ']['EW-RIE*'], 0)}% NAV trong 5 phiên | Thứ hạng {'giữ' if (min(tau.values()) >= .6 and same) else 'không giữ'}; sức chứa không đạt |\n\n"
   "Hàm ý (gợi ý từ các phần mô tả, chưa phải kết luận thống kê): với nhà đầu tư dài hạn trên HOSE, lựa chọn giữa EW-RIE\\* và VS-NL-LW ít quan trọng hơn ba quyết định khác — **mức tập trung** (trần tỷ trọng), "
   "**tốc độ điều chỉnh** (REB, trần turnover) và **quy mô quỹ** so với thanh khoản. GMV chỉ mua thuần túy giảm rủi ro nhưng lợi suất thấp hơn cả tiết kiệm trong 2016–2026.")
