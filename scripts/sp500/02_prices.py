"""Tải giá & khối lượng ngày từ Yahoo Finance (yfinance) cho mọi mã từng thuộc
S&P 500 trong 2015-01-01 → 2026-11-13, rồi ghép thành bảng rộng (hàng = ngày, cột = mã).

Usage: python3 -I scripts/sp500/02_prices.py "data_s&p500"
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf

OUT = Path(sys.argv[1])
START, END = "2015-01-01", "2026-11-14"   # end của Yahoo là exclusive -> lấy tới 13/11
CACHE = OUT / "raw" / "_yahoo_cache"
CACHE.mkdir(parents=True, exist_ok=True)

master = pd.read_csv(OUT / "security_master.csv", parse_dates=["member_from", "member_to"])
tickers = sorted(master.ticker.unique())


def ysym(t):
    if "." in t and t.split(".")[-1] in ("OLD", "21CF"):
        return None   # danh tính lịch sử, mã trên Yahoo đã bị tái sử dụng
    return t.replace(".", "-")


todo = [t for t in tickers if ysym(t) and not (CACHE / f"{t}.csv").exists()]
print("to download:", len(todo))
for i in range(0, len(todo), 40):
    batch = todo[i:i + 40]
    syms = [ysym(t) for t in batch]
    for attempt in range(4):
        try:
            df = yf.download(syms, start=START, end=END, auto_adjust=False, actions=False,
                             group_by="ticker", threads=True, progress=False)
            break
        except Exception as e:   # noqa: BLE001
            print("retry", attempt, e)
            time.sleep(10 * (attempt + 1))
    for t, s in zip(batch, syms):
        try:
            d = df[s].dropna(how="all")
        except KeyError:
            d = pd.DataFrame()
        d.to_csv(CACHE / f"{t}.csv")
    print(i + len(batch), "/", len(todo))
    time.sleep(2)

cal = pd.read_pickle(OUT / "raw" / "_membership_calendar.pkl")

# Một mã có nhiều giai đoạn thành phần có thể là các công ty khác nhau (mã bị tái sử dụng,
# vd. SNDK: SanDisk cũ 2015-2016, Sandisk mới 2025-). Nếu dữ liệu Yahoo bắt đầu sau một
# giai đoạn cũ thì giai đoạn đó thuộc công ty cũ -> đổi danh tính thành <mã>.OLD.
split_log = []
for t, rows in master.groupby("ticker"):
    if len(rows) < 2 or not ysym(t) or not (CACHE / f"{t}.csv").exists():
        continue
    d = pd.read_csv(CACHE / f"{t}.csv", index_col=0, parse_dates=True)
    if d.empty or "Close" not in d or d.Close.notna().sum() == 0:
        continue
    first = d[d.Close.notna()].index.min().tz_localize(None)
    for k, r in rows.iterrows():
        need = max(r.member_from, pd.Timestamp("2015-01-02"))
        if first > need + pd.Timedelta(days=14) and r.member_to < first:
            new = f"{t}.OLD"
            master.loc[k, "ticker"] = new
            span = (cal.index >= r.member_from) & (cal.index <= r.member_to)
            if new not in cal:
                cal[new] = 0
            cal.loc[span, new] = 1
            cal.loc[span, t] = 0
            split_log.append(f"{t} {r.member_from.date()}..{r.member_to.date()} -> {new}")
print("split:", split_log)
master.to_csv(OUT / "security_master.csv", index=False,
              date_format="%Y-%m-%d")
tickers = sorted(master.ticker.unique())

close, adj, vol = {}, {}, {}
report = []
for t in tickers:
    rows = master[master.ticker == t]
    mf, mt = rows.member_from.min(), rows.member_to.max()
    rec = {"ticker": t, "yahoo_symbol": ysym(t), "member_from": mf.date(), "member_to": mt.date()}
    f = CACHE / f"{t}.csv"
    d = pd.read_csv(f, index_col=0, parse_dates=True) if f.exists() else pd.DataFrame()
    if d.empty or "Close" not in d:
        rec.update(status="missing", n_days=0)
        report.append(rec)
        continue
    d = d[d.Close.notna()]
    rec.update(first_date=d.index.min().date(), last_date=d.index.max().date(), n_days=len(d))
    # Kiểm tra tái sử dụng mã: dữ liệu phải bắt đầu trước/ngay khi mã vào chỉ số.
    need_from = max(mf, pd.Timestamp("2015-01-02"))
    if d.index.min() > need_from + pd.Timedelta(days=14):
        rec["status"] = "rejected_ticker_reused_or_partial"
        rec["note"] = f"Yahoo bắt đầu {d.index.min().date()} > vào chỉ số {need_from.date()}"
        report.append(rec)
        continue
    rec["status"] = "ok"
    close[t], adj[t], vol[t] = d["Close"], d["Adj Close"], d["Volume"]
    report.append(rec)

rep = pd.DataFrame(report)
rep.to_csv(OUT / "download_report.csv", index=False)


def panel(dct):
    p = pd.DataFrame(dct).sort_index()
    p.index = pd.to_datetime(p.index).tz_localize(None).normalize()
    p.index.name = "date"
    p = p[(p.index >= START) & (p.index <= "2026-11-13")]
    return p.reindex(columns=sorted(p.columns))


P_adj, P_close, V = panel(adj), panel(close), panel(vol)
P_adj.round(6).to_csv(OUT / "prices.csv")
P_close.round(6).to_csv(OUT / "prices_close_unadjusted.csv")
V.astype("Int64").to_csv(OUT / "volumes.csv")

# Ma trận thành phần theo ngày giao dịch (1 = đang thuộc S&P 500), cho mọi mã kể cả thiếu giá.
mem = cal.reindex(P_adj.index).fillna(0).astype("int8")
mem = mem.reindex(columns=sorted(mem.columns))
mem.to_csv(OUT / "membership_daily.csv")

print(rep.status.value_counts().to_string())
print("panel:", P_adj.shape, P_adj.index.min().date(), P_adj.index.max().date())
json.dump({
    "source": "Yahoo Finance qua yfinance " + yf.__version__,
    "fields": {"prices.csv": "Adj Close (điều chỉnh chia tách + cổ tức), USD",
               "prices_close_unadjusted.csv": "Close (chỉ điều chỉnh chia tách theo Yahoo), USD",
               "volumes.csv": "Volume (cổ phiếu)"},
    "start": START, "end_inclusive": "2026-11-13",
    "panel_shape": list(P_adj.shape),
    "status_counts": rep.status.value_counts().to_dict(),
    "identity_splits": split_log,
    "scraped_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}, open(OUT / "ENV.json", "w"), ensure_ascii=False, indent=1)
