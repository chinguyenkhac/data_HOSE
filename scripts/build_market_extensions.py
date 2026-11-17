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
SNAPSHOTS = [
    ("2015H1", "2015-01-26", "2015-07-26", "2015-01-20",
     "https://static2.vietstock.vn/vietstock/2015/1/20/20150119---vn30.pdf",
     "FLC VIC SSI HAG PVD KBC MSN KDC FPT ITA VNM HPG OGC HVG PVT REE CII DPM HCM MBB GMD VCB IJC PPC HSG STB CSM DRC VSH BVH"),
    ("2015H2", "2015-07-27", "2016-01-22", "2015-07-20",
     "https://static2.vietstock.vn/vietstock/2015/7/20/20150720_CBTT%20-%20VN30_%2020.07.2015.pdf",
     "FLC CII VIC SSI HAG CTG PVD MSN HHS KBC KDC VCB HPG MBB FPT EIB VNM STB ITA DPM REE PVT HCM BVH HSG HVG PPC GMD CSM VSH"),
    ("2016H1", "2016-01-25", "2016-07-22", "2016-01-18",
     "https://www.aseansc.com.vn/uploads/2016/01/20160118_CBTT-%20VN30%20-%20K%E1%BB%B3%201-2016.pdf",
     "VNM CII SSI FLC VIC MBB MSN FPT HAG HPG KDC HHS SBT CTG VCB NT2 PVD HCM KBC BVH DPM GMD REE HSG ITA EIB HVG STB PVT PPC"),
    ("2016H2", "2016-07-25", "2017-01-20", "2016-07-18",
     "https://www.aseansc.com.vn/uploads/2016/07/20160718_30-Danh%20muc%20thanh%20phan%20HOSE-Index%20ky%202%202016-18%207%202016.pdf",
     "VNM CII SSI FLC VIC MBB MSN FPT HAG HPG KDC BID SBT CTG VCB NT2 PVD HCM KBC BVH DPM GMD REE HSG ITA GAS HNG STB MWG PPC"),
    ("2017H1", "2017-01-23", "2017-07-21", "2017-01-16",
     "https://static2.vietstock.vn/vietstock/2017/1/16/20170116_20170116%20-%20CBTT%20danh%20muc%20thanh%20phan%20HOSE-Index%20ky%201%202017.pdf",
     "BID BMP BVH CII CTD CTG DHG DPM FPT GAS GMD HAG HNG HPG HSG ITA KBC KDC MBB MSN MWG NT2 PVD REE SBT SSI STB VCB VIC VNM"),
    ("2017H2", "2017-07-24", "2018-01-19", "2017-07-17",
     "https://bmsc.com.vn/uploads/files/news/HSX/20170717_Danh%20sach%20HOSE-Index%2C%20VNSI%20ky%202%202017.pdf",
     "BID BMP BVH CII CTD CTG DHG DPM FPT GAS GMD HPG HSG KBC KDC MBB MSN MWG NT2 NVL PVD REE ROS SAB SBT SSI STB VCB VIC VNM"),
    ("2018H1", "2018-01-22", "2018-07-20", "2018-01-15",
     "https://www.aseansc.com.vn/uploads/2018/01/20180115_Danh%20sach%20HOSE-Index%2C%20Chi%20so%20VN30%20ky%201%202018.pdf",
     "BID BMP BVH CII CTD CTG DHG DPM FPT GAS GMD HPG HSG KDC MBB MSN MWG NT2 NVL PLX REE ROS SAB SBT SSI STB VCB VIC VJC VNM"),
    ("2018H2", "2018-07-23", "2019-01-25", "2018-07-16",
     "https://www.aseansc.com.vn/uploads/2018/07/16/20180716_Danh%20sach%20HOSE-Index%2C%20VNSI%20ky%207%202018.pdf",
     "BMP CII CTD CTG DHG DPM FPT GAS GMD HPG HSG KDC MBB MSN MWG NVL PLX PNJ REE ROS SAB SBT SSI STB VCB VIC VJC VNM VPB VRE"),
    ("2019H2", "2019-08-05", "2020-01-31", "2019-07-15",
     "https://www.aseansc.com.vn/uploads/2019/07/15/20190715_Danh%20sach%20HOSE-Index%2C%20VNSI%20ky%207%202019.pdf",
     "BID BVH CTD CTG DPM EIB FPT GAS GMD HDB HPG MBB MSN MWG NVL PNJ REE ROS SAB SBT SSI STB TCB VCB VHM VIC VJC VNM VPB VRE"),
    ("2025H2", "2025-08-04", "2025-12-31", "2025-07-16",
     "https://staticfile.hsx.vn/Uploads/UploadDocuments/2388633/20250716%20CBTT-Danh%20muc%20thanh%20phan%20HOSE-Index%20thang%207.2025.pdf",
     "ACB BCM BID CTG DGC FPT GAS GVR HDB HPG LPB MBB MSN MWG PLX SAB SHB SSB SSI STB TCB TPB VCB VHM VIB VIC VJC VNM VPB VRE"),
    ("2026H2", "2026-08-03", "2026-09-30", "2026-07-15",
     "https://staticfile.hsx.vn/Uploads/UploadDocuments/2479382/15072026%20CBTT%20-%20Danh%20muc%20thanh%20phan%20HOSE-Index%20thang%207.2026.pdf",
     "ACB BID BSR CTG FPT GAS GVR HDB HPG LPB MBB MCH MSN MWG SAB SHB SSB SSI STB TCB TCX VCB VHM VIB VIC VJC VNM VPB VPL VRE"),
]


