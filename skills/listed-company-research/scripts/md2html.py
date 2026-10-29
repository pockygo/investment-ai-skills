#!/usr/bin/env python3
"""Render research Markdown as a self-contained readable HTML file."""
import argparse
import html
import re
import sys
from pathlib import Path


def inline(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", text)


def render(src):
    body, toc, in_table, in_list = [], [], False, False
    for line in src.splitlines():
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            if in_table:
                body.append("</tbody></table>"); in_table = False
            if in_list:
                body.append("</ul>"); in_list = False
            level, title = len(heading.group(1)), heading.group(2)
            anchor = f"s{len(toc)+1}"
            toc.append((level, title, anchor))
            body.append(f'<h{level} id="{anchor}">{inline(title)}</h{level}>')
        elif line.strip().startswith("|") and line.strip().endswith("|"):
            cells = [inline(c.strip()) for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r"[-: ]+", html.unescape(c)) for c in cells):
                continue
            if not in_table:
                if in_list:
                    body.append("</ul>"); in_list = False
                body.append("<table><tbody>"); in_table = True
            body.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
        elif re.match(r"^[-*]\s+", line):
            if in_table:
                body.append("</tbody></table>"); in_table = False
            if not in_list:
                body.append("<ul>"); in_list = True
            item = re.sub(r"^[-*]\s+", "", line)
            body.append(f"<li>{inline(item)}</li>")
        elif re.match(r"^!\[(.*?)\]\((.+?)\)\s*$", line.strip()):
            if in_table:
                body.append("</tbody></table>"); in_table = False
            if in_list:
                body.append("</ul>"); in_list = False
            m = re.match(r"^!\[(.*?)\]\((.+?)\)\s*$", line.strip())
            alt, src = m.group(1), m.group(2)
            # 包一层链接：点图可看原图（图表信息密度高，需要放大）
            body.append(f'<figure><a href="{html.escape(src)}" target="_blank" rel="noopener">'
                        f'<img src="{html.escape(src)}" alt="{html.escape(alt)}"></a>'
                        f'<figcaption>{inline(alt)}</figcaption></figure>')
        elif line.strip():
            if in_table:
                body.append("</tbody></table>"); in_table = False
            if in_list:
                body.append("</ul>"); in_list = False
            body.append(f"<p>{inline(line)}</p>")
    if in_table:
        body.append("</tbody></table>")
    if in_list:
        body.append("</ul>")
    nav = "".join(f'<a class="l{n}" href="#{a}">{html.escape(t)}</a>' for n, t, a in toc)
    return nav, "\n".join(body)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src"); parser.add_argument("dest"); parser.add_argument("--title")
    args = parser.parse_args()
    nav, body = render(Path(args.src).read_text(encoding="utf-8"))
    title = args.title or "上市公司研究报告"
    page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{html.escape(title)}</title><style>
body{{margin:0;background:#f4f6f8;color:#17202a;font:15px/1.75 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}}nav{{position:fixed;width:250px;inset:0 auto 0 0;overflow:auto;padding:24px;background:#10243e}}nav a{{display:block;color:#dbe7f5;text-decoration:none;padding:4px 0}}nav .l2{{padding-left:14px}}nav .l3{{padding-left:28px;font-size:13px}}main{{margin-left:250px;max-width:1180px;padding:36px}}article{{background:white;padding:42px;border-radius:10px}}h1,h2{{border-bottom:1px solid #d8e0e8;padding-bottom:8px}}table{{border-collapse:collapse;width:100%;overflow:auto;display:block}}td{{border:1px solid #ccd5df;padding:6px 10px;white-space:nowrap}}tr:first-child{{background:#eaf0f6;font-weight:600}}code{{background:#eef2f5;padding:1px 4px}}figure{{margin:26px 0;text-align:center;max-width:100%}}figure img{{display:block;max-width:100%;width:auto;height:auto;margin:0 auto;border:1px solid #dde3ea;border-radius:6px}}figcaption{{font-size:13px;color:#5b6b7c;margin-top:8px}}@media(max-width:800px){{nav{{position:static;width:auto}}main{{margin:0;padding:12px}}article{{padding:20px}}}}</style></head><body><nav>{nav}</nav><main><article>{body}</article></main></body></html>'''
    Path(args.dest).write_text(page, encoding="utf-8")
    # 自检：样式块在 f-string 内，双大括号写错会静默丢失规则
    for rule in ("figure img{", "max-width:100%", "display:block"):
        if rule not in page:
            print(f"警告：HTML 缺少关键样式 {rule}，图片可能按原始尺寸溢出", file=sys.stderr)
    print(f"OK -> {args.dest}")


if __name__ == "__main__":
    main()
