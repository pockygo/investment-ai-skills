# 投决报告写作指南

## Overview

Write a decision-oriented 投决报告 from a real transaction case instead of from a generic pitch template.
Follow the user's chapter order, preserve the user's writing habits, and turn transaction details into IC-ready tables and concise narrative pages.

## Default Chapter Structure

Use the following four-chapter structure unless the user explicitly changes it:

1. `01 项目概述`
2. `02 项目分析`
3. `03 行业分析`
4. `04 决议事项`

Use Arabic numbering in chapter titles and keep the report tone formal, concise, and investment-committee oriented.

## Workflow

1. Confirm the chapter structure before expanding content.
2. Start from the user's source package, usually including `bp-reader`, `deep-industry-research`, and any additional BP, diligence, interview, financial, or legal materials.
3. Extract all transaction terms, financing facts, and decision items first.
4. Write `1.1 项目概述` as a structured summary table before writing any narrative section.
5. Then distill the source package into each chapter and subsection instead of copying source text mechanically.
6. Keep user-provided labels and transaction terminology unchanged where possible.
7. Mark unknown fields as `待补充` instead of guessing.

## Default Input Package

Assume the user will usually provide some combination of:

- `bp-reader` output
- `deep-industry-research` output
- company BP or pitch deck
- financing plan and term sheet
- management interview notes
- financial statements or finance diligence
- legal diligence and key contract extracts
- customer, supplier, or expert call notes

Treat these materials as the raw evidence set.
Use them to synthesize each subsection in the report.
Do not let any single source dominate the wording if multiple sources provide better evidence.

## Section 1.1 Project Overview Table

When the user asks for `1.1 项目概述`, present it as a table rather than prose.

Use these rows by default:

- `投资主体`
- `投资金额`
- `投前估值`
- `本轮融资总额`
- `本轮其他投资人情况`
- `交易结构`
- `核心条款`
- `退出路径`

Fill each row using the following rules:

- `投资主体`: Write the exact name of the proposed investing fund or investment entity.
- `投资金额`: Write the proposed investment amount by the fund.
- `投前估值`: Write the company's proposed pre-money valuation.
- `本轮融资总额`: Write the total amount the target company plans to raise in the current round.
- `本轮其他投资人情况`: List the other participating investors in the round and each proposed investment amount.
- `交易结构`: Usually write whether the deal is `增资` or `老股转让`; if mixed, state the split clearly.
- `核心条款`: Summarize the binding economic and control provisions, especially `回购条款`, `对赌条款`, and other closing or post-closing obligations.
- `退出路径`: Usually write `上市`、`并购` or `回购`; combine them when the deal documents provide multiple routes.

## Writing Rules For Core Terms

If `核心条款` is simple, keep it in one cell as short bullet-like sentences separated by line breaks.

If `核心条款` is complex, split it inside the table cell into sub-labels such as:

- `回购安排`
- `交割后义务`
- `业绩承诺`
- `特殊股东权利`

Keep each sub-label factual and close to the source wording. Do not rewrite legal clauses into promotional language.

## Table Style Guidance

Use the page as a clean summary page:

- Keep the left column as field labels and the right column as content.
- Prefer full-sentence factual entries over fragmented keywords.
- Preserve RMB units such as `500万元`, `1,700万元`, `10,500万元`.
- For multiple co-investors, list one investor per line with amount aligned in reading order.
- For long clauses, break lines by numbered points.
- For dates, keep exact legal or term-sheet dates.

## Starter Markdown Template

Use this starter block when drafting the section:

```md
# 投决报告

## 01 项目概述

### 1.1 项目概述

| 项目 | 内容 |
| --- | --- |
| 投资主体 | 待补充 |
| 投资金额 | 待补充 |
| 投前估值 | 待补充 |
| 本轮融资总额 | 待补充 |
| 本轮其他投资人情况 | 待补充 |
| 交易结构 | 待补充 |
| 核心条款 | 待补充 |
| 退出路径 | 待补充 |

## 02 项目分析

## 03 行业分析

## 04 决议事项
```

## Section 1.2 Company Introduction

Write `1.2 项目概述-公司简介` as a short, high-density profile page.
This section should summarize what the company does, how it operates, and what its recent operating performance looks like.

Include these three components by default:

1. `公司简介`
2. `商业模式`
3. `业绩情况`

### 1.2.1 公司简介

Open with a compact paragraph that answers:

- What kind of company it is
- What core product or capability it focuses on
- What technical or market position it occupies
- What major application scenarios or end markets it serves
- What proof points support the positioning, such as patents, shipped products, major customers, or technical milestones

Prefer one paragraph with strong factual density over several weak overview sentences.

### 1.2.2 商业模式

Present the business model as short labeled lines rather than as a long paragraph.
Use the user's preferred dimensions when provided.
If the user does not specify dimensions, default to:

- `研发`
- `生产`
- `销售`
- `收款`

Add other labels only when the case clearly needs them, such as:

- `供应商`
- `客户`
- `渠道`
- `认证导入`
- `交付`

For each label, describe the actual operating mechanism in one sentence.
Example directions:

- `研发`: Whether the company does custom development, platform development, or module iteration based on downstream demand.
- `生产`: Whether production is in-house, outsourced, fabless, or hybrid.
- `销售`: Whether the company sells directly to end customers, integrators, distributors, or OEMs.
- `收款`: Whether payment is prepayment, milestone-based, acceptance-based, or long账期 collection.

### 1.2.3 业绩情况

Summarize recent operating and financial performance in a concise block.
Prefer concrete numbers over adjectives.
Common items include:

- revenue by year or recent period
- net profit or adjusted net profit
- cash balance
- leverage or asset-liability ratio
- backlog or signed-but-unrecognized orders
- current-year quarterly run rate or hand-in-hand orders

If multiple years are available, write them in descending recency.
If a metric is management-stated rather than verified, preserve that distinction in wording.

## Style Guidance For Section 1.2

Follow the reference page logic:

- One strong lead paragraph for `公司简介`
- Several labeled lines for `商业模式`
- One dense performance summary for `业绩情况`

Do not turn this page into a full diligence chapter.
The goal is to let the IC understand the company in one page before entering deeper analysis.

## Section 1.3 Project Highlights

Write `1.3 项目概述-项目亮点` as a one-page highlight summary distilled from the full input package.
Do not ask the user to pre-write the highlights.
Generate them from the evidence in `bp-reader`, `deep-industry-research`, and the rest of the case materials.

### Core Requirement

Extract `4-5` highlights by default.
The highlights should collectively cover the most important investment support points across dimensions such as:

- industry
- team
- technology
- customers
- financials

Not every case needs all five dimensions.
Choose the strongest `4-5` arguments that best explain why this project is investable now.

### How To Select Highlights

Prioritize highlights that satisfy most of these conditions:

- closely linked to the investment thesis
- supported by multiple sources or stronger evidence
- differentiated versus peers or substitutes
- relevant to timing, scalability, or return potential
- understandable in one short title plus one explanatory sentence or paragraph

Avoid weak highlights that are generic, repetitive, or unsupported.
If two points are really one argument, merge them.

### Suggested Highlight Angles

Useful angles include:

- `行业机会正在释放`
- `团队具备稀缺经验或连续创业/产业背景`
- `技术路线领先或壁垒清晰`
- `客户资源扎实且验证充分`
- `财务增长快且盈利拐点明确`

Also use case-specific variants when stronger, such as:

- supply-chain position
- regulatory or certification progress
- product cost-performance edge
- order visibility
- commercialization rhythm

### Writing Format

For each highlight:

1. Write a short conclusion-style title.
2. Add one compact explanatory paragraph underneath.

The title should sound like a decision-supporting judgment, not a vague topic label.
Prefer titles such as:

- `下游需求拐点临近，增长确定性增强`
- `核心团队具备产业 know-how 与量产落地经验`
- `客户验证深入，头部客户导入形成先发优势`

Avoid titles such as:

- `行业`
- `团队介绍`
- `技术情况`

### Evidence Standard For Highlights

Each highlight should be traceable back to evidence.
When possible, anchor the paragraph with concrete support such as:

- market growth rates
- shipment or order trends
- customer names or customer types
- patent counts
- product milestones
- revenue growth
- margin improvement
- backlog or hand-in-hand orders

If a point is mainly management-stated, soften the wording rather than overstating certainty.

## Style Guidance For Section 1.3

Follow the reference page logic:

- `4-5` bold conclusion-style highlight titles
- one short supporting paragraph under each title
- no long bullet list
- no appendix-level detail

Keep the page energetic but still factual.
This section should help the IC understand the project's most attractive elements in one pass.

## Section 1.4 Risks And Mitigations

Write `1.4 风险与应对` as a table page.
Use this page to summarize the most important diligence findings, operating risks, legal risks, financial risks, or execution risks that the IC should notice before approving the deal.

### Table Structure

Use a three-column table by default:

- `问题`
- `问题的表现`
- `解决方案`

If the user explicitly prefers the wording from a template, adapt the third column title to forms such as:

- `解决方案/交易保护`
- `整改措施`
- `应对方案`

### How To Populate The Table

Each row should describe one risk issue.
Do not write abstract category labels without concrete manifestations.

Fill the columns using these rules:

- `问题`: Write the risk in concise noun-phrase form, such as historical compliance issue, customer concentration risk, profitability pressure, receivable recovery risk, or governance weakness.
- `问题的表现`: Describe how the problem shows up in the actual case, including facts, amounts, dates, contracts, accounting treatment, ownership structure, litigation, customer dependency, cash flow pressure, or other concrete signals.
- `解决方案`: Write the mitigation plan or transaction protection arrangement, such as supplemental diligence, document remediation, covenant design, milestone conditions, valuation adjustment, indemnity, escrow, governance enhancement, or post-investment整改 requirements.

### Risk Selection Rule

Select the issues that matter most to the investment decision.
Prefer risks that are:

- explicitly identified in finance or legal diligence
- linked to deal completion conditions
- likely to affect valuation or transaction structure
- likely to affect future operations, compliance, or exit

Avoid filling the page with trivial or repetitive points.
If the case has many issues, merge similar items and keep only the highest-impact rows on the main page.

### Evidence Standard For Risks

Risk wording must stay close to the evidence.
Do not weaken a real red flag into vague soft language.
Do not convert management explanations directly into conclusions unless independently supported.

When possible, include:

- exact dates
- precise amounts
- percentage exposure
- named counterparties or related parties
- contractual status
- whether the issue is historical, ongoing, or unresolved

### Mitigation Writing Rule

