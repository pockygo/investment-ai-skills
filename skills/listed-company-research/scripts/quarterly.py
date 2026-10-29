#!/usr/bin/env python3
"""季度财务面板：把季报/半年报/年报的累计数拆成单季，生成同比、环比与 TTM。

设计要点（对应 references/quarterly-panel.md）：
1. 季报有两套列：「本报告期」（单季）与「年初至报告期末」（累计）。取错就会把单季
   当累计相减，算出负数季度。本脚本取累计列，并用年报「分季度主要财务指标」表校验。
2. 单季 = 累计差额：Q1=c1，Q2=c2-c1，Q3=c3-c2，Q4=c4-c3。
3. 环比受季节性影响（Q1 通常最低），因此同比、环比、TTM 并列，趋势以 TTM 为主。

用法:
    python3 scripts/quarterly.py --extracts extracts --out timeseries/季度财务面板.md
"""
import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path

YEAR = re.compile(r"(\d{4})")
KPI_SKIP = ("每股收益", "收益率", "资产总额", "总资产", "资产总计", "净资产", "净资",
            "所有者权益", "调整", "优先股", "永续债")
DAYS = 91.25
FLOW = ("rev", "net", "ded", "ocf", "cost", "rd", "capex")
STOCK = ("ar", "inv", "contract", "debt")


def num(s):
    s = (s or "").strip().replace(",", "")
    if not s or s in {"—", "-", "–"}:
        return None
    if s.endswith("%"):
        return None                       # 增减率列不参与取数
    neg = s.startswith("(") or s.startswith("（") or s.startswith("-")
    s = s.strip("()-—–（）")
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def load(path):
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig")))
    kpi, qdis = defaultdict(list), defaultdict(list)
    stmt = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        p, s = r["period"], r["statement"]
        vals = [num(r[f"v{i}"]) for i in (1, 2, 3, 4)]
        name = r["item"].replace(" ", "")
        if s == "主要会计数据":
            kpi[p].append((name, vals))
        elif s == "分季度指标":
            qdis[p].append((name, vals))
        else:
            stmt[p][s][name] = vals[0]
    return kpi, qdis, stmt


def cum_col(vals):
    """取累计列：季报为 [本报告期, 增减%, 年初至报告期末, 增减%]；其余取首个非空。"""
    if len(vals) >= 3 and vals[2] is not None:
        return vals[2]
    return next((v for v in vals if v is not None), None)


def core_kpi(rows):
    """按顺序取 [营业收入, 归母净利, 扣非, 经营现金流] 并做合理性校验。

    指标名常被 PDF 折行截断（只剩「润（元）」），因此以顺序为主、关键字为辅。
    """
    seq = [(n, cum_col(v)) for n, v in rows if not any(k in n for k in KPI_SKIP)]
    seq = [(n, v) for n, v in seq if v is not None]
    if len(seq) < 4:
        return None

    # 关键字优先：即使指标名被折行截断，多数仍保留「营业收入/净利润/经营活动」等词
    named, used = {}, set()
    for i, (name, v) in enumerate(seq):
        if "营业收入" in name and "rev" not in named:
            named["rev"], _ = v, used.add(i)
        elif "非经常性损益" in name and "净利润" in name and "ded" not in named:
            named["ded"], _ = v, used.add(i)
        elif "净利润" in name and "net" not in named:
            named["net"], _ = v, used.add(i)
        elif "经营活动" in name and "ocf" not in named:
            named["ocf"], _ = v, used.add(i)
    # 顺序兜底：补齐缺失项（如整行只剩「润（元）」的极端折行）
    rest = [v for i, (_, v) in enumerate(seq) if i not in used]
    for key in ("rev", "net", "ded", "ocf"):
        if key not in named and rest:
            named[key] = rest.pop(0)

    rev, net = named.get("rev"), named.get("net")
    ded, ocf = named.get("ded"), named.get("ocf")
    if not rev or rev <= 0 or net is None or net > rev * 1.5:
        return None
    if ded is not None and abs(ded) > abs(net) * 1.5:
        return None
    return {"rev": rev, "net": net, "ded": ded, "ocf": ocf}


