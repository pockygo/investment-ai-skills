---
name: brief-industry-research
description: Perform concise, web-verified private-market industry screening from a BP Reader memo, startup summary, company description, or niche-sector clue. Use when Codex must decide whether a narrow industry direction is worth deeper research, company diligence, monitoring, or passing, and present the result as a structured, comparison-rich, slide-ready investment brief.
---

# Brief Industry Research

## Goal

Turn a company clue or BP screening memo into a concise, evidence-led sector screen that answers:

1. Is this precisely defined niche worth further investment work?
2. Which technology route or value-chain layer is most investable?
3. Why now, and what event would prove or disprove the timing?
4. Does the sector view strengthen or weaken interest in the trigger company?

Keep this shorter than deep research. Build enough analytical density for a partner to make the next-work decision; do not inflate it into a miniature industry encyclopedia.

## Default Behavior

- Treat the user's memo or BP as an entry point, not as evidence.
- Narrow the direction by product, technology route, application, customer, geography, and value-chain position.
- Browse the web for current evidence and cross-check important claims.
- Prefer filings, government or standards documents, industry associations, technical papers, reputable research institutions, listed-company disclosures, credible business media, and funding databases.
- Separate sourced facts, calculations, synthesis, assumptions, and unverified company claims.
- Conclude with `积极看`, `选择性看`, `只看头部`, or `暂不看`.
- Recommend `deep_research`, `company_dd`, `watch`, or `pass`.
- Read [references/analysis-templates.md](references/analysis-templates.md) before drafting. Select only templates that answer a real investment question.

## Workflow

### 1. Define the niche

- Extract the trigger company, product, customer, use case, geography, business model, financing stage, and claimed advantage.
- Define the research scope in one sentence.
- State what is excluded and identify adjacent substitutes.
- Prefer a narrow direction such as `Micro LED车载数字大灯驱动芯片`, not `半导体`.

### 2. Build the five-step research spine

Research in this order:

1. **Product and technology routes**: what problem is solved, which routes compete, what metrics determine customer choice, and which routes are commercially mature?
2. **Industry stage and inflection points**: what stage is the sector in, why now, what event triggers adoption, and when might the investment window close?
3. **Value chain, cost, and profit pool**: who supplies, who pays, where bottlenecks sit, and which layer captures margin?
4. **Market size and commercialization**: what is current demand, what are base/bull/bear scenarios, and what evidence separates narrative from real procurement?
5. **Competition and startup window**: who leads, what incumbents control, where startups can win, and what causes consolidation?

### 3. Verify the commercial stage

- Distinguish `lab -> prototype -> pilot -> customer validation -> design-in -> design-win/nomination -> mass production -> recognized revenue -> cash collection`.
- Verify who owns the budget, the buying process, qualification cycle, ROI, repeat-purchase signal, and working-capital burden.
- For policy-driven markets, verify effective dates and whether policy creates enforceable demand or merely permits adoption.
- For public-company comparisons, verify actual exposure to the same niche.

### 4. Size and compare

- Use at least one bottom-up or unit-based sanity check when market size is central.
- Show ranges and assumptions; do not copy a single forecast as truth.
- Compare routes, layers, or competitors in a table whenever there are at least three objects and three meaningful dimensions.
- Prefer decision columns such as `investment implication`, `startup window`, `evidence quality`, or `what would change the view` over decorative ratings.

### 5. Map the sector to the trigger company

Build a short fit-gap matrix:

`industry success factor -> sector evidence -> company claim/status -> independent proof -> gap -> next diligence action`

Do not turn this into full company diligence. Explain only whether the sector thesis makes the company more or less worth pursuing.

### 6. Decide the next action

- `积极看`: real demand, attractive value capture, good timing, and a plausible startup entry window.
- `选择性看`: attractive only for particular routes, layers, teams, customers, or entry points.
- `只看头部`: the direction is valid but scale, qualification, capital, or trust strongly favors leaders.
- `暂不看`: demand is weak, timing is wrong, economics are poor, competition is crowded, or exit is unattractive.

State the strongest bear case, the invalidation signals, and the minimum evidence needed before spending more time.

## Content Density Contract

Aim for 6–8 slide-ready content units, usually supported by 4–6 analytical tables. Treat these as target ranges, not quotas.

For each core unit:

- Use a conclusion-style heading.
- Provide 2–4 concrete evidence points, normally from more than one source.
- Add a comparison table when comparison, sequencing, or calculation materially improves understanding.
- Explain the causal logic, not only the observation.
- State the investment implication and confidence level.
- Add one bear point or unresolved question.
- Map to the trigger company when relevant.

Do not pad weak evidence to fill space. Label gaps `未验证`, `公开资料不足`, or `需要专家/客户访谈`.

## Output Structure

```markdown
# {{niche_direction}} 行业快速研究

**结论**: {{积极看/选择性看/只看头部/暂不看}}
**一句话判断**: {{thesis}}
**建议动作**: {{deep_research/company_dd/watch/pass}}
**最强反方观点**: {{bear_case}}

## 1. 方向定义与产品本质
{{scope, customer problem, value-chain position, exclusions}}
{{technology-route comparison table when applicable}}
**本节结论 / 投资含义 / 置信度**

## 2. 行业阶段与投资窗口
{{why-now and inflection-point table}}
**本节结论 / 验证信号 / 失效条件**

## 3. 产业链、成本与利润池
{{value-chain or profit-pool comparison}}
**本节结论 / 最值得看的层 / 结构性低回报层**

## 4. 市场与商业化
{{commercialization evidence and scenario sizing}}
**本节结论 / 关键假设 / 数据分歧**

## 5. 竞争格局与创业公司窗口
{{competitive matrix}}
**本节结论 / startup entry window / consolidation risk**

## 6. 目标公司匹配
{{fit-gap table}}
**行业研究增强还是削弱项目兴趣**

## 7. 风险与下一步
- {{top risks}}
- {{deep research questions}}
- {{company diligence questions}}
- {{stop or invalidation signals}}

## Sources
{{linked sources with evidence notes}}
```

## Evidence Standards

- Cite sources near the claims they support.
- Cross-check decisive market, adoption, financing, and competitive claims whenever possible.
- If sources disagree, show the disagreement and explain the chosen range or interpretation.
- Avoid fake precision.
- Never present a BP claim as industry fact without independent verification.
- Treat unsourced claims such as `唯一`, `行业第一`, `最后窗口`, or `确定性爆发` as hypotheses requiring unusually strong evidence.

## Escalate to Deep Research

Recommend deep research when at least one is true:

- The direction is `积极看` or a high-quality `选择性看`.
- Market data conflicts but potential upside is large.
- The company appears to occupy a bottleneck or high-value layer.
- The decision depends on technical, regulatory, profit-pool, or adoption questions that a brief cannot resolve.