Write `解决方案` as actionable measures, not generic comfort language.
Good mitigations usually include one or more of:

- pre-closing cleanup
- supplemental document delivery
- founder or controlling-shareholder commitment
- special indemnity or compensation
- escrow or risk reserve
- valuation adjustment
- milestone-based release
- governance or finance system upgrade
- post-investment KPI or covenant monitoring

If there is no real mitigation yet, state `待落实` rather than inventing a solution.

## Starter Markdown Template For Section 1.4

```md
### 1.4 风险与应对

| 问题 | 问题的表现 | 解决方案 |
| --- | --- | --- |
| 待补充 | 待补充 | 待补充 |
| 待补充 | 待补充 | 待补充 |
| 待补充 | 待补充 | 待补充 |
```

## Style Guidance For Section 1.4

Follow the reference page logic:

- use a table, not narrative paragraphs
- one row per core issue
- keep the first column short
- keep the second and third columns factual and operational

This page should help the IC see not only what can go wrong, but also how the deal can be protected or conditioned.

## Section 2.1 Company Basic Information

Write `2.1 公司基本信息` as a table page.
Use it to give the IC a clean factual snapshot of the legal entity and core management facts before entering deeper business analysis.

### Table Structure

Use the following rows by default:

- `公司名称`
- `注册资本`
- `实缴资本`
- `法定代表人及实控人`
- `核心团队成员`
- `成立时间`
- `注册地址`

Keep the layout simple: left column for field names, right column for values.

### Field Rules

Fill each row using these rules:

- `公司名称`: Use the full registered legal entity name.
- `注册资本`: Use the工商登记或最新公司文件中的注册资本口径.
- `实缴资本`: Use the actual paid-in capital amount; if the amount is partial or scheduled in installments, reflect the latest confirmed status.
- `法定代表人及实控人`: If they are the same person, write together in one row; if they differ, still keep them in the same row but distinguish clearly.
- `核心团队成员`: List the key executives or founding team members most relevant to the investment case. Prefer one person per line, and include role, full-time status, age, or short identifiers when available and useful.
- `成立时间`: Use the legal establishment date of the company.
- `注册地址`: Use the registered address from the latest reliable corporate records.

### Evidence Guidance

Prioritize formal corporate sources when available, such as:

- business registration records
- company charter or latest amendment
- cap table materials
- legal diligence reports
- official company filings

If different materials conflict, prefer the most recent verified legal source and note `待核实` internally before finalizing other sections.

### Writing Rules

This page is factual, not analytical.
Do not add commentary such as whether the registered capital is sufficient or whether the team is strong.
That interpretation belongs elsewhere in the report.

For `核心团队成员`, keep the wording compact.
Good examples:

- `张三，董事长/创始人，全职，45岁`
- `李四，CTO，曾任某头部公司研发负责人`

If the user prefers a more stripped-down style, keep only name plus role.

## Starter Markdown Template For Section 2.1

```md
## 02 项目分析

### 2.1 公司基本信息

| 项目 | 内容 |
| --- | --- |
| 公司名称 | 待补充 |
| 注册资本 | 待补充 |
| 实缴资本 | 待补充 |
| 法定代表人及实控人 | 待补充 |
| 核心团队成员 | 待补充 |
| 成立时间 | 待补充 |
| 注册地址 | 待补充 |
```

## Style Guidance For Section 2.1

Follow the reference page logic:

- use a table, not narrative text
- keep the field labels stable
- keep values concise and standardized
- break lines inside `核心团队成员` when listing multiple people

This page should let a committee member understand the company's legal identity and key human anchors in under a minute.

## Section 2.1 Historical Financing

When the materials contain prior fundraising history, add a subsection under company basic information for `历史融资情况`.
Structure it in two parts:

1. one summary sentence
2. one financing history table

### Opening Summary Sentence

Start with one sentence that summarizes:

- how many financing rounds the company has completed historically
- the approximate cumulative financing amount

Example structure:

`公司历史上累计完成X轮融资，累计融资额约为X亿元。`

If the total amount is not directly stated but can be summed reliably from the table, calculate it.
If the number is uncertain due to partial disclosure or undisclosed bridge rounds, soften the language with `已披露` or `公开可见`.

### Financing Table Structure

Use the following columns by default:

- `融资轮次`
- `融资时间`
- `投前估值`
- `融资金额`
- `投资方`

### Column Rules

Fill the columns using these rules:

- `融资轮次`: Use the round naming exactly as disclosed, such as `天使轮`, `Pre-A轮`, `A轮`, `A+轮`, `战略轮`.
- `融资时间`: Prefer `YYYY.MM` or `YYYY-MM` based on the dominant style in the report. Keep one format consistently.
- `投前估值`: Use the pre-money valuation for that round. If unavailable, write `未披露` or `待补充` rather than inferring.
- `融资金额`: Use the disclosed raise amount for that round.
- `投资方`: List the major participating investors for that round. If the list is very long, keep the lead investors and representative names first.

### Evidence Guidance

Prioritize the following sources:

- cap table and financing summary materials
- BP financing history pages
- legal diligence reports
- shareholder resolutions and transaction documents
- credible public financing disclosures

If different sources conflict, prefer signed transaction material or the latest verified internal summary.

### Writing Rules

This page is descriptive, not analytical.
Do not explain why certain investors matter here unless the user explicitly wants commentary.
Keep investor names readable and separated by commas or line breaks.

If one round has multiple closings but is economically the same round, decide whether to merge based on the user's reporting habit.
If merged, keep the round as one row and reflect the total amount clearly.

## Starter Markdown Template For Historical Financing

```md
#### 历史融资情况

公司历史上累计完成X轮融资，累计融资额约为X亿元。

| 融资轮次 | 融资时间 | 投前估值 | 融资金额 | 投资方 |
| --- | --- | --- | --- | --- |
| 待补充 | 待补充 | 待补充 | 待补充 | 待补充 |
| 待补充 | 待补充 | 待补充 | 待补充 | 待补充 |
```

## Style Guidance For Historical Financing

Follow the reference page logic:

- one short headline sentence before the table
- one row per financing round
- keep the chronology clear
- keep amounts and valuations in a consistent unit system

This subsection should help the IC quickly understand capital formation history and prior investor base.

## Section 2.1 Current Shareholding Structure

When the materials contain a cap table or shareholder register, add a subsection for `当前股权结构`.
Present it as a table page so the IC can quickly understand ownership concentration, founder control, ESOP setup, and investor distribution.

### Table Structure

Use the following columns by default:

- `股东名称`
- `认缴注册资本（万元）`
- `实缴注册资本（万元）`
- `持股比例`

If the source materials do not separately disclose paid-in capital by shareholder, keep the `实缴注册资本（万元）` column and fill `待补充` or use the latest verified breakdown if available.

### Column Rules

Fill the columns using these rules:

- `股东名称`: Use the full legal name of each shareholder. Keep ESOP platforms, holding partnerships, and institutional funds in their disclosed legal form.
- `认缴注册资本（万元）`: Use the subscribed registered capital amount for each shareholder, in `万元`.
- `实缴注册资本（万元）`: Use the actually contributed capital amount for each shareholder, in `万元`, based on the latest verified records.
- `持股比例`: Use the current ownership percentage corresponding to the latest cap table baseline. Keep a consistent percentage format throughout the table.

### Row Rules

List one shareholder per row.
Keep the current post-round or pre-round baseline consistent within the page; do not mix different cap table dates.
If the page includes ESOP platforms or employee holding vehicles, keep them as separate shareholder rows rather than unpacking underlying individuals unless the user explicitly asks.

Add a final `汇总` row when the source style or report template uses one.
The total row should reconcile:

- subscribed capital total
- paid-in capital total when available
- shareholding ratio total of `100.00%`

### Evidence Guidance

Prioritize formal sources such as:

- latest cap table
- shareholder register
- company charter and amendments
- legal diligence reports
- financing closing documents

If different versions of the cap table exist, prefer the latest transaction-reconciled version that matches the intended reporting date.

### Writing Rules

This page is a factual presentation page.
Do not add ownership interpretation, control analysis, or dilution commentary here unless the user explicitly wants a side note.
That analysis belongs in team, governance, or investment logic sections.

Keep names and numbers aligned and standardized.
If the shareholder list is long, still keep the full table on one page when possible rather than truncating important holders.

## Starter Markdown Template For Current Shareholding Structure

```md
#### 当前股权结构

| 股东名称 | 认缴注册资本（万元） | 实缴注册资本（万元） | 持股比例 |
| --- | --- | --- | --- |
| 待补充 | 待补充 | 待补充 | 待补充 |
| 待补充 | 待补充 | 待补充 | 待补充 |
| 汇总 | 待补充 | 待补充 | 100.00% |
```

## Style Guidance For Current Shareholding Structure

Follow the reference page logic:

- use a table only
- one shareholder per row
- keep units in `万元`
- keep percentages formatted consistently
- add a total row when appropriate

This subsection should let the IC quickly understand who owns the company today and in what proportions.

## Section 2.2 Organization Structure

Write `2.2 组织架构` as a combined organization snapshot page.
This page should usually include:

1. key headcount summary bullets
2. an organization chart
3. one or more optional personnel-structure tables when the materials support them

### Core Elements

Include the following by default:

- `员工总数`
- `组织架构图`

When available and useful, also include:

- departmental headcount and share
- education breakdown by headcount and share
- R&D headcount and share
- other relevant personnel composition metrics

### Recommended Page Logic

Arrange the page so the IC can understand the organization in one pass:

- short bullets on the left or top summarizing the key personnel facts
- organization chart in the main visual area
- one small table on the side for education or department structure when available

Do not overload the page with too many tables.
Choose the one or two personnel structure views that best support the investment thesis.

### Summary Bullet Rules

Start with `2-4` bullets summarizing the most decision-relevant organization facts.
Common examples include:

- total employee count
- share of employees with bachelor degree or above
- number and share of R&D staff
- concentration of key technical or operating personnel

Each bullet should use a direct factual sentence.
Examples:

- `公司共有员工36人。`
- `公司本科及以上人员35人，占比97.14%。`
- `公司研发部门共25人，占比71.43%。`

### Organization Chart Rules

The organization chart should reflect the company's actual reporting lines, not a generic template.
Common layers include:

- board or shareholder level
- chairman or founder
- CEO or general manager
- CTO, COO, CFO, sales head, operations head, or other major function leaders
- major departments or business units

If the source material already provides an org chart, preserve its structure and labels as much as possible.
If only textual descriptions are available, reconstruct a simple chart from the evidence without inventing unnecessary positions.

### Optional Personnel Structure Tables

