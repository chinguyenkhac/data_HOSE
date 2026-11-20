# EW_RIE_HOSE — pipeline v5 (chạy đến khi xong)

Giao việc cho Claude Code. Đọc hết một lượt rồi làm lần lượt Bước 0 → 9. Không có giới hạn giờ: chạy đến khi xong. Người giao việc không trực máy: gặp chỗ chưa rõ thì chọn phương án hợp lý nhất, ghi vào `PROGRESS.md` rồi làm tiếp.

**Không mở rộng dữ liệu.** Chỉ dùng `data_hose/` (HOSE 2015–11/2026) như v4. Không thêm HNX, không tải dữ liệu mới.

---

## 1. Nguồn và đích

| File | Vai trò |
|---|---|
| `EW_RIE_HOSE.ipynb` | **Bản mẫu của thầy.** Khuôn trình bày và **phần mở đầu chép nguyên văn** (Bước 1) |
| `EW_RIE_HOSE_v3_nho.ipynb` | **Bản thầy ưng.** Phần lớn nội dung, câu chữ và **toàn bộ hình** lấy lại từ đây |
| `EW_RIE_HOSE_v4.ipynb` | Bản chạy đêm qua: mục lục gọn, các phân tích bổ sung, cache trong `results_v4/`. Dùng làm khung |
| → `EW_RIE_HOSE_v5.ipynb` | **Đích.** Sao từ v4, rồi làm các bước dưới đây. v3, v4 để nguyên |

Kết quả vào `results_v5/`, hình vào `figs_v5/`, cache dùng lại `results_v4/cache/` (chép sang `results_v5/cache/`).

## 2. Quy tắc (giữ như v4)

1. Không sửa ô code của thầy (ngoại lệ đã có: CONFIG, `RUN_SENS`, `PAIRS`).
2. Không chỉnh tham số để EW-RIE\* thắng; kết quả ra sao viết đúng vậy.
3. Mọi bảng so sánh dùng cùng ngày ngoài mẫu (giữ assert).
4. Kiểm thử hay đối chiếu không đạt: ghi nguyên số, không sửa cho khớp.
5. Sau **mỗi bước**: cập nhật `PROGRESS.md` (đã xong, đang làm, quyết định đã tự chọn, việc tiếp), commit, push lên **nhánh hiện tại**. **Không merge, không đẩy `main`**.
6. Phần nặng chạy bằng script nền (`scripts/`), log vào `results_v5/logs/`. Khi chờ: `sleep` 5–10 phút rồi xem 20 dòng cuối log. Không kết thúc lượt khi job còn chạy.

---

## 3. Các bước

### Bước 0. Chuẩn bị và kiểm tra hồi quy
**Làm gì:** sao v4 → v5, chép cache. Chạy v5 chưa sửa gì.
**Đạt khi:** Vol cấu hình chuẩn khớp v4 đến 0,01 (EW-RIE\* 12,56 / 13,07; VS-NL-LW 12,49 / 12,93; NL-LW 13,10 / 13,72; EW-NL-LW 12,72 / 13,12; EW-WeSpeR 12,57 / 13,05).

