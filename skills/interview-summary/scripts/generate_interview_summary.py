"""
Interview Summary Generator (访谈纪要生成器)

Reads a verbatim interview transcript (.docx), asks for metadata,
and generates a formatted interview summary document (.docx).

Usage:
    python generate_interview_summary.py <transcript_path> [--output <output_path>]
"""

import docx
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import re
import sys
import os
from pathlib import Path

# ── Helper: page / paragraph setup ──────────────────────────────────

def _setup_document(doc):
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)

def _add_para(doc, text, font_name="宋体", font_size=12, bold=None,
              align=None, space_before=0, space_after=0):
    para = doc.add_paragraph()
    if align is not None:
        para.alignment = align
    run = para.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(font_size)
    if bold is not None:
        run.bold = bold
    pf = para.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.5
    return para

def _add_empty(doc, size=6):
    para = doc.add_paragraph()
    run = para.add_run("")
    run.font.size = Pt(size)
    pf = para.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    return para


# ── Transcript parsing ──────────────────────────────────────────────

def parse_transcript(docx_path):
    """Parse a transcript docx into a list of (speaker_label, timestamp, text) turns."""
    doc = docx.Document(docx_path)
    turns = []
    speaker = None
    timestamp = None
    texts = []

    for para in doc.paragraphs:
        txt = para.text.strip()
        if not txt:
            continue
        # Detect "发言人1 00:00" style headers
        m = re.match(r"^(发言人[12])\s+([\d:]+)$", txt)
        if m:
            if speaker and texts:
                turns.append((speaker, timestamp, "".join(texts)))
            speaker = m.group(1)
            timestamp = m.group(2)
            texts = []
        elif speaker:
            texts.append(txt)

    if speaker and texts:
        turns.append((speaker, timestamp, "".join(texts)))

    return turns


def identify_speakers(turns):
    """
    Auto-detect which speaker is the interviewee and which are interviewers.
    Returns (interviewee_label, interviewer_labels).
    Heuristic: the person who speaks more is the interviewee.
    """
    word_counts = {}
    for spk, _, text in turns:
        word_counts[spk] = word_counts.get(spk, 0) + len(text)

    sorted_spk = sorted(word_counts.items(), key=lambda x: -x[1])
    interviewee = sorted_spk[0][0]
    interviewers = [s for s, _ in sorted_spk[1:]]
    return interviewee, interviewers


def clean_text(text):
    """Remove filler words and repeated punctuation."""
    # Remove common verbal fillers conservatively, without stripping grammar particles.
    text = re.sub(r"[嗯呃哦]+", "", text)
    text = re.sub(r"(^|[，。！？；：、\s])[啊嘛呀]+(?=[，。！？；：、\s]|$)", r"\1", text)
    # Collapse repeated punctuation
    text = re.sub(r"([，。！？；：、]){2,}", r"\1", text)
    # Collapse multiple spaces
    text = re.sub(r"\s+", "", text)
    # Remove trailing fragments like "对吧？", "是吧？" at end of sentences
    text = re.sub(r"[是对]吧[？吗。]?\s*$", "。", text)
    # Clean up leading and trailing
    text = text.strip("，。；：、 \t")
    if text and not text.endswith(("。", "？", "！", "；", "。")):
        text += "。"
    return text


def chinese_number(num):
    """Return a Chinese section number for common Q&A counts."""
    digits = "零一二三四五六七八九"
    if num <= 10:
        return "十" if num == 10 else digits[num]
    if num < 20:
        return "十" + digits[num % 10]
    tens, ones = divmod(num, 10)
    return digits[tens] + "十" + (digits[ones] if ones else "")


def group_qa(turns, interviewee, interviewers):
    """
    Group turns into Q&A pairs.
    Interviewer statements/questions → Question text
    Interviewee responses → Answer text (accumulated)
    """
    qa_pairs = []
    current_q = None
    current_a_parts = []

    for spk, ts, text in turns:
        if spk == interviewee:
            cleaned = clean_text(text)
            if cleaned and len(cleaned) > 5:  # skip very short utterances
                current_a_parts.append(cleaned)
        else:
            # Save previous Q&A
            if current_q is not None and current_a_parts:
                qa_pairs.append((current_q, list(current_a_parts)))
            # Start new question
            current_q = clean_text(text) if len(text) > 10 else text
            current_a_parts = []

    # Last pair
    if current_q is not None and current_a_parts:
        qa_pairs.append((current_q, list(current_a_parts)))

    # Merge consecutive answers about the same topic
    return qa_pairs


def merge_related_qa(qa_pairs):
    """
    Merge Q&A pairs where the same topic is revisited later.
    Detected by keyword overlap between questions.
    """
    if not qa_pairs:
        return qa_pairs

    merged = [qa_pairs[0]]
    for q, a_parts in qa_pairs[1:]:
        prev_q, prev_a = merged[-1]
        # Simple heuristic: if questions share key terms, merge answers
        q_keywords = set(re.findall(r"[\u4e00-\u9fff\w]{2,}", q))
        prev_keywords = set(re.findall(r"[\u4e00-\u9fff\w]{2,}", prev_q))
        overlap = q_keywords & prev_keywords

        # Also check if this looks like a follow-up (short question)
        is_followup = len(q) < 20

        if is_followup or (overlap and len(overlap) / max(len(q_keywords), 1) > 0.3):
            # Merge answers
            prev_a.extend(a_parts)
        else:
            merged.append((q, a_parts))

    return merged


