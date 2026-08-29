# 构建器输入结构

使用 UTF-8 JSON。所有 `blocks` 均为数组，可包含：

- 字符串：普通正文。
- `{"type":"paragraph","text":"..."}`。
- `{"type":"list","items":["..."],"numbered":true}`。
- `{"type":"table","rows":[[...]],"header_rows":1,"widths":[...],"font_size":9}`。`rows` 包含表头；`widths` 为相对宽度。
- `{"type":"image","path":"绝对路径","width_inches":6.2,"caption":"..."}`。
- `{"type":"page_break"}`。

最小结构：

```json
{
  "company_name": "目标公司全称",
  "short_name": "简称",
  "report_month": "2026年8月",
  "diligence_cutoff": "2026年6月30日",
  "diligence_period": "2023年至2026年6月",
  "third_party_firm": "会计师事务所名称",
  "third_party_report_title": "财务尽职调查报告",
  "units": "万元人民币",
  "background": ["..."],
  "main_matters": {
    "income_profit": {"profit_data": [], "income_change": []},
    "personnel_compensation": [],
    "cash_flow": [],
    "borrowings": []
  },
  "financial_statements": {
    "balance_sheet": [],
    "income_statement": [],
    "cash_flow_statement": []
  },
  "profit_details": {
    "sales_and_margin": {
      "product_revenue": [],
      "product_margin": [],
      "trend_analysis": [],
      "major_customers": []
    },
    "operating_expenses": [],
    "taxation": []
  },
  "balance_details": {
    "trading_financial_assets": [],
    "receivables": [],
    "prepayments": [],
    "inventory": [],
    "fixed_assets": [],
    "contract_liabilities": [],
    "payables": []
  },
  "findings": [
    {"title": "问题标题", "description": ["事实与影响"], "response": ["整改及交易安排"]}
  ]
}
```

## 缺失信息

- 固定小节没有材料时填入：`["未取得可用于核实本事项的资料，相关余额、变动及风险尚无法判断。"]`。
- 第三方机构未知时使用“第三方财务尽调机构（材料未载明）”，不得猜测名称。
- 报告日期未知可不写日期，但必须在背景中说明未能确认。
- 单位以源表为准。同一报告含“元”和“万元”时，每张表单独注明，不得仅依赖全局单位。

## 表格规则

- 期间列保持从早到晚；最近一期注明月日。
- 金额使用千分位，负数使用负号或括号并保持全表一致。
- 合计、资产总计、负债合计、净利润、现金净增加额等关键行使用加粗。
- 表头跨页重复，禁止表格行跨页拆分。
- 宽表优先缩短表头、合理换行和调整列宽，不默认改为横向页面。