Use a side table when the user materials contain reliable personnel composition data.
Common table types include:

- education distribution
- department distribution
- function distribution

For these tables, use columns such as:

- `类别`
- `人数`
- `占比`

Good examples of categories:

- `博士`
- `硕士`
- `本科`
- `本科以下`
- `研发人员`
- `销售人员`
- `生产人员`

If categories overlap, make that clear in wording and do not force them into one additive total unless the source does so.

### Evidence Guidance

Prioritize sources such as:

- HR summaries in BP or diligence materials
- management interview notes
- internal organization charts
- employee roster summaries
- legal or finance diligence materials when they include staffing data

If headcount data differs across materials, use the latest consistent snapshot and keep all ratios tied to that same denominator.

### Writing Rules

This page is mainly descriptive and structural.
Do not turn it into a qualitative team assessment page.
Discussion of founder capability, key-man risk, or talent competitiveness belongs in team analysis or investment logic sections.

Keep all percentages rounded consistently.
If exact totals do not reconcile due to timing differences, prefer the most reliable snapshot and avoid forced arithmetic that contradicts the source.

## Starter Markdown Template For Section 2.2

```md
### 2.2 组织架构

- 公司共有员工X人。
- 公司本科及以上人员X人，占比X%。
- 公司研发人员X人，占比X%。

组织架构图：待补充

| 类别 | 人数 | 占比 |
| --- | --- | --- |
| 待补充 | 待补充 | 待补充 |
| 待补充 | 待补充 | 待补充 |
```

## Style Guidance For Section 2.2

Follow the reference page logic:

- start with short factual bullets
- include the organization chart as a core visual
- add at most one or two compact supporting tables
- keep the page readable rather than exhaustive

This section should help the IC understand whether the company has a credible organizational base for execution and scale-up.

## Section 2.3 Core Team

Write `2.3 核心团队` as a table page.
Use it to present the key executives, founders, and core functional leaders who materially affect the company's execution, technology development, commercialization, or fundraising credibility.

### Table Structure

Use the following columns by default:

- `姓名`
- `职务`
- `学历/年龄`
- `核心背景与关键能力`

Keep one person per row.
The goal is to let the IC quickly understand who the core people are and why they matter.

### Column Rules

Fill the columns using these rules:

- `姓名`: Use the person's standard Chinese or English name as shown in the source materials.
- `职务`: Use the current primary role, such as `创始人/董事长兼总经理`, `CTO`, `研发总监`, `销售负责人`, `COO`.
- `学历/年龄`: Combine highest relevant education background and age in one compact cell. Keep the style consistent across rows, such as `清华大学硕士 / 42岁`.
- `核心背景与关键能力`: Summarize the person's most relevant prior experience, technical or commercial track record, industry tenure, and the key capability they bring to the company today.

### Selection Rule

Do not include every manager.
Select the people most relevant to the investment case, usually:

- founder or actual controller
- CEO or general manager
- CTO or key technical leader
- sales or business leader when commercialization matters
- operations or manufacturing leader when delivery capability matters

In most cases, `3-6` people are enough for the main page.

### Writing Rules For Background And Capability

The last column should not read like a full biography.
Compress each person into one dense paragraph that answers:

- what they did before
- what domain expertise or track record they have
- what part of the company's current capability depends on them

Useful content includes:

- years of industry experience
- prior employers or research institutions
- prior products, programs, or transactions led
- patents, publications, engineering achievements, or customer-development success
- team-building, commercialization, supply-chain, or management capability

Prefer concrete facts over praise words.
Good phrasing:

- `15年行业研发经验，曾负责XX产品量产导入，具备芯片定义与客户协同能力。`
- `连续创业背景，主导多个大客户导入和销售体系搭建，擅长商业化落地。`

Avoid vague language such as:

- `能力很强`
- `经验丰富`
- `综合素质优秀`

unless it is backed by specific facts in the same sentence.

### Evidence Guidance

Prioritize:

- BP founder/team pages
- management interview notes
- resumes and biography summaries
- diligence interview records
- public profiles or company disclosures when included in the user's materials

If some biographies are much more detailed than others, normalize the level of detail instead of copying one long CV next to several thin rows.

### Tone Guidance

This page should be supportive of decision-making, but still factual.
It is acceptable to highlight relevant strengths, as long as the wording remains anchored to evidence.
Do not hide obvious gaps; if a core function lacks a strong leader, that issue belongs in the risk section rather than being glossed over here.

## Starter Markdown Template For Section 2.3

```md
### 2.3 核心团队

| 姓名 | 职务 | 学历/年龄 | 核心背景与关键能力 |
| --- | --- | --- | --- |
| 待补充 | 待补充 | 待补充 | 待补充 |
| 待补充 | 待补充 | 待补充 | 待补充 |
| 待补充 | 待补充 | 待补充 | 待补充 |
```

## Style Guidance For Section 2.3

Follow the reference page logic:

- use a table only
- one person per row
- keep the first three columns concise
- make the last column dense but readable

This section should help the IC quickly assess whether the company has the people required to execute the thesis.

## Section 2.4 Main Business Overview

Write `2.4 主营业务情况` based on the actual product complexity of the company.
Do not force every company into the same page structure.

### Structure Decision Rule

First judge whether the company has:

- multiple product lines, solutions, or business forms that need a top-level map
- only one or a few core products that can be explained directly

Use this rule:

1. If the company has multiple products, multiple solution lines, or a layered product system, start with `2.4 主营业务情况-概览`.
2. If the company has only a small number of core products, skip the overview page and directly introduce each product or business line.

### When To Use `2.4 主营业务情况-概览`

Use an overview page when the business is not easy to understand without a framework first.
Typical cases include:

- multiple product categories
- platform plus modules plus applications
- hardware plus software plus service
- base capability layer plus solution layer plus commercial products
- several downstream scenarios sharing a common technical core

The goal of the overview page is to help the IC quickly understand how the company's product system is organized before reading product-by-product pages.

### Writing Rules For `2.4 主营业务情况-概览`

The overview page should usually contain:

1. one short explanatory paragraph on the left or top
2. one framework graphic or structured diagram in the main visual area
3. optional short labels describing product categories, customer targets, delivery form, or monetization model

The explanatory paragraph should answer:

- how the company's product system should be understood
- what the core underlying capability is
- how many major product forms or solution categories it has
- what commercial value these product forms create

Good framing patterns include:

- `公司产品体系可理解为“底层能力 + 中间平台 + 商业化产品形态”。`
- `公司围绕核心芯片能力，形成样品、小批量量产产品与定制化解决方案三层业务。`

### Diagram Guidance For The Overview Page

If the source materials already contain a strong product-system diagram, preserve its logic and terminology.
If not, reconstruct a simplified framework diagram from the materials.

Common diagram structures include:

- capability layer -> product layer -> scenario layer
- hardware -> software -> service
- platform -> modules -> end solutions
- core technology -> product matrix -> customer segments

Do not invent an overly decorative framework if the business is simple.
Clarity matters more than visual complexity.

### When To Skip The Overview Page

Skip `概览` when:

- the company has only one core product
- the company has two or three products that are easy to compare directly
- the report becomes repetitive if an overview page is inserted

In those cases, go directly into product-level subsections under `2.4`.

### Product-Level Introduction Rules

Whether or not an overview page exists, product-level pages should describe each major product or business line in a consistent way.
Common dimensions include:

- product definition
- target customer
- application scenario
- technical characteristics
- delivery form
- commercialization progress
- pricing or monetization model

Choose only the dimensions that matter for the specific case.
Do not force a rigid template if the business is better explained through a different logic.

### Evidence Guidance

Prioritize:

- BP product pages
- company website or company-introduced product materials included by the user
- management interview notes
- technical diligence or expert interview summaries
- sales materials when they help explain the actual commercial offering

If the company's product descriptions are highly promotional, rewrite them into investor language while preserving the core facts.

## Starter Markdown Template For Section 2.4

```md
### 2.4 主营业务情况

#### 2.4.1 主营业务情况-概览

公司产品体系可理解为“待补充”。

概览图：待补充

#### 2.4.2 产品/业务一

待补充

#### 2.4.3 产品/业务二

待补充
```

## Style Guidance For Section 2.4

Follow the reference page logic:

- decide structure based on product complexity first
- use an overview page only when it genuinely improves comprehension
- keep the overview conceptual and the later pages concrete
- let the business logic drive the section design

This section should help the IC understand what the company actually sells, how the offerings are organized, and why the business model is coherent.

## Product-Level Multi-Page Rules Under Section 2.4

For a single product or product line, it is acceptable to use multiple pages if the content is rich enough.
Do not force all product information onto one page when that would make the section crowded or unclear.

### Default Product Page Modules

For each major product or product line, consider splitting the content into `2-4` pages depending on depth.
Common page types include:

1. `产品介绍`
2. `性能参数与核心特点`
3. `应用领域、市场规模与竞争格局`
4. `典型客户与商业化进展`

Combine or split these modules depending on the amount of available material.

### Page 1: 产品介绍

Use the first page to explain what the product is and how it works at a high level.
This page can include:

- a short textual introduction
- product images
- product workflow or process diagram
- one compact comparison table when there are several models in the same product line

The textual introduction should answer:

- what the product is
- what problem it solves
- how it fits into the customer's production or usage flow
- what its main technical or commercial positioning is

If images are available in the materials, place them.
If images are not available or cannot be inserted, explicitly reserve positions such as:

- `图片位置：产品实物图`
- `图片位置：工艺流程图`
- `图片位置：设备工作场景图`

### Page 2: 性能参数与核心特点

When parameter comparison matters, dedicate a page or half-page to performance parameters.
Typical dimensions include:

- precision
- throughput
- yield
- compatibility
- power or size
- delivery cycle
- price range

Do not list parameters without explanation.
For each important parameter, explain what it represents in the industrial or commercial context.
Examples:

- whether higher precision enables advanced packaging or high-end applications
- whether higher UPH improves customer ROI
- whether broader compatibility reduces switching cost

Also summarize the product's core differentiators, such as:

- higher precision
- stronger compatibility
- lower price
- faster delivery
- easier localization support
- stronger customization capability

### Page 3: 应用领域、市场规模与竞争格局

If the product serves a distinct market, explain that market directly on the product page or product-line page.
Common subtopics include:

- major application scenarios
- market size of the product's core application fields
- growth trend
- domestic and overseas competition
- competing routes or substitute solutions

This page should answer:

- where the product is actually used
- how big the addressable market is
- who the core competitors are
- where the company stands in that landscape

