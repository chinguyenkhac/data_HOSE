"""Fetch daily OHLCV of the VN30 index from VCI (same endpoint vnstock uses)."""
import datetime as dt, requests, pandas as pd, calendar

H = {"Content-Type": "application/json", "Origin": "https://trading.vietcap.com.vn",
     "Referer": "https://trading.vietcap.com.vn/", "User-Agent": "Mozilla/5.0"}
START, END = dt.date(2015, 1, 1), dt.date(2026, 11, 16)

def fetch(symbol, count=4000):
    to = calendar.timegm((END + dt.timedelta(days=2)).timetuple())
    r = requests.post("https://trading.vietcap.com.vn/api/chart/OHLCChart/gap-chart", headers=H, timeout=60,
                      json={"timeFrame": "ONE_DAY", "symbols": [symbol], "to": to, "countBack": count})
    r.raise_for_status()
    d = r.json()[0]
    df = pd.DataFrame({"date": pd.to_datetime([int(t) for t in d["t"]], unit="s").normalize(),
                       "open": d["o"], "high": d["h"], "low": d["l"], "close": d["c"], "volume": d["v"],
                       "value_raw_vci": d["accumulatedValue"]})
    return df[(df.date >= pd.Timestamp(START)) & (df.date <= pd.Timestamp(END))].reset_index(drop=True)

if __name__ == "__main__":
    df = fetch("VN30")
    df.to_csv("data_vn30/vn30_index.csv", index=False, date_format="%Y-%m-%d")
    print(df.head(3), df.tail(3), len(df), sep="\n")
