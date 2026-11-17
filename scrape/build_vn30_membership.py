"""Build VN30 point-in-time membership (data_vn30/vn30_membership.csv + vn30_periods.csv).

Official snapshots are parsed from HOSE 'danh sach thanh phan' PDFs (hosted on static2.vietstock.vn).
Other periods are derived from official change notes / news and carry a lower `quality` label.
Usage: python3 scrape/build_vn30_membership.py <pdf_cache_dir>   (downloads missing PDFs)
"""
import os, sys, csv, subprocess, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from parse_vn30_pdf import vn30_tickers

B = "https://static2.vietstock.vn/vietstock/"
A = "https://www.aseansc.com.vn/uploads/"
PDF = {  # key -> url
 "2016_7": A+"2016/07/20160718_30-Danh%20muc%20thanh%20phan%20HOSE-Index%20ky%202%202016-18%207%202016.pdf",
 "2017_1": B+"2017/1/16/20170116_20170116%20-%20CBTT%20danh%20muc%20thanh%20phan%20HOSE-Index%20ky%201%202017.pdf",
 "2018_1": B+"2018/1/15/20180115_Danh%20sach%20HOSE-Index,%20Chi%20so%20VN30%20ky%201%202018.pdf",
 "2019_1": B+"2019/4/22/20190422_HOSE%20190422%20Update%20HOSE-Index,%20VNSI%20_%20Apr%202019%20-%20MN.pdf",
 "2019_7": B+"2019/7/18/20190718_HOSE%20190718%20List%20of%20constituents%20of%20HOSE-Indexes,%20VNSI%20_%20Jul%202019%20-%20MN.pdf",
 "2021_1": B+"2021/1/26/20210126_HOSE%20210126%20HOSE-Index%20%20VNSI%20Jan%202021%20(attached%20file)%20-%20MN.pdf",
 "2021_7": B+"2021/7/19/20210719_20210719-CBTT%20-%20Danh%20sach%20thanh%20phan%20HOSE-Index_VNSI%20thang%207%202021.pdf",
 "2022_1": A+"2022/01/17/20220117_20220117%20CBTT%20-%20Danh%20sach%20thanh%20phan%20HOSE-Index%20thang%201%202022.pdf",
 "2023_7": B+"2023/7/17/20230717_20230717_cbtt___danh_sach_thanh_phan_hose_index_thang_7_2023.pdf",
 "2024_1": B+"2024/1/15/20240115_20240115_cbtt___danh_sach_thanh_phan_hose_index_thang_1_2024.pdf",
 "2024_7": B+"2024/7/15/20240715_20240715_cbtt___danh_sach_thanh_phan_hose_index_thang_7_2024_1.pdf",
 "2025_1": B+"2025/1/20/20250120_hose_index.pdf",
 "2025_10": B+"2025/10/15/final_20251015_cbtt_cap_nhat_thong_tin_bcs_hose_index_thang_10_2025.pdf",
 "2026_1": B+"2026/1/21/21012026_cbtt___danh_sach_thanh_phan_hose_index_thang_1_2026.pdf",
 "2026_4": B+"2026/4/15/15042026_cbtt___cap_nhat_thong_tin_hose_index_thang_4_2026.pdf",
}
# Current list from VCI (trading.vietcap.com.vn/api/price/symbols/getByGroup?group=VN30), fetched 2026-11-17
VCI_NOW = "ACB BID BSR CTG FPT GAS GVR HDB HPG LPB MBB MCH MSN MWG SAB SHB SSB SSI STB TCB TCX VCB VHM VIB VIC VJC VNM VPB VPL VRE".split()

def get(cache):
    os.makedirs(cache, exist_ok=True)
    out = {}
    for k, u in PDF.items():
        p = os.path.join(cache, "y" + k + ".pdf")
        if not os.path.exists(p):
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            open(p, "wb").write(urllib.request.urlopen(req, timeout=60).read())
        out[k] = set(vn30_tickers(p))
        assert len(out[k]) == 30, (k, len(out[k]))
    return out

