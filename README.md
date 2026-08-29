# 一级市场投资 AI Skills

一套面向一级市场投资团队的 Codex Skills，覆盖 BP 初筛、行业研究、公司分析、访谈纪要、投决材料、投资建议书、投后台账和基金季度报告。

配套工作流指南：[一级市场投资 AI 工作流指南](https://investment-ai-workflow-cn.waymewym.chatgpt.site)

## Skills

| Skill | 用途 |
|---|---|
| `bp-reader` | 阅读 BP、融资材料和项目介绍，形成一级市场项目初筛结论 |
| `brief-industry-research` | 对细分行业方向进行快速研究和投资价值筛选 |
| `deep-industry-research` | 建立行业投资地图、技术路线、市场情景和标的清单 |
| `company-deep-dive` | 深度分析目标公司的团队、产品、客户、财务和投资价值 |
| `interview-summary` | 将中文访谈逐字稿整理为结构化访谈纪要 DOCX |
| `toujue-baogao` | 根据真实项目材料编制或更新中文投决报告和投委会材料 |
| `investment-recommendation-docx` | 按指定 Word 模板生成正式、可编辑的投资建议书 |
| `xiangmu-biao` | 新建或更新投后项目表中的公司 Sheet 和季度经营数据 |
| `fund-quarterly-report` | 根据项目及基金材料生成或更新基金季度报告 |
| `financial-dd-review-report` | 将外部财务尽调材料转化为内部财务尽调审阅报告 DOCX |
| `legal-dd-review-report` | 将外部法律尽调材料转化为内部法律尽调审阅报告 DOCX |
| `ipo-research` | 招股书/问询函研究流水线，产出以利润拆解为主线的结构化研究报告（quick 初筛 / deep 深研双档位） |
| `ipo-overview` | 将已完成 ipo-research 分析的项目摘录为一行记录，追加到项目总览表并渲染总览 HTML |

## 安装

### 让 Codex 从 GitHub 安装

向 Codex 发送：

```text
请从 GitHub 仓库 pockygo/investment-ai-skills 的 skills 目录安装全部 Skills。
```

也可以只指定一个或多个目录，例如：

```text
请从 GitHub 仓库 pockygo/investment-ai-skills 安装：
skills/bp-reader
skills/brief-industry-research
```

### 手动安装

1. 下载仓库 ZIP 并解压。
2. 将需要的完整 Skill 文件夹复制到 Codex Skills 目录：
   - Windows：`C:\Users\你的用户名\.codex\skills\`
   - macOS/Linux：`~/.codex/skills/`
3. 重新打开 Codex，或开始一个新任务。

安装时请保留 Skill 文件夹中的 `SKILL.md`、`agents/`、`scripts/`、`references/` 和 `assets/` 等全部内容。

## 使用说明

- 将项目材料提供给 Codex，并明确指定相应 Skill。
- 输出仅作为投资研究和材料整理辅助，不构成投资建议。
- 使用者应自行核验事实、数据、交易条款和最终投资判断。
