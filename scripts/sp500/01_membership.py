"""Dựng lịch sử thành phần S&P 500 (2015-01-01 → 2026-11-13) từ Wikipedia.

Cách làm: lấy danh sách hiện tại (List of S&P 500 companies) rồi "tua ngược"
bảng thay đổi (Historical components of the S&P 500): với mỗi thay đổi có ngày
hiệu lực > d, bỏ mã được thêm và trả lại mã bị loại.

Usage: python3 -I scripts/sp500/01_membership.py "data_s&p500"
"""
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

OUT = Path(sys.argv[1])
RAW = OUT / "raw"
START, END = pd.Timestamp("2015-01-01"), pd.Timestamp("2026-11-13")


def norm(t):
    if pd.isna(t):
        return None
    t = str(t).strip().upper()
    return t or None


cur_html = next(RAW.glob("wikipedia_List_of_SP500_companies_*.html")).read_text()
hist_html = next(RAW.glob("wikipedia_Historical_components_of_the_SP500_*.html")).read_text()

cur = pd.read_html(io.StringIO(cur_html))[0]
cur.columns = ["ticker", "name", "gics_sector", "gics_sub_industry",
               "headquarters", "date_added", "cik", "founded"]
cur["ticker"] = cur["ticker"].map(norm)

ch = pd.read_html(io.StringIO(hist_html))[0]
ch.columns = ["effective_date", "added_ticker", "added_name",
              "removed_ticker", "removed_name", "reason", "refs"]
ch["effective_date"] = pd.to_datetime(ch["effective_date"], format="mixed")
for c in ("added_ticker", "removed_ticker"):
    ch[c] = ch[c].map(norm)
ch = ch.drop(columns="refs")

# --- chuẩn hoá danh tính: mã lịch sử -> mã hiện tại của CÙNG công ty ---
# (phát hiện qua cảnh báo khi tua ngược; xem raw/_membership_log.json)
ALIAS = {"SATS": "ECHO",    # EchoStar đổi mã
         "FLT": "CPAY",     # FleetCor -> Corpay (2024)
         "RE": "EG",        # Everest Re -> Everest Group (2023)
         "UA.C": "UA",      # Under Armour lớp C: UA.C -> UA (2016)
         "CDAY": "DAY",     # Ceridian -> Dayforce (2024)
         "WLTW": "WTW",     # Willis Towers Watson đổi mã (2022)
         "DWDP": "DD",      # DowDuPont đổi tên thành DuPont (2019)
         "TFCFA": "FOXA.21CF", "TFCF": "FOX.21CF"}   # 21st Century Fox (bị Disney mua 2019)
ch["added_ticker_hist"] = ch["added_ticker"]
ch["removed_ticker_hist"] = ch["removed_ticker"]
for c in ("added_ticker", "removed_ticker"):
    ch[c] = ch[c].map(lambda t: ALIAS.get(t, t) if isinstance(t, str) else t)


def fix(date, col, old, new):
    m = (ch.effective_date == date) & (ch[col] == old)
    assert m.sum() == 1, (date, col, old)
    ch.loc[m, col] = new


# Cùng mã nhưng KHÁC công ty -> tách danh tính (công ty cũ gắn hậu tố .OLD/.21CF)
fix("2015-03-23", "removed_ticker", "AGN", "AGN.OLD")    # Allergan cũ; Actavis đổi mã ACT->AGN
fix("2016-01-19", "removed_ticker", "ACE", "CB.OLD")     # Chubb Corp cũ; ACE đổi tên Chubb, giữ mã CB
fix("2017-09-01", "removed_ticker", "DOW", "DOW.OLD")    # Dow Chemical (-> DowDuPont); Dow Inc mới thêm 2019
fix("2015-09-18", "added_ticker", "FOX", "FOX.21CF")     # 21CF lớp B; Fox Corp mới dùng lại FOX
fix("2017-08-29", "added_ticker", "Q", "IQV")            # QuintilesIMS = IQVIA (Q -> IQV), Q nay là Qnity
fix("2017-11-15", "removed_ticker", "Q", "IQV")
# Đổi mã thuần tuý (thêm & loại cùng một danh tính trong một dòng) -> không làm gì
same = ch.added_ticker.notna() & (ch.added_ticker == ch.removed_ticker)
ch.loc[same, ["added_ticker", "removed_ticker"]] = None
# 2017-09-01 Dow Chemical + DuPont -> DowDuPont (DWDP, nay là DD). Yahoo ghép lịch sử mã DD
# liền mạch (DuPont cũ -> DowDuPont -> DuPont), nên coi DD là một chuỗi liên tục:
fix("2017-09-01", "added_ticker", "DD", None)      # dòng thêm DWDP
fix("2017-09-01", "removed_ticker", "DD", None)    # dòng loại DuPont cũ (thêm SBAC)
ch = ch.sort_values("effective_date", ascending=False, kind="stable")
ch_out = ch[ch.effective_date >= START].copy()
ch_out["effective_date"] = ch_out["effective_date"].dt.date
ch_out.to_csv(OUT / "index_changes.csv", index=False)

