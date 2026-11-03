#!/usr/bin/env python3
"""Check a local filing's PDF structure and optional text clues; no network IO."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata


def normalize(text):
    # Some CMaps leave NULs between otherwise usable characters.
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text).replace("\x00", ""))


def check_pdf(path, identities=(), periods=(), sample_pages=8):
    result = {"path": str(path.resolve()), "structurally_valid": False,
              "identity_clues": [], "period_clues": [],
              "content_scope": "not_assessed"}
    try:
        from pypdf import PdfReader
    except ImportError:
        return {**result, "status": "dependency_unavailable", "error": "pypdf is required"}, 2
    try:
        patterns = {"identity_clues": [re.compile(p, re.I | re.S) for p in identities],
                    "period_clues": [re.compile(p, re.I | re.S) for p in periods]}
    except re.error as exc:
        return {**result, "status": "invalid_pattern", "error": str(exc)}, 2
    try:
        with path.open("rb") as stream:
            head = stream.read(1024)
            if b"%PDF-" not in head:
                raise ValueError("PDF header not found")
            stream.seek(0)
            hasher = hashlib.sha256()
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                hasher.update(block)
            digest = hasher.hexdigest()
        reader = PdfReader(path)
        if reader.is_encrypted and not reader.decrypt(""):
            return {**result, "status": "encrypted_review_required"}, 3
        page_count = len(reader.pages)
        if page_count < 1:
            raise ValueError("No pages")
        result.update(structurally_valid=True, bytes=path.stat().st_size,
                      pages=page_count, sha256=digest)
        extracted, failures = [], []
        for idx in range(min(sample_pages, page_count)):
            try:
                extracted.append(reader.pages[idx].extract_text() or "")
            except Exception as exc:
                failures.append({"page": idx + 1, "error": str(exc)[:180]})
        text = normalize("\n".join(extracted))
        result.update(sampled_pages=min(sample_pages, page_count),
                      extracted_characters=len(text), extraction_failures=failures)
        for field, compiled in patterns.items():
            result[field] = [{"pattern": p.pattern, "matched": bool(p.search(text))}
                             for p in compiled]
        has_checks = bool(identities or periods)
        checks_ok = all(c["matched"] for field in patterns for c in result[field])
        if failures or (has_checks and not checks_ok):
            result["status"] = "visual_or_manual_review_required"
            return result, 3
        result["status"] = "pdf_and_requested_clues_pass" if has_checks else "pdf_valid_content_unchecked"
        return result, 0
    except Exception as exc:
        return {**result, "status": "invalid_or_unreadable_pdf", "error": str(exc)[:300]}, 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--identity", action="append", default=[], help="Required normalized-text regex; repeatable")
    parser.add_argument("--period", action="append", default=[], help="Required period clue regex; repeatable")
    parser.add_argument("--sample-pages", type=int, default=8)
    args = parser.parse_args()
    if args.sample_pages < 1:
        parser.error("--sample-pages must be positive")
    result, code = check_pdf(args.pdf, args.identity, args.period, args.sample_pages)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