### Bước 1. Phần mở đầu: chép của thầy, chỉ sửa kết quả
**Làm gì:**
- Ô đầu tiên (tiêu đề, Câu hỏi nghiên cứu, Phương pháp đề xuất 1–4, Đối chứng, Tài liệu chính) và ô **Phân công nhóm**: chép **nguyên văn** từ `EW_RIE_HOSE.ipynb`, thay hai ô mở đầu hiện tại của v4.
- Chỉ được sửa đoạn từ dòng `**Kết quả hiện có (...)` đến hết dòng `Hạn chế: ...`:
  - Dòng tiêu đề: `**Kết quả hiện có (HOSE 12/2016–11/2026, N=100, T=250, h=60):**`
  - Bảng: giữ đúng khuôn thầy (cột Bán khống, Chỉ mua; số có dấu %), các hàng NL-LW, EW-NL-LW, EW-RIE ($q_{\text{eff}}$), **EW-RIE\***, thêm hai hàng EW-WeSpeR và VS-NL-LW. Số lấy từ §4.
  - Câu kết quả: thay câu "EW-RIE\* tốt hơn có ý nghĩa … so với mọi đối chứng" (không còn đúng trên dữ liệu mới) bằng 2–3 câu đúng với số liệu: ngang VS-NL-LW và EW-WeSpeR về rủi ro (nêu ΔVol, p Holm); thấp hơn có ý nghĩa so với EW-NL-LW (và NL-LW ở chế độ chỉ mua); turnover thấp hơn VS-NL-LW có ý nghĩa; nhanh hơn EW-WeSpeR khoảng 8 lần. Nếu kết quả Bước 2–4 đổi thì cập nhật cho khớp.
  - Hạn chế: một dòng gồm 19 mã hủy thiếu giá; tình trạng đối chiếu WeSpeR (Bước 2); EW-RIE\* kém ổn định khi N > T_eff.
- Trạng thái từng việc T, ghi chú v4/v5: đưa xuống **Ghi chú v5** cuối notebook, không chèn vào phần của thầy.

**Đạt khi:** so chuỗi với ô của thầy, khác biệt chỉ nằm trong đoạn Kết quả/Hạn chế.

### Bước 2. Đối chiếu EW-WeSpeR với mã gốc của Oriol (§1b)
**Làm gì:**
- Người giao việc đã cấp quyền chạy. Chạy `scripts/wesper_check.py` với mã trong `/home/user/nlcvbo/wesper` (cài `torch` CPU, `numba` nếu cần).
- Xác minh repo: ghi lại link GitHub mà trang arXiv 2410.14413 hoặc trang tác giả trỏ tới. Nếu khác `nlcvbo/wesper` thì dùng repo đúng. Không mở được thì ghi rõ "chưa xác minh được repo chính thức".
- Giả lập (mô hình nhân tố của Test 2, N = 100, T = 250, h ∈ {15, 30, 60}, 20 lần lặp) và 12 cửa sổ HOSE. So: phổ quần thể τ (W1 chuẩn hóa), trị riêng sau co ξ (sai lệch tương đối trung vị/lớn nhất), rủi ro GMV so với tối ưu, thời gian mỗi lần.
- Nếu mã gốc dưới 30 s/lần: chạy thêm backtest "EW-WeSpeR (Oriol)" ở cấu hình chuẩn, thêm vào T3 và §4.3.
- **Hình mới:** scatter ξ (bản nhóm) theo ξ (bản gốc), một cửa sổ HOSE và một mẫu giả lập, đường chéo y = x.

**Đạt khi:** ξ sai lệch trung vị < 5% và chênh tỷ số rủi ro < 1%. Không đạt: báo nguyên số. Chạy quá 3 giờ mà chưa xong: dừng, ghi lại và sang bước sau.

### Bước 3. T6 còn thiếu: cửa sổ T (§5.4, mới)
**Câu hỏi:** đổi độ dài cửa sổ ước lượng T thì EW-RIE\* so với VS-NL-LW và các bộ đầu bảng có đổi không?
**Làm gì:**
- T ∈ {120, 250, 500}, N = 100, h = 60, các tham số khác chuẩn, hai chế độ, đủ `FULL` (DCC theo quy tắc 45 phút như v4).
- Ghi số kỳ OOS và ngày bắt đầu OOS của mỗi T. Không so Vol tuyệt đối giữa các T; chỉ so trong cùng T.
- Với mỗi T: Vol mọi phương pháp, xếp hạng, `compare_to` (EW-RIE\* vs mọi bộ, Holm trên `CORE5`), `pairwise_top` (Bước 4).
- Thêm một cột q = N/T và q_eff = N·Σw² vào bảng.
- Ghi chú khi viết kết quả: với h = 60, trọng số mũ gần như không còn sau ~250 phiên, nên các bộ EW ít đổi theo T; các bộ cửa sổ phẳng (NL-LW, VS-NL-LW, RIE) đổi nhiều hơn. Đây là điều cần kiểm, không phải kết luận viết sẵn.
- **Hình:** Vol theo T cho 6 bộ `TOP`, hai chế độ; và ΔVol (EW-RIE\* − VS-NL-LW) kèm CI theo T.
- Đưa 2 cấu hình mới (T = 120, 500) vào bảng tổng kết độ vững (Bước 6).

