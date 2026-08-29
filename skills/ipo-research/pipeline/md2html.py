#!/usr/bin/env python3
"""Markdown 研究报告 -> 带侧边目录的独立 HTML（无外部依赖，离线可读）。

用法:
    python md2html.py <输入.md> <输出.html> [--title 标题]
"""
import argparse
import re

import markdown


TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{ --sidebar-w: 280px; --accent: #1a5fb4; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: -apple-system, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
         color: #24292f; line-height: 1.75; background: #f6f7f9; }}
  nav {{ position: fixed; top: 0; left: 0; bottom: 0; width: var(--sidebar-w); overflow-y: auto;
         background: #fff; border-right: 1px solid #e1e4e8; padding: 20px 16px; font-size: 14px; }}
  nav .toc-title {{ font-weight: 700; font-size: 15px; margin-bottom: 10px; color: var(--accent); }}
  nav a {{ display: block; color: #444; text-decoration: none; padding: 3px 0 3px 8px; border-left: 2px solid transparent; }}
  nav a:hover {{ color: var(--accent); border-left-color: var(--accent); }}
  nav a.lv1 {{ font-weight: 600; margin-top: 8px; padding-left: 0; }}
  nav a.lv2 {{ padding-left: 16px; }}
  nav a.lv3 {{ padding-left: 32px; font-size: 13px; color: #666; }}
  main {{ margin-left: var(--sidebar-w); padding: 32px 48px 80px; max-width: 980px; }}
  article {{ background: #fff; padding: 40px 48px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  h1 {{ font-size: 26px; border-bottom: 2px solid var(--accent); padding-bottom: 10px; }}
  h2 {{ font-size: 21px; margin-top: 40px; border-bottom: 1px solid #e1e4e8; padding-bottom: 6px; }}
  h3 {{ font-size: 17px; margin-top: 28px; color: #333; }}
  table {{ border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 14px; display: block; overflow-x: auto; }}
  th, td {{ border: 1px solid #d0d7de; padding: 6px 12px; text-align: left; white-space: nowrap; }}
  th {{ background: #f0f3f6; }}
  tr:nth-child(even) td {{ background: #fafbfc; }}
  blockquote {{ margin: 12px 0; padding: 8px 16px; background: #fff8e6; border-left: 4px solid #e8a33d; color: #5c4a1f; }}
  code {{ background: #eff1f3; padding: 1px 5px; border-radius: 4px; font-size: 90%; }}
  hr {{ border: none; border-top: 1px dashed #ccc; margin: 32px 0; }}
  strong {{ color: #111; }}
  @media (max-width: 900px) {{
    nav {{ position: static; width: auto; border-right: none; border-bottom: 1px solid #e1e4e8; }}
    main {{ margin-left: 0; padding: 16px; }}
    article {{ padding: 20px; }}
  }}
  @media print {{ nav {{ display: none; }} main {{ margin: 0; max-width: none; }} article {{ box-shadow: none; }} }}
</style>
</head>
<body>
<nav><div class="toc-title">目录</div>{toc}</nav>
<main><article>{body}</article></main>
</body>
</html>
"""


def slugify(text: str, used: set) -> str:
    slug = re.sub(r"[^\w一-鿿-]+", "-", text.strip()).strip("-").lower() or "sec"
    base, i = slug, 2
    while slug in used:
        slug = f"{base}-{i}"
        i += 1
    used.add(slug)
    return slug


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dest")
    ap.add_argument("--title", default=None)
    args = ap.parse_args()

    text = open(args.src, encoding="utf-8").read()

    # 收集标题生成锚点与目录
    used, toc, out_lines = set(), [], []
    for ln in text.splitlines():
        m = re.match(r"^(#{1,3})\s+(.*)", ln)
        if m:
            level, title = len(m.group(1)), m.group(2).strip()
            anchor = slugify(re.sub(r"[*`]", "", title), used)
            toc.append((level, re.sub(r"[*`]", "", title), anchor))
            out_lines.append(f'{"#" * level} <a id="{anchor}"></a>{title}')
        else:
            out_lines.append(ln)
    body_md = "\n".join(out_lines)

    body = markdown.markdown(body_md, extensions=["tables", "sane_lists"])
    toc_html = "\n".join(
        f'<a class="lv{lv}" href="#{anchor}">{title}</a>' for lv, title, anchor in toc
    )
    title = args.title or (toc[0][1] if toc else "研究报告")
    html = TEMPLATE.format(title=title, toc=toc_html, body=body)
    with open(args.dest, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK -> {args.dest}（{len(toc)} 个目录项）")


if __name__ == "__main__":
    main()
