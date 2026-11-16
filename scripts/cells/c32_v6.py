import inspect
ULOG = []
ADJ = {"d": None}          # T2d: {(ngày, mã): cú sốc lợi suất}; None = không điều chỉnh (đúng như bản chuẩn)
def _adj_block(days, tick):
    # ma trận điều chỉnh d (số ngày × N) cho các ngày của kỳ nắm giữ; chỉ cộng vào Y, không đụng tới P hay cửa sổ ước lượng
    M = np.zeros((len(days), len(tick)))
    if ADJ["d"] is not None:
        col = {t: j for j, t in enumerate(tick)}
        for i, dd in enumerate(days):
            for t, j in col.items():
                M[i, j] = ADJ["d"].get((dd, t), 0.0)
    return M
_src = inspect.getsource(run_backtest)
_chk = "        if ok.sum() < N: continue\n"
_sel = "        tick = V.iloc[s - W:s].loc[:, ok].median().sort_values(ascending=False).index[:N]\n"
_Y = "        X = win[tick].fillna(0).values; Y = R.iloc[s:s + REB][tick].fillna(0).values\n"
_S = "            S = estimators[k](X)\n"
assert _src.count(_chk) == 1 and _src.count(_sel) == 1 and _src.count(_Y) == 1 and _src.count(_S) == 1, "mã nguồn run_backtest của thầy đã đổi"
PRE_SHORT = []      # v6 §5.4: số kỳ thiếu phiên trước cửa sổ cho bộ VS "đủ T"
def _xpre(R, s, W, tick, pre):
    # v6: cửa sổ mở rộng thêm `pre` phiên NGAY TRƯỚC cửa sổ ước lượng (chỉ dữ liệu quá khứ) để khởi động EWMA của bộ VS "đủ T"
    a = s - W - pre
    if a < 0: PRE_SHORT.append(-a)
    return R.iloc[max(0, a):s][tick].fillna(0).values
exec(_src.replace("def run_backtest(", "def run_backtest_x(")
         .replace(_chk, '        ok &= (win == 0).mean() <= cfg.get("ZERO_MAX", 1.0)          # v3: lọc mã đứng giá (cửa sổ quá khứ)\n' + _chk)
         .replace(_sel, _sel + "        ULOG.append(dict(date=dates[s], n_eligible=int(ok.sum()), tickers=list(tick)))\n")
         .replace(_S, "            S = estimators[k](X if not getattr(estimators[k], 'pre', 0) else _xpre(R, s, W, tick, estimators[k].pre))            # v6: bộ VS \"đủ T\"\n")
         .replace(_Y, _Y + "        if ADJ[\"d\"] is not None: Y = Y.copy(order=\"K\"); Y += _adj_block(dates[s:s + REB], tick)            # v4 T2d: cú sốc ngày hủy niêm yết (chỉ vào lợi suất nắm giữ)\n"))
run_backtest_thay = run_backtest                        # bản gốc của thầy (đối chứng)
def run_backtest(*a, **k):                              # các ô của thầy gọi run_backtest → dùng bản có lọc (và điều chỉnh nếu ADJ["d"])
    ULOG.clear(); return run_backtest_x(*a, **k)

PERIODS = [("2016-17 Ổn định", "2016-01-01", "2017-12-31"), ("2018-19 Điều chỉnh", "2018-01-01", "2019-12-31"),
           ("2020Q1 COVID", "2020-01-01", "2020-03-31"), ("2020-21 Bùng nổ", "2020-04-01", "2021-12-31"),
           ("2022 Sụt giảm", "2022-01-01", "2022-12-31"), ("2023-24 Phục hồi", "2023-01-01", "2024-12-31"),
           ("2025-26", "2025-01-01", "2026-12-31")]

_p, _v = P.iloc[-900:], V.iloc[-900:]                   # kiểm tra: ZERO_MAX = 1.0 ⇒ trùng hệt bản của thầy; ADJ rỗng ⇒ không đổi
_a = run_backtest_thay(_p, _v, {"NL-LW": est_nllw}, CONFIG, True)["NL-LW"]["r"]
_b = run_backtest(_p, _v, {"NL-LW": est_nllw}, dict(CONFIG, ZERO_MAX=1.0), True)["NL-LW"]["r"]
assert _a.index.equals(_b.index) and np.array_equal(_a.values, _b.values)
ADJ["d"] = {}                                           # d = 0 (dict rỗng nhưng bật nhánh cộng): phải trùng hệt
_c = run_backtest(_p, _v, {"NL-LW": est_nllw}, dict(CONFIG, ZERO_MAX=1.0), True)["NL-LW"]["r"]; ADJ["d"] = None
assert np.array_equal(_b.values, _c.values)
print(f"run_backtest (có lọc) ≡ run_backtest của thầy khi ZERO_MAX = 1.0 ✔ | d = 0 trùng hệt ✔ | cấu hình chuẩn: ZERO_MAX = {CONFIG['ZERO_MAX']:.0%}")
