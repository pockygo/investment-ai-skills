# Fixed framework and drafting rules

## Contents

1. Fixed report architecture
2. Evidence matrix
3. Issue selection and ordering
4. Drafting rules by block
5. Supplemental updates
6. Coverage and quality gates
7. Lessons distilled from the retained example

## 1. Fixed report architecture

Keep this order and wording. Company-specific issue titles and update topics may change; the three top-level chapters may not.

1. Cover: `[公司全称]`, `法务尽职调查报告`, `[部门名称]`, `[YYYY年M月]`.
2. 目录.
3. `一、法务尽调背景情况`: paragraph 1 identifies the internal reviewer, target, cutoff, and scope; paragraph 2 identifies third-party counsel/report/date, review status, and supplemental period or missing supplemental material.
4. `二、主要法律问题`: repeat `（一）[问题标题]` → `1、详细描述` → `根据《法律尽调报告》：` → facts/table → `2、风险分析` → internal analysis → `3、处理建议` → protections.
5. `三、补充尽调期间公司情况的更新`: repeat `（一）[更新主题]` with numbered subtopics or concise update paragraphs.

Default to all three sub-blocks for each Chapter II issue. A block may be omitted only when it is truly inapplicable, the evidence matrix records why, and subsequent labels are renumbered continuously. Lack of information is not a reason to omit a block; write the limitation and residual risk.

## 2. Evidence matrix

Create one row per candidate issue:

| Field | Requirement |
|---|---|
| issue_id | Stable internal identifier |
| issue_title | Neutral, specific issue title |
| source_file | Exact filename/report title |
| source_locator | Page, chapter, table, clause, annex, or paragraph marker |
| source_type | Executed agreement, registry, counsel report, company statement, public record, initiation report, other |
| fact | Atomic fact; do not combine disputed alternatives |
| third_party_view | Counsel's conclusion, if any, clearly attributed |
| missing_material | Documents or confirmations not supplied |
| internal_analysis | Independent impact analysis and current-law basis |
| materiality | High / medium / low with rationale |
| deal_mechanism | CP, covenant, R&W, indemnity, escrow/price, consent/waiver, follow-up, other |
| supplemental_status | Open / partly remediated / remediated / worsened / unknown |
| inclusion | Include / combine / omit |
| disposition_reason | Required for combine or omit |

Maintain source locators even though the retained report does not display footnotes. This makes the draft auditable and prevents unattributed copying.

## 3. Issue selection and ordering

Include by default:

- unresolved high/material findings in any supplied diligence report;
- defects affecting ownership, control, capitalization, authority, title, licenses, core assets, key contracts, cash flow, tax exposure, sanctions, litigation, enforceability, or IPO/exit feasibility;
- triggered or near-triggered redemption, liquidation, anti-dilution, consent, default, or change-of-control provisions;
- missing evidence that prevents a material legal conclusion;
- incomplete remediation requiring a deal protection or dated follow-up.

Combine closely related findings only when they share the same root cause, consequence, and remediation. The retained example combined shareholder auction risk, nominee holding risk, and fund filing issues under `股东相关事宜`. Do not combine merely to shorten the report.

Omit a low/routine issue from Chapter II only when all are true: impact is limited, no core right/asset/permit is affected, no deal condition is needed, ordinary representations or housekeeping can address it, and the evidence matrix records the reason. Never omit an issue because the source report is long.

Order issues by decision relevance, normally: ownership/control and historical equity defects; investor rights and transaction conflicts; tax and quantified liabilities; shareholder/title/IPO blockers; capitalization and corporate compliance; core assets, premises, licenses, IP, key contracts; then other material compliance.

## 4. Drafting rules by block

### Detailed description

- Attribute the source: `根据《法律尽调报告》：`, `根据公司提供的……`, or `根据补充材料……`.
- State dates, parties, amounts, percentages, document names, deadlines, and status exactly.
- Preserve qualifications such as `根据公司相关人员说明`, `尚未提供`, and `截至尽调截止日`.
- Use a table only for repeated records such as tax events, shareholders, certificates, or contracts. Repeat header rows across pages.
- Do not insert internal recommendations into this block.

### Risk analysis

- Separate the governing rule, application to verified facts, consequence, probability/uncertainty, and transaction impact.
- Check current law against official sources when material. Specify historical law separately when judging an old act.
- Do not copy a long statute. Quote only the necessary proposition and paraphrase the rest.
- Explain effects on cash flow, ownership stability, enforceability, compliance, financing, operations, IPO/exit, or closing.
- When facts are missing, state what cannot be concluded and why.

### Handling recommendations

Translate each risk into a proportionate mechanism:

- `交割先决条件`: resolve before funding/closing.
- `交割后承诺`: remediate after closing with owner and deadline.
- `陈述与保证`: factual allocation and disclosure protection.
- `专项赔偿/托管/价款调整`: identifiable monetary exposure.
- `同意/豁免/确认文件`: third-party or regulator action required.
- `回购/交叉触发`: reserve for material failure affecting the investment thesis, control, exit, or listing; define the trigger precisely.
- `补充核查`: specify the missing document and responsible party.

Name the obligor, deliverable, timing, evidence of completion, and consequence of non-performance whenever supported by the transaction context.

## 5. Supplemental updates

Chapter III is a dated delta log, not a second risk list.

- State the supplemental period in Chapter I.
- Describe only new or changed facts after the base diligence cutoff.
- Link updates to open Chapter II issues in the private matrix.
- Distinguish executed from proposed status. A resolution is not proof that registration, payment, waiver, or transfer completed.
- State residual steps: unexecuted agreements, unpaid consideration, missing filings, incomplete registrations, or pending approvals.
- If no supplemental material was supplied, keep Chapter III and state that no supplemental materials were available and status could not be updated. Do not claim there were no changes.

## 6. Coverage and quality gates

Fail the draft if any answer is `no`:

- Does every source issue have an evidence-matrix disposition?
- Does every included fact have a locator and source type?
- Are company statements distinguished from documents and public records?
- Are third-party findings distinguished from internal conclusions?
- Are all material missing documents disclosed?
- Are current-law propositions verified as of the report date?
- Are historic acts analyzed under the law then in effect where relevant?
- Does every recommendation map to a specific issue and deal mechanism?
- Are supplemental updates separated from base findings and residual risk stated?
- Are names, dates, amounts, percentages, defined terms, and numbering consistent?
- Are the cover, TOC, three chapters, issue sub-blocks, header/footer, and page numbers present?
- Has every rendered page been inspected without clipping, overlap, broken tables, or unintended blank pages?

## 7. Lessons distilled from the retained example

The third-party report contained a 10-item issue list. The retained review selected seven: state-owned equity procedure, special investor rights, tax, shareholder/title matters, unpaid subsidiary capital, leased premises, and expired management-system certificates. It omitted subsidiary structure, bank notice/consent duties, and domain filing from Chapter II. This demonstrates judgment-based triage, not an instruction to always select the same categories.

The retained review compressed counsel analysis into decision-relevant facts, preserved a factual tax table, reframed recommendations into investment-agreement protections, used a separate supplemental chapter for proposed transfers and corporate changes, and retained uncertainty where execution, approval, payment, registration, or filing was incomplete.