Use tables when competitor comparison is important.
Useful comparison columns include:

- `公司名称`
- `简介`
- `关键参数`
- `市占率`
- `竞争位置`

### Page 4: 典型客户与商业化进展

When customer validation is a core part of the thesis, include a page on customer adoption.
Useful content includes:

- representative customer names
- customer types
- current project stage
- demo, trial, sample, pilot, order, batch delivery, or repeat purchase status
- revenue contribution or commercialization significance

If confidentiality prevents naming all customers, describe them by category and mention disclosed benchmark customers where possible.

### Model Comparison Rule

If one product line contains multiple models, variants, or generations, use a compact comparison table.
Useful rows include:

- model name
- key parameter
- price
- application
- representative customer

Do not overbuild the table.
Choose only the rows that help the IC understand positioning differences.

### Market And Competition Writing Rule

When discussing market size and competition, stay specific to the product rather than the entire company.
If the product targets a niche of a larger industry, use the niche market when possible.
If only broader industry data is available, clearly state that it is a proxy.

### Evidence Guidance For Product Pages

Prioritize:

- BP product and customer slides
- product brochures provided by the user
- management interviews
- expert interviews
- technical diligence
- sales pipeline summaries
- third-party market reports already included in the user's material package

If a claim is based mainly on the company's own statement, keep the wording appropriately qualified.

## Starter Markdown Template For A Single Product Under Section 2.4

```md
#### 2.4.X 产品/业务名称

##### 产品介绍

产品介绍：待补充

图片位置：产品实物图
图片位置：工艺/原理示意图

##### 性能参数与核心特点

| 参数/指标 | 当前水平 | 代表含义 |
| --- | --- | --- |
| 待补充 | 待补充 | 待补充 |
| 待补充 | 待补充 | 待补充 |

核心差异或特点：待补充

##### 应用领域、市场规模与竞争格局

应用领域：待补充
市场规模：待补充

| 公司名称 | 简介 | 关键参数/特点 | 市场地位 |
| --- | --- | --- | --- |
| 待补充 | 待补充 | 待补充 | 待补充 |

##### 典型客户与商业化进展

典型客户：待补充
商业化进展：待补充
```

## Style Guidance For Single Product Pages

Follow the reference page logic:

- allow one product to span multiple pages when needed
- reserve image positions when no usable image is available
- explain why parameters matter instead of only listing them
- keep market and competition tied to the product, not abstract industry talk

These pages should help the IC move from understanding the product itself to understanding its commercial value and competitive position.

## Section 2.5 Competitive Advantages

Write `2.5 竞争优势` as a decision-support page that answers one core question:

`为什么是这家公司胜出。`

Use this section to synthesize the company's competitive advantages, core capabilities, and structural barriers.
Do not merely repeat the product features, team biographies, or market descriptions already shown in prior pages.
Instead, convert those facts into a sharper explanation of why this company is better positioned than peers.

### Core Objective

This page should explain:

- why the company can win in its target market
- what is difficult for competitors to replicate
- why the company's current position is not accidental
- what combination of team, product, customer, execution, and industry position creates defensibility

### Structure Options

Choose one of these two structures based on the case:

1. `4-6` conclusion-style advantage points with short supporting paragraphs
2. a small summary table of `竞争优势` / `具体体现` / `对投资价值的意义`

Default to the first structure unless the user or template strongly prefers tabular presentation.

### Typical Advantage Dimensions

Useful dimensions include:

- technical barrier
- product performance or cost-performance edge
- customer validation and sticky relationships
- founder or team know-how
- supply-chain or manufacturing coordination capability
- commercialization efficiency
- data or model accumulation
- certification or regulatory barrier
- first-mover advantage in a niche market
- localization advantage

Not every case needs every dimension.
Select the `4-6` strongest factors that most directly support the investment thesis.

### Writing Rules

Each advantage point should contain:

1. a conclusion-style title
2. one short paragraph explaining the evidence and strategic meaning

Good title examples:

- `技术门槛高且跨工艺兼容能力突出`
- `头部客户导入深入，形成验证与口碑双重壁垒`
- `创始团队兼具产业经验与商业化落地能力`
- `本土化交付与服务能力带来更强替代机会`

Avoid vague titles such as:

- `技术优势`
- `客户优势`
- `团队很好`

The supporting paragraph should connect concrete facts to competitive position.
For example:

- not only `精度更高`
- but `精度达到X水平，使其能够进入Y类高端场景，而国内可比厂商较少`

### What Counts As A Barrier

Treat a claimed barrier as valid only when the materials show some evidence that it is hard to replicate.
Useful evidence includes:

- long development cycle
- deep customer verification
- cross-disciplinary know-how
- accumulated data or case base
- integration with customer workflows
- difficult-to-copy supply-chain collaboration
- scarce talent concentration
- installed base and after-sales network

Do not call something a barrier if it is only an internal aspiration or a generic industry requirement.

### Difference From Section 1.3

`1.3 项目亮点` is the high-level investment highlight page.
`2.5 竞争优势` is deeper and more analytical.

The distinction is:

- `1.3` tells the IC what is attractive
- `2.5` tells the IC why this company specifically can win

So this section may reuse evidence from earlier pages, but should sharpen it into competitive logic rather than repeating headlines.

### Evidence Guidance

Build this section from cross-page synthesis, especially:

- product and technical pages
- customer and commercialization evidence
- team and organization pages
- market and competition analysis
- expert interviews
- diligence conclusions

The best version of this page usually combines facts from several prior sections.

### Tone Guidance

This page can be more thesis-driven than basic information pages, but it still must stay evidence-based.
It is acceptable to make comparative judgments, as long as they are grounded in the materials.
Do not overclaim durable moat if the business is still early and the evidence only supports a temporary lead.

## Starter Markdown Template For Section 2.5

```md
### 2.5 竞争优势

#### 竞争优势一：待补充

待补充

#### 竞争优势二：待补充

待补充

#### 竞争优势三：待补充

待补充

#### 竞争优势四：待补充

待补充
```

## Style Guidance For Section 2.5

Follow the reference page logic:

- focus on why this company wins
- use conclusion-style subheadings
- connect facts to defensibility and investment value
- avoid repeating prior sections without adding judgment

This section should make the IC believe the company's edge is real, relevant, and hard enough to复制 in the target market.

## Section 2.6 Supplier Overview

Write `2.6 供应商情况` as a combined data-and-analysis section.
This section should usually include:

1. major supplier tables for the past three years
2. a concise analysis of supplier concentration, stability, dependency, and supply-chain structure

Do not stop at listing suppliers.
The IC needs both the raw procurement data and the interpretation of what that data means for delivery capability, cost structure, and supply-chain risk.

### Core Scope

Focus on the `过去3年` major suppliers by procurement amount.
The default presentation is the `前三大供应商` or `前五大供应商` for each year, depending on what the materials disclose.
Follow the disclosure caliber in the source materials and do not fabricate rankings beyond the evidence.

### Table Structure

For each year, use a separate table.
Use the following columns by default:

- `供应商名称`
- `金额`
- `采购内容`

If the source materials provide helpful context, it is acceptable to add:

- `币种`
- `供应商类型`

If the source uses a more precise accounting label such as `采购金额（万元）`, keep that wording.

### Table Rules

Fill the table using these rules:

- `供应商名称`: Use the disclosed legal or commercial supplier name. If anonymity is required, preserve the user's anonymization style consistently.
- `金额`: Use the procurement amount disclosed for that year. Keep the unit consistent.
- `采购内容`: Describe the actual goods or services procured, such as wafers, foundry services, packaging, testing, core components, software licenses, or outsourced manufacturing services.

Keep one supplier per row.
Add a `合计` row when the source materials provide one or when it can be summed reliably.

### Year-By-Year Presentation Rule

Present the most recent year first unless the user prefers chronological order.
A common structure is:

- `2025年前三大供应商`
- `2024年前三大供应商`
- `2023年前三大供应商`

This makes it easier for the IC to start from the latest supply-chain reality.

### Required Analysis After The Tables

After the tables, provide a short analysis block.
Do not merely restate the rankings.
The analysis should extract what the supplier data says about the company's supply chain.

Useful angles include:

- supplier concentration
- dependence on one or two critical suppliers
- whether key suppliers are stable across years
- whether the company has alternative suppliers or backup capacity
- whether procurement is concentrated in foundries, materials, components, or outsourced services
- whether supply-chain structure reflects bargaining weakness or strategic partnership
- whether localization or国产替代 is improving
- whether supplier concentration may create production or pricing risk

### Good Analysis Questions

The analysis should help answer questions such as:

- Is the supply chain stable or fragile?
- Does the company rely excessively on a small number of upstream partners?
- Are the core suppliers high-quality and industry-standard?
- Is there meaningful substitute capacity if a key supplier changes terms or encounters disruption?
- Does the current supply-chain setup support future scale-up?

### Writing Rules For The Analysis

Keep the analysis concise but directional.
Usually `3-6` bullets or short paragraphs are enough.
Good analysis statements often include:

- one key fact
- one interpretation

Examples:

- `采购主要集中于晶圆代工环节，说明公司上游成本核心受制于产能与代工报价，需持续关注关键晶圆厂合作稳定性。`
- `核心供应商连续多年保持稳定，表明公司已建立相对成熟的上游协作关系，但替代来源仍较有限。`
- `部分产品已转入国内Fab流片，反映公司在供应链本土化方面已有进展，有助于缩短交付周期并降低外部不确定性。`

### Evidence Guidance

Prioritize:

- audited or finance-confirmed procurement tables
- diligence reports
- supplier summaries from the company
- interview notes that help identify supplier role, dependence level, or substitution difficulty

If the company provides supplier names but not consistent accounting caliber, distinguish clearly between:

- purchase amount
- payable balance
- contract amount
- production capacity reservation

Do not mix them in one ranking table.

### Risk Awareness

This section can contain positive supply-chain stability analysis, but do not hide dependency issues.
If supplier concentration is high or key substitution is difficult, state it here and also carry the implication into the risk section where appropriate.

## Starter Markdown Template For Section 2.6

```md
### 2.6 供应商情况

#### 2025年前三大供应商

| 供应商名称 | 金额 | 采购内容 |
| --- | --- | --- |
| 待补充 | 待补充 | 待补充 |
| 合计 | 待补充 | - |

#### 2024年前三大供应商

| 供应商名称 | 金额 | 采购内容 |
| --- | --- | --- |
| 待补充 | 待补充 | 待补充 |
| 合计 | 待补充 | - |

#### 2023年前三大供应商

| 供应商名称 | 金额 | 采购内容 |
| --- | --- | --- |
| 待补充 | 待补充 | 待补充 |
| 合计 | 待补充 | - |

供应商分析：待补充
```

