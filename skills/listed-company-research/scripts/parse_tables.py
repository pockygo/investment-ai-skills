#!/usr/bin/env python3
"""三表 + 主要会计数据 → CSV（按 PDF 坐标重建行，不依赖文本流顺序）。

供 quarterly.py 消费，也可单独用于任意多项报告期的数字底稿。

年报 PDF 的文本流顺序并不可靠（有的年份数字在上、指标名在下），
pdftotext 的阅读顺序会因此错位。这里用 pdfplumber 取词坐标：
同一 y 的词聚成一行、按 x 排序 —— 视觉顺序即逻辑顺序。

用法:
    python3 scripts/index_sections.py md --out index      # 先建章节索引（强烈建议）
    python3 scripts/parse_tables.py --out extracts
    python3 scripts/parse_tables.py --out extracts --periods fy2024 fy2025 --show

注意：缺少 --index 时会退化为全文扫描——速度更慢，且指标名跨行拼接质量略降。
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

import pdfplumber

TITLE = re.compile(r"^\s*\d{0,2}\s*[、.．]?\s*(合并|母公司)[^，。]{0,10}?(资产负债表|利润表|现金流量表)\s*$")
KPI_HEAD = re.compile(r"主要会计数据和财务指标")
QUARTER_HEAD = re.compile(r"分季度主要财务指标")
QUARTER_END = re.compile(r"上述财务指标|季度报告、半年度报告相关财务指标存在")
NOISE = re.compile(r"^(流|其中：其中|以|列）|（|\)|适用|不适用)")
CONT = re.compile(r"^(的|列|填|）|\)|其中：)")
TAIL = re.compile(r"^(的|列|填|）|\)|流|额|润)")   # 名称尾行的典型开头
TAIL_EXACT = {"（元）", "（元/股）", "（或股本）"}
NUM = re.compile(r"^[-(（]?\d[\d,]*\.?\d*[)）]?%?$|^[—–-]$")
SCAN_SPAN = 30
Y_TOL = 4
GAP = 9        # 名称与数字行视为同一行的最大基线差（pt）


GLUE = ((re.compile(r"(%)[ \t]*(?=[\d(（-])"), r"\1 "),
        (re.compile(r"([)）])[ \t]*(?=[\d(（-])"), r"\1 "))


def split_numbers(line):
    for rx, rep in GLUE:            # 拆开「73.06%2,747,517,835.72」这类粘连
        line = rx.sub(rep, line)
    tokens = line.split()
    nums = []
    while tokens and len(nums) < 6 and NUM.match(tokens[-1]):
        nums.append(tokens.pop())
    return " ".join(tokens).strip(), list(reversed(nums))


def frag_ok(text):
    s = text.strip()
    if not s or len(s) > 34:          # 允许「购建固定资产、无形资产和其他」这类长名
        return False
    if re.search(r"[0-9。？?□√]", s) or s in {"适用", "不适用", "是", "否"}:
        return False
    return True


def page_lines(page):
    """按基线把词重建成行：同一 y 聚类、按 x 排序，返回 (top, text)。"""
    try:
        words = page.extract_words(x_tolerance=1.5, y_tolerance=2.5)
    except Exception:
        return []
    bins = {}
    for w in words:
        bins.setdefault(int(w["bottom"] // Y_TOL), []).append(w)
    out = []
    for k in sorted(bins):
        ws = sorted(bins[k], key=lambda w: w["x0"])
        text = " ".join(w["text"] for w in ws).strip()
        if text:
            out.append((min(w["bottom"] for w in ws), text))
    return out


def detect_mode(rr):
    """判定该文档的排版：指标名在数字行上方（above）还是下方（below）。

    部分年报（2024 等）数字单元格上对齐、名称单元格下对齐，基线差约 5pt，
    数字印在名称上方。按「数字行最近邻的短文本行在上还是在下」投票决定。
    """
    parsed = [(p, y, *split_numbers(t)) for p, y, t in rr]
    above = below = pair = total = 0
    for i, (_, y, item, nums) in enumerate(parsed):
        if not nums:
            continue
        total += 1
        prev_ok = i and not parsed[i - 1][3] and frag_ok(parsed[i - 1][2]) \
            and abs(parsed[i - 1][1] - y) <= GAP
        next_ok = i + 1 < len(parsed) and not parsed[i + 1][3] and frag_ok(parsed[i + 1][2]) \
            and abs(parsed[i + 1][1] - y) <= GAP
        if prev_ok:
            above += 1
        if next_ok:
            below += 1
        if prev_ok and not item.strip():
            pair += 1
    # 三行式（名字/数字交替）：数字行大多没有同行名称，且上方紧邻名称
    if total and pair / total > 0.6:
        return "pair"
    return "below" if below > above else "above"


def iter_rows(rr, mode="above"):
    if mode == "pair":                     # 名字一行、数字一行交替：直接上下配对
        parsed = [(p, y, *split_numbers(t)) for p, y, t in rr]
        rows = []
        for i, (page, y, item, nums) in enumerate(parsed):
            if not nums:
                continue
            head = item.strip()
            name = head
            if not head and i:
                pv = parsed[i - 1]
                if not pv[3] and frag_ok(pv[2]) and abs(pv[1] - y) <= GAP * 2:
                    name = pv[2].strip()
            name = name.strip()
            if not name or len(name) < 2:
                continue
            if len(nums) == 1 and nums[0].isdigit() and int(nums[0]) == page:
                continue
            if re.fullmatch(r"[\d\s,.\-()%—–]+", name) or NOISE.match(name):
                continue
            rows.append([page, name, nums])
        return rows

    """跨行拼接产出 (page, item, nums)。

    折行有三种排版：
      A. 数字独占一行                  → 名称 = 相邻碎片
      B. 数字行以续行词开头（的/列/填） → 名称 = 相邻碎片 + 本行残名
      C. 名称尾行在数字行之后（"…（元）"）→ 回填到刚产出的那一行
    同一行内「名称 + 数字」的正常排版直接成行。
    """
    parsed = [(p, y, *split_numbers(t)) for p, y, t in rr]
    rows, pending, pending_page, pending_y = [], [], 0, None
    amend, amend_y = None, None

    for page, y, item, nums in parsed:
        if not nums:
            s = item.strip()
            if not frag_ok(s):
                pending, pending_y = [], None
                continue
            is_tail = bool(TAIL.match(s)) or s in TAIL_EXACT
            if amend is not None and is_tail and amend_y is not None \
                    and abs(y - amend_y) <= GAP * 2.5 and len(s) <= 14:
                amend[1] += s                      # C：数字行后的名称尾行
                amend, amend_y = None, None        # 尾行只可能有一行，用完即清
                continue
            if len(pending) < 3 and (pending_y is None or abs(y - pending_y) <= GAP * 2):
                if not pending:
                    pending_page = page
                pending.append(s)
                pending_y = y
            else:
                pending, pending_y = [s], y
                pending_page = page
            continue

        head = item.strip()
        if mode == "below":
            # 名称在数字下方：紧邻其后、间距很小的碎片才是本行名称
            name = head
            j_gap = y
            pending_ok = not head
            pending, pending_y = [], None
        else:
            merged = bool(pending) and (not head or bool(CONT.match(head)))
            name = ("".join(pending) + head) if (not head or CONT.match(head)) else head
            pending, pending_y = [], None
        name = name.strip()
        amend, amend_y = None, None
        if not name or len(name) < 2:
            continue
        if len(nums) == 1 and nums[0].isdigit() and int(nums[0]) == page:
            continue
        if re.fullmatch(r"[\d\s,.\-()%—–]+", name) or NOISE.match(name):
            continue
        row = [pending_page or page, name, nums]
        rows.append(row)
        if mode == "above" and (not head or merged):
            amend, amend_y = row, y
    return rows


def pair_below(rr):
    """below 排版专用：把紧随数字行、间距 <= GAP 的名称碎片并进去。"""
    parsed = [(p, y, *split_numbers(t)) for p, y, t in rr]
    rows, i = [], 0
    while i < len(parsed):
        page, y, item, nums = parsed[i]
        if not nums:
            i += 1
            continue
        parts = [item.strip()] if item.strip() else []
        j, prev_y = i + 1, y
        while j < len(parsed) and not parsed[j][3]:
            s = parsed[j][2].strip()
            if not frag_ok(s) or abs(parsed[j][1] - prev_y) > GAP:
                break
            parts.append(s)
            prev_y = parsed[j][1]
            j += 1
        name = "".join(parts).strip()
        if name and len(name) >= 2 and not re.fullmatch(r"[\d\s,.\-()%—–]+", name) \
                and not NOISE.match(name) and not (len(nums) == 1 and nums[0].isdigit()
                                                   and int(nums[0]) == page):
            rows.append([page, name, nums])
        i = j if j > i + 1 else i + 1
    return rows


def section_window(index_dir, period):
    p = Path(index_dir) / f"{period}.json"
    if not p.exists():
        return None, None
    meta = json.loads(p.read_text(encoding="utf-8"))
    secs = meta.get("sections", [])
    fin = next((s for s in secs if re.search(r"财务报告|财务报表", s["title"])), None)
    kpi = next((s for s in secs if re.search(r"简介|主要财务|基本情况", s["title"])), None)
    if not (fin or kpi):
        return None, None
    lo = min(x["start"] for x in (fin, kpi) if x)
    hi = fin["start"] + SCAN_SPAN if fin else None
    return lo, hi


def parse_block(rr):
    """按文档排版选解析器：below（名称在数字下方）/ pair（名称与数字交替成行）/ above。"""
    mode = detect_mode(rr)
    if mode == "below":
        return pair_below(rr)
    return iter_rows(rr, mode)


def collect(pdf_path, lo, hi):
    rr = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        n = len(pdf.pages)
        for i in range(max(0, (lo or 1) - 1), min(n, hi or n)):
            for y, text in page_lines(pdf.pages[i]):
                rr.append((i + 1, y, text))
    segs = []
    for idx, (page, _, text) in enumerate(rr):
        m = TITLE.match(text)
        if m:
            segs.append((f"{m.group(1)}{m.group(2)}", idx, page))
    rows = []
    for i, (name, idx, page) in enumerate(segs):
        end = segs[i + 1][1] if i + 1 < len(segs) else min(idx + 130, len(rr))
        rows += [(name, pg, it, nums) for pg, it, nums in parse_block(rr[idx:end])]

    k0 = next((i for i, (_, _, t) in enumerate(rr) if KPI_HEAD.search(t)), None)
    q0 = next((i for i, (_, _, t) in enumerate(rr) if QUARTER_HEAD.search(t)), None)
    if k0 is not None:
        kend = q0 if (q0 and q0 > k0) else min(k0 + 120, len(rr))
        rows += [("主要会计数据", pg, it, nums) for pg, it, nums in parse_block(rr[k0:kend])]
    if q0 is not None:
        qend = next((i for i, (_, _, t) in enumerate(rr) if i > q0 and QUARTER_END.search(t)),
                    min(q0 + 80, len(rr)))
        rows += [("分季度指标", pg, it, nums) for pg, it, nums in parse_block(rr[q0:qend])]
    return rows, len(segs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default="md")
    ap.add_argument("--index", default="index")
    ap.add_argument("--out", default="extracts")
    ap.add_argument("--periods", nargs="*")
    ap.add_argument("--show", action="store_true")
    args = ap.parse_args()

    manifest = {m["name"]: m["source"] for m in
                json.loads((Path(args.md) / "manifest.json").read_text(encoding="utf-8"))}
    periods = sorted(manifest) if not args.periods else args.periods
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    all_rows, report = [], []
    for period in periods:
        src = manifest.get(period)
        if not src or not Path(src).exists():
            print(f"  {period}: 缺 PDF，跳过", file=sys.stderr)
            continue
        lo, hi = section_window(args.index, period)
        rows, n_seg = collect(src, lo, hi)
        report.append((period, n_seg, len(rows)))
        all_rows += [(period, *r) for r in rows]
        with open(out / f"fin_{period}.csv", "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.writer(fh)
            w.writerow(["period", "statement", "page", "item", "v1", "v2", "v3", "v4"])
            for s, pg, it, nums in rows:
                w.writerow([period, s, pg, it, *((nums + [""] * 4)[:4])])

    with open(out / "fin_all.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["period", "statement", "page", "item", "v1", "v2", "v3", "v4"])
        for period, s, pg, it, nums in all_rows:
            w.writerow([period, s, pg, it, *((nums + [""] * 4)[:4])])

    for period, n_seg, n_row in report:
        print(f"  {period:<9} 表 {n_seg:>2} 段 / 行 {n_row:>4}")
    print(f"OK -> {out}/fin_all.csv ({len(all_rows):,} 行)")

    if args.show:
        keys = ("营业收入", "营业成本", "归属于上市公司股东的净利润",
                "扣除非经常性损益", "经营活动产生的现金流量净额", "存货", "应收账款")
        for period, *_ in report:
            print(f"\n=== {period}")
            for p, s, pg, it, nums in all_rows:
                if p == period and s in ("主要会计数据", "合并利润表") \
                        and any(k in it for k in keys) and len(it) <= 34:
                    print(f"  p{pg:<3} {s:<6} {it:<30}{'  '.join(nums[:2])}")


if __name__ == "__main__":
    main()
