# QA dữ liệu HOSE 2015–nay (T1)

- Khoảng ngày: 2015-01-05 → 2026-11-10 (2957 phiên)
- security_master: 513 giai đoạn niêm yết, 512 mã; đã hủy: 105
- Có giá điều chỉnh: 493 mã; thiếu: 19 mã (xem `missing_tickers.csv`)

## 1. Số mã ngừng giao dịch theo năm
|      |   hủy niêm yết (master) |   ngừng có giá (prices.csv) |
|-----:|------------------------:|----------------------------:|
| 2015 |                      17 |                          11 |
| 2016 |                       6 |                           3 |
| 2017 |                       7 |                           4 |
| 2018 |                       7 |                           5 |
| 2019 |                       8 |                           8 |
| 2020 |                       6 |                           7 |
| 2021 |                       5 |                           2 |
| 2022 |                      10 |                           9 |
| 2023 |                      13 |                          13 |
| 2024 |                      12 |                          12 |
| 2025 |                       7 |                           6 |
| 2026 |                       7 |                           9 |

Năm có 0 mã ngừng: không có

## 2. Security master vs. mã lấy được giá
- Mã trong master: 512 | có giá: 493 | thiếu: 19

| ticker   | reason                                        | vci_detail                                      | listing_date   | delisting_date   | delist_reason   |
|:---------|:----------------------------------------------|:------------------------------------------------|:---------------|:-----------------|:----------------|
| BCI      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'BCI'. | 2009-03-16     | 2018-02-23       | hop_nhat        |
| BGM      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'BGM'. | 2011-06-20     | 2017-08-10       | bat_buoc        |
| BHS      | không có giá điều chỉnh (VCI); có giá gốc HSX | VCI không có mã: Nguồn 'vci' không có mã 'BHS'. | 2006-12-20     | 2017-08-30       | hop_nhat        |
| GTN      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'GTN'. | 2014-10-03     | 2022-03-08       | bat_buoc        |
| KSA      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'KSA'. | 2010-07-27     | 2018-08-02       | bat_buoc        |
| KSS      | không có giá điều chỉnh (VCI)                 | VCI trả rỗng trong khoảng niêm yết HOSE         | 2010-01-04     | 2016-08-12       | bat_buoc        |
| KTB      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'KTB'. | 2010-10-01     | 2016-03-03       | bat_buoc        |
| NHS      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'NHS'. | 2010-07-02     | 2015-10-28       | tu_nguyen       |
| NHW      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'NHW'. | 2010-01-26     | 2015-02-25       | tu_nguyen       |
| NVN      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'NVN'. | 2010-03-30     | 2015-05-06       | bat_buoc        |
| PME      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'PME'. | 2017-11-08     | 2021-12-06       | bat_buoc        |
| PTK      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'PTK'. | 2012-09-25     | 2016-03-03       | bat_buoc        |
| SBC      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'SBC'. | 2010-06-02     | 2015-02-12       | tu_nguyen       |
| SEC      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'SEC'. | 2010-01-06     | 2015-09-28       | hop_nhat        |
| TAC      | không có giá điều chỉnh (VCI)                 | VCI trả rỗng trong khoảng niêm yết HOSE         | 2006-12-26     | 2022-05-20       | bat_buoc        |
| TIC      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'TIC'. | 2009-10-12     | 2017-10-12       | hop_nhat        |
| VIS      | không có giá điều chỉnh (VCI)                 | VCI trả rỗng trong khoảng niêm yết HOSE         | 2006-12-25     | 2022-04-22       | bat_buoc        |
| VPK      | không có giá điều chỉnh (VCI); có giá gốc HSX | VCI không có mã: Nguồn 'vci' không có mã 'VPK'. | 2006-12-21     | 2020-01-13       | bat_buoc        |
| VTF      | không có giá điều chỉnh (VCI)                 | VCI không có mã: Nguồn 'vci' không có mã 'VTF'. | 2010-09-24     | 2015-12-15       | chua_ro         |

