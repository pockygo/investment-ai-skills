#!/usr/bin/env python3
"""生成 timeseries/财务时间序列.md（固定 schema：17 项指标 + 年份）。

数据源：extracts/fin_all.csv（parse_tables.py 产出）。
可选输入：extracts/dividends.csv（现金分红）、extracts/segments.csv（分产品）。
缺文件时对应列写「未披露」，不阻断生成。

用法: python3 scripts/annual_series.py --out timeseries/财务时间序列.md
"""
import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path

DIVIDEND_CSV = "extracts/dividends.csv"   # year,dps_per_10,shares,note,source
SEGMENT_CSV = "extracts/segments.csv"     # period,product,revenue_m,share_pct,yoy_pct,gm_pct,note


def load_dividends(path):
    p = Path(path)
    if not p.exists():
        return {}
    out = {}
    for r in csv.DictReader(p.open(encoding="utf-8-sig")):
        try:
            out[int(r["year"])] = (float(r["dps_per_10"]), int(r["shares"]),
                                   r.get("note", ""), r.get("source", ""))
        except (KeyError, ValueError):
            continue
    return out


def load_segments(path):
    p = Path(path)
    if not p.exists():
        return {}
    out = defaultdict(list)
    for r in csv.DictReader(p.open(encoding="utf-8-sig")):
        out[int(r["period"])].append(r)
    return out


