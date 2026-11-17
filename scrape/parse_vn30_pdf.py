"""Extract the VN30 constituent tickers from a HOSE 'danh muc thanh phan' PDF (text via pdftotext)."""
import re, subprocess, sys

STOP = re.compile(r"dự phòng|reserve|VNMidcap|VNSmallcap|VN100|VNAllShare", re.I)
ROW = re.compile(r"^\s*(\d{1,2})\s+([A-Z][A-Z0-9]{2})\b")

def vn30_tickers(pdf):
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    out, seen_rows = [], 0
    for line in txt.splitlines():
        if out and STOP.search(line):
            break
        m = ROW.match(line)
        if m:
            out.append(m.group(2))
    return out

if __name__ == "__main__":
    for p in sys.argv[1:]:
        t = vn30_tickers(p)
        print(p, len(t), " ".join(t))
