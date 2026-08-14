---
name: deep-industry-research
description: Build rigorous, comparison-rich private-market industry investment roadmaps from a prior sector brief, BP, company clue, sector name, or local research materials. Use when Codex must deeply analyze technology routes, adoption timing, value chains, profit pools, market scenarios, competition, investable segments, target companies, risks, and exits, then deliver a slide-ready report with web-verified evidence, analytical tables, visuals, Markdown, Word, and PDF.
---

# Deep Industry Research

## Goal

Create a substantial, evidence-led industry investment roadmap that helps a private-market investor:

- understand how the industry works and changes;
- decide whether, where, when, and at what stage to invest;
- compare technology routes and value-chain positions;
- screen companies and identify potential targets;
- connect sector conclusions to a trigger company;
- define what evidence, events, and risks to track next.

Do not produce a generic overview or a collection of thin one-paragraph sections. Build a report whose core sections can be reused as complete investment-committee or presentation pages.

## Default Behavior

- Treat the triggering BP or company as an entry point, not as proof.
- Read local materials first. Inventory sources and inspect important figures or tables visually.
- Browse the web for current, corroborating evidence.
- Distinguish local material, web evidence, company claims, calculations, synthesis, and assumptions.
- Preserve useful source visuals and create original comparison tables, charts, or diagrams where they improve understanding.
- Read both references before drafting:
  - [references/report-structure.md](references/report-structure.md)
  - [references/analysis-templates.md](references/analysis-templates.md)
- Save final deliverables in the active workspace's `outputs/` directory unless the user specifies another writable location:
  - `{{sector_slug}}-deep-industry-research.md`
  - `{{sector_slug}}-deep-industry-research.docx`
  - `{{sector_slug}}-deep-industry-research.pdf`
- Keep intermediate figures and source assets in `outputs/{{sector_slug}}-assets/`.

## Inputs

Accept any combination of:

- `brief-industry-research` output;
- `bp-reader` output or project memo;
- company BP or pitch deck;
- industry name, niche, or investment theme;
- reports, papers, PDFs, slides, spreadsheets, datasets, interview notes, or user-selected folders.

Build a source inventory when multiple materials are provided.

## Workflow

### 1. Define the research question

- Identify sector, niche, geography, technology routes, customer segment, application, and value-chain scope.
- State the trigger company or prior decision when applicable.
- Define what is excluded and identify adjacent substitutes.
- Set the report title and `sector_slug`.

### 2. Build the source and evidence map

- Record each local source's title, path, date, relevant pages/sections, and evidence quality.
- Extract text from documents and visually inspect important pages, charts, and tables.
- Plan web research for technology, demand, market size, value chain, profit pool, competition, financing, IPO/M&A, policy, and public-company comparisons.
- Prefer filings, prospectuses, audited reports, standards, government documents, industry associations, peer-reviewed papers, reputable institutions, and credible business media.
- Cross-check decisive claims across independent sources when possible.

### 3. Research through the five-step spine

Build the analytical core in this order:

1. **Product and technology routes**: customer problem, route mechanics, selection metrics, substitutes, maturity, and commercialization bottlenecks.
2. **Industry stage and inflection points**: technology, demand, policy, supply-chain, cost, and capital-market catalysts; adoption triggers and invalidation signals.
3. **Value chain, cost, and profit pool**: upstream/downstream structure, cost breakdown, bottlenecks, pricing power, margins, capex, working capital, and structurally weak layers.
4. **Market size and growth**: TAM/SAM/SOM, bottom-up sanity checks, scenarios, timing, unit economics, and source disagreements.
5. **Competition and startup window**: global and China leaders, startup archetypes, qualification barriers, consolidation, route substitution, and where new entrants can still win.

Then build the investability layer: financing heat, investable segment ranking, screening standards, target map, exit path, bear case, trigger-company implications, and monitoring roadmap.

### 4. Verify commercialization and economics

- Distinguish `lab -> prototype -> pilot -> customer validation -> design-in -> design-win/nomination -> mass production -> recognized revenue -> cash collection`.
- Identify buyer, budget source, procurement cycle, qualification burden, ROI, repeat-purchase evidence, and false-demand traps.
- Explain how margins, price, yield, capex, working capital, and scale economics change across the adoption curve.
- Treat company shipment or order claims as low-quality evidence until independently corroborated.

### 5. Build comparisons and models