## Style Guidance For Section 2.6

Follow the reference page logic:

- show the raw tables clearly
- then add analysis instead of stopping at data listing
- highlight both supply stability and dependency risk
- keep the analysis grounded in year-over-year comparison

This section should help the IC understand not only who the suppliers are, but also what the supply-chain structure implies for cost, delivery, and scaling risk.

## Section 2.7 Customer Overview

Write `2.7 客户情况` as a combined data-and-analysis section.
This section should usually include:

1. top-customer tables for the past three years
2. a concise analysis of customer structure, concentration, continuity, and expansion

Do not stop at listing customers.
The IC needs both the raw customer data and the interpretation of what that data means.

### Core Scope

Focus on the `过去3年` top customers by revenue or confirmed income amount.
The default presentation is the `前十大客户` for each year, unless the source materials provide fewer named customers.

### Table Structure

For each year, use a separate table.
Use the following columns by default:

- `客户名称`
- `金额`
- `销售产品/服务`

If the source materials also provide a strong industry label or application field, it is acceptable to add:

- `行业应用`

If the source uses a more precise accounting label such as `确认收入金额（万元）`, keep that wording.

### Table Rules

Fill the table using these rules:

- `客户名称`: Use the disclosed legal or commercial customer name. If anonymity is required, preserve the user's anonymization style consistently.
- `金额`: Use the revenue, confirmed income, or sales amount disclosed for that year. Keep the unit consistent.
- `销售产品/服务`: Describe the actual product, module, solution, or service sold to that customer.

Keep one customer per row.
Add a `合计` row when the source materials provide one or when it can be summed reliably.

### Year-By-Year Presentation Rule

Present the most recent year first unless the user prefers chronological order.
A common structure is:

- `2025年前十大客户`
- `2024年前十大客户`
- `2023年前十大客户`

This makes it easier for the IC to start from the latest operating reality.

### Required Analysis After The Tables

After the tables, provide a short analysis block.
Do not merely restate the rankings.
The analysis should extract what the customer data says about the business.

Useful angles include:

- customer concentration
- stability of repeat customers across years
- whether the top customers are growing or shrinking
- whether customer types are becoming more diversified
- whether benchmark customers have been successfully introduced
- whether the customer base is concentrated in a few applications or geographies
- whether new customer expansion is visible
- whether the company depends too heavily on a single customer

### Good Analysis Questions

The analysis should help answer questions such as:

- Is the customer base stable or fragile?
- Is the company repeatedly serving the same high-quality customers?
- Are top customers validating product-market fit?
- Is there obvious single-customer dependency risk?
- Is customer expansion broadening into new sectors or remaining narrow?

### Writing Rules For The Analysis

Keep the analysis concise but directional.
Usually `3-6` bullets or short paragraphs are enough.
Good analysis statements often include:

- one key fact
- one interpretation

Examples:

- `第一大客户连续三年位居前列，且采购金额持续增长，说明公司在核心客户体系中的份额仍在提升。`
- `前十大客户中新增多家VR/AR客户，反映公司应用场景正在从单一赛道向相邻场景扩展。`
- `客户结构整体较稳，但前两大客户占比较高，仍需关注集中度风险。`

### Evidence Guidance

Prioritize:

- audited or finance-confirmed customer revenue tables
- diligence reports
- customer sales summaries from the company
- interview notes that help identify customer quality or purchasing stage

If the company provides customer names but not revenue confirmation standard, distinguish clearly between:

- shipped amount
- confirmed revenue
- signed order
- pipeline

Do not mix them in one ranking table.

### Risk Awareness

This section can contain positive customer-validation analysis, but do not hide concentration issues.
If customer concentration is high, state it here and also carry the implication into the risk section where appropriate.

## Starter Markdown Template For Section 2.7

```md
### 2.7 客户情况

#### 2025年前十大客户

| 客户名称 | 金额 | 销售产品/服务 |
| --- | --- | --- |
| 待补充 | 待补充 | 待补充 |
| 合计 | 待补充 | - |

#### 2024年前十大客户

| 客户名称 | 金额 | 销售产品/服务 |
| --- | --- | --- |
| 待补充 | 待补充 | 待补充 |
| 合计 | 待补充 | - |

#### 2023年前十大客户

| 客户名称 | 金额 | 销售产品/服务 |
| --- | --- | --- |
| 待补充 | 待补充 | 待补充 |
| 合计 | 待补充 | - |

客户分析：待补充
```

## Style Guidance For Section 2.7

Follow the reference page logic:

- show the raw tables clearly
- then add analysis instead of stopping at data listing
- highlight both validation strength and concentration risk
- keep the analysis grounded in year-over-year comparison

This section should help the IC understand not only who the customers are, but also what the customer structure implies for business quality and future growth.

## Section 2.8 Backlog Orders

Write `2.8 在手订单` as a combined table-and-analysis section.
Use it to show the company's currently signed backlog or major contract base that supports future revenue visibility.

### Core Scope

Focus on signed and currently effective orders or contracts that the company treats as in-hand backlog.
Do not mix in pure pipeline, verbal intent, or unsigned forecast unless the user explicitly asks for that broader口径.

### Table Structure

Use a table with the following columns by default:

- `客户名称`
- `签约时间`
- `产品内容`
- `合同金额（万元）`
- `预付款比例`

If the source materials use an explicit sequence column, it is acceptable to add:

- `序号`

### Column Rules

Fill the columns using these rules:

- `客户名称`: Use the disclosed legal or commercial customer name. If anonymity is required, preserve the user's anonymization style consistently.
- `签约时间`: Use the contract signing date or order confirmation date from the source material.
- `产品内容`: Describe the product, module, solution, NRE, service, or project content covered by the contract.
- `合同金额（万元）`: Use the signed contract amount, in `万元`, with unit consistency across the table.
- `预付款比例`: Use the disclosed advance payment ratio or payment structure. If the source uses mixed wording such as deposit plus stage payment, keep the source logic concise and readable.

Keep one contract or one order item per row unless the source materials clearly aggregate multiple contracts into one customer-level summary.

### Writing Rules For The Table

Prefer the latest active orders first if no specific sort order is required.
If the list is long, keep the key orders that best represent backlog quality and size on the main page.
If there are many smaller orders, summarize them outside the main table rather than overcrowding the page.

If the contracts contain different billing structures, preserve meaningful distinctions such as:

- fixed prepayment ratio
- milestone payment
- 100% prepayment
- `0，30天付`

Do not force these into a uniform numeric format if that would lose information.

### Required Analysis After The Table

After the table, provide a short analysis block.
Do not only say that the company has many orders.
Explain what the order book implies for revenue visibility and execution quality.

Useful angles include:

- whether the backlog is concentrated in a few major customers
- whether the order mix matches the company's main products
- whether prepayment ratios are high or low
- whether payment terms help cash flow
- whether the orders indicate repeat customer procurement
- whether the backlog supports near-term revenue growth
- whether a large share of orders comes from NRE, sample, or early-stage projects rather than scalable product revenue

### Good Analysis Questions

The analysis should help answer questions such as:

- Are these orders real and commercially meaningful?
- How strong is near-term revenue visibility?
- Are payment terms favorable enough to support operating cash flow?
- Is backlog quality high, or is it dependent on a few uncertain projects?
- Do the orders validate product demand in the target market?

### Writing Rules For The Analysis

Keep the analysis concise and factual.
Usually `2-5` bullets or short paragraphs are enough.
Good analysis statements often include:

- one fact from the table
- one implication for revenue quality, customer validation, or cash flow

Examples:

- `在手订单以Micro LED相关产品为主，说明公司当前商业化重心与主营业务方向一致。`
- `多数合同带有较高比例预付款，有助于缓解生产爬坡阶段的现金流压力。`
- `在手订单集中于少数头部客户，虽然提升了收入可见性，但也意味着一定客户集中度风险。`

### Evidence Guidance

Prioritize:

- signed contract lists
- sampled contract review results from diligence
- finance-confirmed backlog summaries
- legal diligence when it verifies contract authenticity or key payment terms

If the company mixes:

- signed contracts
- framework agreements
- purchase orders
- NRE agreements

then distinguish them clearly in wording instead of treating them as fully equivalent backlog.

### Risk Awareness

This section can support the growth thesis, but do not overstate certainty.
If backlog includes many early-stage, cancelable, or low-prepayment projects, say so directly.
Carry meaningful contract-quality concerns into the risk section when needed.

## Starter Markdown Template For Section 2.8

```md
### 2.8 在手订单

| 客户名称 | 签约时间 | 产品内容 | 合同金额（万元） | 预付款比例 |
| --- | --- | --- | --- | --- |
| 待补充 | 待补充 | 待补充 | 待补充 | 待补充 |
| 待补充 | 待补充 | 待补充 | 待补充 | 待补充 |

订单分析：待补充
```

## Style Guidance For Section 2.8

Follow the reference page logic:

- show the contract table clearly
- then add short analysis instead of stopping at the list
- pay attention to prepayment terms and order quality
- connect backlog to revenue visibility and execution risk

This section should help the IC understand whether the company's near-term growth has real signed support behind it.

## Section 2.9 Financial Analysis - Balance Sheet

Write `2.9 财务分析-资产负债表（单位：万元）` as a structured financial review section.
This section should present the balance sheet in table form and then comment on the major line items with high absolute amount or high balance-sheet share.

### Data Horizon Rule

Show at least `两年一期` of data by default.
If the materials contain `三年一期`, then use `三年一期`.
If the latest period is an interim period such as `2026/02/28`, it is acceptable to show that latest一期 together with the prior year-end periods, as long as the dates are clearly labeled.

Keep all figures in `万元`.

### Split-Page Rule

This section usually needs to be split into two pages because one page cannot hold all line items clearly:

1. `资产类科目`
2. `负债和所有者权益`

Do not force both onto one crowded page unless the line items are extremely limited.

### Page 1: 资产类科目

Use a table for the asset side.
Common rows include:

- `货币资金`
- `交易性金融资产`
- `应收账款`
- `预付款项`
- `其他应收款`
- `存货`
- `合同资产`
- `其他流动资产`
- `流动资产合计`
- `长期股权投资`
- `固定资产`
- `无形资产`
- `商誉`
- `长期待摊费用`
- `非流动资产合计`
- `资产总计`

Adjust the rows according to the actual financial statements.
Do not invent line items not present in the source statements.

### Page 2: 负债和所有者权益

