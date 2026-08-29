# Builder input schema

Pass a UTF-8 JSON object to `scripts/build_report.py`.

## Root object

```json
{
  "company_name": "项目公司全称",
  "short_name": "公司简称",
  "department": "风控法务部",
  "report_month": "2026年8月",
  "diligence_cutoff": "2026年7月31日",
  "review_scope": "历史沿革、主营业务、资质证照、资产等情况",
  "third_party_firm": "某律师事务所",
  "third_party_report_title": "关于某公司项目之法律尽职调查报告",
  "third_party_report_date": "2026年8月10日",
  "supplemental_period": "2026年8月11日至2026年8月20日",
  "background_paragraphs": [],
  "issues": [],
  "supplemental_updates": []
}
```

If `background_paragraphs` is empty or omitted, the builder composes the two retained-pattern paragraphs from metadata.

## Issue object

```json
{
  "title": "问题标题",
  "description": ["事实段落", {"type": "table", "headers": ["列1", "列2"], "rows": [["值1", "值2"]], "widths": [0.3, 0.7]}],
  "risk_analysis": ["风险分析段落"],
  "recommendations": ["建议段落"],
  "source_intro": "根据《法律尽调报告》：",
  "omit_risk_analysis": false,
  "omit_reason": ""
}
```

`title`, `description`, and `recommendations` are required. `risk_analysis` is required unless `omit_risk_analysis=true` and `omit_reason` is nonempty. Blocks accept strings, paragraph objects, list objects, and table objects.

## Content block objects

```json
{"type": "paragraph", "text": "正文"}
{"type": "list", "items": ["第一项", "第二项"], "numbered": true}
{"type": "table", "headers": ["序号", "事项"], "rows": [["1", "内容"]], "widths": [0.15, 0.85]}
```

`widths` are optional fractions and must sum approximately to 1.0. Tables use explicit geometry and repeating headers.

## Supplemental update object

```json
{
  "title": "公司正在解决股东相关问题",
  "content": [{"type": "paragraph", "text": "1、股权转让"}, "更新事实及尚待完成事项。"]
}
```

If no supplemental material exists, use a supported statement such as `未取得补充尽调材料，相关事项截至本报告出具日的更新状态尚无法核查。` Do not state that no changes occurred unless verified.