def read(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    members = []
    for label, start, end, observed, source, names in SNAPSHOTS:
        tickers = names.split()
        assert len(tickers) == len(set(tickers)) == 30, label
        members.extend(dict(snapshot=label, effective_from=start, effective_until=end,
                            ticker=t, source=source, observed_at=observed,
                            status="verified_snapshot") for t in tickers)
    write(VN / "membership_snapshots.csv", list(members[0]), members)

    master = read(ROOT / "data_hose/security_master.csv")
    report = []
    data = {kind: read(ROOT / f"data_hose/{kind}.csv") for kind in ("prices", "volumes", "values")}
    for label, start, end, observed, source, names in SNAPSHOTS:
        tickers = names.split()
        valid = {r["ticker"] for r in master if r["listing_date"] <= start and
                 (not r["delisting_date"] or r["delisting_date"] >= start)}
        assert set(tickers) <= valid, f"{label}: not listed at effective date: {set(tickers)-valid}"
        for kind, rows in data.items():
            assert set(tickers) <= set(rows[0]), f"{label}: missing columns in {kind}"
            subset = [dict(date=r["date"], **{t: r[t] for t in tickers}) for r in rows
                      if start <= r["date"] <= end]
            assert subset and len({r["date"] for r in subset}) == len(subset)
            write(VN / f"{kind}_verified_{label}.csv", ["date"] + tickers, subset)
            counts = Counter(t for r in subset for t in tickers if r[t] != "")
            report.extend(dict(snapshot=label, dataset=kind, ticker=t,
                               sessions=len(subset), observed=counts[t],
                               coverage=round(counts[t]/len(subset), 6)) for t in tickers)
        print(f"{label}: {len(tickers)} members, {len(subset)} sessions")
    write(VN / "coverage_by_snapshot.csv", list(report[0]), report)

    # These are transfer leads only. They are not the historical HNX universe.
    transfer = [dict(ticker=r["ticker"], hose_start=r["listing_date"],
                     evidence=r["source"], note="HNX before HOSE; HNX dates/prices unverified")
                for r in master if r["exchange_before"].strip().upper() == "HNX"]
    write(HN / "transfer_candidates.csv", ["ticker", "hose_start", "evidence", "note"], transfer)
    print(f"VN30: {len(SNAPSHOTS)} verified snapshots; "
          f"minimum per-series coverage {min(r['coverage'] for r in report):.1%}")
    print(f"HNX: {len(transfer)} transfer candidates; historical HNX panel pending source acquisition")


if __name__ == "__main__":
    main()
