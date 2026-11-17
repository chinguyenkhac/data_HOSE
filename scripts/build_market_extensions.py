"""Build strictly sourced VN30 snapshots and audit HNX transfer candidates.

Run at repository root: python scripts/build_market_extensions.py
Never infer index membership from today's constituents or HOSE transfer metadata.
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VN = ROOT / "data_vn30"
HN = ROOT / "data_hnx"
TICKERS = "FLC VIC SSI HAG PVD KBC MSN KDC FPT ITA VNM HPG OGC HVG PVT REE CII DPM HCM MBB GMD VCB IJC PPC HSG STB CSM DRC VSH BVH".split()
SOURCE = "https://static2.vietstock.vn/vietstock/2015/1/20/20150119---vn30.pdf"
START, END = "2015-01-26", "2015-07-26"  # next review effective 2015-07-27; do not extend beyond it


def read(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    assert len(TICKERS) == len(set(TICKERS)) == 30
    members = [dict(effective_from=START, effective_until=END, ticker=t, source=SOURCE,
                    observed_at="2015-01-20", status="verified_snapshot") for t in TICKERS]
    write(VN / "membership_snapshots.csv", list(members[0]), members)

    master = read(ROOT / "data_hose/security_master.csv")
    valid = {r["ticker"] for r in master if r["listing_date"] <= START and
             (not r["delisting_date"] or r["delisting_date"] >= START)}
    assert set(TICKERS) <= valid, f"Snapshot has stocks outside HOSE listing interval: {set(TICKERS)-valid}"

    report = []
    for kind in ("prices", "volumes", "values"):
        rows = read(ROOT / f"data_hose/{kind}.csv")
        subset = [dict(date=r["date"], **{t: r[t] for t in TICKERS}) for r in rows
                  if START <= r["date"] <= END]
        assert subset and len({r["date"] for r in subset}) == len(subset)
        write(VN / f"{kind}_verified_2015H1.csv", ["date"] + TICKERS, subset)
        counts = Counter(t for r in subset for t in TICKERS if r[t] != "")
        report.extend(dict(dataset=kind, ticker=t, sessions=len(subset), observed=counts[t],
                           coverage=round(counts[t]/len(subset), 6)) for t in TICKERS)
    write(VN / "coverage_2015H1.csv", list(report[0]), report)

    # These are transfer leads only. They are not the historical HNX universe.
    transfer = [dict(ticker=r["ticker"], hose_start=r["listing_date"],
                     evidence=r["source"], note="HNX before HOSE; HNX dates/prices unverified")
                for r in master if r["exchange_before"].strip().upper() == "HNX"]
    write(HN / "transfer_candidates.csv", ["ticker", "hose_start", "evidence", "note"], transfer)
    print(f"VN30: {len(TICKERS)} constituents, {len(subset)} sessions; "
          f"minimum per-series coverage {min(r['coverage'] for r in report):.1%}")
    print(f"HNX: {len(transfer)} transfer candidates; historical HNX panel pending source acquisition")


if __name__ == "__main__":
    main()
