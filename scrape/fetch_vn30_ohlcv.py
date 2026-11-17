"""Fetch daily OHLCV (VCI) for every ticker that was ever in data_vn30/vn30_membership.csv."""
import os, sys, time, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from fetch_vn30_index import fetch

tickers = sorted(pd.read_csv("data_vn30/vn30_membership.csv").ticker.unique())
os.makedirs("data_vn30/ohlcv", exist_ok=True)
missing = []
for t in tickers:
    try:
        df = fetch(t)
    except Exception as e:
        df = pd.DataFrame()
    if df.empty:
        missing.append(t); print("MISSING", t); continue
    df.drop(columns=["value_raw_vci"]).to_csv(f"data_vn30/ohlcv/{t}.csv", index=False, date_format="%Y-%m-%d")
    print(t, len(df), df.date.min().date(), df.date.max().date())
    time.sleep(0.3)
open("data_vn30/ohlcv_missing.txt", "w").write("\n".join(missing))