def pick(items, names, contains=None):
    for n in names:
        v = items.get(n)
        if v is not None:
            return v
    if contains:
        for k, v in items.items():
            if v is not None and all(c in k for c in contains):
                return v
    return None


def tag_of(period):
    if period.startswith("fy"):
        return "fy"
    if period.startswith("h1"):
        return "h1"
    if period.startswith("q1"):
        return "q1"
    if period.startswith("q3"):
        return "q3"
    return None


def build(kpi, stmt):
    cum, warn = {}, []
    for period in sorted(kpi):
        m = YEAR.search(period)
        tag = tag_of(period)
        if not m or not tag:
            continue
        core = core_kpi(kpi[period])
        if not core:
            warn.append(f"{period}: 核心指标不足，跳过")
            continue
        inc = stmt.get(period, {}).get("合并利润表", {})
        cash = stmt.get(period, {}).get("合并现金流量表", {})
        bs = stmt.get(period, {}).get("合并资产负债表", {})
        cum[int(m.group(1)), tag] = {
            **core,
            "cost": pick(inc, ("其中：营业成本", "营业成本", "减：营业成本"),
                          contains=("营业成本",)),
            "rd": pick(inc, ("研发费用",)),
            "capex": pick(cash, ("购建固定资产、无形资产和其他长期资产支付的现金",),
                          contains=("购建固定资产",)),
            "ar": pick(bs, ("应收账款",)),
            "inv": pick(bs, ("存货",)),
            "contract": pick(bs, ("合同负债",)),
            "debt": sum(v for v in (pick(bs, ("短期借款",)), pick(bs, ("长期借款",)),
                                    pick(bs, ("一年内到期的非流动负债",))) if v) or None,
        }
        # 经营现金流以现金流量表为准：KPI 表偶有缺行，且名称易被折行截断
        ocf_stmt = pick(cash, ("经营活动产生的现金流量净额",), contains=("经营活动产生的现金",))
        if ocf_stmt is not None:
            cum[int(m.group(1)), tag]["ocf"] = ocf_stmt

    quarters = {}
    years = sorted({y for y, _ in cum})
    for y in years:
        q1, h1, q3, fy = (cum.get((y, t)) for t in ("q1", "h1", "q3", "fy"))

        def sub(a, b, fields=FLOW):
            if not a or not b:
                return None
            out = {}
            for f in fields:
                x, z = a.get(f), b.get(f)
                out[f] = None if (x is None or z is None) else x - z
            out.update({k: a.get(k) for k in STOCK})
            return out

        if q1:
            quarters[(y, 1)] = q1
        q2 = sub(h1, q1)
        if q2:
            quarters[(y, 2)] = q2
        q3q = sub(q3, h1)
        if q3q:
            quarters[(y, 3)] = q3q
        q4 = sub(fy, q3)
        if q4:
            quarters[(y, 4)] = q4
    return quarters, cum, warn


def validate(quarters, qdis):
    """用年报「分季度主要财务指标」校验累计相减的结果。"""
    issues, checked = [], 0
    for period, rows in qdis.items():
        m = YEAR.search(period)
        if not m:
            continue
        year = int(m.group(1))
        seq = [(n, v) for n, v in rows if not any(k in n for k in KPI_SKIP)]
        disclosed = [v for _, vals in seq[:1] for v in vals if v is not None]
        if len(disclosed) < 4:
            continue
        for qi, dv in enumerate(disclosed[:4], 1):
            q = quarters.get((year, qi))
            if not q or q.get("rev") is None:
                continue
            checked += 1
            if abs(q["rev"] - dv) > max(1e5, abs(dv) * 0.005):
                issues.append((year, qi, q["rev"], dv))
    return checked, issues


