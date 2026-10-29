#!/usr/bin/env python3
"""季度经营面板（2×2）：单季营收、单季净利、单季毛利率、TTM 营收。

复用 quarterly.py 的解析结果，保证与 timeseries/季度财务面板.md 同源。
依赖 matplotlib；中文字体按 STHeiti / Songti SC / Arial Unicode MS 回退。

用法: python3 scripts/quarter_charts.py --company 三环集团 --out report/charts
"""
import argparse
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
    ap.add_argument("--company", default="", help="公司简称，用于图标题")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    kpi, qdis, stmt = Q.load(Path(args.extracts) / "fin_all.csv")
    quarters, cum, _ = Q.build(kpi, stmt)
    keys = sorted(quarters)

    rev = [quarters[k]["rev"] / 1e6 for k in keys]
    net = [(quarters[k].get("net") or 0) / 1e6 for k in keys]
    gm = []
    for k in keys:
        q = quarters[k]
        gm.append((1 - q["cost"] / q["rev"]) * 100 if q.get("cost") and q.get("rev") else None)
    ttm = [None] * len(keys)
    for i in range(3, len(keys)):
        win = [quarters[keys[j]] for j in range(i - 3, i + 1)]
        ttm[i] = sum(w["rev"] for w in win) / 1e6

    def yoy(series):
        out_ = []
        for i, (y, q) in enumerate(keys):
            prev = quarters.get((y - 1, q))
            cur = quarters[(y, q)]
            a = cur.get("rev" if series is rev else "net")
            b = prev.get("rev" if series is rev else "net") if prev else None
            out_.append((a / b - 1) * 100 if a and b else None)
        return out_

    yoy_rev, yoy_net = yoy(rev), yoy(net)
    labels = [f"{str(y)[2:]}Q{q}" for y, q in keys]
    x = list(range(len(keys)))
    skip = labels.index("21Q1") if "21Q1" in labels else -1

    fig, axes = plt.subplots(2, 2, figsize=(12.4, 8.8), dpi=200, sharex=True)
    company = f"{args.company} " if args.company else ""
    fig.suptitle(f"{company}季度经营面板（{labels[0][:2]}Q{labels[0][-1]}–{labels[-1][:2]}Q{labels[-1][-1]}）", fontsize=15,
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
    ax.bar(x, rev, color=[YEAR_COLORS[y] for y, _ in keys], width=0.72, zorder=2)
    style(ax, "百万元", "① 单季营业收入（柱）与同比（线）")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.set_ylim(0, max(rev) * 1.18)
    axb = ax.twinx()
    xs = [i for i, v in enumerate(yoy_rev) if v is not None and i > skip]
    axb.plot(xs, [yoy_rev[i] for i in xs], color=LINE, lw=1.6, marker="o", ms=2.6, zorder=5)
    axb.axhline(0, color="#aaa", lw=0.7, ls="--")
    axb.set_ylim(min(yoy_rev[i] for i in xs) - 12, max(yoy_rev[i] for i in xs) + 18)
    axb.tick_params(labelsize=9)
    axb.text(0.015, 0.94, "线=同比（右轴 %）", transform=axb.transAxes, fontsize=9,
             color=LINE, va="top")
    axb.spines["top"].set_visible(False)
    ax.annotate(f"{rev[-1]:,.0f}", (len(keys) - 1, rev[-1]), textcoords="offset points",
                xytext=(-4, 6), ha="right", fontsize=9, color="#333", fontweight="bold")

    # ② 单季净利 + 同比
    ax = axes[0][1]
    ax.bar(x, net, color=[YEAR_COLORS[y] for y, _ in keys], width=0.72, zorder=2)
    style(ax, "百万元", "② 单季归母净利润（柱）与同比（线）")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.set_ylim(0, max(net) * 1.18)
    axb = ax.twinx()
    xs = [i for i, v in enumerate(yoy_net) if v is not None and i > skip]
    axb.plot(xs, [yoy_net[i] for i in xs], color=LINE, lw=1.6, marker="o", ms=2.6, zorder=5)
    axb.axhline(0, color="#aaa", lw=0.7, ls="--")
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
    ax.plot(vx, vy, color=ACCENT, lw=1.8, marker="o", ms=3, zorder=4)
    # 不填充：年份色带已在背景，再填一层会让谷底不清晰
    ax.set_ylim(35, max(vy) + 4)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    imin = vy.index(min(vy))
    ax.annotate(f"谷底 {vy[imin]:.1f}%", (vx[imin], vy[imin]), textcoords="offset points",
                xytext=(6, -14), fontsize=9.5, color="#8a3a2a")
    ax.annotate(f"{vy[-1]:.1f}%", (vx[-1], vy[-1]), textcoords="offset points",
                xytext=(-6, 10), ha="right", fontsize=10, color=ACCENT, fontweight="bold")

    # ④ TTM 营收
    ax = axes[1][1]
    year_bands(ax)
    style(ax, "百万元", "④ TTM 营业收入（滚动四季）")
    vx = [i for i, v in enumerate(ttm) if v is not None]
    vy = [ttm[i] for i in vx]
    ax.plot(vx, vy, color=LINE, lw=2.0, marker="o", ms=3, zorder=4)
    ax.fill_between(vx, vy, min(vy) * 0.9, color=LINE, alpha=0.10, zorder=1)
    ax.set_ylim(min(vy) * 0.88, max(vy) * 1.08)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.annotate(f"{vy[-1]:,.0f}", (vx[-1], vy[-1]), textcoords="offset points",
                xytext=(-6, 10), ha="right", fontsize=10, color=LINE, fontweight="bold")

    tick_idx = list(range(0, len(keys), 2))          # 隔一个标一次，避免 26 个标签挤在一起
    for ax in axes[1]:
        ax.set_xticks(tick_idx)
        ax.set_xticklabels([labels[i] for i in tick_idx], rotation=45, ha="right", fontsize=9)
    for ax in axes[0]:
        ax.tick_params(labelbottom=False, bottom=False)

    handles = [plt.Rectangle((0, 0), 1, 1, color=YEAR_COLORS[y])
               for y in sorted({k[0] for k in keys})]
    fig.legend(handles, [str(y) for y in sorted({k[0] for k in keys})], loc="upper right",
               ncol=7, frameon=False, fontsize=10, title="年份", title_fontsize=10,
               bbox_to_anchor=(0.995, 0.975))
    fig.text(0.012, 0.012,
             "数据：各期定期报告；单季=累计差额；毛利率=1−营业成本/营业收入；TTM=滚动四季之和。"
             "2020 年无上年同期，同比留空；2021Q1 同比（营收 +117.6%、净利 +165.3%）"
             "受 2020Q1 疫情低基数影响未入图。",
             fontsize=9.6, color="#666")
    fig.tight_layout(rect=(0, 0.03, 1, 0.94))

    png, svg = out / "quarterly_panel.png", out / "quarterly_panel.svg"
    fig.savefig(png, bbox_inches="tight")
    fig.savefig(svg, bbox_inches="tight")
    print(f"OK -> {png} / {svg}")
    print(f"   26 季：营收 {rev[0]:,.0f}→{rev[-1]:,.0f}；净利 {net[0]:,.0f}→{net[-1]:,.0f}；"
          f"毛利率 {gm[0]:.1f}%→{gm[-1]:.1f}%；TTM {ttm[-1]:,.0f}")


if __name__ == "__main__":
    main()