Use a separate table for liabilities and equity.
Common rows include:

- `短期借款`
- `应付账款`
- `预收款项`
- `合同负债`
- `应付职工薪酬`
- `应交税费`
- `其他应付款`
- `流动负债合计`
- `非流动负债合计`
- `负债合计`
- `实收资本`
- `资本公积`
- `未分配利润`
- `所有者权益合计`
- `负债和所有者权益总计`

Adjust the rows to match the actual statement structure used in the source materials.

### Table Presentation Rules

Use the reporting dates as column headers.
A typical structure is:

- `2026/02/28`
- `2025/12/31`
- `2024/12/31`
- `2023/12/31`

Keep the same date set across the asset page and the liabilities/equity page.
Preserve statement order as much as possible so the report remains reconcilable to the original financial statements.

### Required Analysis After The Tables

After each table, add short text analysis for the line items with high amount, high share, or strong change significance.
Do not mechanically explain every row.

Prioritize analysis of:

- large cash balances
- major receivables
- large prepayments
- inventory
- major fixed assets or long-term investments
- contract liabilities or advance receipts
- payable structure
- capital structure
- accumulated losses or retained earnings deficits

### Writing Rules For The Analysis

Each analysis point should answer two things:

1. what the item is
2. why it matters

Good analysis statements often include:

- composition of the balance
- aging or maturity profile
- major counterparties
- whether the item reflects healthy operating support or potential risk
- whether the balance is temporary or structural

Examples:

- `货币资金占总资产比例较高，说明公司账面流动性较充裕。`
- `应收账款账期主要在1年内，但客户集中度较高，仍需关注回款节奏。`
- `预付款项主要对应晶圆代工或关键材料采购，反映公司上游资源锁定需求较强。`
- `未分配利润持续为负，说明公司仍处于投入期，尚未实现稳定盈利积累。`

### Materiality Rule

Do not analyze immaterial balances just to fill space.
Only comment on:

- high-share items
- unusual items
- fast-growing items
- items relevant to the investment thesis or risk judgment

### Evidence Guidance

Prioritize:

- audited financial statements
- finance diligence reports
- management accounts when clearly labeled
- notes to the financial statements

If the source statement and diligence commentary differ, prefer the statement figures and use the commentary only to interpret composition or risk.

### Tone Guidance

This section should stay analytical but disciplined.
Do not turn it into a generic finance textbook explanation.
Focus on what the balance sheet reveals about liquidity, capital intensity, operating model, and risk.

## Starter Markdown Template For Section 2.9

```md
### 2.9 财务分析-资产负债表（单位：万元）

#### 资产类科目

| 资产 | 2025/12/31 | 2024/12/31 | 2023/12/31 |
| --- | --- | --- | --- |
| 货币资金 | 待补充 | 待补充 | 待补充 |
| 应收账款 | 待补充 | 待补充 | 待补充 |
| 预付款项 | 待补充 | 待补充 | 待补充 |
| 存货 | 待补充 | 待补充 | 待补充 |
| 流动资产合计 | 待补充 | 待补充 | 待补充 |
| 固定资产 | 待补充 | 待补充 | 待补充 |
| 非流动资产合计 | 待补充 | 待补充 | 待补充 |
| 资产总计 | 待补充 | 待补充 | 待补充 |

资产分析：待补充

#### 负债和所有者权益

| 负债和所有者权益 | 2025/12/31 | 2024/12/31 | 2023/12/31 |
| --- | --- | --- | --- |
| 应付账款 | 待补充 | 待补充 | 待补充 |
| 预收款项/合同负债 | 待补充 | 待补充 | 待补充 |
| 流动负债合计 | 待补充 | 待补充 | 待补充 |
| 负债合计 | 待补充 | 待补充 | 待补充 |
| 实收资本 | 待补充 | 待补充 | 待补充 |
| 资本公积 | 待补充 | 待补充 | 待补充 |
| 未分配利润 | 待补充 | 待补充 | 待补充 |
| 所有者权益合计 | 待补充 | 待补充 | 待补充 |
| 负债和所有者权益总计 | 待补充 | 待补充 | 待补充 |

负债和所有者权益分析：待补充
```

## Style Guidance For Section 2.9

Follow the reference page logic:

- split assets and liabilities/equity into two pages
- use balance-sheet rows that match the source statements
- keep the unit fixed at `万元`
- analyze only the large or meaningful balances

This section should help the IC quickly understand the company's asset structure, liabilities profile, capital base, and the main balance-sheet signals behind the business.

## Section 2.9 Financial Analysis - Income Statement

Write `2.9 财务分析-利润表（单位：万元）` as a table-based operating performance section.
This section is similar in logic to the balance-sheet section, but it usually fits on one page.

### Data Horizon Rule

Show at least `两年一期` of data by default.
If the materials contain `三年一期`, then use `三年一期`.
If a latest interim period is available and relevant, it can be included together with historical annual periods as long as the dates are clearly labeled.

Keep all figures in `万元`.

### Page Layout Rule

The income statement generally fits on one page.
Do not split it unless the source statement is unusually detailed or the template explicitly requires more room.

### Table Structure

Use the reporting dates as column headers.
Common rows include:

- `营业收入`
- `营业成本`
- `毛利`
- `毛利率`
- `税金及附加`
- `销售费用`
- `管理费用`
- `研发费用`
- `财务费用`
- `营业利润`
- `利润总额`
- `净利润`
- `调整后净利润` when the materials explicitly provide it

Adjust the rows according to the actual statements and the fund's reporting habit.
Do not invent metrics not supported by the materials.

### Required Analysis After The Table

After the table, add short analysis for the most important profit-and-loss drivers.
Do not explain every row.

Prioritize analysis of:

- revenue growth or decline
- gross margin level and trend
- expense structure
- R&D投入强度
- sales efficiency
- operating leverage
- profit turning points
- whether adjusted profit meaningfully differs from accounting net profit

### Writing Rules For The Analysis

Each point should explain:

1. what changed or what matters
2. what it implies for the business

Examples:

- `营业收入保持较快增长，说明公司商业化推进已有初步成效。`
- `毛利率持续提升，反映产品结构优化或规模效应开始显现。`
- `研发费用率维持高位，说明公司仍处于较强投入阶段。`
- `净利润仍为负，但亏损收窄，表明公司接近盈亏平衡点。`

### Evidence Guidance

Prioritize:

- audited financial statements
- finance diligence reports
- management accounts when clearly labeled
- notes to the statements when needed to explain unusual items

## Starter Markdown Template For Income Statement

```md
#### 2.9 财务分析-利润表（单位：万元）

| 利润表项目 | 2025/12/31 | 2024/12/31 | 2023/12/31 |
| --- | --- | --- | --- |
| 营业收入 | 待补充 | 待补充 | 待补充 |
| 营业成本 | 待补充 | 待补充 | 待补充 |
| 毛利 | 待补充 | 待补充 | 待补充 |
| 毛利率 | 待补充 | 待补充 | 待补充 |
| 销售费用 | 待补充 | 待补充 | 待补充 |
| 管理费用 | 待补充 | 待补充 | 待补充 |
| 研发费用 | 待补充 | 待补充 | 待补充 |
| 财务费用 | 待补充 | 待补充 | 待补充 |
| 营业利润 | 待补充 | 待补充 | 待补充 |
| 净利润 | 待补充 | 待补充 | 待补充 |

利润表分析：待补充
```

## Style Guidance For Income Statement

Follow the reference page logic:

- usually keep it to one page
- focus analysis on收入、毛利、费用和利润变化
- use only statement-supported metrics

This section should help the IC understand revenue quality, cost structure, and the company's path toward or away from profitability.

## Section 2.9 Financial Analysis - Cash Flow Statement

Write `2.9 财务分析-现金流量表（单位：万元）` as a table-based cash generation section.
This section follows a similar logic to the balance-sheet section, but may require two pages or more when line items are numerous.

### Data Horizon Rule

Show at least `两年一期` of data by default.
If the materials contain `三年一期`, then use `三年一期`.
Keep all figures in `万元`.

### Split-Page Rule

The cash flow statement may require `2页或更多` depending on the number of line items and the user's template.
Split the page when needed to preserve readability.
Common split logic includes:

1. operating cash flow items
2. investing and financing cash flow items

or

1. detailed cash flow line items
2. summary plus analysis

Choose the simpler structure that best matches the source statements.

### Table Structure

Use the reporting dates as column headers.
Common rows include:

- `销售商品、提供劳务收到的现金`
- `收到其他与经营活动有关的现金`
- `购买商品、接受劳务支付的现金`
- `支付给职工以及为职工支付的现金`
- `支付的各项税费`
- `支付其他与经营活动有关的现金`
- `经营活动产生的现金流量净额`
- `投资活动产生的现金流量净额`
- `筹资活动产生的现金流量净额`
- `现金及现金等价物净增加额`

Adjust the rows according to the actual statements and the level of detail needed for the report.

### Required Analysis After The Table

After the table, add short analysis for the major cash flow signals.
Do not explain every row.

Prioritize analysis of:

- whether operating cash flow is positive or negative
- whether losses are translating into cash burn
- relationship between revenue growth and cash collection
- capital expenditure burden
- dependence on external financing
- prepayments and customer advances that support cash flow
- whether cash inflow quality is improving

### Writing Rules For The Analysis

Each point should explain:

1. what the cash flow pattern is
2. why it matters for the investment case

Examples:

- `经营活动现金流持续为负，说明公司仍处于投入期，业务扩张尚未转化为稳定经营现金回流。`
- `客户预付款比例较高，对经营现金流形成一定支撑。`
- `筹资活动现金流是现金增长的主要来源，说明公司当前仍依赖外部融资支持扩张。`
- `资本开支阶段性上升，与产线、设备或研发平台建设相关。`

### Evidence Guidance

Prioritize:

- audited cash flow statements
- finance diligence reports
- cash collection summaries
- explanatory notes around capex, financing, or unusual payments

### Tone Guidance

This section should focus on cash conversion and financing dependence.
Do not confuse profit with cash generation.
The aim is to help the IC understand whether the business can fund itself, how quickly it burns cash, and what role external capital still plays.

## Starter Markdown Template For Cash Flow Statement

