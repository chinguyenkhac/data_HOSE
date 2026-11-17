# HNX historical data: acquisition status

The existing `data_hose/security_master.csv` identifies **26 tickers** whose preceding exchange is HNX. `transfer_candidates.csv` preserves these as research leads, including their first HOSE listing date. This is **not** an HNX universe, listing master, or HNX price panel. No HNX backtest is valid from these rows alone.

Acquisition specification for 2015–present:

1. Obtain HNX's *current and delisted* listing histories. Store one row per listing interval, with ticker, stable issuer/security identifier where available, first and last trading date, delisting/transfer reason, provenance URL and extraction date. Validate exchange changes against the HOSE master without merging same ticker across different issuers.
2. Obtain each security's daily raw close, adjusted close (or corporate-action factors), matched volume and traded value from a licensed historical source. Retain exchange source, adjustment convention, units, retrieval timestamp and response status. Preserve missing and suspension days as blank; do not fill them with zero prices.
3. Audit each listing interval: counts and coverage by year, missing delisted symbols, split/dividend discontinuities, price/volume/value units, 2015 start availability, and the number of rebalance dates eligible for N=30/50 under the existing 95%-coverage and zero-return filters.
4. If an old HNX stock moves to HOSE or UPCoM, record separate exchange intervals. Do not infer a liquidation return from a change of venue. Choose and document the return convention when trading halts or delisting occurs while held.

Potential primary sources: HNX's listed/delisted securities pages and historical end-of-day data service. The API/CSV export and availability of complete 2015–present adjusted prices have **not** been verified in this environment. HNX web requests returned HTTP 503 on 2026-11-17, so an HNX price file is not included here. A source with bulk history and corporate actions, or an exchange data agreement, may be necessary. Record its terms before publishing copied data in this public repository.

Only write `security_master.csv`, `prices.csv`, `volumes.csv`, and `values.csv` in this directory after these checks. The generation script `scripts/build_market_extensions.py` updates just the transfer leads.
