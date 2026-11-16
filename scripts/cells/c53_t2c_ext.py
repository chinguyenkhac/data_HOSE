# T2c (v5): kiểm định Sharpe sau phí EW-RIE* vs VS-NL-LW (Jobson–Korkie–Memmel trên lợi suất ròng) và mức phí hòa vốn của Sharpe sau phí.
from scipy.optimize import brentq
def sharpe_net(o, c): return ann(net(o, c))[1]
rows = []
for m in MODES:
    a_, b_ = T2R[21, m]["out"]["EW-RIE*"], T2R[21, m]["out"]["VS-NL-LW"]
    for lab, c in (("gộp", 0.0), ("COST 0,20%", .002), ("COST 0,25% (gốc)", .0025)):
        ra, rb = (a_["r"], b_["r"]) if c == 0 else (net(a_, c), net(b_, c)); assert ra.index.equals(rb.index)
        z, p = jkm_test(ra.values, rb.values); rows.append({"Chế độ": VN[m], "Phí": lab, "Sharpe EW-RIE*": ann(ra)[1], "Sharpe VS-NL-LW": ann(rb)[1], "ΔSharpe (EW-RIE* − VS-NL-LW)": ann(ra)[1] - ann(rb)[1], "p JKM": p})
T2J = pd.DataFrame(rows).set_index(["Chế độ", "Phí"]); save(T2J.reset_index(), "T2c_sharpe_jkm")
cap("Bảng", "Sharpe và kiểm định Jobson–Korkie–Memmel (p hai phía) giữa EW-RIE\\* và VS-NL-LW trên lợi suất gộp/ròng, REB = 21; ΔSharpe < 0: EW-RIE\\* thấp hơn.")
show(T2J, 3)
BE = {}
for m in MODES:
    a_, b_ = T2R[21, m]["out"]["EW-RIE*"], T2R[21, m]["out"]["VS-NL-LW"]; g = lambda c: sharpe_net(a_, c) - sharpe_net(b_, c)
    BE[m] = brentq(g, 0, 0.05) if g(0) * g(0.05) < 0 else np.nan
BEs = {m: (f"{BE[m]:.2%}".replace(".", ",") if np.isfinite(BE[m]) else "không có trong [0; 5%]") for m in MODES}
md("**Kết quả (v5).** Mức phí một chiều làm Sharpe sau phí của EW-RIE\\* bằng VS-NL-LW (hòa vốn): " + f"chỉ mua {BEs['long_only']}, bán khống {BEs['short_ok']}. "
   + " ".join(f"{VN[m]}, COST 0,25%: ΔSharpe {f2(T2J.loc[(VN[m], 'COST 0,25% (gốc)'), 'ΔSharpe (EW-RIE* − VS-NL-LW)'], 3)}, p JKM {pv(T2J.loc[(VN[m], 'COST 0,25% (gốc)'), 'p JKM'])}." for m in MODES)
   + " Hòa vốn nằm ngoài [0; 5%] nghĩa là EW-RIE\\* ít giao dịch hơn nhưng không bù được chênh lệch Sharpe gộp.")
