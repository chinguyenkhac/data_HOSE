### 3.3 Tiện ích chung

- `run` (backtest có cache theo từng phương pháp), `run_full`, `metrics`, `cap` (chú thích "Bảng n"/"Hình n").
- Đối chứng thêm cho T3 (1/N, PCA-auto, DCC-GARCH(1,1)) và bộ VS-EW-RIE\*; bộ VS "đủ T" (§5.4) và hai biến thể VS của T5d.
- **12 phương pháp `M12`:** 10 bộ của thầy, EW-WeSpeR, VS-EW-RIE\*. **12 cặp định trước `PAIRS12`**, mỗi cặp chỉ khác một thành phần; ΔVol = Vol(bộ trước) − Vol(bộ sau), âm là bộ trước rủi ro thấp hơn:

| Cụm | Câu hỏi | Cặp |
|---|---|---|
| A | Làm sạch đúng lý thuyết có hơn xấp xỉ không? | EW-RIE\* − EW-NL-LW · EW-RIE\* − EW-RIE (q_eff) · EW-RIE\* − EW-WeSpeR |
| B | Trọng số mũ có giúp không? | EW-NL-LW − NL-LW · EW-RIE\* − RIE |
| C | Trước và sau chuẩn hóa biến động (VS) | VS-NL-LW − NL-LW · VS-RIE − RIE · VS-EW-RIE\* − EW-RIE\* |
| D | Trong họ VS, ai hơn? | VS-EW-RIE\* − VS-NL-LW · VS-EW-RIE\* − VS-RIE · VS-RIE − VS-NL-LW |
| E | Trọng số mũ hay VS? (cặp thầy hỏi) | EW-RIE\* − VS-NL-LW |

- **Kiểm định:** sai khác phương sai Ledoit–Wolf (2011), bản HAC và bản bootstrap khối (b = 21, M = 2000; **p bootstrap là kết quả chính**); Holm trên cả 12 cặp, riêng từng cấu hình và từng chế độ; Jobson–Korkie–Memmel cho Sharpe. `pair_table` (bảng chi tiết), `pair_grid` + `pair_heatmap` (heatmap cặp; dấu \* chỉ hiệu chỉnh trong từng cột, mang tính mô tả), Bảng A (`table_a`: hàng = phương pháp, in đậm giá trị thấp nhất mỗi cột).
