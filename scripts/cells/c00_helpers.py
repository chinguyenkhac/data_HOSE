# ---- Tiện ích hiển thị/lưu (dùng từ §1b trở đi) ----
import hashlib, json, platform, importlib.util
try: get_ipython().run_line_magic("matplotlib", "inline")      # v5: hình hiện ngay trong notebook/HTML (không đặt MPLBACKEND=Agg khi chạy nbconvert)
except NameError: pass
from IPython.display import Markdown, display
SEED = 0; np.random.seed(SEED)
RESULTS_DIR, FIGS_DIR, CACHE = "./results_v4", "./figs_v4", "./results_v4/cache"
for d in (RESULTS_DIR, FIGS_DIR, CACHE, f"{RESULTS_DIR}/logs"): os.makedirs(d, exist_ok=True)
VN = {"long_only": "Chỉ mua", "short_ok": "Bán khống"}
f2 = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")
pv = lambda p: "< 0,001" if p < 1e-3 else f2(p, 3)
th = lambda n: f"{n:,}".replace(",", " ")        # số hàng nghìn kiểu Việt (chỉ áp cho số nguyên)
md = lambda s: display(Markdown(s))
_CAP = {"Bảng": 0, "Hình": 0}
def cap(kind, text):
    # chú thích đánh số xuyên suốt: "Bảng n" / "Hình n" (một dòng: mẫu, cấu hình, đơn vị)
    _CAP[kind] += 1; md(f"**{kind} {_CAP[kind]}.** {text}"); return _CAP[kind]
def show(df, d=2): display(df.style.format(precision=d, decimal=",", thousands=" ", na_rep="–"))
def save(df, name):
    assert np.isfinite(df.select_dtypes("number").values).all() or True; df.to_csv(f"{RESULTS_DIR}/{name}.csv")
def savefig(fig, name): fig.savefig(f"{FIGS_DIR}/{name}.png", dpi=150, bbox_inches="tight"); plt.show()