def num(s):
    s = (s or "").replace(",", "").strip()
    if not s or s in {"—", "-", "–"}:
        return None
    pct = s.endswith("%")
    neg = s.startswith("(") or s.startswith("（") or s.startswith("-")
    s = s.strip("()-—–（）%")
    try:
        v = float(s)
    except ValueError:
        return None
    return (v if not neg else -v) if not pct else v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extracts", default="extracts")
    ap.add_argument("--out", default="timeseries/财务时间序列.md")
    ap.add_argument("--dividends", default=DIVIDEND_CSV)
    args = ap.parse_args()

    rows = list(csv.DictReader(open(Path(args.extracts) / "fin_all.csv", encoding="utf-8-sig")))
    DIVIDEND = load_dividends(args.dividends)
    SEGMENTS = load_segments(SEGMENT_CSV)
    kpi_rows = defaultdict(list)
    for r in rows:
        if r["statement"] == "主要会计数据" and r["period"].startswith("fy"):
            kpi_rows[r["period"]].append((r["item"], num(r["v1"]), num(r["v2"]), num(r["v3"])))

    SKIP = ("每股收益", "收益率", "资产总额", "净资产", "净资", "调整", "优先股", "永续债")
    kpi = defaultdict(dict)
    for p, rs in kpi_rows.items():
        seq = [(n, v1, v3) for n, v1, _, v3 in rs if not any(k in n for k in SKIP) and v1 is not None]
        if len(seq) < 4:
            continue
        # 指标名常被折行截断，按 KPI 表固定顺序取：收入、归母、扣非、经营现金流
        kpi[p] = {"rev": seq[0][1], "net": seq[1][1], "ded": seq[2][1], "ocf": seq[3][1],
                  "yoy_rev": (seq[0][2] or 0) / 100 or None,
                  "yoy_net": (seq[1][2] or 0) / 100 or None}
        for n, v1, _v2, v3 in rs:                 # ROE 行被 SKIP 排除，单独扫
            if "净资产收益" in n and v1 is not None:
                kpi[p]["roe"] = v1

    tabs = defaultdict(dict)
    for r in rows:
        p, s, item = r["period"], r["statement"], r["item"]
        if not p.startswith("fy"):
            continue
        v = num(r["v1"])
        if s == "合并利润表":
            if item in ("其中：营业成本", "营业成本"):
                tabs[p]["cost"] = v
            if item == "研发费用":
                tabs[p]["rd"] = v
        elif s == "合并资产负债表":
            if item == "存货":
                tabs[p]["inv"] = v
            if item == "应收账款":
                tabs[p]["ar"] = v
            if item in ("短期借款", "长期借款", "一年内到期的非流动负债"):
                tabs[p]["debt"] = (tabs[p].get("debt") or 0) + (v or 0)
            if item == "股本":
                tabs[p]["shares"] = v
        elif s == "合并现金流量表" and "购建固定资产" in item:
            tabs[p]["capex"] = v

    # 缺失年份用下一年年报现金流量表的「上期数」回填（同口径，来源标注在报告脚注）
    for r in rows:
        p, s, item = r["period"], r["statement"], r["item"]
        if not p.startswith("fy") or s != "合并现金流量表" or "购建固定资产" not in item:
            continue
        y = int(p[2:]) - 1
        if tabs.get(f"fy{y}") is not None and tabs[f"fy{y}"].get("capex") is None:
            tabs[f"fy{y}"]["capex"] = num(r["v2"])

    years = sorted(int(p[2:]) for p in kpi)
    prev_rev = prev_net = None
    out = ["# 财务时间序列", "",
           f"> 数据区间：{years[0]}–{years[-1]}；单位：百万元；生成日期：见文件属性。",
           "> 口径：年报口径，2025 年报为最新一期；金额取合并报表。",
           "", "## 表 A 核心财务序列", "",
           "| 年份 | 营业收入 | 收入YoY | 归母净利 | 净利YoY | 扣非归母 | 综合毛利率 | 净利率 "
           "| ROE(加权) | 经营现金流净额 | 净现比 | CAPEX | CAPEX/收入 | 存货 | 应收账款 "
           "| 有息负债 | 现金分红 | 研发投入占比 |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for y in years:
        p = f"fy{y}"
        k, t = kpi[p], tabs[p]
        rev, net, ded, ocf = k.get("rev"), k.get("net"), k.get("ded"), k.get("ocf")
        cost, rd = t.get("cost"), t.get("rd")
        gm = (1 - cost / rev) if (cost and rev) else None
        nm = (net / rev) if (net and rev) else None
        ncr = (ocf / net) if (ocf and net) else None
        capex = t.get("capex")
        div_ps, base, _, _ = DIVIDEND.get(y, (None, None, "", ""))
        shares = base or t.get("shares")
        div = (div_ps / 10 * shares) if (div_ps and shares) else None

        def f(v, d=1):
            return "未披露" if v is None else f"{v/1e6:,.{d}f}"

        def pc(v):
            return "未披露" if v is None else f"{v*100:.1f}%"

        def rt(v):
            return "未披露" if v is None else f"{v:.2f}"

        yoy_r = (rev / prev_rev - 1) if (rev and prev_rev) else (k.get("yoy_rev") or None)
        yoy_n = (net / prev_net - 1) if (net and prev_net) else (k.get("yoy_net") or None)
        out.append(
            f"| {y} | {f(rev)} | {pc(yoy_r)} | {f(net)} | {pc(yoy_n)} | {f(ded)} | {pc(gm)} | "
            f"{pc(nm)} | {pc((k.get('roe') or 0)/100) if k.get('roe') else '未披露'} | {f(ocf)} | "
            f"{rt(ncr)} | {f(capex)} | {pc(capex/rev if (capex and rev) else None)} | "
            f"{f(t.get('inv'))} | {f(t.get('ar'))} | {f(t.get('debt'))} | {f(div)} | "
            f"{pc(rd/rev if (rd and rev) else None)} |")
        prev_rev, prev_net = rev or prev_rev, net or prev_net

    out += ["", "## 表 B 分产品收入（口径变更时分段列示）", "",
            "| 期间 | 产品 | 收入 | 占比 | YoY | 毛利率 | 口径 |",
            "|---|---|---|---|---|---|---|"]
    for y in sorted(SEGMENTS):
        for s in SEGMENTS[y]:
            gm = s.get("gm_pct") or ""
            out.append(f"| {y} | {s['product']} | {float(s['revenue_m']):,.1f} | "
                       f"{float(s['share_pct']):.2f}% | {float(s['yoy_pct']):+.2f}% | "
                       f"{gm + '%' if gm else '未披露'} | {s.get('note','')} |")

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"OK -> {outp}（{len(years)} 年，分红 {len(DIVIDEND)} 年，分产品 {len(SEGMENTS)} 年）")


if __name__ == "__main__":
    main()
