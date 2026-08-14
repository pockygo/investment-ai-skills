#!/usr/bin/env python3
"""Validate the compact public-information task list schema."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_COLUMNS = [
    "报告位置",
    "待补充事项",
    "搜索口径/资料要求",
    "证据标准",
    "回填位置",
]

PRIVATE_TERMS = [
    "银行流水",
    "客户PO",
    "PO原件",
    "股转协议",
    "投资协议",
    "劳动合同",
    "员工花名册",
    "供应商采购金额",
]


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("task_list", type=Path)
    args = parser.parse_args()

    if not args.task_list.is_file():
        print(f"ERROR: task list not found: {args.task_list}", file=sys.stderr)
        return 2

    lines = args.task_list.read_text(encoding="utf-8").splitlines()
    header_index = -1
    for index, line in enumerate(lines):
        if line.lstrip().startswith("|") and split_row(line) == REQUIRED_COLUMNS:
            header_index = index
            break

    errors: list[str] = []
    if header_index < 0:
        errors.append("缺少规定的五列表头，或列名/顺序不一致")
    else:
        data_lines: list[str] = []
        for line in lines[header_index + 2 :]:
            if not line.lstrip().startswith("|"):
                if data_lines:
                    break
                continue
            data_lines.append(line)

        if not data_lines:
            errors.append("公开信息任务表没有数据行")

        seen: set[tuple[str, str]] = set()
        for row_number, line in enumerate(data_lines, start=1):
            cells = split_row(line)
            if len(cells) != len(REQUIRED_COLUMNS):
                errors.append(
                    f"第{row_number}条任务列数为{len(cells)}，应为{len(REQUIRED_COLUMNS)}"
                )
                continue

            for column, value in zip(REQUIRED_COLUMNS, cells):
                if not value:
                    errors.append(f"第{row_number}条任务的“{column}”为空")

            key = (cells[0], cells[1])
            if key in seen:
                errors.append(f"任务重复：{cells[0]} / {cells[1]}")
            seen.add(key)

            combined = " ".join(cells)
            for term in PRIVATE_TERMS:
                if term in combined:
                    errors.append(
                        f"第{row_number}条包含非公开尽调事项“{term}”，应移入Word尽调清单"
                    )

    if errors:
        print("PUBLIC TASK LIST VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PUBLIC TASK LIST VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