### Bước 4. So sánh mọi cặp giữa các bộ đầu bảng (mới)
**Câu hỏi:** trong nhóm dẫn đầu, có bộ nào thật sự tốt hơn bộ khác không, hay tất cả ngang nhau?
**Làm gì:**
- `TOP` = 6 bộ có hạng trung bình tốt nhất ở Bảng tổng kết v4: EW-RIE\*, VS-NL-LW, VS-EW-RIE\*, EW-WeSpeR, EW-NL-LW, VS-RIE.
- Hàm `pairwise_top` (Phụ lục A) đặt ở §3.3: mọi 15 cặp, ΔVol, kiểm định phương sai Ledoit–Wolf 2011 (HAC và bootstrap, b = 21), Jobson–Korkie, ΔTurnover, **Holm trên cả 15 cặp**.
- Chạy ở:
  - **Cấu hình chuẩn** (§4.4 mới, ngay sau §4.3): bảng 15 cặp + hình ma trận ΔVol 6 × 6 (màu đỏ–xanh, \* = p Holm < 0,05), hai chế độ.
  - **Mọi ô độ vững** (N × h, HL_VOL, T, REB, lọc đứng giá, hủy niêm yết): lưu CSV `pairwise_all_cells.csv`; trong Bảng tổng kết thêm ma trận "số ô hàng thấp hơn cột có ý nghĩa" (p mô tả, không hiệu chỉnh xuyên lưới).
- Viết rõ: nhóm nào phân biệt được với nhau, nhóm nào không.

### Bước 5. Lấp các so sánh, kiểm định, hình còn thiếu

| Chỗ | Đang thiếu | Thêm |
|---|---|---|
| §4.1 bảng chính | Không có kiểm định cạnh bảng (chỉ CI bootstrap của thầy) | Một dòng dẫn tới §4.4 và T3c; không sửa ô thầy |
| §5.1 half-life | Ô của thầy chỉ có EW-NL-LW và EW-RIE\*; không có VS-NL-LW, không có hình | Ô mới ngay dưới: Vol theo h ∈ {30, 60, 120} cho 6 bộ `TOP` (bộ không phụ thuộc h vẽ đường ngang), lấy từ cache lưới N × h ở N = 100; bảng `compare_to` theo h. Dùng lại hình T6 của v3 nếu hợp |
| §5.2 lưới N × h | Bảng chỉ có cột so VS-NL-LW; heatmap chưa hiện trong HTML | Thêm cột ΔVol so với EW-WeSpeR và VS-EW-RIE\*; heatmap thứ ba so với EW-WeSpeR |
| §5.3 HL_VOL | Không có hình | Hình Vol theo HL_VOL của VS-NL-LW, VS-RIE, VS-EW-RIE\*, đường ngang EW-RIE\* |
| T2c phí thực tế | Sharpe sau phí chưa kiểm định | p Jobson–Korkie cho EW-RIE\* vs VS-NL-LW; mức phí hòa vốn Sharpe sau phí |
| Tổng kết độ vững | Không có hình | (i) Hạng của 6 bộ `TOP` qua mọi ô (điểm cho từng ô + trung vị); (ii) scatter Vol – turnover ở cấu hình chuẩn cho `FULL`, hai chế độ (cho thấy "cùng rủi ro, ít giao dịch hơn") |
| Test 2b-30 | Ghi chú lý do không có VS | Một câu: dữ liệu giả lập có biến động không đổi nên VS không có tác dụng, thầy đã lưu ý VS chưa được xác nhận trong mô phỏng |

