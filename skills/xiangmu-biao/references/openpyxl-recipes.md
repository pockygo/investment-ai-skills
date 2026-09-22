# openpyxl 操作代码库（项目表.xlsx 专用）

核心约束：表内有跨区公式（四区 IRR `=B65` 引用七区 XIRR 结果；七区 `=J37` 引用四区；XIRR 区间引用本区行），**严禁 insert_rows / 删行**。以下代码均验证过（2026Q2 批量更新，8 个 sheet 移位+写行）。

## 0. 执行规范

```bash
cp 项目表.xlsx 项目表_backup_$(date +%Y%m%d).xlsx   # 批量修改前必做
PYTHONIOENCODING=utf-8 python _update_script.py      # 脚本写文件执行，不用 python -c 内联
```

不用 `python -c "..."` 的原因：bash 双引号会吞掉 `\$`、`\d` 等反斜杠，正则静默失效；单引号又无法嵌套。一律 Write 成 .py 再跑。

## 1. 全表公式行号修正（移位前置步骤）

在第 R 行插入行前，把全表公式中所有引用行号 >= R 的引用 +1。
同时覆盖两类：位于 R 之下、将随移位的公式（XIRR 区间），和位于 R 之上、引用 R 之下区域的公式（四区 `=B65`）。

```python
import re
ref_re = re.compile(r'(\$?)([A-Z]{1,3})(\$?)(\d{1,4})')

def fix_formulas(ws, R):
    def sub(m):
        rownum = int(m.group(4))
        if rownum >= R:
            return '%s%s%s%d' % (m.group(1), m.group(2), m.group(3), rownum + 1)
        return m.group(0)
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith('='):
                new = ref_re.sub(sub, c.value)
                if new != c.value:
                    c.value = new
```

注意：公式中出现的非引用数字（如 `=181.2612*I24`）因无字母前缀不会被误伤；函数名（XIRR/SUM/IFERROR）无数字也不会匹配。

## 2. 安全移位（R..max_row 下移一行，替代 insert_rows）

```python
from copy import copy

def shift_down(ws, R):
    max_row = ws.max_row
    # 1) 解除起点 >= R 的合并区域并记录（区块标题 A:L、注释行 A:L 都是合并的）
    shifted = []
    for m in list(ws.merged_cells.ranges):
        if m.min_row >= R:
            shifted.append((m.min_row, m.min_col, m.max_row, m.max_col))
            ws.unmerge_cells(str(m))
    # 2) 自底向上复制值+样式+行高（必须先解合并，否则写 MergedCell 报错）
    for r in range(max_row, R - 1, -1):
        for col in range(1, 13):
            src, dst = ws.cell(r, col), ws.cell(r + 1, col)
            dst.value = src.value
            dst._style = copy(src._style)
        if r in ws.row_dimensions:
            ws.row_dimensions[r + 1].height = ws.row_dimensions[r].height
    # 3) 重新合并（+1 行）
    for (r1, c1, r2, c2) in shifted:
        ws.merge_cells(start_row=r1 + 1, start_column=c1,
                       end_row=r2 + 1, end_column=c2)
```

调用顺序：`fix_formulas(ws, R)` → `shift_down(ws, R)` → `write_row(...)`。移位后原 R 行残留旧内容副本，由 write_row 整行覆盖。

## 3. 写入新行（样式复制自上一行）

```python
from copy import copy
from openpyxl.utils import get_column_letter

def write_row(ws, R, vals):  # vals: {'A':..,'B':..,...'J':..}，缺省列写 None
    for col in range(1, 13):
        letter = get_column_letter(col)
        above, cell = ws.cell(R - 1, col), ws.cell(R, col)
        cell._style = copy(above._style)   # 边框/数字格式/字体随行复制
        cell.value = vals.get(letter)
    if (R - 1) in ws.row_dimensions:
        ws.row_dimensions[R].height = ws.row_dimensions[R - 1].height
```

若目标空白行存在整行合并（蔚谱案例：空白间隔行被合并 A:L），先 `ws.unmerge_cells` 再写。

## 4. 写后校验脚本（改完必跑）

```python
import openpyxl
from openpyxl.utils import get_column_letter
wb = openpyxl.load_workbook('项目表.xlsx')
for name in 改动sheet列表:
    ws = wb[name]
    # a) 六区标题起到表尾的全部非空单元格
    # b) 全部公式单元格（isinstance(v,str) and v.startswith('=')）
    # c) 新行样式抽查：cell.border.left.style=='thin'、
    #    number_format in ('#,##0.00','0.00%')、font.name=='微软雅黑'
    # d) 合并区域：[str(m) for m in ws.merged_cells.ranges if m.min_row >= 新行号]
```

人工核对点：四区 IRR 引用已 +1、XIRR 区间已 +1、七区 `=J37` 类引用四区的公式行号不变、注释行文本随移位到位。

## 5. 数字格式速查

