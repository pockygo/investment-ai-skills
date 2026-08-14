---
name: investment-recommendation-docx
description: Create or update Chinese investment recommendation documents（投资建议书）from a retained Word/DOCX template and source investment materials in PPTX, PDF, DOCX, XLSX, or image form. Use when Codex must preserve a reference investment memo's fonts, colors, headers, footers, tables, and chapter framework; transfer source text and tables into editable Word content with high fidelity; insert product, technology, market-size, or financial visuals in the corresponding chapters; and render-verify the final DOCX. Also use for requests such as“按投决PPT写投资建议书”“以这个Word为模板”“把项目报告转成投资建议书”或“不要截图，要可编辑文字和表格”。
---

# 投资建议书生成

将 Word 模板视为格式权威，将 PPTX/PDF 等材料视为内容权威。输出可编辑、可核验的投资建议书，不把整页幻灯片或报告页面截图塞入 Word。

## 必须配合的技能

- 涉及 DOCX 时，先完整阅读并遵循 `documents` Skill，尤其是模板提炼、创建和逐页渲染验收要求。
- 涉及 PPTX 时，先完整阅读并遵循 `presentations` Skill；读取已有 PPTX 可解析 OOXML 或使用只读库，不得改变源文件。
- 涉及 PDF 时，先完整阅读并遵循 `pdf` Skill。
- 涉及 XLSX 时，先完整阅读并遵循 `spreadsheets` Skill。

## 核心原则

1. Word 模板控制封面、字体、字号、颜色、标题层级、页边距、页眉页脚、页码和表格外观。
2. 项目材料控制事实、数字、表格、团队履历、产品描述、交易条款及预测，不用旧模板正文补足新项目事实。
3. PPT/PDF 中的文字必须输入为 Word 正文；原生表格必须重建为可编辑 Word 表格。
4. 仅将产品照片、设备照片、技术结构图、工艺示意图、市场规模图、周期曲线图等视觉内容作为图片插入。
5. 禁止用整页 PPT/PDF 截图代替正文或表格。原生图表无法可靠重建时，只裁取图表对象区域，并同时保留图表数据表。
6. 使用直接陈述语气。不得写“投决报告中”“项目报告中”“项目组观点”“根据PPT”等制作过程措辞。
7. 不虚构缺失内容。没有退出计划、客户名称或财务数据时，留空、使用“—”或明确“未列示”，不得自行编造。

## 工作流

### 1. 固定输入与输出

- 将源文件复制到任务工作目录，记录绝对路径、大小、SHA-256、页数/幻灯片数。
- 输出到新的 DOCX，绝不覆盖模板或源材料。
- 创建任务级 `artifact.md`，记录模板证据、内容映射、可编辑槽位、媒体规则和验收门槛。

### 2. 提炼 Word 模板

- 渲染并查看模板每一页。
- 运行 section/style/image/field 等审计，识别所有不同页面模式。
- 保留模板封面、主题、样式、编号、页眉页脚、页码和页面几何。
- 优先复制模板后编辑；不得从空白文档套用通用样式冒充模板。

### 3. 建立源材料覆盖清单

- PPTX：逐页提取所有文本框、原生表格、图表数据、图片对象、位置和尺寸。可运行 `scripts/extract_investment_ppt.py`。
- PDF：逐页提取正文和表格；若出现类似“棣栬姱”的乱码，尝试 `text.encode("gbk").decode("utf-8")`，并逐页对照渲染结果。
- 为每页/每张幻灯片记录：目标章节、正文是否已写入、表格是否已重建、图片是否已插入或明确不采用。
- 不因提取器只返回标题就假定页面没有内容；必须查看渲染页确认是否包含图表、图片或栅格化文字。

### 4. 映射章节

按模板实际结构映射，不机械照搬源材料目录。常见映射见 `references/chapter-mapping.md`。至少覆盖：

- 释义
- 投资概要：公司基本情况、核心条款、亮点、风险
- 行业概况：产业链、规模、驱动因素、趋势、竞争格局
- 公司情况：设立、股权、融资、组织结构
- 团队和管理
- 产品、技术与业务：产品、工艺、订单、客户、竞争优势
- 财务分析及预测
- 估值、收益与退出
- 投资方案及保障条款

### 5. 写入正文与表格

- 尽可能保留原文措辞、数据单位、日期、表头、脚注和资料来源，只做必要的换行、标点和错别字修复。
- 逐人保留团队履历，不压缩成概括性人物简介。
- 表格必须完整输入；重复表格可在“投资概要”和“投资方案”各保留一次，以匹配模板语义。
- 过宽表格按业务语义拆分：资产/负债及权益、经营/投资/筹资现金流、产品订单/验证进展等。不得以缩至不可读字号或截图解决。
- 财务预测、敏感性分析和历史融资表保留所有年份、单位、合计及负数。

### 6. 插入视觉内容

- 优先提取 PPTX 中独立图片对象，保持原始分辨率。
- 对原生图表，优先同时生成可编辑数据表和图表区域图片；可运行 `scripts/crop_ppt_charts.py`。
- 将图片紧邻相应正文并添加黑色图注。
- 产品图、设备图和技术图可保留原色；Word 正文、标题、页眉页脚和表格文字必须服从模板颜色要求。
- 不使用装饰性整页截图，不重复插入同一图片。

### 7. 黑白与模板一致性

- 用户要求无彩色文字时，正文、标题、表格、页眉页脚、页码域和文本框文字全部设为黑色。
- 表格首行默认白底黑字，除非用户明确要求保留模板的其他处理。
- 注意 python-docx 未必暴露页码域或页眉文本框的字色；必要时在保存后直接审计并修正 `document.xml`、`header*.xml` 和 `footer*.xml` 的 `w:color`。
- 不改变模板中的品牌图形，除非用户要求去色或移除。

### 8. 验收

- 运行 `scripts/audit_investment_docx.py` 做结构检查。
- 用 Word 或 `documents` Skill 的渲染流程生成 PDF/PNG。
- 查看每一页，不只查看缩略图。检查：文字裁切、表格越界、行被截断、图片失真、标题孤行、空白页、页眉页脚错位及页码。
- 发现问题后修改并重新渲染；最后一次 OOXML 修改后必须再次渲染。
- 最终只交付 DOCX，除非用户另行要求 PDF 或中间文件。

## 禁止事项

- 不把整页 PPT/PDF 当作正文图片。
- 不把表格截图当作 Word 表格。
- 不仅写摘要而遗漏源材料的团队、订单、财务或交易条款。
- 不沿用旧模板中的旧项目事实。
- 不用“材料显示”“报告指出”等反复转述代替直接写作。
- 不因排版困难而把正文缩到不可读字号。

## 资源

- `scripts/extract_investment_ppt.py`：提取 PPTX 文本、表格、图表数据及独立图片。
- `scripts/crop_ppt_charts.py`：从已渲染幻灯片中裁取原生图表对象区域。
- `scripts/audit_investment_docx.py`：检查 DOCX 禁用措辞、字体颜色、表格底纹及必要内容。
- `references/chapter-mapping.md`：详细章节映射、表格拆分及图片选择规则。