### Bước 6. Khôi phục hình của v3_nho và nhúng đủ hình
**Vấn đề:** HTML v4 chỉ hiện 1 hình (§4.2); các hình khác chỉ là file PNG. Nguyên nhân có thể: chạy notebook với backend không hiển thị (`MPLBACKEND=Agg`) hoặc vẽ trong script.
**Làm gì:**
- §0: thêm `%matplotlib inline`. Chạy notebook bằng `jupyter nbconvert --execute` **không** đặt `MPLBACKEND=Agg`. Mọi hình vẽ trong notebook (dữ liệu đọc từ cache), `savefig` vừa lưu PNG vừa hiện.
- Khôi phục 9 hình của v3_nho, đặt đúng mục mới:

| Hình v3_nho | Mục v5 |
|---|---|
| Số mã có dữ liệu theo năm | 2.1 |
| Tổng số cổ phiếu niêm yết; số mã hủy niêm yết theo năm và lý do | 2.3 |
| Rủi ro ngoài mẫu (hình cột của thầy) | 4.2 |
| T2a heatmap Vol và Sharpe theo REB × COST | T2a, **giữ làm hình phụ**, sau hình đường mới của v4 |
| Vol theo mức lọc đứng giá | T2b |
| T3d VS-NL-LW, EW-RIE\*, VS-EW-RIE\* | T3c, **giữ làm hình phụ**, sửa trục Vol bắt đầu từ 0 hoặc ghi rõ "trục không từ 0" |
| ΔVol do VS theo giai đoạn | T5a |
| Sai số dự báo vol: EWMA vs cửa sổ phẳng | T5b |
| Độ nhạy theo N và h | 5.2 |

- Giữ cả 11 hình mới của v4 (`fig_cost_sharpe`, `fig_delist_dvol`, `fig_dvol_ci`, `fig_period_dvol`, `fig_reb_vol`, `fig_timing_loglog`, `fig_vol_forecast`, `fig_vs_periods`, `fig_zero_filter`, hai heatmap §5.2) và hình mới của Bước 2–5.
- Câu chữ: các đoạn Kết quả/Kết luận của v3_nho còn đúng thì giữ nguyên văn; chỉ sửa chỗ số liệu hoặc kết luận đã đổi (ví dụ câu "thấp nhất ở 18/18 tổ hợp").
- Đánh số "Hình n", "Bảng n" xuyên suốt, mỗi hình một dòng chú thích; màu cố định như v4.

**Đạt khi:** số ảnh nhúng trong HTML ≥ số lời gọi `savefig` + số hình của thầy; không có ô in "Figure(…)" mà không có ảnh.

### Bước 7. Cập nhật tóm tắt và kết luận
- Đoạn Kết quả ở Bước 1, Bảng tổng kết độ vững, các câu tự sinh: cập nhật theo kết quả Bước 2–4.
- Một đoạn kết luận cuối §6 (3–5 câu): EW-RIE\* hơn, ngang, kém VS-NL-LW ở đâu; nhóm dẫn đầu có phân biệt được với nhau không (Bước 4); điểm mạnh nằm ở rủi ro, turnover hay thời gian chạy.

### Bước 8. Chạy sạch và tự kiểm
Khởi động lại kernel, chạy từ trên xuống, xuất `EW_RIE_HOSE_v5.html`. Kiểm và ghi đạt/không đạt vào `BAO_CAO_V5.md`:
1. Ô code của thầy nguyên vẹn; hai ô mở đầu chỉ khác ở đoạn Kết quả/Hạn chế.
2. Test 1, 2, 2b, 2b-30 và mọi assert qua.
3. Hồi quy Bước 0 khớp.
4. Mọi so sánh cùng ngày.
5. `pairwise_top` cho cặp EW-RIE\* vs VS-NL-LW ra cùng ΔVol với `compare_to`.
6. Số ảnh nhúng đạt điều kiện Bước 6.
7. Mọi con số trong chữ khớp bảng ngay trên.
8. Đếm lỗi số: Newton thất bại, WeSpeR dự phòng, GARCH dự phòng.