- Use an analytical table when comparing at least three objects across meaningful dimensions.
- Use timelines for stage changes, charts for quantitative trends, diagrams for structures or flows, and prose for nuance that resists tabulation.
- Show formulas, units, periods, assumptions, and scenario differences for market sizing or economic models.
- Prefer decision columns such as `investment implication`, `startup window`, `evidence quality`, `failure mode`, or `what changes the view`.
- Do not convert bullets into decorative tables.

### 6. Map the sector to the trigger company

When a company triggered the work, map industry success factors throughout the report:

`industry conclusion -> company position -> available proof -> capability gap -> diligence action`

Do not postpone all company relevance to the final chapter. Add concise company implications after the major technology, demand, value-chain, market, and competition sections, then synthesize them at the end.

### 7. Generate and verify deliverables

- Produce polished Markdown first.
- Generate editable Word and polished PDF versions.
- Use real headings, editable tables, source notes, captions, page numbers, and a table of contents.
- Render and visually inspect the PDF. Check clipped text, table width, image resolution, captions, citations, and page balance.
- Inspect or render the Word file when possible.
- If a required renderer is unavailable, still deliver the remaining formats and explain the limitation.

## Content Depth Contract

Aim for 15–25 slide-ready analysis units, typically supported by 12–18 analytical tables and 5–8 quantitative or structural visuals. Adapt to the sector and available evidence; never fabricate or pad to hit a count.

Each core section—especially technology routes, industry timing, demand, value chain, profit pool, market size, competition, investable segments, and risks—must contain at least one complete analysis unit:

1. conclusion-style heading;
2. clear thesis;
3. 3–5 concrete evidence points, normally from multiple sources;
4. one analytical table, chart, timeline, or diagram when useful;
5. causal reasoning;
6. investment implication;
7. strongest bear point or alternative explanation;
8. confidence level and data that would change the view;
9. trigger-company implication when applicable.

Do not mark a core section complete with one or two summary paragraphs. If evidence is insufficient, produce a structured gap analysis and research plan instead of pretending to have depth.

## Evidence Discipline

- Never present BP claims as industry facts without independent verification.
- Support each major investment claim with cited evidence, a transparent calculation, or an explicit assumption.
- Label evidence quality:
  - **High**: filings, prospectuses, audited reports, government or standards documents, associations, peer-reviewed papers.
  - **Medium**: reputable consulting or broker research, credible media, cross-checked investor presentations.
  - **Low**: BP claims, unsourced charts, reposts, unverified databases.
- Explain source disagreements and use ranges or scenarios.
- Avoid false precision.
- Cite web sources with links and local files by filename plus page or section.
- Treat `唯一`, `行业第一`, `最后窗口`, `确定性爆发`, and similar claims as hypotheses requiring unusually strong evidence.

## Argument and Table Quality

Use this pattern for decisive judgments:

```markdown
**论点**: ...
**证据**: ...
**论证**: ...
**投资含义**: ...
**反方观点**: ...
**置信度/待验证**: ...
**对目标公司的影响**: ...
```

For tables:

- state the decision question the table answers;
- use specific mechanisms, numbers, or evidence rather than only `高/中/低`;
- include sources in cells, captions, or adjacent notes;
- write a short conclusion below the table;
- keep tables readable in Word and PDF; split oversized matrices instead of shrinking them into illegibility.

## Visual Discipline

- Use visuals only for technology structure, timelines, market growth, value chains, cost curves, competition, target maps, or other relationships that benefit materially.
- Give every visual a descriptive title, caption, period, unit, and source.
- Recreate an original table or diagram when a source image cannot be reused clearly.
- Preserve source visuals only when they add analytical value.
- Avoid decorative imagery.

## Quality Gate

Before delivery, verify:

- the five-step industry spine is complete or explicitly marked as not applicable;
- every core section satisfies the content depth contract;
- market figures have units, periods, formulas, and scenarios;
- technology claims distinguish performance from manufacturability and customer adoption;
- demand evidence distinguishes orders, shipments, revenue, and cash collection;
- comparisons use genuinely comparable companies or routes;
- each decisive table has a conclusion and source;
- the strongest bear case is developed fairly;
- target-company implications are evidence-based;
- the report states invalidation signals and next tracking actions;
- Markdown, Word, and PDF are internally consistent and visually usable.

## Tone

Write like a skeptical senior investor building a reusable sector map:

- decisive but explicit about uncertainty;
- specific rather than generic;
- comparison-rich and commercially grounded;
- clear about where to invest, where not to invest, and why;
- useful even when the trigger company is unattractive.
