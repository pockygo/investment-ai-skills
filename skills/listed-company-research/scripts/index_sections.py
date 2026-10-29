#!/usr/bin/env python3
"""为带 <!-- pN --> 锚点的报告文本建立章节索引（供分层阅读定位）。

用法:
    python3 scripts/index_sections.py md --out index
产物:
    index/<period>.json   每份报告的章节表（标题/起止页/字符数/估算token）
    index/sections.md     全部报告汇总表
"""
import argparse
import json
import re
from pathlib import Path

KIND_BY_PREFIX = [("fy", "年报"), ("h1", "半年报"), ("q", "季报")]

SEC = re.compile(r"^第([一二三四五六七八九十]+)节\s*(.*\S)?\s*$")
SEC_Q = re.compile(r"^([一二三四五六七八九十]+)、\s*(\S.{0,28})$")
PAGE = re.compile(r"^<!-- p(\d+) -->$")
NUM_CSV = re.compile(r"\d{1,3},\d{3}")
BAD = re.compile(r"(\.{3,}|^\s*\d+\s*$)")

EST_CHARS_PER_TOKEN = 1.35  # 中文粗估


def kind_of(period):
    for prefix, label in KIND_BY_PREFIX:
        if period.startswith(prefix):
            return label
    return "其他"


def load(path):
    """返回 (lines, pages_list, 最后页码)。"""
    lines = path.read_text(encoding="utf-8").splitlines()
    pages = [int(m.group(1)) for l in lines if (m := PAGE.match(l.strip()))]
    return lines, pages, (max(pages) if pages else 1)


def scan_headings(lines):
    """识别一级（第X节）与二级（一、）标题，返回 [(page, title, level)]。"""
    heads, page = [], 0
    for raw in lines:
        m = PAGE.match(raw.strip())
        if m:
            page = int(m.group(1))
            continue
        line = raw.strip()
        if not line or len(line) > 40 or NUM_CSV.search(line) or BAD.search(line):
            continue
        if SEC.match(line):
            heads.append((page, line, 1))
        elif SEC_Q.match(line):
            heads.append((page, line, 2))
    return heads


def dedupe(heads):
    """同一标题（忽略空白）可能在页眉/目录重复出现，保留最早出现的那次。"""
    seen, out = set(), []
    for page, title, lvl in heads:
        key = (re.sub(r"\s+", "", title), lvl)
        if key in seen:
            continue
        seen.add(key)
        out.append((page, title, lvl))
    out.sort()
    return out


def chars_in(lines, p0, p1):
    total, page, keep = 0, 0, False
    for raw in lines:
        m = PAGE.match(raw.strip())
        if m:
            page = int(m.group(1))
            keep = p0 <= page <= p1
            continue
        if keep:
            total += len(raw.strip())
    return total


def build_sections(lines, heads, last_page):
    lvl1 = [(p, t) for p, t, l in heads if l == 1]
    lvl2 = [(p, t) for p, t, l in heads if l == 2]
    base = lvl1 if lvl1 else lvl2          # 季报没有「节」，用一、二、三 当章节
    if not base:
        return []
    secs = []
    for i, (page, title) in enumerate(base):
        end = base[i + 1][0] - 1 if i + 1 < len(base) else last_page
        end = max(end, page)
        ch = chars_in(lines, page, end)
        secs.append({"title": title, "pages": f"{page}-{end}", "start": page,
                     "end": end, "chars": ch,
                     "est_tokens": int(ch / EST_CHARS_PER_TOKEN)})
    return secs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md_dir")
    ap.add_argument("--out", default="index")
    args = ap.parse_args()
    md_dir, out = Path(args.md_dir), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    recs = []
    for path in sorted(md_dir.glob("*.md")):
        period = path.stem
        lines, pages, last = load(path)
        if not lines:
            continue
        heads = dedupe(scan_headings(lines))
        secs = build_sections(lines, heads, last)
        total = chars_in(lines, 1, last)
        rec = {"period": period, "kind": kind_of(period), "pages": len(pages) or last,
               "chars": total, "est_tokens": int(total / EST_CHARS_PER_TOKEN),
               "sections": secs}
        (out / f"{period}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        recs.append(rec)

    out_lines = ["# 报告章节索引", "",
                 f"共 {len(recs)} 份 / {sum(r['chars'] for r in recs):,} 字符 "
                 f"≈ {sum(r['est_tokens'] for r in recs):,} token", ""]
    for r in recs:
        out_lines += [f"## {r['period']}（{r['kind']}）{r['pages']} 页 / "
                      f"{r['chars']:,} 字 ≈ {r['est_tokens']:,} token", "",
                      "| 章节 | 页 | 字符 | ≈token | 占比 |", "|---|---|---|---|---|"]
        for s in r["sections"]:
            share = s["chars"] / r["chars"] * 100 if r["chars"] else 0
            out_lines.append(f"| {s['title']} | {s['pages']} | {s['chars']:,} | "
                             f"{s['est_tokens']:,} | {share:.0f}% |")
        out_lines.append("")
    (out / "sections.md").write_text("\n".join(out_lines), encoding="utf-8")

    print(f"OK {len(recs)} periods -> {out}/sections.md")
    for r in recs:
        if not r["sections"]:
            print(f"  {r['period']:<9} {r['pages']:>4}p {r['chars']:>8,}字  (无章节)")
            continue
        top = max(r["sections"], key=lambda s: s["chars"])
        print(f"  {r['period']:<9} {r['pages']:>4}p {r['chars']:>8,}字 "
              f"{len(r['sections'])}节  最大: {top['title'][:16]} {top['chars']/r['chars']*100:.0f}%")


if __name__ == "__main__":
    main()