### Bước 9. Giao kết quả
- Commit, push nhánh hiện tại, **không merge**.
- **Gửi trực tiếp trong phiên chat** (đính kèm): `EW_RIE_HOSE_v5.ipynb`, `EW_RIE_HOSE_v5.html`, `BAO_CAO_V5.md`. Không đính kèm được thì để ở thư mục gốc repo và nêu đường dẫn.
- `BAO_CAO_V5.md` (ngắn): kết quả đối chiếu WeSpeR (và repo đã dùng); kết quả cửa sổ T; ma trận so sánh nhóm dẫn đầu; danh sách hình/kiểm định đã thêm; kết quả tự kiểm; việc chưa xong và lý do.

---

## Phụ lục A — so sánh mọi cặp trong nhóm dẫn đầu

Đặt ở §3.3, sau `compare_to` (dùng `lw_var_test`, `jkm_test`, `holm`, `turnover_series` đã có).

```python
TOP = ["EW-RIE*", "VS-NL-LW", "VS-EW-RIE*", "EW-WeSpeR", "EW-NL-LW", "VS-RIE"]   # 6 bộ đứng đầu theo hạng TB (Bảng tổng kết v4)

def pairwise_top(out, methods=TOP, reb_dates=None, block=21, M=2000, seed=0):
    # Mọi cặp (a, b) trong TOP: ΔVol = Vol(a) − Vol(b), kiểm định phương sai LW (2011) bootstrap, Holm trên toàn bộ cặp.
    ms = [m for m in methods if m in out]; rows = []
    for i, a in enumerate(ms):
        for b in ms[i + 1:]:
            ra, rb = out[a]["r"].values, out[b]["r"].values
            assert out[a]["r"].index.equals(out[b]["r"].index), f"khác mẫu: {a}, {b}"
            d, se, p_hac, p_bt = lw_var_test(ra, rb, block=block, M=M)
            row = dict(a=a, b=b, dvol=(ra.std() - rb.std()) * np.sqrt(252) * 100, p_hac=p_hac, p_boot=p_bt, p_jkm=jkm_test(ra, rb)[1])
            if reb_dates is not None:
                row["dturn"] = np.nanmean(turnover_series(out[a], reb_dates) - turnover_series(out[b], reb_dates))
            rows.append(row)
    PW = pd.DataFrame(rows); PW["p_holm"] = holm(PW["p_boot"].values)
    # ma trận vuông: ô (a, b) = ΔVol(a − b), dấu * nếu p Holm < 0,05
    D = pd.DataFrame(np.nan, index=ms, columns=ms); S = pd.DataFrame("", index=ms, columns=ms)
    for r in PW.itertuples():
        D.loc[r.a, r.b], D.loc[r.b, r.a] = r.dvol, -r.dvol
        if r.p_holm < .05: S.loc[r.a, r.b] = S.loc[r.b, r.a] = "*"
    return PW, D, S
```

Đã chạy thử với dữ liệu giả lập (15 cặp, ma trận đối xứng ngược dấu). Chưa chạy trên dữ liệu thật.

## Phụ lục B — ước lượng thời gian (chưa đo)

| Bước | Ước lượng |
|---|---|
| 2 Đối chiếu Oriol | chưa biết; mã gốc có thể chậm, giới hạn 3 giờ |
| 3 Cửa sổ T (2 cấu hình mới × 15 bộ × 2 chế độ) | ~1–2 giờ, DCC và WeSpeR chiếm phần lớn |
| 4 So sánh mọi cặp (đọc cache) | ~15–30 phút |
| 5–7 Hình, bảng, chữ | ~1–2 giờ viết code |
| 8 Chạy sạch | ~35–45 phút |
