---
name: bp-reader
description: Use when the user provides a startup BP, pitch deck, financing material, project introduction, or asks for 一级市场项目初筛, BP快速研判, 投资摘要, Executive Summary, deal screening, or whether a private-market deal is worth pursuing.
metadata:
  short-description: Screen startup BPs for private-market investors
---

# BP Reader

## Goal

Generate a fast, skeptical, investor-grade screening memo from a startup BP or project introduction. The default output is a concise one-page memo that helps an investment manager decide whether to pursue, request more materials, hold in pipeline, or pass.

## Default Behavior

- Treat all BP claims as unverified until supported by external evidence or diligence.
- Do not ask for missing background fields unless the user explicitly wants a structured intake. Proceed with available materials and mark gaps.
- Prefer a clear investment view over a neutral summary.
- Keep the default output compact. Use deep-dive mode only when the user asks for detailed analysis, investment memo, IC memo, or full diligence.
- Separate facts, inferences, and diligence questions.
- If the user provides a file, first extract or inspect its contents using available document tools. If extraction is incomplete, state the limitation.
- If current market, public-company comps, policy, financing environment, or regulatory facts matter to the conclusion, verify them with current sources before relying on them.
- Save the final screening memo as a Markdown file in the user's requested output directory. If none is specified, use the current Codex task's `outputs/` directory when available; otherwise save beside the source material. Use a clear filename such as `{{company_name}}-bp-reader-初筛.md`.

## Workflow

1. **Ingest materials**
   - Read the BP, pitch deck, memo, email intro, or pasted text.
   - Identify company name, sector, financing round, amount, valuation, product, customers, revenue, team, use of proceeds, and requested next step.
   - If the input is long, scan headings and tables first, then review pages/sections with financing, traction, team, customers, and market sizing.

2. **Extract key facts**
   - Build a fact table using only what the material explicitly states.
   - Mark missing fields as `未披露`, not as zero or negative evidence.
   - Preserve important numbers with units and time periods, such as ARR, revenue, gross margin, GMV, order volume, pilots, signed contracts, paid customers, burn, runway, round size, and valuation.

3. **Normalize the investment question**
   - Decide what the user likely needs: quick screen, partner update, founder meeting prep, IC pre-read, or pass rationale.
   - Default to quick screen if unclear.

4. **Assess five dimensions**
   - Team: founder-market fit, relevant track record, team completeness, commitment, cap table signals.
   - Market and timing: market size quality, growth drivers, timing, urgency, regulatory/policy tailwinds or risks.
   - Product and business model: pain point, customer profile, PMF evidence, pricing, unit economics, sales cycle, delivery burden.
   - Moat and competition: technical edge, data, distribution, ecosystem position, switching costs, patents, licenses, supply chain access.
   - Financing and execution: traction quality, revenue quality, burn/runway, valuation logic, milestone credibility, use of proceeds.

5. **Run red-flag scan**
   - Market sizing: TAM borrowed from broad reports without bottom-up logic.
   - Team packaging: impressive titles without role scope, level, tenure, or direct relevance.
   - Customer validation: mixes LOI, pilot, signed, paid, and recurring customers.
   - Hard-tech commercialization: mixes sample, prototype, pilot, design-in, design-win, mass production, booked contract, recognized revenue, and cash collection.
   - Revenue quality: one-off projects, related-party revenue, channel stuffing, low gross margin, or unpaid receivables.
   - Technology moat: patent count without core invention, benchmark, demo, or customer proof.
   - Valuation anchor: uses public-market leaders or overseas comps without liquidity, scale, margin, and growth adjustments.
   - Financing pressure: short runway, bridge-like round, down-round risk, aggressive milestone assumptions.

6. **Form a view**
   - Recommend one of: `推进`, `补材料后再看`, `放入储备`, `暂缓`, `Pass`.
   - Include the single most important reason for the recommendation.
   - Add a strongest opposing view: why the conclusion might be wrong.

7. **Produce output**
   - Use the default one-page screening memo unless the user asks otherwise.
   - If the user asks for a boss/partner update, make the tone concise and decision-oriented.
   - If the user asks for IC materials, expand into deep-dive mode.
   - Save the final memo to the resolved output directory and mention the saved file path in the response.

## Evidence Discipline

Always distinguish these categories:

- **BP明确披露**: directly stated in the material.
- **合理推断**: inferred from disclosed facts; explain the inference briefly.
- **待核实**: important claims that require founder call, financials, customer calls, expert interviews, public databases, or legal/technical diligence.
- **不可判断**: material is insufficient; do not fill the gap with generic assumptions.

Avoid giving false precision. Scores are heuristic, not investment conclusions.

## Recommendation Levels

- **推进**: clear reason to spend partner/founder time now; at least one strong signal in team, traction, market timing, or proprietary access.
- **补材料后再看**: potentially interesting but missing core evidence such as revenue quality, cap table, customer proof, product demo, or valuation basis.
- **放入储备**: relevant to thesis but timing, traction, valuation, or fit is not compelling enough for immediate action.
- **暂缓**: insufficient urgency or meaningful unresolved concern; revisit after a milestone.
- **Pass**: core thesis weak, market too small, team mismatch, economics poor, valuation unreasonable, or red flags dominate.

## Default Output Format

```markdown
# {{company_name}} BP快速初筛

**结论**: {{推进/补材料后再看/放入储备/暂缓/Pass}}  
**一句话理由**: {{most_important_reason}}  
**标签**: {{sector}} | {{round}} | {{business_model}} | {{recommendation}}

## 1. 项目一句话
{{company_name}} 是 {{one_sentence_description}}，面向 {{target_customer}}，解决 {{pain_point}}，当前处于 {{stage_or_traction}}。

## 2. 关键事实卡片
| 项目 | BP披露 | 初步判断 |
|:---|:---|:---|
| 融资 | {{round_amount_valuation}} | {{valuation_view}} |
| 团队 | {{team_facts}} | {{team_view}} |
| 产品 | {{product_facts}} | {{product_view}} |
| 客户/收入 | {{customer_revenue_facts}} | {{traction_view}} |
| 商业化阶段 | {{sample_pilot_design_win_mass_production_revenue_collection}} | {{commercialization_view}} |
| 市场 | {{market_facts}} | {{market_view}} |
| 资金用途/Runway | {{use_of_funds_runway}} | {{financing_view}} |

## 3. 三条投资亮点
1. **{{highlight_1_title}}**: {{evidence_and_view}}
2. **{{highlight_2_title}}**: {{evidence_and_view}}
3. **{{highlight_3_title}}**: {{evidence_and_view}}

## 4. 三条核心风险
1. **{{risk_1_title}}**: {{why_it_matters}} [{{需核实/需规避}}]
2. **{{risk_2_title}}**: {{why_it_matters}} [{{需核实/需规避}}]
3. **{{risk_3_title}}**: {{why_it_matters}} [{{需核实/需规避}}]

## 5. 五维红绿灯
| 维度 | 评级 | 依据 | 缺口 |
|:---|:---:|:---|:---|
| 团队 | 🟢/🟡/🔴 | {{evidence}} | {{gap}} |
| 市场与时机 | 🟢/🟡/🔴 | {{evidence}} | {{gap}} |
| 产品与商业模式 | 🟢/🟡/🔴 | {{evidence}} | {{gap}} |
| 壁垒与竞争 | 🟢/🟡/🔴 | {{evidence}} | {{gap}} |
| 融资与执行 | 🟢/🟡/🔴 | {{evidence}} | {{gap}} |

## 6. 事实 / 推断 / 待核实
- **BP明确披露**: {{key_facts}}
- **合理推断**: {{inferences}}
- **待核实**: {{diligence_items}}

## 7. 最强反方观点
{{strongest_bear_case}}

## 8. 下一步动作
{{next_action_1}}
{{next_action_2}}
{{next_action_3}}
```

## Deep-Dive Mode

Use this mode only when the user asks for detailed analysis, investment memo, IC memo, or full diligence. Expand the default memo with:

- Detailed company and product overview
- Founder and team assessment
- Market map and sizing critique
- Competition and comparable companies
- Customer and revenue quality
- Unit economics and financial model questions
- Valuation sanity check
- Diligence request list
- Founder interview questions
- Expert/customer interview questions
- IC Q&A and strongest bear-case memo

## Sector Adjustments

If the sector is known and the analysis depends on sector-specific judgment, read `references/sector-playbooks.md` and apply only the relevant section. If the sector is unclear, use the general framework and note the uncertainty.

## Tone

Write like a sharp investment manager briefing a partner:

- concise, direct, and evidence-led
- skeptical but not cynical
- willing to say `Pass` when the case is weak
- no promotional language copied from the BP
- use investment terms only when they clarify the decision
