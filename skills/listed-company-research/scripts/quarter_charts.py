#!/usr/bin/env python3
"""季度经营面板（2×2）：单季营收、单季净利、单季毛利率、TTM 营收。

复用 quarterly.py 的解析结果，保证与 timeseries/季度财务面板.md 同源。
依赖 matplotlib；中文字体按 STHeiti / Songti SC / Arial Unicode MS 回退。

用法: python3 scripts/quarter_charts.py --company 三环集团 --out report/charts
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import quarterly as Q  # noqa: E402

plt.rcParams["font.sans-serif"] = ["STHeiti", "Songti SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["svg.fonttype"] = "path"

YEAR_COLORS = {2020: "#c9d6e3", 2021: "#a8bfd6", 2022: "#7f9fbe",
               2023: "#5c7f9e", 2024: "#3f6480", 2025: "#2b4c66", 2026: "#c8553d"}
LINE = "#1f6f8b"
ACCENT = "#c8553d"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extracts", default="extracts")
    ap.add_argument("--out", default="report/charts")
    ap.add_argument("--expected-quarters", type=Path, help="源文件逐季清单 quarter,status,source,page,reason")
    ap.add_argument("--company", default="", help="公司简称，用于图标题")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    kpi, qdis, stmt = Q.load(Path(args.extracts) / "fin_all.csv")
    quarters, cum, warnings = Q.build(kpi, stmt)
    inventory_path = args.expected_quarters or Path(args.extracts) / "quarter_coverage.csv"
    if args.expected_quarters and not inventory_path.exists():
        raise SystemExit(f"缺少季度清单: {inventory_path}")
    inventory = list(csv.DictReader(inventory_path.open(encoding="utf-8-sig"))) if inventory_path.exists() else []
    expected = {}
    for row in inventory:
        m = re.fullmatch(r"(\d{4})Q([1-4])", row.get("quarter", ""))
        if not m:
            raise SystemExit(f"无效季度: {row.get('quarter')}")
        k = int(m[1]), int(m[2])
        if k in expected:
            raise SystemExit(f"季度清单重复: {row['quarter']}")
        if row.get("status") not in ("available", "unavailable"):
            raise SystemExit(f"{row['quarter']}: status须为available/unavailable")
        if row["status"] == "available" and k not in quarters:
            raise SystemExit(f"已有季度未提取入图: {row['quarter']}")
        if row["status"] == "unavailable" and not row.get("reason", "").strip():
            raise SystemExit(f"{row['quarter']}: 缺失季度须说明原因")
        if row["status"] == "unavailable" and k in quarters:
            raise SystemExit(f"{row['quarter']}: 清单标未提供，但已提取到数据，请核实")
        expected[k] = row
    if expected and set(quarters) - set(expected):
        raise SystemExit("源文件清单漏列已提取季度，请补齐quarter_coverage.csv")
    all_keys = set(quarters) | set(expected)
    if not all_keys:
        raise SystemExit("没有可绘制季度")
    first, last = min(all_keys), max(all_keys)
    keys = [(n//4, n%4+1) for n in range(first[0]*4+first[1]-1, last[0]*4+last[1])]
    for k in keys:
        quarters.setdefault(k, {})
    year_colors = {y: YEAR_COLORS.get(y, plt.get_cmap("tab20")(i % 20))
                   for i, y in enumerate(sorted({k[0] for k in keys}))}

    rev = [quarters[k]["rev"] / 1e6 if quarters[k].get("rev") is not None else float("nan") for k in keys]
    net = [quarters[k]["net"] / 1e6 if quarters[k].get("net") is not None else float("nan") for k in keys]
    gm = []
    for k in keys:
        q = quarters[k]
        gm.append((1 - q["cost"] / q["rev"]) * 100 if q.get("cost") is not None and q.get("rev") else None)
    ttm = []
    for key in keys:
        values = Q.ttm_values(quarters, key)
        ttm.append(values["rev"] / 1e6 if values and values["rev"] is not None else None)

    def yoy(series):
        out_ = []
        for i, (y, q) in enumerate(keys):
            prev = quarters.get((y - 1, q))
            cur = quarters[(y, q)]
            a = cur.get("rev" if series is rev else "net")
            b = prev.get("rev" if series is rev else "net") if prev else None
            out_.append((a / b - 1) * 100 if a is not None and b else None)
        return out_

    yoy_rev, yoy_net = yoy(rev), yoy(net)
    labels = [f"{y}Q{q}" for y, q in keys]
    x = list(range(len(keys)))

    fig, axes = plt.subplots(2, 2, figsize=(max(14, len(keys) * 0.43), 10), dpi=200, sharex=True)
    company = f"{args.company} " if args.company else ""
    fig.suptitle(f"{company}季度经营面板（{labels[0]}至{labels[-1]}）", fontsize=15,
                 x=0.012, ha="left", y=0.985)

    def year_bands(ax):
        years = [k[0] for k in keys]
        starts = {}
        for i, y in enumerate(years):
            starts.setdefault(y, i)
        for j, (y, s) in enumerate(sorted(starts.items())):
            e = max(i for i, yy in enumerate(years) if yy == y)
            if j % 2 == 0:
                ax.axvspan(s - 0.5, e + 0.5, color="#f2f5f8", zorder=0, linewidth=0)

    def style(ax, ylabel, title):
        ax.set_title(title, fontsize=13, loc="left", pad=9)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(axis="y", color="#e8e8e8", linewidth=0.8, zorder=0)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(axis="both", labelsize=9.5)

    # ① 单季营收 + 同比
    ax = axes[0][0]
    ax.bar(x, rev, color=[year_colors[y] for y, _ in keys], width=0.72, zorder=2)
    style(ax, "百万元", "① 单季营业收入（柱）与同比（线）")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.margins(y=0.15)
    axb = ax.twinx()
    xs = [i for i, v in enumerate(yoy_rev) if v is not None]
    axb.plot(x, [v if v is not None else float("nan") for v in yoy_rev], color=LINE, lw=1.6, marker="o", ms=2.6, zorder=5)
    axb.axhline(0, color="#aaa", lw=0.7, ls="--")
    if xs:
        axb.set_ylim(min(yoy_rev[i] for i in xs) - 12, max(yoy_rev[i] for i in xs) + 18)
    axb.tick_params(labelsize=9)
    axb.text(0.015, 0.94, "线=同比（右轴 %）", transform=axb.transAxes, fontsize=9,
             color=LINE, va="top")
    axb.spines["top"].set_visible(False)
    ax.annotate(f"{rev[-1]:,.0f}", (len(keys) - 1, rev[-1]), textcoords="offset points",
                xytext=(-4, 6), ha="right", fontsize=9, color="#333", fontweight="bold")

    # ② 单季净利 + 同比
    ax = axes[0][1]
    ax.bar(x, net, color=[year_colors[y] for y, _ in keys], width=0.72, zorder=2)
    style(ax, "百万元", "② 单季归母净利润（柱）与同比（线）")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.margins(y=0.15)
    axb = ax.twinx()
    xs = [i for i, v in enumerate(yoy_net) if v is not None]
    axb.plot(x, [v if v is not None else float("nan") for v in yoy_net], color=LINE, lw=1.6, marker="o", ms=2.6, zorder=5)
    axb.axhline(0, color="#aaa", lw=0.7, ls="--")
    if xs:
        axb.set_ylim(min(yoy_net[i] for i in xs) - 15, max(yoy_net[i] for i in xs) + 22)
    axb.tick_params(labelsize=9)
    axb.text(0.015, 0.94, "线=同比（右轴 %）", transform=axb.transAxes, fontsize=9,
             color=LINE, va="top")
    axb.spines["top"].set_visible(False)
    ax.annotate(f"{net[-1]:,.0f}", (len(keys) - 1, net[-1]), textcoords="offset points",
                xytext=(-4, 6), ha="right", fontsize=9, color="#333", fontweight="bold")

    # ③ 单季毛利率
    ax = axes[1][0]
    year_bands(ax)
    style(ax, "毛利率 %", "③ 单季毛利率")
    vx = [i for i, v in enumerate(gm) if v is not None]
    vy = [gm[i] for i in vx]
    ax.plot(x, [v if v is not None else float("nan") for v in gm], color=ACCENT, lw=1.8, marker="o", ms=3, zorder=4)
    # 不填充：年份色带已在背景，再填一层会让谷底不清晰
    ax.margins(y=0.15)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.1f}%"))
    if vy:
        imin = vy.index(min(vy))
        ax.annotate(f"谷底 {vy[imin]:.1f}%", (vx[imin], vy[imin]), textcoords="offset points",
                    xytext=(6, -14), fontsize=9.5, color="#8a3a2a")
        ax.annotate(f"{vy[-1]:.1f}%", (vx[-1], vy[-1]), textcoords="offset points",
                    xytext=(-6, 10), ha="right", fontsize=10, color=ACCENT, fontweight="bold")
    else:
        ax.text(.5, .5, "未提供单季毛利率，详见逐季数据表", transform=ax.transAxes, ha="center")

    # ④ TTM 营收
    ax = axes[1][1]
    year_bands(ax)
    style(ax, "百万元", "④ TTM 营业收入（滚动四季）")
    vx = [i for i, v in enumerate(ttm) if v is not None]
    vy = [ttm[i] for i in vx]
    ax.plot(x, [v if v is not None else float("nan") for v in ttm], color=LINE, lw=2.0, marker="o", ms=3, zorder=4)
    if vy:
        ax.fill_between(x, [v if v is not None else float("nan") for v in ttm], min(vy) * 0.9, color=LINE, alpha=0.10, zorder=1)
    ax.margins(y=0.15)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    if vy:
        ax.annotate(f"{vy[-1]:,.0f}", (vx[-1], vy[-1]), textcoords="offset points",
                    xytext=(-6, 10), ha="right", fontsize=10, color=LINE, fontweight="bold")
    else:
        ax.text(.5, .5, "不足连续四季或资料缺失，TTM无法计算", transform=ax.transAxes, ha="center")

    tick_idx = list(range(len(keys)))  # 每一季度均保留位置与标签
    for ax in axes.flat:
        ax.tick_params(labelbottom=True)
        ax.set_xticks(tick_idx)
        ax.set_xticklabels([labels[i] for i in tick_idx], rotation=65, ha="right", fontsize=8)

    handles = [plt.Rectangle((0, 0), 1, 1, color=year_colors[y])
               for y in sorted({k[0] for k in keys})]
    fig.legend(handles, [str(y) for y in sorted({k[0] for k in keys})], loc="upper right",
               ncol=7, frameon=False, fontsize=10, title="年份", title_fontsize=10,
               bbox_to_anchor=(0.995, 0.975))
    fig.text(0.012, 0.012,
             f"数据：各期定期报告；单季=累计差额；完整展示{len(keys)}季，不删除异常同比。"
             "空位为未提供/不可计算；具体原因及逐季数值见quarterly_panel_data.csv。",
             fontsize=9, color="#666")
    fig.tight_layout(rect=(0, 0.06, 1, 0.94))

    png, svg = out / "quarterly_panel.png", out / "quarterly_panel.svg"
    fig.savefig(png, bbox_inches="tight")
    fig.savefig(svg, bbox_inches="tight")
    fields = ["quarter", "revenue_m", "revenue_yoy_pct", "parent_profit_m", "parent_yoy_pct", "gross_margin_pct", "ttm_revenue_m", "missing_reason"]
    data_rows = []
    for i, k in enumerate(keys):
        q = quarters[k]
        row = dict(zip(fields[:-1], [f"{k[0]}Q{k[1]}", q.get("rev")/1e6 if q.get("rev") is not None else None,
                    yoy_rev[i], q.get("net")/1e6 if q.get("net") is not None else None, yoy_net[i], gm[i], ttm[i]]))
        missing = [field for field in fields[1:-1] if row[field] is None]
        reasons = {"revenue_m": "收入缺失，须核查来源", "parent_profit_m": "归母缺失，须核查来源",
                   "gross_margin_pct": "成本或收入缺失/分母为零，毛利率无法计算",
                   "revenue_yoy_pct": "无可比收入/基数为零或资料缺失，同比无法计算",
                   "parent_yoy_pct": "无可比归母/基数为零或资料缺失，同比无法计算",
                   "ttm_revenue_m": "不足连续四季或收入缺失，TTM无法计算"}
        row["missing_reason"] = "; ".join(filter(None, [expected.get(k, {}).get("reason", ""),
                 "待核查：清单未明确本季度" if k not in expected and not q else ""] + [reasons[field] for field in missing]))
        data_rows.append(row)
    with (out / "quarterly_panel_data.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader(); writer.writerows(data_rows)
    manifest = {"source_inventory_provided": bool(inventory), "quarter_count": len(keys),
                "quarters": [r["quarter"] for r in data_rows],
                "missing_by_metric": {f: [r["quarter"] for r in data_rows if r[f] is None] for f in fields[1:-1]},
                "extraction_warnings": warnings, "scope": "逐季覆盖检查；指标原文语义与未提供原因仍须核验"}
    (out / "quarterly_panel_coverage.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    plt.close(fig)
    print(f"已生成 PNG/SVG、逐季数据CSV及覆盖JSON：{len(keys)}季，{keys[0]}至{keys[-1]}")
    if not inventory:
        print("未提供独立季度清单，尚未验证源文件季度覆盖完整性。")



if __name__ == "__main__":
    main()