# --- tua ngược để có tập thành phần tại mỗi ngày thay đổi ---
members = set(cur["ticker"])
warnings = []
# snapshots: (ngày hiệu lực, tập thành phần có hiệu lực TỪ ngày đó)
snapshots = [(END + pd.Timedelta(days=1), frozenset(members))]
for d, g in ch[ch.effective_date > START].groupby("effective_date", sort=False):
    snapshots.append((d, frozenset(members)))
    for _, r in g.iterrows():
        if isinstance(r.added_ticker, str):
            if r.added_ticker in members:
                members.discard(r.added_ticker)
            else:
                warnings.append(f"{d.date()} undo add {r.added_ticker}: không có trong tập")
        if isinstance(r.removed_ticker, str):
            if r.removed_ticker in members:
                warnings.append(f"{d.date()} undo remove {r.removed_ticker}: đã có trong tập")
            members.add(r.removed_ticker)
snapshots.append((START, frozenset(members)))
snapshots.sort(key=lambda x: x[0])

# --- ma trận thành phần theo ngày lịch (sau đó cắt theo ngày giao dịch ở bước 2) ---
days = pd.date_range(START, END, freq="D")
all_t = sorted(set().union(*[s for _, s in snapshots]))
mask = pd.DataFrame(0, index=days, columns=all_t, dtype="int8")
for (d0, s), (d1, _) in zip(snapshots[:-1], snapshots[1:]):
    sl = (days >= d0) & (days < d1)
    mask.loc[sl, sorted(s)] = 1
mask.index.name = "date"
mask.to_pickle(OUT / "raw" / "_membership_calendar.pkl")

# --- giai đoạn thành phần (interval) mỗi mã ---
rows = []
for t in all_t:
    s = mask[t].values
    i = 0
    while i < len(s):
        if s[i]:
            j = i
            while j + 1 < len(s) and s[j + 1]:
                j += 1
            rows.append((t, days[i], days[j]))
            i = j + 1
        else:
            i += 1
iv = pd.DataFrame(rows, columns=["ticker", "start", "end"])

name_map = dict(zip(cur.ticker, cur.name))
for _, r in ch.iterrows():
    for t, n in ((r.added_ticker, r.added_name), (r.removed_ticker, r.removed_name)):
        if isinstance(t, str) and t not in name_map and not pd.isna(n):
            name_map[t] = n


def lookup(t, col, ref):
    """Ngày thêm/loại thực tế gần ref nhất trong bảng thay đổi."""
    g = ch[ch[col] == t]
    if g.empty:
        return None, None
    k = (g.effective_date - ref).abs().idxmin()
    return g.loc[k, "effective_date"], g.loc[k, "reason"]


out = []
for _, r in iv.iterrows():
    add_d, add_reason = (None, None)
    rem_d, rem_reason = (None, None)
    if r.start > START:
        add_d, add_reason = lookup(r.ticker, "added_ticker", r.start)
    if r.end < END:
        rem_d, rem_reason = lookup(r.ticker, "removed_ticker", r.end + pd.Timedelta(days=1))
    out.append({
        "ticker": r.ticker,
        "name": name_map.get(r.ticker),
        "member_from": r.start.date(),
        "member_to": r.end.date(),
        "in_index_before_2015": r.start == START,
        "date_added": add_d.date() if add_d is not None else
        (cur.set_index("ticker").date_added.get(r.ticker) if r.ticker in name_map else None),
        "date_removed": rem_d.date() if rem_d is not None else None,
        "removal_reason": rem_reason,
        "current_member": r.end == END,
    })
master = pd.DataFrame(out)
cmeta = cur.set_index("ticker")[["gics_sector", "gics_sub_industry", "cik", "headquarters", "founded"]]
master = master.join(cmeta, on="ticker")
master.to_csv(OUT / "security_master.csv", index=False)

cur.to_csv(OUT / "constituents_current.csv", index=False)

cnt = mask.sum(axis=1)
print("tickers ever member:", len(all_t), "intervals:", len(iv))
print("member count min/max:", cnt.min(), cnt.max())
print(cnt.resample("YE").agg(["min", "max"]).to_string())
print("warnings:", len(warnings))
print("\n".join(warnings))
json.dump({"n_tickers": len(all_t), "n_intervals": len(iv), "warnings": warnings,
           "count_min": int(cnt.min()), "count_max": int(cnt.max()),
           "built_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
          open(OUT / "raw" / "_membership_log.json", "w"), ensure_ascii=False, indent=1)
