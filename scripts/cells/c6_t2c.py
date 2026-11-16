# T2c. Quy ước chi phí. run_backtest: phí kỳ = COST × Σ|w_mới − w_cũ| ⇒ COST là phí MỘT CHIỀU áp cho cả mua lẫn bán.
# HOSE: phí môi giới ~0,15% mỗi chiều + thuế bán 0,1% ⇒ bất đối xứng (mua 0,15%, bán 0,25%).
def trade_cost(w_new, w_old, c_buy, c_sell):
    u = w_new.index.union(w_old.index); d = w_new.reindex(u, fill_value=0) - w_old.reindex(u, fill_value=0)
    return c_buy * d.clip(lower=0).sum() + c_sell * (-d).clip(lower=0).sum()
rng = np.random.default_rng(SEED)
for _ in range(200):     # unit test: có mã ra/vào universe và tỷ trọng âm (bán khống), Σw = 1 ở cả hai kỳ
    a_ = pd.Series(rng.normal(size=6), index=list("ABCDEF")); a_ /= a_.sum(); b_ = pd.Series(rng.dirichlet(np.ones(4)), index=list("DEFG"))
    u = a_.index.union(b_.index); turn = (a_.reindex(u, fill_value=0) - b_.reindex(u, fill_value=0)).abs().sum()
    assert np.isclose(trade_cost(a_, b_, .0025, .0025), .0025 * turn) and np.isclose(trade_cost(a_, b_, .0015, .0025), .002 * turn)
o_new = run({"NL-LW": est_nllw}, dict(CONFIG, REB=63, COST=0.004))["out"]["NL-LW"]          # chạy lại thật với COST khác
assert np.allclose(net(T2R[(63, "long_only")]["out"]["NL-LW"], 0.004).values, o_new["r_net"].values, atol=1e-14)
SC = {"Gộp": None, "COST 0,25% (chuẩn)": .0025, "Mua 0,15% / bán 0,25%": .002}
T22 = pd.concat({(VN[m], sc): pd.Series({k: ann(o["r"] if c is None else net(o, c))[1] for k, o in T2R[(21, m)]["out"].items()}) for m in ("short_ok", "long_only") for sc, c in SC.items()}, axis=1).reindex(M12)
save(T22, "T2c_sharpe_convention")
cap("Bảng", "Sharpe (năm hóa) theo quy ước phí, REB = 21, 12 phương pháp; in đậm: cao nhất mỗi cột. Với Σw = 1, giá trị mua = giá trị bán = turnover/2 nên phí (mua 0,15%, bán 0,25%) ≡ COST đối xứng 0,20% (unit test 200 trường hợp, và r_net tính lại khớp backtest chạy lại thật).")
display(T22.style.format(precision=3, decimal=",").highlight_max(axis=0, props="font-weight: bold"))
md("**Kết quả.** Sharpe theo phí thực tế (mua 0,15% / bán 0,25%) — " + "; ".join(f"{VN[m]}: cao nhất {e_(T22[(VN[m], 'Mua 0,15% / bán 0,25%')].idxmax())} ({f2(T22[(VN[m], 'Mua 0,15% / bán 0,25%')].max(), 3)}), EW-RIE\\* {f2(T22.loc['EW-RIE*', (VN[m], 'Mua 0,15% / bán 0,25%')], 3)}, VS-NL-LW {f2(T22.loc['VS-NL-LW', (VN[m], 'Mua 0,15% / bán 0,25%')], 3)}" for m in ("short_ok", "long_only")) + ".\n\n"
   f"**Kết luận.** Giả định COST = 0,25% hơi bảo thủ so với phí thực tế (tương đương 0,20%); thứ tự Sharpe của 12 bộ giữa hai quy ước phí "
   + ("không đổi." if all((T22[(VN[m], 'COST 0,25% (chuẩn)')].rank() == T22[(VN[m], 'Mua 0,15% / bán 0,25%')].rank()).all() for m in MODES) else "có đổi ở vài vị trí."))