# ── Document generation ─────────────────────────────────────────────

def generate_summary(transcript_path, output_path, metadata):
    """
    Generate a formatted interview summary.
    metadata: dict with keys: title, 访谈类型, 访谈对象, 访谈对象背景,
              访谈人员, 访谈地点, 访谈时间, 访谈方式, 访谈对象来源
    """
    # Parse transcript
    turns = parse_transcript(transcript_path)
    interviewee, interviewers = identify_speakers(turns)
    qa_pairs = group_qa(turns, interviewee, interviewers)
    qa_pairs = merge_related_qa(qa_pairs)

    # Verify: if there are no meaningful Q&A, fall back to showing raw content
    if not qa_pairs:
        # Join all interviewee text and present as continuous narrative
        all_text = "".join(clean_text(t) for spk, _, t in turns if spk == interviewee)
        qa_pairs = [("访谈内容", [all_text])]

    doc = Document()
    _setup_document(doc)

    # ── Title ──
    title_text = metadata.get("title", "项目访谈问卷")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(title_text)
    r.font.name = "微软雅黑"
    r.font.size = Pt(18)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.5

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("项目访谈问卷")
    r2.font.name = "微软雅黑"
    r2.font.size = Pt(18)
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(0)
    p2.paragraph_format.line_spacing = 1.5

    _add_empty(doc)

    # ── Table ──
    table_labels = ["访谈类型", "访谈对象", "访谈对象背景",
                    "访谈人员", "访谈地点", "访谈时间", "访谈方式", "访谈对象来源"]
    table = doc.add_table(rows=8, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT

    for i, label in enumerate(table_labels):
        key = label
        value = metadata.get(key, "—")

        cell0 = table.rows[i].cells[0]
        cell0.text = ""
        p0 = cell0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        r0.font.name = "宋体"
        r0.font.size = Pt(12)
        r0.bold = True

        cell1 = table.rows[i].cells[1]
        cell1.text = ""
        p1 = cell1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(value)
        r1.font.name = "宋体"
        r1.font.size = Pt(12)
        r1.bold = False

    for row in table.rows:
        row.cells[0].width = Cm(3.5)

    _add_empty(doc)

    # ── Interview Notes ──
    _add_para(doc, "访谈纪要：", font_name="宋体", font_size=12,
              bold=True, space_before=6, space_after=3)

    # ── Q&A Content ──
    for idx, (question, answers) in enumerate(qa_pairs, 1):
        q_text = question if len(question) > 5 else f"问题{idx}"
        if not re.match(r"^[一二三四五六七八九十]+、", q_text):
            q_text = f"{chinese_number(idx)}、{q_text}"
        _add_para(doc, q_text, font_name="宋体", font_size=12,
                  bold=True, space_before=6, space_after=0)
        for ans in answers:
            _add_para(doc, ans, font_name="宋体", font_size=12,
                      bold=False, space_before=0, space_after=2)
        _add_empty(doc)

    doc.save(output_path)
    return output_path, len(qa_pairs)


# ── CLI entry point ─────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate interview summary from transcript")
    parser.add_argument("transcript", help="Path to verbatim transcript .docx file")
    parser.add_argument("--output", "-o", default=None, help="Output .docx path (default: auto-generated)")
    parser.add_argument("--title", default="访谈项目", help="Project / company name for the title")
    parser.add_argument("--type", default="高管访谈", help="访谈类型")
    parser.add_argument("--interviewee", default="", help="访谈对象 (姓名：___  职务：___)")
    parser.add_argument("--background", default="", help="访谈对象背景")
    parser.add_argument("--interviewer", default="", help="访谈人员")
    parser.add_argument("--location", default="", help="访谈地点")
    parser.add_argument("--date", default="", help="访谈时间")
    parser.add_argument("--method", default="现场访谈", help="访谈方式")
    parser.add_argument("--source", default="企业", help="访谈对象来源")

    args = parser.parse_args()

    if not os.path.exists(args.transcript):
        print(f"[Error] Transcript file not found: {args.transcript}")
        sys.exit(1)

    metadata = {
        "title": args.title,
        "访谈类型": args.type,
        "访谈对象": args.interviewee,
        "访谈对象背景": args.background,
        "访谈人员": args.interviewer,
        "访谈地点": args.location,
        "访谈时间": args.date,
        "访谈方式": args.method,
        "访谈对象来源": args.source,
    }

    output = args.output
    if output is None:
        base = os.path.splitext(os.path.basename(args.transcript))[0]
        output = os.path.join(os.path.dirname(args.transcript),
                              f"{base}_访谈纪要.docx")

    result_path, qa_count = generate_summary(args.transcript, output, metadata)
    print(f"[OK] Generated interview summary: {result_path}")
    print(f"     {qa_count} Q&A pairs extracted")


if __name__ == "__main__":
    main()
