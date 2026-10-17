#!/usr/bin/env python3
"""将 项目总览.md 渲染为适合 1920×1080 阅读的 HTML。

用法: python3 render_overview.py [总览.md] [输出.html]
特点: 冻结表头与首列、三年一期数据按年份分行、斑马纹与悬停高亮。
"""
import re
import sys
import html

PERIOD_LABELS = ["2023", "2024", "2025", "2026H1"]
# 需要按 " / " 拆成多行并加年份标签的列
PERIOD_COLS = {"近三年一期营收", "近三年一期净利润", "近三年一期毛利率"}


def parse_md_table(md_text):
    """提取第一个 markdown 表格，返回 (headers, rows)，rows 为字符串列表。"""
    lines = [l.rstrip() for l in md_text.splitlines()]
    start = None
    for i, l in enumerate(lines):
        if l.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            start = i
            break
    if start is None:
        sys.exit("未找到 markdown 表格")
    headers = [c.strip() for c in lines[start].strip().strip("|").split("|")]
    rows = []
    for l in lines[start + 2:]:
        if not l.strip().startswith("|"):
            break
        rows.append([c.strip() for c in l.strip().strip("|").split("|")])
    return headers, rows


def md_inline(text):
    """处理单元格内的少量 markdown：链接 [t](u) 与行内代码。"""
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text.replace("`", "")


def render_cell(header, value):
    if header in PERIOD_COLS and " / " in value:
        parts = [p.strip() for p in value.split(" / ")]
        lis = []
        for i, p in enumerate(parts):
            if re.match(r"^20\d\d", p):  # 已自带年份标签（如 "2026Q1：..."）
                yr, _, rest = p.partition("：")
                lis.append(f'<div class="period"><span class="yr">{html.escape(yr)}</span>{md_inline(rest)}</div>')
                continue
            label = PERIOD_LABELS[i] if i < len(PERIOD_LABELS) else f"期间{i + 1}"
            lis.append(f'<div class="period"><span class="yr">{label}</span>{md_inline(p)}</div>')
        return "".join(lis)
    if header == "报告":
        return md_inline(value).replace(">研究报告<", ">查看报告<")
    return md_inline(value).replace("<br>", "<br>")


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "项目总览.md"
    dst = sys.argv[2] if len(sys.argv) > 2 else "项目总览.html"
    md_text = open(src, encoding="utf-8").read()
    headers, rows = parse_md_table(md_text)

    # 列宽策略（按列名）
    col_class = {
        "公司名称": "c-name", "所处行业": "c-ind", "公司简介": "c-desc",
        "近三年一期营收": "c-num", "近三年一期净利润": "c-num", "近三年一期毛利率": "c-num",
        "拟上市板块": "c-sm", "审核状态": "c-sm", "问询轮次": "c-xs", "拟募资额": "c-sm",
        "第一大客户及占比": "c-mid", "净现比(最新年度)": "c-mid", "最严重红旗": "c-desc",
        "研究档位": "c-xs", "报告": "c-xs", "分析日期": "c-sm",
    }

    thead = "".join(f'<th class="{col_class.get(h, "")}">{html.escape(h)}</th>' for h in headers)
    body_rows = []
    for r in rows:
        tds = "".join(
            f'<td class="{col_class.get(h, "")}">{render_cell(h, v)}</td>'
            for h, v in zip(headers, r)
        )
        body_rows.append(f"<tr>{tds}</tr>")

    page = TEMPLATE.replace("{{THEAD}}", thead).replace("{{TBODY}}", "\n".join(body_rows))
    with open(dst, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"OK -> {dst}（{len(rows)} 个项目）")


TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IPO 项目研究总览</title>
<style>
  :root { --bd: #d8dee6; --hd: #1f3a5f; --accent: #2563eb; }
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 28px 40px 60px;
    font: 15px/1.65 -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
    color: #1f2329; background: #f5f6f8;
  }
  h1 { font-size: 22px; margin: 0 0 4px; color: var(--hd); }
  .sub { color: #6b7280; font-size: 13px; margin-bottom: 18px; }
  .wrap { overflow-x: auto; background: #fff; border: 1px solid var(--bd);
          border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,.06); }
  table { border-collapse: separate; border-spacing: 0; min-width: 100%; }
  th, td { padding: 10px 12px; border-bottom: 1px solid var(--bd);
           border-right: 1px solid #edf0f4; vertical-align: top; text-align: left; }
  thead th {
    position: sticky; top: 0; z-index: 3; background: var(--hd); color: #fff;
    font-size: 13px; white-space: nowrap; border-right-color: rgba(255,255,255,.15);
  }
  tbody tr:nth-child(even) { background: #f8fafc; }
  tbody tr:hover { background: #eef4ff; }
  /* 冻结首列 */
  .c-name { position: sticky; left: 0; z-index: 2; background: inherit;
            min-width: 170px; max-width: 200px; font-weight: 600; }
  thead .c-name { z-index: 4; background: var(--hd); }
  tbody tr:nth-child(odd) .c-name { background: #fff; }
  tbody tr:nth-child(even) .c-name { background: #f8fafc; }
  tbody tr:hover .c-name { background: #eef4ff; }
  td.c-name { box-shadow: 2px 0 0 var(--bd); }
  /* 列宽 */
  .c-ind { min-width: 150px; max-width: 190px; }
  .c-desc { min-width: 260px; max-width: 340px; }
  .c-num { min-width: 150px; white-space: nowrap; }
  .c-mid { min-width: 130px; max-width: 180px; }
  .c-sm { min-width: 90px; white-space: nowrap; }
  .c-xs { min-width: 60px; white-space: nowrap; text-align: center; }
  /* 三年一期分行 */
  .period { display: flex; gap: 8px; align-items: baseline; }
  .period .yr { flex: none; font-size: 11px; color: #fff; background: #94a3b8;
                border-radius: 4px; padding: 0 5px; min-width: 44px; text-align: center; }
  a { color: var(--accent); text-decoration: none; font-weight: 600; }
  a:hover { text-decoration: underline; }
</style>
</head>
<body>
<h1>IPO 项目研究总览</h1>
<div class="sub">金额单位：万元 · 三年一期 = 2023 / 2024 / 2025 / 2026H1 · 表格可横向滚动，首列与表头已冻结</div>
<div class="wrap">
<table>
<thead><tr>{{THEAD}}</tr></thead>
<tbody>
{{TBODY}}
</tbody>
</table>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