```md
#### 2.9 财务分析-现金流量表（单位：万元）

| 现金流量表项目 | 2025/12/31 | 2024/12/31 | 2023/12/31 |
| --- | --- | --- | --- |
| 销售商品、提供劳务收到的现金 | 待补充 | 待补充 | 待补充 |
| 购买商品、接受劳务支付的现金 | 待补充 | 待补充 | 待补充 |
| 支付给职工以及为职工支付的现金 | 待补充 | 待补充 | 待补充 |
| 经营活动产生的现金流量净额 | 待补充 | 待补充 | 待补充 |
| 投资活动产生的现金流量净额 | 待补充 | 待补充 | 待补充 |
| 筹资活动产生的现金流量净额 | 待补充 | 待补充 | 待补充 |
| 现金及现金等价物净增加额 | 待补充 | 待补充 | 待补充 |

现金流量表分析：待补充
```

## Style Guidance For Cash Flow Statement

Follow the reference page logic:

- allow two or more pages when needed
- focus on operating cash flow, capex, financing dependence, and cash conversion
- keep the unit fixed at `万元`
- analyze only the lines that matter for liquidity and funding

This section should help the IC understand how the business turns contracts and accounting profit into real cash, and how dependent it remains on outside capital.

## Section 2.10 Financial Forecast

Write `2.10 盈利预测` as a forward-looking financial section.
This section should usually include:

1. a `未来3-5年` forecast profit table
2. supporting forecast assumptions or short analytical commentary
3. optional revenue breakdown by business line, product, customer type, or application when that helps explain the model

Keep the unit in `万元`.

### Forecast Horizon Rule

Default to `未来3年` when the materials are limited.
Use `未来5年` when the user materials already contain a longer forecast model or when the investment case depends on a medium-term scale-up path.

Do not fabricate precision beyond what the materials support.
If outer years are highly uncertain, it is acceptable to keep the core table shorter and describe the longer-term direction qualitatively.

### Core Table Structure

Use a forecast profit table as the main exhibit.
Common rows include:

- `营业收入`
- `营业成本`
- `毛利`
- `毛利率`
- `销售费用`
- `管理费用`
- `研发费用`
- `财务费用`
- `营业利润`
- `净利润`

If the case uses adjusted profit logic, it is acceptable to add:

- `调整后净利润`

### Revenue Breakdown Option

Sometimes forecast revenue should be broken down further.
Do this when the business logic is not understandable from one top-line revenue row.

Useful breakdown dimensions include:

- by product line
- by business segment
- by application field
- by customer type
- by region

Examples:

- `Micro LED驱动芯片`
- `Micro OLED DDIC`
- `NRE收入`
- `标准化SaaS`
- `企业解决方案`

Only add a breakdown table when it truly helps explain the forecast.
Do not create unnecessary complexity for a simple business.

### Required Supporting Analysis

The forecast table should not stand alone.
Add supporting text that explains either:

1. the main forecast assumptions
2. the logic behind major revenue, margin, or profit changes

Useful assumptions or analytical angles include:

- shipment or order growth
- customer expansion
- new product launch ramp
- price assumptions
- yield or gross margin improvement
- capacity release
- expense ratio change
- R&D intensity trend
- operating leverage
- capex or investment phase transition

### Good Forecast Questions

The analysis should help answer questions such as:

- What is driving revenue growth?
- Is growth coming from volume, price, new customers, or new products?
- Why does gross margin improve or decline?
- When does the company achieve break-even or meaningful profitability?
- Which business lines contribute the most to future growth?

### Writing Rules For Forecast Analysis

Keep the analysis concise but explicit.
Usually `3-6` bullets or short paragraphs are enough.
Good analysis points often include:

- one forecast assumption
- one expected financial impact

Examples:

- `收入增长主要来自Micro LED产品放量及老客户采购份额提升。`
- `随着高毛利产品占比提升，预计整体毛利率将稳步改善。`
- `研发费用绝对额仍将增长，但费用率有望随收入规模扩大而逐步下降。`
- `公司预计于X年实现盈亏平衡，核心驱动来自收入放量与费用摊薄。`

### Evidence Guidance

Prioritize:

- company financial model
- management forecast assumptions
- diligence-adjusted forecast
- in-hand order and pipeline support
- product commercialization schedule
- market growth assumptions already established elsewhere in the report

If the forecast is management-provided and not independently stress-tested, preserve that distinction in wording.

### Tone Guidance

This section should be constructive but not promotional.
Treat the forecast as an analytical scenario, not as a guaranteed outcome.
If certain assumptions are aggressive, reflect that clearly in the wording or connect them to the risk section.

## Starter Markdown Template For Section 2.10

```md
### 2.10 盈利预测（单位：万元）

| 利润表预测项目 | 2026E | 2027E | 2028E |
| --- | --- | --- | --- |
| 营业收入 | 待补充 | 待补充 | 待补充 |
| 营业成本 | 待补充 | 待补充 | 待补充 |
| 毛利 | 待补充 | 待补充 | 待补充 |
| 毛利率 | 待补充 | 待补充 | 待补充 |
| 销售费用 | 待补充 | 待补充 | 待补充 |
| 管理费用 | 待补充 | 待补充 | 待补充 |
| 研发费用 | 待补充 | 待补充 | 待补充 |
| 财务费用 | 待补充 | 待补充 | 待补充 |
| 营业利润 | 待补充 | 待补充 | 待补充 |
| 净利润 | 待补充 | 待补充 | 待补充 |

预测假设/分析：待补充

可选收入拆解：待补充
```

## Style Guidance For Section 2.10

Follow the reference page logic:

- use a forward-looking profit table as the core exhibit
- pair the table with assumptions or analytical explanation
- add revenue breakdown only when it improves understanding
- make clear what drives growth and盈利改善

This section should help the IC judge whether the company's future earnings path is credible, what assumptions support it, and where the main uncertainty lies.

## Section 2.11 Comparable Companies

Write `2.11 可比公司` as a valuation-support section.
This section should usually include:

1. a comparable companies table
2. a short written interpretation of what the comps imply

The goal is not only to list market data, but to help the IC understand where the target company sits relative to listed peers in business model, scale, and valuation level.

### Table Structure

Use the following columns by default:

- `公司名称`
- `股票代码`
- `主营业务简介`
- `市值`
- `营收（亿元）`
- `净利润（亿元）`
- `PS`
- `PE`

You may add columns such as `交易所` or `备注` only when they materially improve clarity.

### Key Data Rule

For `营收（亿元）` and `净利润（亿元）`, use the **最近一个完整年度** data.
Do not mix trailing twelve months, interim period, or forecast-year figures into this table unless the user explicitly asks for them.

If the company is loss-making and `PE` is not meaningful, write `N.M.` or another consistent non-meaningful marker rather than forcing a number.

### Comp Selection Rule

Choose comparable companies based on actual business similarity, not just broad sector labels.
Useful similarity dimensions include:

- product type
- end market
- business model
- technology route
- stage of commercialization
- customer profile

It is acceptable to mix domestic and overseas comps when the domestic market lacks perfect matches.
If the comp set is mixed-quality, make that limitation explicit in the written commentary.

### Writing Rules For The Table

Keep `主营业务简介` short and functional.
It should help the IC understand why the company is included in the comp set.

Good examples:

- `主营Micro LED驱动芯片及显示相关IC`
- `面向先进封装设备的高端装备厂商`
- `提供企业级零售SaaS与智能终端解决方案`

Do not write promotional descriptions.

### Required Commentary After The Table

After the table, add a short interpretation section.
Do not stop at the table.

The commentary should explain:

- what the comp set tells us about market valuation range
- which comps are the closest and which are only reference anchors
- whether the target company should trade at a premium, discount, or in-line multiple, and why
- what limitations exist in the comp methodology

### Good Commentary Questions

The written analysis should help answer questions such as:

- Are there true direct comparables, or only partial analogs?
- Where does the target company sit relative to peers on growth, profitability, and technological position?
- Which metric is more meaningful in this case, `PS` or `PE`?
- If the company is early-stage or loss-making, should valuation focus more on revenue and growth than earnings?

### Writing Rules For Commentary

Keep the commentary concise but judgmental.
Usually `3-6` bullets or short paragraphs are enough.
Useful angles include:

- valuation band
- growth versus profitability tradeoff
- whether listed peers are more mature than the target
- whether the target deserves a premium for faster growth or a discount for execution risk

Examples:

- `可比公司整体PS区间为X-Y倍，考虑到目标公司仍处于早期放量阶段，PS相较PE更具参考意义。`
- `若与更成熟的上市公司相比，目标公司在规模和盈利能力上仍有差距，因此估值不宜简单套用头部公司倍数。`
- `部分可比公司在技术路线或应用场景上仅部分重合，因此该组可比更多用于提供估值锚点，而非严格一一对应。`

### Evidence Guidance

Use the same口径 across all companies in the table.
Ensure:

- market value uses one consistent observation date or period
- revenue and net profit use the latest full fiscal year
- PS and PE are calculated or quoted consistently

If different geographies use different fiscal calendars, keep that in mind and note it if necessary.

### Tone Guidance

This section should support valuation discussion without creating false precision.
Comparable companies are an anchor, not the final answer.
Be explicit when the comp set is imperfect.

## Starter Markdown Template For Section 2.11

```md
### 2.11 可比公司

| 公司名称 | 股票代码 | 主营业务简介 | 市值 | 营收（亿元） | 净利润（亿元） | PS | PE |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 |
| 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 |

可比公司分析：待补充
```

## Style Guidance For Section 2.11

Follow the reference page logic:

- use a structured comps table first
- keep revenue and net profit on the latest full-year basis
- then explain what the comp set means for valuation
- be honest about imperfect comparability

This section should help the IC understand the valuation anchor set, the target company's relative positioning, and the limits of market-based comparison.

## Section 3 Industry Analysis

Write `03 行业分析` as a modular chapter.
Every subsection in this chapter may span more than one page when the case requires it.
Do not compress complex industry material into one page per heading if that would reduce clarity.

The purpose of this chapter is to explain the product's industry context, policy backdrop, demand logic, value-chain position, market size, competitive landscape, and future direction.

## Section 3.1 Product Or Service Industry Introduction

Write `3.1 XXX简介`, where `XXX` refers to the company's most important product or service.
This section should define what the product or service is, how it is classified, and how different technical routes compare.

### Core Content

This section should usually include:

1. product or service definition
2. product classification
3. technical route comparison

### Writing Rules

Start by answering:

- what the product/service is
- where it sits in the industry
- how the market usually classifies it

Then explain the major technical routes or solution paths.
For route comparison, focus on dimensions such as:

- core principle
- performance
- cost
- maturity
- application suitability
- key tradeoffs

If the route comparison is important, use a table.
Useful columns include:

- `技术路线`
- `核心原理`
- `主要优势`
- `主要劣势`
- `适用场景`
- `产业化阶段`

### Style Guidance For Section 3.1

