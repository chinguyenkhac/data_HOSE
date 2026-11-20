# ---- 8.0 (tiếp) Kiểm hồi quy: cấu hình chuẩn, REB = 21 phải trùng lợi suất cache v6 (cả hai chế độ) ----
for nm in ("EW-RIE*", "VS-EW-RIE*", "VS-NL-LW", "NL-LW", "EW-NL-LW", "EW-RIE (q_eff)", "RIE", "VS-RIE"):
    for m, mm in (("lo", "long_only"), ("so", "short_ok")):
        r = returns8(nm, STD8, 21)[m][0]; ref = OUT0[mm][nm]["r"]
        assert r.index.equals(ref.index) and float(np.abs(r.values - ref.values).max()) < 1e-12, (nm, m)
print(f"✔ lõi §8 khớp v6 cho 8 bộ × 2 chế độ ở cấu hình chuẩn | {len(T8) if 'T8' in globals() else 'chưa nạp'} kiểm định đã cache")
