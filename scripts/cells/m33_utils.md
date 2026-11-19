### 3.3 (bổ sung) Tiện ích chung

- `run` (backtest có cache), `metrics`, `cap` (chú thích "Bảng n"/"Hình n").
- Kiểm định: `hac`, `lw_var_test` (Ledoit–Wolf 2011: p HAC và **p bootstrap = kết quả chính**), `jkm_test`, `holm`, **`compare_to`**: mỗi cặp báo ΔVol (pp, < 0 là EW-RIE\* rủi ro thấp hơn), CI 95% bootstrap khối, p LW, p Holm (chỉ trên `CORE5`), p Jobson–Korkie, ΔTurnover kèm CI.
- **`FULL`** (15 phương pháp, chạy ở mọi thí nghiệm): Sample, Ledoit-Wolf, NL-LW, MP-clip, RIE, VS-NL-LW, VS-RIE, EW-NL-LW, EW-RIE (q\_eff), EW-WeSpeR, EW-RIE\*, PCA-auto, DCC-GARCH(1,1), 1/N, VS-EW-RIE\*. **`CORE5`** (họ kiểm định chính, định trước): EW-RIE\* so với NL-LW, EW-NL-LW, EW-WeSpeR, VS-NL-LW.
- `run_full`: chạy từng phương pháp một (mỗi cái một cache); phần không phụ thuộc h (hay HL\_VOL) chỉ tính một lần.
