#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把已有第八区的样式归一到规范（默认 dry-run，不改内容）。

默认只做「样式归一」（字体/底纹/边框/数字格式/换行/行高/合计行橙底），
不动任何数值、不改列宽、不改行位置。两项会改到内容的动作需显式开关：

    --apply-totals   合计行 A 补「合计」标签，B/C 改成 =SUM() 公式（数值不变，但从写死变公式）
    --clean-merges   删掉八区内除标题 A:L 以外的多余合并区域（如晋成残留的 E84:F84）

用法：
    PYTHONIOENCODING=utf-8 python normalize_equity_block.py --workbook 项目表.xlsx
    PYTHONIOENCODING=utf-8 python normalize_equity_block.py --workbook 项目表.xlsx \
        --sheets 晋成半导体,盛欣科 --apply-totals --clean-merges --write
"""

import argparse
import sys

import openpyxl
from openpyxl.styles import Border, PatternFill

from _equity_common import (ALIGN_CTR, ALIGN_HDR, ALIGN_LEFT, BORDER, FILL_HEAD,
                            FILL_TITLE, FILL_TOTAL, FMT_AMT, FMT_PCT, FONT_BODY,
                            FONT_HEAD, FONT_TITLE, FONT_TOTAL, _row_height,
                            backup, ensure_writable, scan_block8)


def normalize_sheet(ws, apply_totals=False, clean_merges=False):
    # ws 以 data_only=False 载入：既拿得到公式（识别 =SUM 合计行），也拿得到数值
    info = scan_block8(ws, wsf=ws)
    if info is None:
        return None
    changes = []
    t = info['title']

    # 1) 标题行：合并 A:L + 规范样式
    if str(t) not in {str(m) for m in ws.merged_cells.ranges} and \
       not any(m.min_row == t and m.min_col == 1 and m.max_col == 12 for m in ws.merged_cells.ranges):
        ws.merge_cells(start_row=t, start_column=1, end_row=t, end_column=12)
        changes.append('标题行补 A:L 合并')
    c = ws.cell(t, 1)
    if (c.font.name, c.font.bold, c.font.color.rgb if c.font.color else None) != ('微软雅黑', True, 'FFFFFFFF') or \
       (c.fill.fgColor.rgb or '')[-6:].upper() != '2F5597':
        c.font, c.fill = FONT_TITLE, FILL_TITLE
        changes.append('标题行字体/底纹归一')

    # 2) 表头行
    for h in info['header_rows']:
        for col in range(1, 4):
            cell = ws.cell(h, col)
            if cell.font.name != '微软雅黑' or not cell.font.bold or \
               (cell.fill.fgColor.rgb or '')[-6:].upper() != 'D9E1F2' or cell.border.left.style != 'thin':
                cell.font, cell.fill, cell.alignment, cell.border = FONT_HEAD, FILL_HEAD, ALIGN_HDR, BORDER
        if (ws.row_dimensions[h].height or 0) < 28:
            ws.row_dimensions[h].height = 30
    if len(info['header_rows']) > 1:
        changes.append('⚠ 表头跨 %d 行（规范为单行，脚本不改行结构，需人工决定）' % len(info['header_rows']))

    # 3) 明细行
    for r, a, b, cc in info['data']:
        cell_a, cell_b, cell_c = ws.cell(r, 1), ws.cell(r, 2), ws.cell(r, 3)
        cell_a.font, cell_a.alignment, cell_a.border = FONT_BODY, ALIGN_LEFT, BORDER
        cell_b.font, cell_b.alignment, cell_b.border = FONT_BODY, ALIGN_CTR, BORDER
        cell_c.font, cell_c.alignment, cell_c.border = FONT_BODY, ALIGN_CTR, BORDER
        if cell_b.number_format != FMT_PCT:
            cell_b.number_format = FMT_PCT
        if cell_c.number_format != FMT_AMT:
            cell_c.number_format = FMT_AMT
        need = _row_height(a if isinstance(a, str) else '')
        if (ws.row_dimensions[r].height or 0) < need:
            ws.row_dimensions[r].height = need
    if info['data']:
        changes.append('明细 %d 行样式归一（字体/边框/格式/换行/行高）' % len(info['data']))

    # 4) 合计行
    tr = info['total_row']
    if tr is None:
        changes.append('⚠ 无合计行（需人工补：A=合计，B/C=SUM 公式，橙底）')
    else:
        for col in range(1, 4):
            cell = ws.cell(tr, col)
            cell.font, cell.border = FONT_TOTAL, BORDER
        if (ws.cell(tr, 1).fill.fgColor.rgb or '')[-6:].upper() != 'FCE4D6':
            for col in range(1, 4):
                ws.cell(tr, col).fill = FILL_TOTAL
            changes.append('合计行补橙底 FCE4D6')
        if apply_totals:
            first, last = info['data'][0][0], info['data'][-1][0]
            if not isinstance(ws.cell(tr, 1).value, str) or not ws.cell(tr, 1).value.strip():
                ws.cell(tr, 1, '合计')
                changes.append('合计行补「合计」标签')
            if not (isinstance(ws.cell(tr, 2).value, str) and ws.cell(tr, 2).value.startswith('=')):
                ws.cell(tr, 2, '=SUM(B%d:B%d)' % (first, last))
                changes.append('合计行 B 改 SUM 公式')
            if not (isinstance(ws.cell(tr, 3).value, str) and ws.cell(tr, 3).value.startswith('=')):
                ws.cell(tr, 3, '=SUM(C%d:C%d)' % (first, last))
                changes.append('合计行 C 改 SUM 公式')

    # 5) 多余合并（表头行内的跨行合并属结构问题，保留并另行提示）
    header_span = set()
    for h in info['header_rows']:
        header_span.add(h)
    if clean_merges and info['stray_merges']:
        for m in list(ws.merged_cells.ranges):
            if m.min_row < t:
                continue
            if m.min_row == t and m.min_col == 1 and m.max_col == 12:
                continue
            if m.min_row in header_span or m.max_row in header_span:
                changes.append('⚠ 保留表头内合并 %s（跨行表头需人工改为单行）' % m)
                continue
            ws.unmerge_cells(str(m))
            changes.append('删除多余合并 %s' % m)
    elif info['stray_merges']:
        changes.append('⚠ 多余合并（加 --clean-merges 删除）：%s' % ', '.join(info['stray_merges']))

    return changes


def main():
    ap = argparse.ArgumentParser(description='第八区样式归一（默认 dry-run）')
    ap.add_argument('--workbook', required=True)
    ap.add_argument('--sheets', default='')
    ap.add_argument('--apply-totals', action='store_true',
                    help='合计行补「合计」标签 + SUM 公式')
    ap.add_argument('--clean-merges', action='store_true', help='删除八区内多余合并区域')
    ap.add_argument('--write', action='store_true', help='真正落盘（默认 dry-run）')
    ap.add_argument('--dry-run', action='store_true', help='显式干跑（默认行为，仅为可读性提供）')
    args = ap.parse_args()

    wb = openpyxl.load_workbook(args.workbook)
    wanted = [s.strip() for s in args.sheets.split(',') if s.strip()] or wb.sheetnames
    wsf = openpyxl.load_workbook(args.workbook, data_only=False)

    plan = {}
    for n in wanted:
        ch = normalize_sheet(wb[n], args.apply_totals, args.clean_merges)
        if ch is None:
            print('%-12s 未建八区，跳过' % n)
            continue
        plan[n] = ch
        print('%-12s %s' % (n, '；'.join(ch) if ch else '已符合规范，无改动'))

    acted = [n for n, ch in plan.items() if any(not c.startswith('⚠') for c in ch)]
    if not args.write:
        print('\n[DRY-RUN] 将改动 %d 个 sheet：%s' % (len(acted), ', '.join(acted) if acted else '无'))
        if any('⚠' in c for n in plan for c in plan[n]):
            print('注意：带 ⚠ 的项目脚本不会自动处理（表头跨行/缺合计行/多余合并），需人工或加开关。')
        print('确认后加 --write 落盘（自动备份 .bak-时间戳）。')
        return 0
    if not acted:
        print('\n无需写入。')
        return 0
    b = backup(args.workbook)
    ensure_writable(args.workbook)
    wb.save(args.workbook)
    print('\n[WROTE] 备份：%s' % b)
    print('下一步：PYTHONIOENCODING=utf-8 python validate_workbook.py --workbook %s --strict' % args.workbook)
    return 0


if __name__ == '__main__':
    sys.exit(main())
