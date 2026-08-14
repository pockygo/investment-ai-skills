---
name: toujue-baogao
description: Create, complete, and revise Chinese internal investment decision reports and IC materials from real deal materials, with a compact AI-oriented public-information task list and a controlled evidence backfill workflow. Use when Codex needs to draft or update a 投决报告, 投委会材料, 投资决策报告, IC memo, 待补充内容清单, 公开信息补充结果, or backfill policies, industry data, competitors, market values, financial performance, transaction terms, diligence findings, and interview evidence.
---

# 投决报告

## Goal

Create a decision-oriented Chinese 投决报告 from real project materials.
The report should help the investment committee decide whether to approve the transaction, under what terms, and with what unresolved risks or conditions.

## Required Reference

Before drafting, outlining, or revising any report section, read `references/report-writing-guide.md`.
That guide contains the full chapter structure, section-by-section page logic, table fields, analysis rules, and appendix format defined by the user.

For a full report, treat the reference as a binding specification, not optional guidance.
Do not replace its structure with a shorter IC memo unless the user explicitly requests a condensed version.

For a full report, missing-information register, public-evidence search, or report backfill task, also read `references/gap-register-guide.md`.

## Default Inputs

Expect the user to provide some combination of:

- `bp-reader` output
- `deep-industry-research` output
- BP or pitch deck
- financing plan, cap table, and term sheet
- legal, financial, technical, or commercial diligence materials
- management, customer, supplier, and expert interview notes
- financial statements, forecasts, customer lists, supplier lists, orders, and contracts
- comparable-company or valuation materials

Treat the materials as an evidence set.
Distill them into the report instead of copying source text mechanically.

## Default Chapter Structure

Use this structure unless the user changes it:

1. `01 项目概述`
2. `02 项目分析`
3. `03 行业分析`
4. `04 决议事项`
5. `附录 访谈纪要` when interview notes are available

## Core Workflow

1. Build a source inventory and identify which materials support each section.
2. Extract transaction terms first, especially investment entity, amount, valuation, round size, other investors, transaction structure, core terms, and exit route.
3. Draft `1.1 项目概述` as the anchor transaction table.
4. Create the complete heading and table skeleton required by `references/report-writing-guide.md` before filling content.
5. Fill every chapter using the section rules in the reference.
6. Mark unknown fields as `待补充`, `待确认`, or `以正式交易文件为准`; do not invent missing facts.
7. Separate verified evidence, company-stated claims, investor analysis, and unresolved issues.
8. Build the compact public-information task list using `references/gap-register-guide.md`.
9. Put company-only, transaction-only, interview, and adviser-verification gaps in the supplementary diligence question list, not in the public-information task list.
10. Run the completeness gates in this skill before delivery.
11. Keep the writing formal, concise, factual, and investment-committee oriented.

## Non-Negotiable Completeness Rules

Apply these rules whenever the user requests a full report:

1. Preserve every default section required by `references/report-writing-guide.md`, including sections whose supporting data is missing.
2. Never omit a section because evidence is unavailable. Keep its heading, required table fields, and analysis slot, then write `待补充`, `待确认`, or a precise evidence limitation.
3. Do not merge sections that the reference treats separately. In particular:
   - `1.3 项目亮点` is not a substitute for `2.5 竞争优势`.
   - `2.7 客户情况` is not a substitute for `2.8 在手订单`.
   - `2.9 财务分析` is not a substitute for `2.10 盈利预测`.
   - industry summary prose is not a substitute for `3.2 行业政策`, `3.3 行业痛点及驱动因素`, `3.4 产业链情况`, or `3.7 未来的发展趋势`.
4. Keep the required table labels and units. Do not casually rename fields such as `投前估值`, `本轮融资总额`, or `预付款比例`.
5. Present balance sheet assets, balance sheet liabilities/equity, income statement, and cash flow statement separately under `2.9`. If current statements are missing, preserve the tables and mark the missing periods and line items.
6. Use the latest full-year basis for comparable-company financials. If unavailable, keep the current-period table as `待补充`; label older market data as historical and do not present it as current.
7. Repeat the complete `1.1 项目概述` transaction table in `4.1 决议事项`, updated for the latest proposed terms.
8. When interview notes exist, use one interviewee per page or page-break block, with a basic information table, `纪要核心要点`, and `访谈评价`.
9. Additional analytical sections are allowed, but they may not replace or renumber the required sections.
10. Only omit or combine a required section when the user explicitly directs that structural change. State the deviation in the deliverable.

## Evidence And Placeholder Rules

- Missing data changes the cell content, not the report structure.
- Distinguish `已核验事实`, `管理层口径`, `投资人分析`, and `待核验事项` in the wording.
- Do not mix confirmed revenue, signed orders, shipped products, in-validation products, and sales pipeline in one amount column.
- Do not present suggested investor protections as agreed transaction terms. Separate `已取得条款` from `建议争取条款`.
- When older materials are the only source, label the date and historical nature explicitly.
- Treat stale, undated, generic, or non-reconcilable data as a gap even when the report does not literally contain `待补充`.
- Separate gaps by acquisition route. Put only publicly searchable gaps in the Markdown task list. Put private deal, company, interview, and adviser gaps in the Word diligence list.

