"""Khôi phục .ipynb (chỉ mã + markdown, không output) từ HTML nbconvert (template lab)."""
import sys, json, re
from bs4 import BeautifulSoup
from markdownify import markdownify
import nbformat

def convert(src, dst):
    soup = BeautifulSoup(open(src, encoding="utf-8").read(), "lxml")
    cells = []
    for c in soup.select("div.jp-Cell"):
        cls = c.get("class", [])
        if "jp-CodeCell" in cls:
            pre = c.select_one("div.jp-InputArea-editor pre")
            if pre is None: continue
            cells.append(nbformat.v4.new_code_cell(pre.get_text()))
        elif "jp-MarkdownCell" in cls:
            body = c.select_one("div.jp-RenderedMarkdown")
            for a in body.select("a.anchor-link"): a.decompose()
            md = markdownify(str(body), heading_style="ATX", bullets="-").strip()
            cells.append(nbformat.v4.new_markdown_cell(md))
    nb = nbformat.v4.new_notebook(cells=cells)
    nbformat.write(nb, dst)
    print(dst, len(cells), "cells,", sum(c.cell_type == "code" for c in cells), "code")

if __name__ == "__main__": convert(sys.argv[1], sys.argv[2])
