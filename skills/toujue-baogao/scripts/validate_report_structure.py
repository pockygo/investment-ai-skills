#!/usr/bin/env python3
"""Validate the required structure of a full toujue-baogao Markdown report."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_LITERAL_HEADINGS = [
    "## 01 项目概述",
    "### 1.1 项目概述",
    "### 1.2 公司简介",
    "### 1.3 项目亮点",
    "### 1.4 风险与应对",
    "## 02 项目分析",
    "### 2.1 公司基本信息",
    "### 2.2 组织架构",
    "### 2.3 核心团队",
    "### 2.4 主营业务情况",
    "### 2.5 竞争优势",
    "### 2.6 供应商情况",
    "### 2.7 客户情况",
    "### 2.8 在手订单",
    "### 2.9 财务分析",
    "### 2.10 盈利预测",
    "### 2.11 可比公司",
    "## 03 行业分析",
    "### 3.2 行业政策",
    "### 3.3 行业痛点及驱动因素",
    "### 3.4 产业链情况",
    "### 3.5 市场规模",
    "### 3.6 竞争格局",
    "### 3.7 未来的发展趋势",
    "## 04 决议事项",
    "### 4.1 决议事项",
]

TRANSACTION_FIELDS = [
    "投资主体",
    "投资金额",
    "投前估值",
    "本轮融资总额",
    "本轮其他投资人情况",
    "交易结构",
    "核心条款",
    "退出路径",
]

FINANCIAL_COMPONENTS = ["资产负债表", "利润表", "现金流量表"]
INTERVIEW_FIELDS = ["访谈日期", "访谈对象", "对象背景", "参访人员", "访谈形式"]


def section(text: str, heading_pattern: str, next_level: int = 3) -> str:
    match = re.search(heading_pattern, text, flags=re.MULTILINE)
    if not match:
        return ""
    tail = text[match.end() :]
    next_heading = re.search(rf"^#{{1,{next_level}}}\s", tail, flags=re.MULTILINE)
    return tail[: next_heading.start()] if next_heading else tail


def has_heading(text: str, heading: str) -> bool:
    suffix = r"(?:\s|（|$)"
    return re.search(rf"^{re.escape(heading)}{suffix}", text, flags=re.MULTILINE) is not None


def validate(text: str, require_interviews: bool) -> list[str]:
    errors: list[str] = []

    for heading in REQUIRED_LITERAL_HEADINGS:
        if not has_heading(text, heading):
            errors.append(f"缺少必需章节：{heading}")

    if not re.search(r"^### 3\.1 .+简介\s*$", text, flags=re.MULTILINE):
        errors.append("缺少必需章节：### 3.1 [核心产品或服务]简介")

    for heading in ("### 1.1 项目概述", "### 4.1 决议事项"):
        body = section(text, rf"^{re.escape(heading)}.*$", next_level=3)
        for field in TRANSACTION_FIELDS:
            if not re.search(rf"^\|\s*{re.escape(field)}\s*\|", body, flags=re.MULTILINE):
                errors.append(f"{heading} 缺少交易字段：{field}")

    financial_body = section(text, r"^### 2\.9 财务分析.*$", next_level=3)
    for component in FINANCIAL_COMPONENTS:
        if component not in financial_body:
            errors.append(f"### 2.9 财务分析 缺少：{component}")

    if require_interviews:
        if "## 附录 访谈纪要" not in text:
            errors.append("有访谈材料时必须包含：## 附录 访谈纪要")
        else:
            interview_body = section(text, r"^## 附录 访谈纪要\s*$", next_level=2)
            for field in INTERVIEW_FIELDS:
                if not re.search(rf"^\|\s*{re.escape(field)}\s*\|", interview_body, flags=re.MULTILINE):
                    errors.append(f"访谈附录缺少基础字段：{field}")
            for label in ("纪要核心要点", "访谈评价"):
                if label not in interview_body:
                    errors.append(f"访谈附录缺少：{label}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument(
        "--no-interviews",
        action="store_true",
        help="Allow omission of the interview appendix when no interview materials exist.",
    )
    args = parser.parse_args()

    if not args.report.is_file():
        print(f"ERROR: report not found: {args.report}", file=sys.stderr)
        return 2

    text = args.report.read_text(encoding="utf-8")
    errors = validate(text, require_interviews=not args.no_interviews)
    if errors:
        print("STRUCTURE VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("STRUCTURE VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
