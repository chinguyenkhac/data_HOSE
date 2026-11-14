"""Xuất delisted.csv (mã bị loại khỏi S&P 500) và QA.md.

Usage: python3 -I scripts/sp500/03_reports.py "data_s&p500"
"""
import sys
from pathlib import Path

import pandas as pd

OUT = Path(sys.argv[1])
m = pd.read_csv(OUT / "security_master.csv")
r = pd.read_csv(OUT / "download_report.csv").set_index("ticker")
P = pd.read_csv(OUT / "prices.csv", index_col=0, parse_dates=True)
V = pd.read_csv(OUT / "volumes.csv", index_col=0, parse_dates=True)
M = pd.read_csv(OUT / "membership_daily.csv", index_col=0, parse_dates=True)

m["price_status"] = m.ticker.map(r.status)
m["yahoo_first_date"] = m.ticker.map(r.first_date)
m["yahoo_last_date"] = m.ticker.map(r.last_date)
m.to_csv(OUT / "security_master.csv", index=False)

d = m[~m.current_member].copy()
txt = d.removal_reason.fillna("").str.lower()
d["removal_type"] = "index_rebalance"   # bị loại do vốn hoá, vẫn còn niêm yết
d.loc[txt.str.contains("acqui|merg|bought|purchas|taken private|buyout"), "removal_type"] = "acquired_or_merged"
d.loc[txt.str.contains("spin|split"), "removal_type"] = "spin_off_related"
d.loc[txt.str.contains("bankrupt|chapter 11"), "removal_type"] = "bankruptcy"
d.loc[d.ticker.str.endswith((".OLD", ".21CF")), "note"] = "mã đã bị công ty khác dùng lại; danh tính lịch sử"
d = d.sort_values("date_removed")
d.to_csv(OUT / "delisted.csv", index=False)

mem = M.reindex(columns=P.columns).fillna(0)
cov = ((P.notna() & (mem == 1)).sum(axis=1) / M.sum(axis=1)).resample("YE").mean()
ret = P.pct_change(fill_method=None)
jumps = [(t, ret[t].abs().idxmax().date(), round(float(ret[t].abs().max()), 3))
         for t in P.columns if ret[t].abs().max() > 0.5]
neg = int((P <= 0).sum().sum())
st = r.status.value_counts()

lines = [
    "# QA – data_s&p500",
    "",
    f"- Kỳ: {P.index.min().date()} → {P.index.max().date()}, {len(P)} phiên giao dịch.",
    f"- Số danh tính từng thuộc S&P 500 trong kỳ: {len(r)}; có giá: {st.get('ok', 0)}, "
    f"không có trên Yahoo: {st.get('missing', 0)}, bị loại vì mã đã bị tái sử dụng / chỉ có 1 phiên: "
    f"{st.get('rejected_ticker_reused_or_partial', 0)}.",
    f"- Số thành phần mỗi ngày (tính cả nhiều lớp cổ phiếu): {int(M.sum(axis=1).min())}–{int(M.sum(axis=1).max())}.",
    "- Thành phần hiện tại thiếu giá: "
    + (", ".join(r[(r.member_to == "2026-11-13") & (r.status != "ok")].index) or "không có") + ".",
    f"- Giá ≤ 0: {neg} ô.",
    "",
    "## Tỷ lệ thành phần có giá (trung bình theo năm)",
    "",
    "Thiếu chủ yếu là các công ty đã bị mua lại / phá sản – Yahoo xoá lịch sử của mã đã hủy niêm yết,",
    "nên dữ liệu những năm đầu vẫn còn **survivorship bias** (xem `delisted.csv`, cột `price_status`).",
    "",
    "| Năm | Tỷ lệ |", "|---|---|",
    *[f"| {i.year} | {v:.1%} |" for i, v in cov.items()],
    "",
    "## Biến động 1 phiên > 50% (cần lưu ý)",
    "",
    "Phần lớn là biến động thật (GME 2021, OXY/TRGP 3/2020...). Ngoại lệ đã biết: DHR 2016-07-05",
    "(Yahoo điều chỉnh sai sự kiện tách Fortive). Yahoo không điều chỉnh spin-off một cách nhất quán.",
    "",
    "| Mã | Ngày | |ret| |", "|---|---|---|",
    *[f"| {t} | {dd} | {x} |" for t, dd, x in jumps],
    "",
    "## Xử lý danh tính (mã đổi / mã tái sử dụng)",
    "",
    "Xem `scripts/sp500/01_membership.py` (ALIAS, fix) và `ENV.json` → `identity_splits`.",
    "Các danh tính hậu tố `.OLD`/`.21CF` là công ty cũ có mã đã bị công ty khác dùng lại;",
    "chúng có trong `security_master.csv`, `membership_daily.csv` nhưng không có giá.",
]
(OUT / "QA.md").write_text("\n".join(lines) + "\n")
print(d.removal_type.value_counts().to_string())
print(d.groupby("removal_type").price_status.value_counts().to_string())
