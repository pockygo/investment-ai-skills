#!/usr/bin/env python3
"""解析带页码锚点的 MD，生成章节索引和表格清单。

用法:
    python build_index.py <md文件> <输出目录> [--prefix prospectus]

输出:
    <输出目录>/<prefix>_sections.json  章节标题 -> 行号区间、起始页码
    <输出目录>/<prefix>_tables.json    每张表 -> 页码、行号区间、所属章节、首行内容
"""
import argparse
import json
import re
from pathlib import Path

PAGE_RE = re.compile(r"^<!--\s*p(\d+)\s*-->\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)")
TABLE_ROW_RE = re.compile(r"^\|.*\|\s*$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md")
    ap.add_argument("out_dir")
    ap.add_argument("--prefix", default=None)
    args = ap.parse_args()

    md_path = Path(args.md)
    prefix = args.prefix or md_path.stem
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = md_path.read_text(encoding="utf-8").splitlines()

    # 行号 -> 页码映射
    page_at = {}
    cur = 0
    for i, ln in enumerate(lines):
        m = PAGE_RE.match(ln)
        if m:
            cur = int(m.group(1))
        page_at[i] = cur

    headings = []
    for i, ln in enumerate(lines):
        m = HEADING_RE.match(ln)
        if m:
            headings.append({"level": len(m.group(1)), "title": m.group(2).strip(),
                             "line": i + 1, "page": page_at[i]})

    sections = []
    for j, h in enumerate(headings):
        end = headings[j + 1]["line"] - 1 if j + 1 < len(headings) else len(lines)
        sections.append({**h, "end_line": end})

    tables, i = [], 0
    while i < len(lines):
        if TABLE_ROW_RE.match(lines[i]):
            start = i
            while i < len(lines) and (TABLE_ROW_RE.match(lines[i]) or not lines[i].strip()):
                i += 1
            block = lines[start:i]
            # 向上找最近的标题和首个非空文本行当表名线索
            section = next((h["title"] for h in reversed(headings) if h["line"] <= start + 1), "")
            caption = ""
            for k in range(start - 1, max(0, start - 6), -1):
                t = lines[k].strip()
                if t and not PAGE_RE.match(t):
                    caption = t[:80]
                    break
            tables.append({"page": page_at[start], "start_line": start + 1, "end_line": i,
                           "section": section, "caption": caption,
                           "header": block[0][:150] if block else "", "rows": len(block)})
        else:
            i += 1

    (out_dir / f"{prefix}_sections.json").write_text(
        json.dumps(sections, ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / f"{prefix}_tables.json").write_text(
        json.dumps(tables, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{md_path.name}: {len(sections)} 个标题, {len(tables)} 张表, {cur} 页")


if __name__ == "__main__":
    main()