This section can use one or multiple pages.
The goal is to help the IC understand the technical and commercial context of the company's core product before discussing the broader industry.

## Section 3.2 Industry Policy

Write `3.2 行业政策` in table form.
Use it to summarize the most relevant policies affecting the industry.

### Table Structure

Use the following columns by default:

- `政策名称`
- `发布时间`
- `内容简介`
- `可能的行业影响`

### Writing Rules

Select only policies that materially affect:

- demand creation
- subsidy or procurement direction
- technology localization
- compliance thresholds
- industrial investment
- standard setting

Avoid generic macro policies unless they directly shape the industry.

### Style Guidance For Section 3.2

This section may span more than one page when policy history is important.
Prefer concise policy summaries and practical impact interpretation over long quotation blocks.

## Section 3.3 Industry Pain Points And Drivers

Write `3.3 行业痛点及驱动因素` as an analytical section.
This section should explain both:

- what problems or frictions exist in the industry today
- what forces are driving change, adoption, or growth

### Structure

You may use:

1. paired `痛点` / `驱动因素` bullets
2. a two-column table
3. separate short subsections for pain points and drivers

### Common Pain-Point Angles

- high cost
- low yield
- poor efficiency
- supply bottlenecks
- labor dependence
- weak standardization
- poor customer experience
- limited domestic substitution

### Common Driver Angles

- policy support
- downstream demand growth
- cost reduction
- technology maturation
-国产替代
- AI or digitalization demand
- new application scenarios

### Style Guidance For Section 3.3

This section should make the industry logic feel inevitable rather than abstract.
Tie each pain point and driver back to why the target company is relevant.

## Section 3.4 Industry Chain

Write `3.4 产业链情况` as a table-led section with supporting commentary.
This section should explain what each major link in the value chain does, which companies are typical players, which links hold bargaining power, and where the profit pool is concentrated.

### Table Structure

Use a table with columns such as:

- `环节`
- `主要职责/做什么`
- `典型公司`
- `主导权`
- `利润水平/利润归属`

You may rename the last two columns slightly when needed, but the meaning should stay the same.

### Writing Rules

For each value-chain link, explain:

- what the link contributes
- what type of companies dominate it
- whether the link controls standards, customers, technology, channels, capacity, or profit allocation

After the table, add short commentary on:

- which link captures the most profit
- where the target company sits
- whether the target company's link has strategic leverage or margin pressure

### Style Guidance For Section 3.4

This section can span multiple pages if the chain is complex.
Keep the table clean, then use text to explain profit distribution and bargaining structure.

## Section 3.5 Market Size

Write `3.5 市场规模` as a chart-plus-text section.
This section should explain the overall market size, relevant sub-segment market size, and how the estimates are derived.

### Core Content

This section should usually include:

1. overall market size
2. sub-segment market size
3. source or calculation method
4. growth trend

### Writing Rules

Use charts when possible.
If charting is not available, structure the market-size data in a compact table and describe the trend clearly.

Always explain where the market-size figures come from.
Valid approaches include:

- cited third-party report
- industry association data
- public company disclosures
- bottom-up estimate based on shipments, ASP, penetration, installed capacity, or customer count assumptions

When using third-party reports, cite the source by name.
When using a bottom-up estimate, describe the key assumptions explicitly.

### Style Guidance For Section 3.5

This section may take multiple pages when both broad and niche markets matter.
The point is not only to show a big number, but to convince the IC that the market estimate is reasoned and relevant to the target.

## Section 3.6 Competitive Landscape

Write `3.6 竞争格局` as a list- or table-based competitive review.
This section should identify the main competitors and explain their business positioning, market role, financial scale, and market value or valuation where relevant.

### Core Content

For each key competitor, include:

- competitor name
- business and positioning summary
- market or technology status
- financial data when available
- market value or valuation when available

### Presentation Options

Use either:

1. a structured list with one competitor per block
2. a comparison table

Useful table columns include:

- `公司名称`
- `业务简介`
- `行业地位`
- `营收/利润`
- `市值/估值`
- `与目标公司的关系`

### Writing Rules

Do not only name competitors.
Explain:

- who leads the market
- who occupies adjacent niches
- where the target company overlaps or differentiates
- whether the landscape is fragmented or concentrated

### Style Guidance For Section 3.6

This section may require more than one page when there are both domestic and overseas players.
Use clear competitive categories if needed, such as international leaders, domestic leaders, niche challengers, and substitute routes.

## Section 3.7 Future Trends

Write `3.7 未来的发展趋势` as a forward-looking industry section.
This section should explain how the industry is likely to evolve over the next several years.

### Typical Trend Angles

- technology migration
- cost curve decline
- supply-chain localization
- customer concentration changes
- software-hardware integration
- AI enablement
- product standardization
- premiumization or commoditization
- capacity expansion
- policy tightening or support continuation

### Writing Rules

Do not make this section a generic trend list.
Focus on the trends that matter most to:

- the industry's growth path
- the target company's strategic position
- timing of investment returns

Use `3-6` well-supported trends by default.
Each trend should contain:

1. the direction of change
2. why it is happening
3. what it means for the target company

### Style Guidance For Section 3.7

This section can span multiple pages if needed.
The goal is to close the chapter by showing where the industry is going and whether the target company is aligned with that direction.

## Style Guidance For Chapter 03

Follow these principles across the whole industry chapter:

- every subsection may span multiple pages
- move from definition to structure to scale to competition to future direction
- combine tables, charts, and concise text instead of long prose walls
- always connect industry facts back to the target company's strategic relevance

This chapter should help the IC answer not just whether the industry is attractive, but whether the company is positioned in the right place within it.

## Section 4.1 Decision Items

Write `4.1 决议事项` by repeating the same core transaction table used in `1.1 项目概述`.
This page is the final decision-summary page for the investment committee.

### Core Rule

Reuse the `1.1 项目概述` table structure directly.
Do not redesign the fields unless the user explicitly asks for a different IC format.

Use these rows by default:

- `投资主体`
- `投资金额`
- `投前估值`
- `本轮融资总额`
- `本轮其他投资人情况`
- `交易结构`
- `核心条款`
- `退出路径`

### Writing Rules

Keep the wording aligned with the latest agreed transaction terms.
If any term changed during diligence or negotiation, make sure `4.1` reflects the final IC version rather than the initial summary version.

If some items remain unresolved, mark them clearly as:

- `待补充`
- `待确认`
- `以正式交易文件为准`

### Purpose Of This Page

This page should let the IC see, in one place, exactly what is being approved.
It is acceptable for this page to closely resemble `1.1`, because its role is to restate the final decision package rather than introduce new analysis.

## Starter Markdown Template For Section 4.1

```md
## 04 决议事项

### 4.1 决议事项

| 项目 | 内容 |
| --- | --- |
| 投资主体 | 待补充 |
| 投资金额 | 待补充 |
| 投前估值 | 待补充 |
| 本轮融资总额 | 待补充 |
| 本轮其他投资人情况 | 待补充 |
| 交易结构 | 待补充 |
| 核心条款 | 待补充 |
| 退出路径 | 待补充 |
```

## Style Guidance For Section 4.1

Follow the reference page logic:

- repeat the `1.1` transaction table
- use the latest final terms
- keep the page concise and approval-oriented

This section should function as the final IC decision snapshot.

## Appendix Interview Notes

Write `附录 访谈纪要` using a one-interviewee-per-page format.
Each interview subject should usually have an independent page.

### Core Page Structure

For each interviewee, structure the page in three layers:

1. a basic information table
2. `纪要核心要点`
3. `访谈评价`

### Basic Information Table

Use a two-column table by default:

- `项目`
- `内容`

Common rows include:

- `访谈日期`
- `访谈对象`
- `对象背景`
- `参访人员`
- `访谈形式`

Add or remove rows only when the interview format requires it.

### Field Rules

Fill the rows using these rules:

- `访谈日期`: Use the actual interview date.
- `访谈对象`: Include the interviewee's name, title, and organization.
- `对象背景`: Briefly explain why this person matters, such as their employer, role in the value chain, purchasing authority, technical authority, or direct relationship with the target company.
- `参访人员`: List the investor-side participants, company participants, or diligence participants when available.
- `访谈形式`: Describe the format, such as face-to-face, video call, phone call, site visit, or customer diligence interview.

### Core Notes Section

After the table, add `纪要核心要点`.
Summarize the interview using concise bullet points.
Each bullet should focus on a specific conclusion or observation rather than a verbatim conversation log.

Useful content includes:

- cooperation content
- technical verification
- procurement or usage status
- product evaluation
- order outlook
- cooperation model
- supplier/customer relationship
- business process details
- perceived strengths and risks

Prefer fact-rich bullets over long narrative paragraphs.

### Interview Evaluation

End each page with a short `访谈评价` block.
This is not a transcript summary; it is the investor-side interpretation of what the interview means.

The evaluation should answer:

- whether the interview supports or weakens the investment thesis
- whether the interview verified a key claim
- what risks or uncertainties remain
- whether follow-up verification is still needed

Keep this section concise and judgment-oriented.

### Writing Rules

Do not convert the interview page into a full narrative article.
Keep it structured, factual, and easy to scan.
Avoid over-polishing interview content into marketing language.

If the interview contains uncertainty or contradiction, preserve it.
Do not smooth over mixed signals.

### Evidence Guidance

Prioritize:

- interview transcript
- meeting notes
- diligence memo
- follow-up confirmation notes

If the interviewee statement is unverified, make that clear in wording.

### Confidentiality Guidance

If names or companies must be anonymized, preserve a consistent anonymization style.
Even when anonymized, keep enough context for the IC to understand the person's role in the ecosystem.

## Starter Markdown Template For Appendix Interview Notes

```md
## 附录 访谈纪要

### 访谈纪要：访谈对象A

| 项目 | 内容 |
| --- | --- |
| 访谈日期 | 待补充 |
| 访谈对象 | 待补充 |
| 对象背景 | 待补充 |
| 参访人员 | 待补充 |
| 访谈形式 | 待补充 |

纪要核心要点：

- 待补充
- 待补充
- 待补充

访谈评价：待补充
```

## Style Guidance For Appendix Interview Notes

Follow the reference page logic:

- one interviewee per page
- start with a basic information table
- use bullets for core notes
- end with a short evaluation

This appendix should help the IC quickly absorb third-party validation, customer feedback, expert views, and remaining uncertainties from interviews.

## Output Standard

Write for an investment committee, not for fundraising.
Lead with facts, transaction structure, and decision implications.
When a user gives a page screenshot or visual sample, follow the information structure first and the wording style second.
