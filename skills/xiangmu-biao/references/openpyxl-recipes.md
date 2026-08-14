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