## 3. So lợi suất ngày với prices.csv cũ (data_HOSE)
- Mã chung: 453, ngày chung: 2955, cặp (mã, ngày) so được: 964,264
- Tỷ lệ |Δr| > 0,5%: **0.025%** (242 cặp)
- Mã chỉ có ở bản mới (thêm vào, chủ yếu mã đã hủy): 40: AGF, ATA, ATG, AVF, BT6, C21, CDO, CLG, CMT, CYC, DCT, DIC, GTT, HLA, HLG, HSI, HTT, HVG, ICF, KAC, KHA, KSH, LMH, MPC, MTG, PPI, PXL, PXT, SAP, STT, TIE, TS4, TTP, TV1, VHG, VLF, VNA, VNH, VNI, VST
- Mã chỉ có ở bản cũ: 0: 

Mã lệch nhiều nhất (số ngày |Δr|>0,5%):
|     |   số ngày |
|:----|----------:|
| VOS |        83 |
| ANV |        64 |
| TDG |        21 |
| CCL |        16 |
| HCD |        14 |
| CDC |        14 |
| TSC |        11 |
| HAX |         9 |
| LCG |         5 |
| EVG |         2 |

## 4. Phiên |r| > 7% (biên độ HOSE) ngoài phiên đầu niêm yết
- Ngưỡng dùng: |r| > 7.5% (lợi suất thường; 7% + 0,5 đpt cho làm tròn bước giá/hệ số điều chỉnh).
- Tổng: 437 / 988,572 quan sát (0.044%); trong đó 317 ca ở mã có giá điều chỉnh < 2.000đ (VCI làm tròn 100đ → nhiễu bước giá, không phải lỗi biên độ).
- Lưu ý: giá đã điều chỉnh nên ngày GDKHQ có thể lệch khỏi biên độ; phiên sau đình chỉ dài, phiên giao dịch trở lại có biên độ ±20%.

Mã nhiều phiên nhất:
|     |   số phiên |
|:----|-----------:|
| VNH |        109 |
| GTT |         76 |
| VLF |         63 |
| AVF |         45 |
| SSC |         16 |
| HLA |         14 |
| SAP |         13 |
| BSI |         13 |
| VND |         11 |
| TVB |         11 |
| BBC |          7 |
| QBS |          6 |
| KHG |          6 |
| HAP |          6 |
| LAF |          6 |

15 trường hợp lớn nhất:
| date                | ticker   |         r |
|:--------------------|:---------|----------:|
| 2015-05-06 00:00:00 | CCL      |  0.535433 |
| 2020-01-10 00:00:00 | AGG      | -0.330162 |
| 2016-05-26 00:00:00 | GTT      |  0.166667 |
| 2019-06-21 00:00:00 | TEG      |  0.14455  |
| 2016-05-25 00:00:00 | GTT      | -0.142857 |
| 2015-10-05 00:00:00 | GTT      | -0.142857 |
| 2015-05-19 00:00:00 | AVF      |  0.142857 |
| 2016-05-27 00:00:00 | GTT      |  0.142857 |
| 2016-05-13 00:00:00 | GTT      |  0.142857 |
| 2016-05-23 00:00:00 | GTT      |  0.142857 |
| 2016-05-19 00:00:00 | GTT      |  0.142857 |
| 2022-10-20 00:00:00 | EMC      |  0.127389 |
| 2016-05-11 00:00:00 | GTT      | -0.125    |
| 2016-05-18 00:00:00 | GTT      | -0.125    |
| 2016-05-24 00:00:00 | GTT      | -0.125    |

## 5. Đuôi giá lặp lại với volume = 0 sau ngày giao dịch cuối
Quy tắc dựng: ngày volume = 0 bị đặt NaN, nên đuôi giá phải bằng 0 mã.
- Số mã vi phạm: **0**


## 6. Khác
- Tỷ lệ phiên r = 0: 15.3%
- Tỷ lệ NaN trong khoảng niêm yết: 30.0% (gồm cả ngoài khoảng niêm yết)
