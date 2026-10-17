#!/usr/bin/env python3
"""PDF -> Markdown 转换脚本（ipo-research pipeline 第一步）。

主路：MinerU（表格保真，本地模型，零 API token）。
降级：docling -> pdftotext -layout。
输出统一为带页码锚点 `<!-- pN -->` 的 Markdown 文件，N 为 PDF 物理页码（从 1 开始）。

用法:
    python convert.py <pdf路径> <输出目录> [--name 输出名] [--backend mineru|docling|pdftotext] [--max-pages N]
"""
import argparse
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path


# ---------- HTML table -> Markdown ----------

class _TableParser(HTMLParser):
    """把简单 HTML 表格转成 Markdown；遇到跨行/跨列合并时放弃转换（保留 HTML）。"""

    def __init__(self):
        super().__init__()
        self.rows = []
        self._row = None
        self._cell = None
        self.merged = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr":
            self._row = []
        elif tag in ("td", "th"):
            if attrs.get("colspan") not in (None, "1") or attrs.get("rowspan") not in (None, "1"):
                self.merged = True
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None:
            text = "".join(self._cell).strip().replace("|", "\\|").replace("\n", " ")
            self._row.append(re.sub(r"\s+", " ", text))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            if self._row:
                self.rows.append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def html_table_to_md(html: str):
    """成功返回 markdown 字符串，失败（合并单元格等）返回 None。"""
    p = _TableParser()
    try:
        p.feed(html)
    except Exception:
        return None
    if p.merged or not p.rows:
        return None
    width = max(len(r) for r in p.rows)
    rows = [r + [""] * (width - len(r)) for r in p.rows]
    out = ["| " + " | ".join(rows[0]) + " |", "|" + " --- |" * width]
    for r in rows[1:]:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


# ---------- MinerU 后端 ----------

def _find_one(base: Path, pattern: str):
    hits = sorted(base.rglob(pattern))
    return hits[0] if hits else None


def convert_mineru(pdf: Path, out_dir: Path, max_pages=None) -> Path:
    work = out_dir / (pdf.stem + "_mineru")
    work.mkdir(parents=True, exist_ok=True)
    mineru_bin = Path(sys.executable).with_name("mineru")
    cmd = [str(mineru_bin if mineru_bin.exists() else "mineru"),
           "-p", str(pdf), "-o", str(work), "-b", "pipeline", "-l", "ch"]
    if max_pages:
        cmd += ["-s", "0", "-e", str(max_pages - 1)]
    subprocess.run(cmd, check=True)

    content_list = _find_one(work, "*_content_list.json")
    if content_list:
        return _md_from_content_list(content_list, out_dir, pdf.stem)
    md = _find_one(work, "*.md")
    if md:
        dest = out_dir / f"{pdf.stem}.md"
        dest.write_text(md.read_text(encoding="utf-8"), encoding="utf-8")
        return dest
    raise RuntimeError("MinerU 运行成功但未找到输出文件")


def _md_from_content_list(cl_path: Path, out_dir: Path, stem: str) -> Path:
    """从 content_list.json 重建 MD，注入页码锚点；表格尽量转 Markdown。"""
    blocks = json.loads(cl_path.read_text(encoding="utf-8"))
    lines, cur_page = [], 0
    for b in blocks:
        page = b.get("page_idx", 0) + 1
        if page != cur_page:
            cur_page = page
            lines.append(f"\n<!-- p{page} -->\n")
        btype = b.get("type")
        if btype == "text":
            level = b.get("text_level", 0)
            text = (b.get("text") or "").strip()
            if not text:
                continue
            lines.append(("#" * min(level, 6) + " " + text) if level else text)
            lines.append("")
        elif btype == "table":
            for cap in b.get("table_caption", []) or []:
                lines.append(f"表：{cap}")
            body = b.get("table_body", "") or ""
            md_table = html_table_to_md(body) if body else None
            lines.append(md_table if md_table else body)
            for note in b.get("table_footnote", []) or []:
                lines.append(f"注：{note}")
            lines.append("")
        # 图片块跳过（招股书中多为 logo/流程图，文字版无需保留）
    dest = out_dir / f"{stem}.md"
    dest.write_text("\n".join(lines), encoding="utf-8")
    return dest


# ---------- docling 后端（降级） ----------

def convert_docling(pdf: Path, out_dir: Path, max_pages=None) -> Path:
    from docling.document_converter import DocumentConverter

    result = DocumentConverter().convert(str(pdf))
    dest = out_dir / f"{pdf.stem}.md"
    dest.write_text(result.document.export_to_markdown(), encoding="utf-8")
    return dest


# ---------- pdftotext 后端（保底） ----------

def convert_pdftotext(pdf: Path, out_dir: Path, max_pages=None) -> Path:
    cmd = ["pdftotext", "-layout"]
    if max_pages:
        cmd += ["-f", "1", "-l", str(max_pages)]
    cmd += [str(pdf), "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    pages = raw.split("\f")
    lines = []
    for i, page in enumerate(pages, start=1):
        page = page.strip()
        if not page:
            continue
        lines.append(f"\n<!-- p{i} -->\n")
        lines.append(page)
    dest = out_dir / f"{pdf.stem}.md"
    dest.write_text("\n".join(lines), encoding="utf-8")
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("out_dir")
    ap.add_argument("--name", default=None, help="输出文件名（不含扩展名），默认用 PDF 文件名")
    ap.add_argument("--backend", default="mineru", choices=["mineru", "docling", "pdftotext", "auto"])
    ap.add_argument("--max-pages", type=int, default=None)
    args = ap.parse_args()

    pdf = Path(args.pdf).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    backends = ["mineru", "docling", "pdftotext"] if args.backend == "auto" else [args.backend]
    last_err = None
    for be in backends:
        try:
            fn = {"mineru": convert_mineru, "docling": convert_docling, "pdftotext": convert_pdftotext}[be]
            dest = fn(pdf, out_dir, args.max_pages)
            if args.name:
                renamed = dest.with_name(args.name + ".md")
                dest.rename(renamed)
                dest = renamed
            print(f"OK [{be}] -> {dest}")
            return
        except Exception as e:  # noqa: BLE001
            print(f"后端 {be} 失败: {e}", file=sys.stderr)
            last_err = e
    sys.exit(f"所有后端均失败，最后错误: {last_err}")


if __name__ == "__main__":
    main()
