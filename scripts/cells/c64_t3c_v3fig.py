# T3c (hình phụ, lấy lại từ v3_nho): Vol của VS-NL-LW, EW-RIE*, VS-EW-RIE* (trục Vol KHÔNG bắt đầu từ 0, ghi rõ trên hình)
fig, ax = plt.subplots(1, 2, figsize=(12, 3.8)); K = ["VS-NL-LW", "EW-RIE*", "VS-EW-RIE*"]
for a_, m in zip(ax, MODES):
    v = [OUT0[m][k]["m"]["Vol %"] for k in K]; a_.bar(K, v, color=["#e0a800", COL["EW-RIE*"], "#c0392b"])
    for i, x in enumerate(v): a_.text(i, x, f2(x), ha="center", va="bottom")
    a_.set_ylim(min(v) - 0.6, max(v) + 0.4); a_.set_ylabel("Vol %/năm (trục không bắt đầu từ 0)"); a_.set_title(f"{VN[m]} – Vol (%/năm)"); a_.spines[["top", "right"]].set_visible(False)
fig.suptitle("VS-NL-LW, EW-RIE* và VS-EW-RIE*"); plt.tight_layout(); savefig(fig, "fig_T3d_vs_ew_rie")
cap("Hình", "Hình phụ (v3): Vol của VS-NL-LW, EW-RIE\\* và VS-EW-RIE\\* ở cấu hình chuẩn. **Trục Vol không bắt đầu từ 0** (để thấy chênh lệch nhỏ); các chênh lệch này không có ý nghĩa thống kê (Bảng T3c).")
