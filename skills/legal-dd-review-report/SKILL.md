---
name: legal-dd-review-report
description: Generate a Chinese internal legal due diligence review report（法务尽职调查审阅报告/法律尽调审阅报告）from project initiation reports, third-party legal due diligence reports, supplemental diligence materials, transaction documents, and related project files. Use when Codex must review legal DD materials, identify and triage deal risks, draft internal legal conclusions and transaction protections, or produce a DOCX that strictly follows the retained three-chapter framework and visual style of the user's “5-法律尽调审阅报告”.
---

# Legal DD Review Report

Produce an internal review, not a shortened copy of counsel's report. Preserve the retained report's structure and distinguish source facts, third-party views, internal analysis, and supplemental updates.

## Required resources

Read before drafting:

- `references/framework.md` for the fixed chapter architecture, issue selection, writing rules, and QA gates.
- `references/template-spec.md` for the retained template contract and visual rules.
- `references/input-schema.md` when using `scripts/build_report.py`.

Use `assets/review-report-template.docx` as the design authority. Do not replace it with a generic Word preset.

## Workflow

1. Inventory every supplied file. Record filename, document type, author/issuer, date, diligence cutoff, covered entity, and evidentiary role. Never infer that a later-dated file is an update unless its contents establish that.
2. Extract all relevant content. Use `scripts/extract_sources.py` for DOCX, PDF, Markdown, and TXT sources; use the appropriate document/PDF/spreadsheet skill for visually complex files or formats not supported by the script. Inspect tables, appendices, headers, footnotes, comments, and tracked changes where relevant.
3. Build a private evidence matrix before writing. For every candidate issue record: source locator, verified fact, missing material, third-party conclusion, internal risk analysis, materiality, proposed protection, supplemental status, inclusion decision, and exclusion reason. Do not deliver this matrix unless requested.
4. Reconcile conflicts by authority and date. Prefer executed agreements and official records for their own contents; use company explanations only as explanations; preserve unresolved conflicts explicitly. Never silently choose a favorable version.
5. Triage issues under `references/framework.md`. Include all unresolved high/material matters. Record a reason for every source issue omitted from Chapter II. When uncertain, include the issue and label the uncertainty.
6. Verify every current legal proposition that materially supports the internal risk analysis against an official, current source. Record the effective date and jurisdiction. Do not browse merely to replace facts that should come from supplied deal materials.
7. Draft a structured JSON file that satisfies `references/input-schema.md`. Keep the report in the exact cover + TOC + three-chapter architecture. Each Chapter II issue uses “详细描述—风险分析—处理建议”; use the documented narrow exception only when a block is genuinely inapplicable.
8. Build the DOCX with `scripts/build_report.py`. Work on a copy of the retained asset. Do not modify the asset.
9. Refresh the TOC and fields in Word/WPS if available. Otherwise preserve `w:updateFields=true` and state that fields refresh on open.
10. Render the final DOCX to page images and inspect every page. Verify title page, TOC, headings, tables, pagination, header/footer rule, page numbers, clipping, and blank pages. Iterate until clean.
11. Run the coverage and legal-quality gates in `references/framework.md`. Deliver the DOCX plus a concise note identifying unresolved inputs and deferred field refresh, if any.

## Hard rules

- Do not change the three top-level chapter titles or order.
- Do not invent facts, dates, amounts, parties, agreement terms, law citations, government confirmations, remediation status, or transaction protections.
- Do not present a third-party lawyer's conclusion as the internal team's independent verification.
- Begin third-party-derived issue descriptions with `根据《法律尽调报告》：` unless the evidence matrix shows the fact was independently verified; identify other source reports by their actual titles.
- Keep historical risk and supplemental remediation separate. An update may reduce residual risk but must not erase the original issue.
- Do not omit a source issue without recording the disposition and reason in the evidence matrix.
- Use calibrated language such as `经核查`, `根据公司说明`, `尚未提供`, `暂无法确认`, `可能`, and `存在……风险` according to evidentiary strength.
- Make recommendations operational: assign them to a deal mechanism such as a closing condition, post-closing covenant, representation and warranty, indemnity, price/escrow protection, waiver, consent, or follow-up diligence. Do not impose repurchase liability mechanically when the risk does not justify it.
- Treat the result as a professional draft requiring responsible legal review before external reliance.

## Commands

Use the bundled workspace Python runtime.

```powershell
python scripts/extract_sources.py --out extracted.md input1.docx input2.pdf
python scripts/build_report.py report.json --out 法律尽调审阅报告.docx
```
