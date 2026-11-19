# ---- 7.0 (tiếp) Kiểm hồi quy: lợi suất Y·w (tỷ trọng cố định trong kỳ, như run_backtest) từ tỷ trọng đích tính lại phải trùng cache v6 ----
REG7 = check_v6_regression(M7X)
print("Lệch lớn nhất so với lợi suất v6 (chỉ mua, 118 kỳ): " + ", ".join(f"{k} {v:.1e}" for k, v in REG7.items()))
assert (REG7 < 1e-12).all(), "tỷ trọng tính lại không khớp v6"
print(f"✔ khớp v6 cho cả {len(REG7)} bộ | mẫu ngoài mẫu {DATES7[S_REG[0]]:%d/%m/%Y} → {DATES7[END7 - 1]:%d/%m/%Y}, {END7 - S_REG[0]} phiên, {len(S_REG)} kỳ")