## Two-Stage Supplementation Workflow

### Stage 1: Materials-Based Draft

For a full report, default to these deliverables unless the user narrows the scope:

1. `<项目名>_投决报告_<日期>.md`
2. `<项目名>_待补充内容清单_<日期>.md`
3. `<项目名>_补充尽调问题清单_<日期>.docx`

The Markdown public-information task list must cover only gaps that can be fully or partially addressed through public research, including:

- stale or historical figures that require a current-period refresh
- generic policy references without exact title, issuer, date, or document number
- comparable-company figures without a unified observation date or latest full-year basis
- public market size, industry chain, technology route, competitor, patent, corporate-registration, and public legal information

Use exactly these five columns:

- `报告位置`
- `待补充事项`
- `搜索口径/资料要求`
- `证据标准`
- `回填位置`

Keep the list compact and optimized as an instruction set for another AI research pass. Merge related search tasks when they use the same source set and will be backfilled together.

Do not put company financial statements, customer POs, private supplier data, transaction agreements, employee files, or other non-public evidence in this Markdown list. Convert those gaps into the Word supplementary diligence question list.

Do not browse by default during Stage 1 unless the user requests current public research or the original task inherently requires current information.

### Stage 2: Public Evidence And Backfill

When the user asks to research the register:

1. Process every row in the public-information task list.
2. Browse the internet and prioritize primary sources:
   - government and regulator websites for policy
   - exchange filings, annual reports, and official investor relations releases for listed-company performance
   - exchange or reliable market-data pages for market value at a stated observation date
   - company product pages, patents, and formal disclosures for product and competitor facts
3. Produce `<项目名>_公开信息补充结果_<日期>.md` before editing the report.
4. Identify each result by the original `报告位置` and `待补充事项`; the compact list does not use gap IDs.
5. For every result, record source link, source date, observation date, evidence grade, data caliber, and proposed report wording.
6. Do not expand the search scope to company-private, transaction-private, interview, or adviser-verification gaps.
7. Unless the user explicitly authorizes direct backfill, present the search result for confirmation before updating the report.
8. After approval, update the report and the register together, preserve citations near the supported claims, and rerun all validation.

## Public Data Calibration Rules

- Policy: record exact policy title, issuing authority, publication date, document number when available, current validity, and project relevance.
- Listed-company performance: use the latest complete fiscal year and cite the annual report or formal results release.
- Market value: state the observation date, exchange, share class, and currency. State the FX date and rate when converting currencies.
- Valuation multiples: use consistent dates and financial periods. Write `N.M.` when PE is not meaningful.
- Private-company valuation: use only disclosed financing or transaction evidence and label its date and nature. Do not equate financing headlines with current fair value.
- Industry data: distinguish third-party estimates, issuer calculations, and investor calculations.
- Conflicting sources: prefer the most recent authoritative primary source and document the conflict.
- Search failure: write `公开渠道未检索到可靠信息`; do not fill the gap with weak inference.

## Completeness Gate

Before delivery:

1. Run:

   `python3 scripts/validate_report_structure.py <report.md>`

2. Run:

   `python3 scripts/validate_gap_register.py <gap-register.md>`

3. Add `--no-interviews` to the report validator only when the source package contains no interview notes.
4. Fix every reported error. Do not deliver a full report or gap register with validator errors.
5. Manually confirm that every table contains either evidence-backed content or an explicit placeholder.
6. Manually compare `1.1` and `4.1` to ensure the transaction terms are aligned.
7. Reconcile each public-search task to its report backfill location.
8. Confirm that the Markdown list has exactly five columns and contains no company/private diligence requests.
9. Report any user-directed structural deviation in the final response.

## Output Expectations

Default to the three Stage 1 deliverables for a full report. Use Markdown for the report and compact public-information task list, and Word for the supplementary diligence question list. If the user explicitly requests only one format or artifact, follow that scope.

The report should:

- lead with the transaction and decision ask
- preserve the full reference structure unless the user explicitly requests a condensed report
- use tables for structured factual pages
- use short analysis paragraphs after tables when interpretation is required
- include risks and mitigations in the main body
- connect industry analysis back to the target company's investability
- keep appendix interview notes one interviewee per page
- provide a separate, compact public-information task list with the required five-column schema
- separate public-search tasks from company, transaction, interview, and adviser-verification requests
- keep public-search results reviewable before report backfill

## Quality Bar

The report should let an IC member quickly understand:

- what is being approved
- why the company is attractive
- why this company can win
- what the key evidence says
- where the major risks remain
- whether the terms and valuation are supportable
