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
assert np.allclose(net(T2R[63, "long_only"]["out"]["NL-LW"], 0.004).values, o_new["r_net"].values, atol=1e-14)
print("Unit test 200/200 pass: Σw = 1 ⇒ giá trị mua = giá trị bán = turnover/2 ⇒ phí (mua 0,15%, bán 0,25%) ≡ COST đối xứng 0,20%.")
print("Kiểm chứng: r_net tính lại từ turnover trùng với chạy lại backtest thật (REB = 63, COST = 0,40%).")
SC = {"Gộp": None, "COST 0,25% (gốc)": .0025, "Mua 0,15% / bán 0,25%": .002}
T2C = pd.DataFrame([dict(mode=VN[m], method=k, scen=sc, Sharpe=ann(o["r"] if c is None else net(o, c))[1])
                    for m in MODES for k, o in T2R[21, m]["out"].items() for sc, c in SC.items()]).pivot(index="method", columns=["mode", "scen"], values="Sharpe")
T2C = T2C.reindex(index=FULL, columns=pd.MultiIndex.from_product([VN.values(), SC])); save(T2C, "T2c_cost_convention_full")
cap("Bảng", "Sharpe theo quy ước phí (REB = 21), các phương pháp chính. Đủ FULL: `results_v4/T2c_cost_convention_full.csv`.")
show(T2C.loc[MAIN], 3)
