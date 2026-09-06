#!/usr/bin/env python3
"""Convert multiple PDFs to page-anchored text and write a manifest."""
import argparse
import json
import re
import subprocess
from pathlib import Path


def safe_name(value):
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")
    if not value:
        raise ValueError("empty output name")
    return value


def convert(pdf, dest):
    raw = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        check=True, capture_output=True, text=True
    ).stdout
    pages = raw.split("\f")
    blocks = []
    for number, page in enumerate(pages, 1):
        if page.strip():
            blocks.extend([f"<!-- p{number} -->", page.strip(), ""])
    dest.write_text("\n".join(blocks), encoding="utf-8")
    return len([p for p in pages if p.strip()])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("out_dir")
    parser.add_argument("pdfs", nargs="+")
    parser.add_argument("--names", nargs="*", help="one stable period name per PDF")
    args = parser.parse_args()
    if args.names and len(args.names) != len(args.pdfs):
        parser.error("--names count must match PDF count")
    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for idx, item in enumerate(args.pdfs):
        pdf = Path(item).resolve()
        if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
            raise SystemExit(f"not a PDF file: {pdf}")
        name = safe_name(args.names[idx] if args.names else pdf.stem)
        dest = out / f"{name}.md"
        pages = convert(pdf, dest)
        rows.append({"name": name, "source": str(pdf), "output": str(dest), "pages": pages})
        print(f"OK {pdf.name} -> {dest.name} ({pages} pages)")
    (out / "manifest.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