def fmt(v, digits=1):
    return "未披露" if v is None else f"{v/1e6:,.{digits}f}"


def pct(v):
    return "未披露" if v is None else f"{v*100:+.1f}%"


def ratio(v):
    return "未披露" if v is None else f"{v:.2f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extracts", default="extracts")
    ap.add_argument("--out", default="timeseries/季度财务面板.md")
    args = ap.parse_args()

    kpi, qdis, stmt = load(Path(args.extracts) / "fin_all.csv")
    quarters, cum, warn = build(kpi, stmt)
    if not quarters:
        raise SystemExit("没有可用季度数据；先运行 parse_tables.py")
    for w in warn:
        print("警告: " + w)

    keys = sorted(quarters)
    q_at = lambda i: quarters.get(keys[i]) if 0 <= i < len(keys) else None

    def yoy(i, f):
        cur, prev = q_at(i), quarters.get((keys[i][0] - 1, keys[i][1]))
        if not cur or not prev:
            return None
        a, b = prev.get(f), cur.get(f)
        return None if (not a or b is None) else b / a - 1

    def qoq(i, f):
        if i == 0:
            return None
        a, b = q_at(i - 1).get(f), q_at(i).get(f)
        return None if (not a or b is None) else b / a - 1

    def ttm(i):
        if i < 3:
            return None
        win = [q_at(j) for j in range(i - 3, i + 1)]
        if any(w is None for w in win):
            return None
        rev = sum(w.get("rev") or 0 for w in win)
        net = sum(w.get("net") or 0 for w in win)
        cost = sum(w.get("cost") or 0 for w in win)
        ocf = sum(w.get("ocf") or 0 for w in win)
        gm = (1 - cost / rev) if (rev and cost) else None
        return {"rev": rev, "net": net, "gm": gm,
                "ncr": (ocf / net) if net else None}

    checked, issues = validate(quarters, qdis)
    L = ["# 季度财务面板", "",
         f"> 覆盖 {keys[0][0]}Q{keys[0][1]}–{keys[-1][0]}Q{keys[-1][1]}，共 {len(keys)} 个季度；"
         "金额单位：百万元。",
         "> 口径：单季 = 累计数差额（季报取「年初至报告期末」列）；季报与半年报未经审计。"
         f"与年报「分季度主要财务指标」交叉校验 {checked} 格，不一致 {len(issues)} 格。", ""]

    L += ["## 表 A 单季规模与盈利", "",
          "| 季度 | 营业收入 | YoY | QoQ | 归母净利 | YoY | QoQ | 扣非净利 |",
          "|---|---|---|---|---|---|---|---|"]
    for i, k in enumerate(keys):
        q = quarters[k]
        L.append(f"| {k[0]}Q{k[1]} | {fmt(q.get('rev'))} | {pct(yoy(i,'rev'))} | "
                 f"{pct(qoq(i,'rev'))} | {fmt(q.get('net'))} | {pct(yoy(i,'net'))} | "
                 f"{pct(qoq(i,'net'))} | {fmt(q.get('ded'))} |")

    L += ["", "## 表 B 单季盈利质量", "",
          "| 季度 | 毛利率 | 净利率 | 扣非/归母 | 经营现金流 | 净现比 | 研发费用 | 研发/收入 |",
          "|---|---|---|---|---|---|---|---|"]
    for k in keys:
        q = quarters[k]
        rev, cost, net = q.get("rev"), q.get("cost"), q.get("net")
        gm = (1 - cost / rev) if (rev and cost) else None
        nm = (net / rev) if (rev and net is not None) else None
        dr = (q["ded"] / net) if (q.get("ded") is not None and net) else None
        ncr = (q["ocf"] / net) if (q.get("ocf") is not None and net) else None
        rdr = (q["rd"] / rev) if (q.get("rd") is not None and rev) else None
        L.append(f"| {k[0]}Q{k[1]} | {pct(gm) if gm is not None else '未披露'} | "
                 f"{pct(nm) if nm is not None else '未披露'} | {ratio(dr)} | "
                 f"{fmt(q.get('ocf'))} | {ratio(ncr)} | {fmt(q.get('rd'))} | "
                 f"{pct(rdr) if rdr is not None else '未披露'} |")

    L += ["", "## 表 C 滚动四季（TTM，消除季节性）", "",
          "| 季度 | TTM 收入 | 收入 YoY | TTM 归母 | 归母 YoY | TTM 毛利率 | TTM 净现比 |",
          "|---|---|---|---|---|---|---|"]
    for i, k in enumerate(keys):
        t = ttm(i)
        if not t:
            L.append(f"| {k[0]}Q{k[1]} | — | — | — | — | — | — |")
            continue
        p = ttm(i - 4) if i >= 4 else None
        ry = (t["rev"] / p["rev"] - 1) if (p and p.get("rev")) else None
        ny = (t["net"] / p["net"] - 1) if (p and p.get("net")) else None
        L.append(f"| {k[0]}Q{k[1]} | {fmt(t['rev'])} | "
                 f"{pct(ry) if ry is not None else '—'} | {fmt(t['net'])} | "
                 f"{pct(ny) if ny is not None else '—'} | "
                 f"{pct(t['gm']) if t['gm'] is not None else '未披露'} | {ratio(t['ncr'])} |")

    L += ["", "## 表 D 累计口径（与正式披露对齐）", "",
          "| 年度 | Q1 累计 | H1 累计 | 9M 累计 | FY | FY YoY |", "|---|---|---|---|---|---|"]
    for y in sorted({k[0] for k in keys}):
        vals = [quarters.get((y, i), {}).get("rev") for i in (1, 2, 3, 4)]
        c1, c2, c3, c4 = vals
        h1 = (c1 + c2) if (c1 is not None and c2 is not None) else None
        h9 = sum(vals[:3]) if all(v is not None for v in vals[:3]) else None
        fy = sum(vals) if all(v is not None for v in vals) else None
        prev_fy = cum.get((y - 1, "fy"), {}).get("rev")
        fyoy = (fy / prev_fy - 1) if (fy and prev_fy) else None
        L.append(f"| {y} | {fmt(c1)} | {fmt(h1)} | {fmt(h9)} | {fmt(fy)} | "
                 f"{pct(fyoy) if fyoy is not None else '—'} |")

    L += ["", "## 表 E 季度营运资金", "",
          "| 季度 | 应收账款 | 存货 | 合同负债 | 应收/收入(天) | 存货/成本(天) | 有息负债 |",
          "|---|---|---|---|---|---|---|"]
    for k in keys:
        q = quarters[k]
        rev, cost = q.get("rev"), q.get("cost")
        ard = (q["ar"] / rev * DAYS) if (q.get("ar") is not None and rev) else None
        invd = (q["inv"] / cost * DAYS) if (q.get("inv") is not None and cost) else None
        L.append(f"| {k[0]}Q{k[1]} | {fmt(q.get('ar'))} | {fmt(q.get('inv'))} | "
                 f"{fmt(q.get('contract'))} | {f'{ard:.0f}' if ard is not None else '未披露'} | "
                 f"{f'{invd:.0f}' if invd is not None else '未披露'} | {fmt(q.get('debt'))} |")

    if issues:
        L += ["", "## 校验不一致项", "", "| 年度 | 季度 | 相减值 | 披露值 |", "|---|---|---|---|"]
        for y, qi, a, b in issues[:20]:
            L.append(f"| {y} | Q{qi} | {a/1e6:,.1f} | {b/1e6:,.1f} |")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"OK -> {out}（{len(keys)} 个季度；校验 {checked} 格，不一致 {len(issues)} 格）")


if __name__ == "__main__":
    main()
