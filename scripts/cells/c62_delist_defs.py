# ---- T2d (định nghĩa): sự kiện hủy niêm yết và cú sốc lợi suất ngày hủy ----
LASTPX = P.apply(lambda s: s.last_valid_index())
DL_REASON = MASTER.dropna(subset=["delisting_date"]).sort_values("delisting_date").groupby("ticker").tail(1).set_index("ticker")["reason"].fillna("chua_ro")
DL_REASON = DL_REASON.where(DL_REASON.isin(["bat_buoc", "hop_nhat", "tu_nguyen", "chuyen_san"]), "chua_ro")
_ev = []
for t in sorted(DELISTED):
    if t in LASTPX.index and pd.notna(LASTPX[t]) and LASTPX[t] < P.index[-1]:
        i = P.index.searchsorted(LASTPX[t], side="right"); _ev.append(dict(ticker=t, last_px=LASTPX[t], next_day=P.index[i], reason=DL_REASON.get(t, "chua_ro")))
DL_EVENTS = pd.DataFrame(_ev)                       # mỗi mã đã hủy có giá: ngày có giá cuối, ngày giao dịch đầu tiên sau đó, lý do
SCENARIOS = {"S0 (0%, hiện tại)": (0.0, ("bat_buoc", "chua_ro")), "S1 (−30%)": (-0.30, ("bat_buoc", "chua_ro")),
             "S2 (−100%)": (-1.0, ("bat_buoc", "chua_ro")), "S1 mọi lý do": (-0.30, ("bat_buoc", "chua_ro", "hop_nhat", "tu_nguyen", "chuyen_san"))}
def delist_adj(name):
    sh, rs = SCENARIOS[name]
    return {(r.next_day, r.ticker): sh for r in DL_EVENTS.itertuples() if r.reason in rs}
def run_full_scn(name, cfg=None, long_only=True, methods=None):
    # chạy FULL với cú sốc hủy niêm yết (tag riêng để không trúng nhầm cache); S0 dùng đúng cache chuẩn
    if name.startswith("S0"): return run_full(cfg, long_only, methods)
    ADJ["d"] = delist_adj(name)
    try: return run_full(cfg, long_only, methods, tag="delist:" + name)
    finally: ADJ["d"] = None
