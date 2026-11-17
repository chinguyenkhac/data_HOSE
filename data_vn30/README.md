# VN30 historical data: verified slice

Current verified interval: **2015-01-26 through 2015-07-26** (120 trading sessions). The 2015-01-20 constituent announcement and its attached 30-stock PDF are the membership source: https://static2.vietstock.vn/vietstock/2015/1/20/20150119---vn30.pdf . The next semiannual revision took effect 2015-07-27, so this dataset ends before that date. The 2015-07-27 boundary must be checked against the next official constituent notice before extending membership.

`membership_snapshots.csv` holds the 30 names and announcement/effective dates. The three `*_verified_2015H1.csv` files are filtered from `data_hose/{prices,volumes,values}.csv`. They contain exactly these 30 tickers, with the original numeric values and blank-cell convention. `coverage_2015H1.csv` counts observed cells. Rebuild with `python scripts/build_market_extensions.py`.

**QA:** 30 distinct constituents; all 30 were listed on HOSE on the effective date according to `data_hose/security_master.csv`; all 30 have price, volume and value in each of the 120 selected sessions. Prices are VCI adjusted closes; values in `data_hose` are an approximation (`adjusted_price × volume`), not exchange-reported transaction value. This verified slice is **not** a complete VN30 history or an investable backtest from 2015 to 2026. Obtain each six-month constituent announcement and its effective date, validate each added/removed security, and expand this panel only after filling the intervening snapshots. The 2015-01-05 to 2015-01-23 trading days also need the previous index review's membership.

The missing-price list `data_hose/missing_tickers.csv` should be cross-checked after the complete membership history is assembled. A present-day VN30 ticker list must never be projected backwards.