def build(cache):
    L = get(cache)
    P = []  # (from, to, set, quality, note)
    s1_17 = L["2017_1"]
    # checks: 7/2016 official list == 1/2017 list reversed with the official change note
    assert L["2016_7"] == (s1_17 - {"BMP","CTD","DHG"}) | {"FLC","HCM","PPC"}, "7/2016 vs 1/2017 mismatch"
    l3 = (L["2016_7"] - {"BID","GAS","HNG","MWG"}) | {"EIB","HHS","HVG","PVT"}      # press: 7/2016 review
    l2 = (l3 - {"SBT","NT2"}) | {"CSM","VSH"}                                        # press: 1/2016 review
    P.append(("2015-07-27", "2016-01-24", l2, "news_inferred",
              "list before 1/2016 review: 7/2016 HOSE list reversed through press-reported 7/2016 (+BID,GAS,HNG,MWG -EIB,HHS,HVG,PVT) and 1/2016 (+SBT,NT2 -CSM,VSH) changes; start date = 4th Monday of Jul 2015 (assumed)"))
    P.append(("2016-01-25", "2016-07-24", l3, "news_inferred", "7/2016 HOSE list reversed through press-reported 7/2016 changes"))
    P.append(("2016-07-25", "2017-01-22", L["2016_7"], "official", "HOSE list 2/2016"))
    P.append(("2017-01-23", "2017-07-23", s1_17, "official", "HOSE list 1/2017"))
    P.append(("2017-07-24", "2018-01-21", (s1_17 - {"HAG","HNG","ITA"}) | {"NVL","ROS","SAB"}, "news_inferred",
              "7/2017 review: +NVL,ROS,SAB -HAG,HNG,ITA (press); consistent with HOSE 1/2018 list"))
    P.append(("2018-01-22", "2018-07-22", L["2018_1"], "official", "HOSE list 1/2018"))
    P.append(("2018-07-23", "2019-02-10", (L["2018_1"] - {"BID","BVH","NT2"}) | {"PNJ","VPB","VRE"}, "news_inferred",
              "7/2018 review: +PNJ,VPB,VRE -BID,BVH,NT2 (press)"))
    P.append(("2019-02-11", "2019-08-04", L["2019_1"], "official", "HOSE list 1/2019 (as of Apr-2019 update)"))
    P.append(("2019-08-05", "2020-01-31", L["2019_7"], "official", "HOSE list 7/2019"))
    l20a = (L["2019_7"] - {"DPM","GMD"}) | {"PLX","POW"}                              # press: 1/2020 review
    l20b = (l20a - {"CTD","BVH"}) | {"KDH","TCH"}                                     # press: 7/2020 review
    assert L["2021_1"] == (l20b - {"SAB","EIB","ROS"}) | {"BVH","PDR","TPB"}, "2020 chain does not reach HOSE 1/2021 list"
    P.append(("2020-02-03", "2020-08-02", l20a, "news_inferred", "1/2020 review: +PLX,POW -DPM,GMD (press); chain verified against HOSE 1/2021 list"))
    P.append(("2020-08-03", "2021-01-31", l20b, "news_inferred", "7/2020 review: +KDH,TCH -CTD,BVH (press); chain verified against HOSE 1/2021 list"))
    P.append(("2021-02-01", "2021-08-01", L["2021_1"], "official", "HOSE list 1/2021 (effective date = first Monday of Feb, assumed)"))
    P.append(("2021-08-02", "2022-02-06", L["2021_7"], "official", "HOSE list 7/2021"))
    P.append(("2022-02-07", "2022-07-31", L["2022_1"], "official", "HOSE list 1/2022 (effective date assumed first Monday of Feb)"))
    P.append(("2022-08-01", "2023-02-05", (L["2022_1"] - {"PNJ"}) | {"VIB"}, "news_inferred", "8/2022: +VIB -PNJ (press)"))
    P.append(("2023-02-06", "2023-08-06", (L["2022_1"] - {"PNJ","KDH"}) | {"VIB","BCM"}, "inferred_date_uncertain",
              "KDH->BCM swap occurred between 2022-08 and 2023-08 (exact date not found)"))
    P.append(("2023-08-07", "2024-02-04", L["2023_7"], "official", "HOSE list 7/2023"))
    P.append(("2024-02-05", "2024-08-04", L["2024_1"], "official", "HOSE list 1/2024"))
    P.append(("2024-08-05", "2025-02-02", L["2024_7"], "official", "HOSE list 7/2024"))
    P.append(("2025-02-03", "2025-08-03", L["2025_1"], "official", "HOSE list 1/2025"))
    P.append(("2025-08-04", "2026-02-01", L["2025_10"], "official", "HOSE update 10/2025 (7/2025 review: +DGC -BVH effective 2025-08-04)"))
    P.append(("2026-02-02", "2026-08-02", L["2026_1"], "official", "HOSE list 1/2026 (4/2026 update identical)"))
    P.append(("2026-08-03", "2026-11-16", set(VCI_NOW), "vci_current_list", "VCI group VN30 as of 2026-11-17; effective date assumed 2026-08-03"))
    return P

if __name__ == "__main__":
    cache = sys.argv[1] if len(sys.argv) > 1 else "/tmp/vn30_pdfs"
    P = build(cache)
    for p in P:
        assert len(p[2]) == 30, p
    os.makedirs("data_vn30", exist_ok=True)
    with open("data_vn30/vn30_periods.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["effective_from","effective_to","n","quality","note"])
        for a,b,s,q,n in P: w.writerow([a,b,len(s),q,n])
    with open("data_vn30/vn30_membership.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["effective_from","effective_to","ticker","quality"])
        for a,b,s,q,n in P:
            for t in sorted(s): w.writerow([a,b,t,q])
    print(len(P), "periods;", len({t for p in P for t in p[2]}), "distinct tickers")
