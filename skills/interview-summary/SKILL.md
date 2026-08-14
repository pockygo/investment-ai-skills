---
name: interview-summary
description: >
  Convert verbatim interview transcripts (逐字稿) in .docx format into
  structured interview summary documents (访谈纪要). Use when Codex
  receives interview transcripts with multiple speakers (e.g. 发言人1,
  发言人2) and needs to produce a formatted .docx report with metadata
  table and organized Q&A content. Works with Mandarin Chinese transcripts.
---

# 访谈纪要整理 (Interview Summary Generator)

Convert verbatim interview transcripts into professional, formatted interview summary documents (.docx).

## When to Use

Trigger when:
- User provides a `.docx` transcript labeled with speakers like `发言人1`, `发言人2`, or named speakers
- User asks to turn a transcript into an "访谈纪要" (interview summary)
- User provides metadata (company name, interviewee info, date, etc.) alongside a transcript

## Workflow

### Step 1: Read the Transcript

Use `python-docx` to read the transcript. Typical format:

```
方鹏05221_原文
2026年05月30日 21:28
发言人1   00:00
[text...]
发言人2   01:23
[text...]
```

### Step 2: Collect Metadata

Ask the user to confirm these fields (or accept them if already provided):

| Field | Meaning | Example |
|-------|---------|---------|
| Project title | 项目名称 | 诺宇医药管理层访谈 |
| 访谈类型 | Interview type | 高管访谈 |
| 访谈对象 | Interviewee | 姓名：方鹏    职务：创始人 |
| 访谈对象背景 | Background | 诺宇医药，核药创新药公司 |
| 访谈人员 | Interviewer(s) | 方鹏 |
| 访谈地点 | Location | 诺宇医药会议室 |
| 访谈时间 | Date | 2026/05/21 |
| 访谈方式 | Method | 现场访谈（保留☐选项） |
| 访谈对象来源 | Source | 企业 |

Preserve the checkbox format in 访谈方式: `现场访谈，电话访谈，☐视频访谈，☐其他_______`

### Step 3: Parse Speaker Turns

Extract all turns into `(speaker, timestamp, text)` tuples.

**Speaker identification:** The speaker with the most total text is the **interviewee**; other speakers are **interviewers/investors**.

### Step 4: Build Q&A Pairs

**Extract questions from interviewers:**
- Convert interviewer statements/comments into **concise questions**
- If an interviewer makes an observation (e.g., "您的观点特别有意思，就是往窄处走"), turn it into a question (e.g., "您的创业逻辑是什么？为什么选择核药这个方向？")
- Number questions with Chinese numerals: `一、` `二、` `三、` ...

**Extract answers from the interviewee:**
- Use the interviewee's text as the answer content
- Split long continuous narratives into logical paragraphs by topic shifts

**Text cleanup:**
1. Remove filler words: 嗯, 啊, 呃, 哦, 嘛, 呀, 吧 (when used as verbal fillers, not grammatical particles)
2. Collapse repeated punctuation: `，，` → `，`
3. Remove trailing fragments: "对吧？", "是吧？", "你知道吧"
4. Fix obvious OCR/speech-recognition errors where context is clear
5. Preserve all technical terms, drug names, company names, numbers, percentages
6. DO NOT paraphrase or summarize — keep the original meaning and phrasing

**Answer consolidation (critical):**
- If the same topic is mentioned in multiple places across the transcript, **merge all related content into a single comprehensive answer**
- Short follow-up questions that revisit the same topic → append the response to the previous answer
- Topics that appear in early chat and are elaborated on later → merge into the first occurrence

### Step 5: Organize Content into Logical Sections

Group Q&A by theme, not by transcript order. Typical section structure:

| Section | Content |
|---------|---------|
| 个人背景与转行原因 | Education, research experience, why left academia |
| 创业逻辑与方向选择 | Why this industry, competitive moat |
| 核心技术布局 | Molecule design, pipeline, differentiation |
| 公司架构与团队 | Org structure, key people, fundraising |
| 行业见解 | Views on industry trends, competitors |
| 挑战与应对 | Specific challenges and solutions |

If the user requested specific topics, adjust the structure accordingly.

### Step 6: Generate the .docx

**Option A — Use the helper script for a first pass:**
```bash
python3 <skill-dir>/scripts/generate_interview_summary.py <input.docx> \
  --output <output.docx> \
  --title "项目名称" \
  --interviewee "姓名：___    职务：___" \
  --background "___" \
  --interviewer "___" \
  --location "___" \
  --date "___" \
  --method "现场访谈，电话访谈，☐视频访谈，☐其他_______" \
  --source "企业"
```
Then manually review and refine the output (questions need rewriting, answers need merging).

**Option B — Build from template (recommended for best quality):**
1. Copy `<skill-dir>/assets/访谈纪要模板.docx` as a starting point
2. Fill in the metadata table with user-provided values
3. Write each Q&A pair manually with proper reformulation:

```
   一、[Converted question in bold, 宋体 12pt]
   [Merged answer in normal, 宋体 12pt]

   二、[Next question]
   [Next answer]
   ...
```

4. Ensure each question is a proper Chinese question (not a verbatim transcript line)

### Step 7: Validate and Deliver

- Questions should read naturally as standalone questions
- Answers should be coherent, filler-free, and logically organized
- Merged answers should not contain duplicate content
- Verify the `.docx` opens and renders correctly
- Tell the user what you did: number of Q&A pairs, any merge decisions made

## Output Format Details

| Element | Style | Font |
|---------|-------|------|
| Title | Centered, 2 lines | 微软雅黑 18pt |
| Table left col | Bold | 宋体 12pt |
| Table right col | Normal | 宋体 12pt |
| "访谈纪要：" header | Bold | 宋体 12pt |
| Question text | Bold | 宋体 12pt |
| Answer text | Normal | 宋体 12pt |
| Spacing | 1.5 line spacing | — |

## Page Setup

- A4 paper (21 × 29.7 cm)
- Margins: L/R 3.17 cm, T/B 2.54 cm