- 金额：`'#,##0.00'`；百分比：`'0.00%'`；**日期：`'yyyy/m/d'`（短日期，用户明确要求，禁用 yyyy-mm-dd 长格式）**
- 写日期用 `datetime.date` 对象 + number_format `'yyyy/m/d'`，不要写字符串
- openpyxl 读到的已有日期是 `datetime.datetime`，判断显示格式看 number_format 而非值

## 6. 财报 PDF 文本量检测（决定提取路径）

```python
import fitz
doc = fitz.open(f)
total = sum(len(p.get_text()) for p in doc)   # ≈0 → 扫描件，渲染图片走子代理
```

扫描件渲染：`page.get_pixmap(matrix=fitz.Matrix(3, 3))` 存 PNG，ReadMediaFile 阅读，关键区域用 region 裁切放大。

## 7. 表尾追加区块（第八区「最新股权结构」专用）

八区永远追加在七区之后，**这是唯一不需要 `fix_formulas` / `shift_down` 的操作**：上方单元格与公式引用完全不受影响（2026-09-22 实测，八区落地后 ①–⑦ 区与旧版逐格 diff = 0）。所以不要习惯性地先跑移位算法。

```python
from copy import copy
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

FONT_T = Font(name='微软雅黑', size=11, bold=True, color='FFFFFFFF')
FONT_H = Font(name='微软雅黑', size=10, bold=True)
FONT_B = Font(name='微软雅黑', size=10)
FILL_T, FILL_H, FILL_TOT = '2F5597', 'D9E1F2', 'FCE4D6'
side = Side(style='thin', color='999999')
BD = Border(left=side, right=side, top=side, bottom=side)
CTR = Alignment(horizontal='center', vertical='center', wrap_text=True)
LFT = Alignment(horizontal='left', vertical='center', wrap_text=True)

def append_equity_block(ws, rows, title='八、最新股权结构',
                        header=('股东（发起人）', '持股比例', '认缴出资额（万元）'),
                        note=None, height=32.0):
    """rows: [(股东, 比例float, 金额float)]，已按比例降序。返回 (标题行, 合计行)。"""
    start = ws.max_row + 2                     # 末行后空 1 行
    ws.merge_cells(start_row=start, start_column=1, end_row=start, end_column=12)
    c = ws.cell(start, 1, title); c.font = FONT_T
    c.fill = PatternFill('solid', fgColor=FILL_T)
    c.alignment = Alignment(horizontal='left', vertical='center')
    ws.row_dimensions[start].height = 20
    r = start + 1
    for i, h in enumerate(header, 1):          # 表头：单行，不跨行合并
        cell = ws.cell(r, i, h); cell.font = FONT_H
        cell.fill = PatternFill('solid', fgColor=FILL_H)
        cell.alignment = CTR; cell.border = BD
    ws.row_dimensions[r].height = 30
    if note:                                   # 注释行：9 号灰字，说明来源/基准日/口径
        r += 1
        nc = ws.cell(r, 1, note)
        nc.font = Font(name='微软雅黑', size=9, color='808080')
        ws.row_dimensions[r].height = 22
    first = r + 1
    for name, pct, amt in rows:
        r += 1
        for col, val, f, al in ((1, name, 'General', LFT),
                                (2, pct, '0.0000%', CTR),
                                (3, amt, '#,##0.00', CTR)):
            cell = ws.cell(r, col, val)
            cell.font = FONT_B; cell.border = BD
            cell.alignment = al; cell.number_format = f
        ws.row_dimensions[r].height = height   # A 列 wrap 需要行高
    r += 1                                     # 合计行：SUM 公式 + 橙底，禁止写死数值
    ws.cell(r, 1, '合计')
    ws.cell(r, 2, f'=SUM(B{first}:B{r-1})')
    ws.cell(r, 3, f'=SUM(C{first}:C{r-1})')
    for col in range(1, 4):
        cell = ws.cell(r, col)
        cell.font = Font(name='微软雅黑', size=10, bold=True)
        cell.fill = PatternFill('solid', fgColor=FILL_TOT)
        cell.border = BD
        cell.number_format = '0.0000%' if col == 2 else ('#,##0.00' if col == 3 else 'General')
    # 合计行样式收尾：A/B/C 之外的列补边框可不做，八区只用 A:C
    return start, r
```

追加后必查：

1. `ΣC == 一区「注册资本（万元）」C16`、`ΣB == 100%`（容差 1e-5）；
2. 我方基金/其 SPV 行与②区「当前持股比例」能对上（差异必须在注释里写明穿透关系）;
3. 八区内部增删股东行时，只有本区行号变动——但 `=SUM(B首:B末)` 区间必须同步（`fix_formulas(ws, R)` 会连带修正区间，可复用）；
4. 若是给**尚无八区**的 sheet 追加，末行可能是注释行或七区 XIRR 行——一律 `start = ws.max_row + 2`，不要覆盖末行。

