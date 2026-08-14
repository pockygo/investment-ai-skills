---
name: company-deep-dive
description: Use when the user wants to deeply analyze a private-market company after BP screening and industry research, especially to answer whether the company is a good target within a validated sector thesis. This skill ingests BP, bp-reader output, brief-industry-research, deep-industry-research, company materials, financials, customer data, and competitor materials to produce a rigorous company investment analysis.
metadata:
  short-description: Deep company investment analysis after sector validation
---

# Company Deep Dive

## Goal

Determine whether a company is an attractive private-market investment target **after** the sector direction has been screened or researched.

The core question is:

> If the industry thesis is valid, does this company have real alpha?

This skill should connect company facts to the industry investment roadmap. It should not repeat generic industry research unless needed to explain company positioning.

## Default Behavior

- Use prior artifacts when available:
  - `bp-reader` memo
  - `brief-industry-research` output
  - `deep-industry-research` report
  - BP/deck/company intro
  - financial model, revenue data, customer list, cap table, financing terms, product specs, technical reports, diligence notes
- Treat company-provided claims as unverified unless supported by contracts, financials, customer calls, third-party sources, demos, filings, or other evidence.
- Use the industry roadmap to judge whether the company sits in a high-value segment.
- Focus on company-specific alpha: team, technology, product, customers, revenue quality, competitive advantage, execution, financing, valuation, and exit path.
- Produce Markdown, Word (`.docx`), and PDF outputs in the user's requested output directory. If none is specified, use the current Codex task's `outputs/` directory when available; otherwise save beside the source material.
- Save assets under `<resolved-output-dir>/{{company_slug}}-company-deep-dive-assets/`.

## Inputs

Accept any of:

- BP/pitch deck/company intro
- `bp-reader` output
- `brief-industry-research` output
- `deep-industry-research` output
- company financials, contracts, customer lists, product specs, cap table, financing plan
- competitor materials
- public web sources
- user notes or diligence records

If multiple files are available, build a source inventory before analysis.

## Workflow

1. **Define the investment question**
   - Company name, sector, financing stage, proposed round, amount, valuation, and user's decision need.
   - State the sector thesis being tested.
   - State the company-specific question: why this company, not just this industry?

2. **Inventory and extract evidence**
   - Read all supplied materials.
   - Extract key claims and classify them as company-stated, independently verified, inferred, or unverified.
   - Build an evidence table for important claims: team, technology, product, customers, revenue, gross margin, contracts, funding, valuation, and milestones.

3. **Map company to industry roadmap**
   - Identify where the company sits in the value chain.
   - Determine whether it is in a high-value, investable, or avoid segment from the industry roadmap.
   - Compare company positioning to the sector's investable segment ranking.

4. **Analyze company alpha**
   - Team and founder-market fit.
   - Technology/product differentiation.
   - Commercialization stage and customer validation.
   - Revenue quality and unit economics.
   - Competitive landscape and alternatives.
   - Moat and defensibility.
   - Execution capability and milestone credibility.
   - Financing need, runway, and use of proceeds.
   - Valuation reasonableness and return path.

5. **Use argument-driven writing**
   - For core judgments, use `论点 -> 证据 -> 论证 -> 投资含义 -> 置信度/待验证`.
   - Do not produce a list of unsupported conclusions.
   - Explicitly state what would change the investment view.

6. **Reach a decision**
   - Recommend one of:
     - `推进投资条款讨论`
     - `进入强DD`
     - `补材料后再判断`
     - `跟踪观察`
     - `Pass`
   - Include reasoning, not just a label.

7. **Generate outputs**
   - Save:
     - `{{company_slug}}-company-deep-dive.md`
     - `{{company_slug}}-company-deep-dive.docx`
     - `{{company_slug}}-company-deep-dive.pdf`
   - Include source inventory, evidence quality, and open issues.
   - Render/check PDF if possible.
   - Keep Word editable: real headings, editable text, editable tables, embedded images with captions.

## Evidence Standards

- Never treat BP claims as verified facts.
- Every important company claim should be assigned one of:
  - **Verified**: supported by financials, contracts, customer calls, third-party records, filings, or reliable public sources.
  - **Company-stated**: stated in BP/materials but not independently verified.
  - **Inferred**: reasonable inference from available facts.
  - **Unclear**: insufficient information.
- Separate sales contracts, confirmed revenue, recognized revenue, invoicing, collection, backlog, LOI, pilot, design-in, design-win, mass production, and repeat orders.
- For hard-tech companies, force a commercialization ladder:
  `sample/prototype -> pilot -> customer validation -> design-in -> design-win/nomination -> mass production -> recognized revenue -> cash collection`.
- For revenue, distinguish recurring product revenue, one-time NRE/development fee, sample revenue, project revenue, related-party revenue, and channel revenue.

## Report Structure

Use `references/report-structure.md` for the full company deep dive structure. Adapt depth to available materials, but preserve the investment logic.

## Output Quality

The report should be useful for partner discussion or pre-IC review. It should:

- explain the company in the context of the industry roadmap
- identify what is real, what is claimed, and what remains unknown
- show whether the company has alpha beyond industry beta
- include investment decision, diligence priorities, valuation issues, and deal risks
- remain useful even if the final recommendation is Pass
