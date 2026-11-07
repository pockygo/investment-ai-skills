# 巨潮资讯（cninfo）下载与版本选择

## 1. 接口与主体

- 股票映射：`https://www.cninfo.com.cn/new/data/szse_stock.json`，用 `code` + `zwjc` 查 `orgId`；沪市与深市都在同一份清单。
- 公告查询：`POST https://www.cninfo.com.cn/new/hisAnnouncement/query`
  - `stock=<code>,<orgId>`
  - `category`：`category_ndbg_szsh`（年报）、`category_bndbg_szsh`（半年报）、`category_yjdbg_szsh`（一季报）、`category_sjdbg_szsh`（三季报）
  - `seDate=YYYY-01-01~YYYY-MM-DD`、`column=szse`、`plate=sh|sz`、`pageSize=30`
  - 返回 `announcements[].adjunctUrl`，PDF 前缀 `https://static.cninfo.com.cn/`
- 直接 `git clone github.com` 可能超时；`codeload.github.com` 与 `api.github.com` 可用，下载 ZIP 后用 `api.github.com/git/trees?recursive=1` 校验。

## 2. 期间口径

- 年报按**报告期年份**归档：2020 年发布的“2019 年年度报告”归 `fy2019`。用 `seDate` 从 2019-01-01 起会带入 FY2018 年报，必须按标题年份过滤。
- 季报：一季报、三季报各 1 份；半年报 1 份。2026 年三季报在 2026-10-30 前后披露，截止日设为任务日。
- 目标期间矩阵示例：2019–2025 年报 7 期 + 2019–2026 一季报 8 期 + 半年报 8 期 + 三季报 8 期 = 31 期/公司。

## 3. 版本选择（最容易错）

同一期间常有 2–6 个版本，按以下优先级选**一个主文件**：

| 版本 | 处理 |
|---|---|
| 摘要 / 英文版 | 排除 |
| 正文 vs 全文（2019–2021 季报常见） | 取全文 |
| 更新后 / 更正后 / 修正后 | 取最新更正版 |
| 更新前 / 已取消 | 排除 |
| 同标题、同时间的两条 | 巨潮有时把“摘要”也标成“年报”，按页数取大者（如 293 页 vs 13 页） |

- 更正版是整份替换稿时，以更正版为主；局部更正保留原件并在台账备注。
- 选完后核对：PDF 头、页数、封面公司名、封面期间短语（如“2021 年年度报告”）。186 份里出现 0 页、10 页“年报”都说明选错。
- 页数分布可作 sanity check：A 股年报通常 150–300 页，半年报 100–230 页，季报 9–40 页。

## 4. 归档与台账

- 命名：`公司简称_YYYY年报.pdf`、`_YYYY一季报.pdf`、`_YYYY半年报.pdf`、`_YYYY三季报.pdf`。
- 每家公司一个目录，台账字段：公司、代码、期间、类型、原始标题、公告日期、下载日期、状态、页数、大小、SHA-256、本地路径、来源链接、备注。
- 状态区分“已取得/待核验/缺失/受限”，不要把“下载成功”当“内容核验通过”。
- 增量更新按“公司 + 实际期间 + 类型”建稳定键；不要按行号匹配。

## 5. 常见坑

- `szse_stock.json` 的 `orgId` 对沪市也适用；不要只查深市。
- 60xxxx 股票用 `plate=sh`，00xxxx/30xxxx 用 `plate=sz`；`column` 统一 `szse` 即可。
- 静态 PDF 域名是 `static.cninfo.com.cn`，不是 `www`。
- 同一公告 ID 可能返回 302；用 `urllib`/`requests` 跟随重定向后再校验文件头。
- 公告标题里的“（更新后）”可能是全角括号，匹配时统一全半角。
