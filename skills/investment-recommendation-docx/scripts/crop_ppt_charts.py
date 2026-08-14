#!/usr/bin/env python3
"""Crop native chart regions from rendered slide PNGs using extraction coordinates."""

import argparse
import json
from pathlib import Path

from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("extract_json")
    ap.add_argument("slides_dir", help="Directory containing slide_001.png or slide-1.png renders")
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()
    data = json.loads(Path(args.extract_json).read_text(encoding="utf-8"))
    slides = Path(args.slides_dir)
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    sw, sh = data["slide_width"], data["slide_height"]
    made = 0
    for s in data["slides"]:
        if not s["charts"]:
            continue
        candidates = [slides / f"slide_{s['slide']:03d}.png", slides / f"slide_{s['slide']:02d}.png", slides / f"slide-{s['slide']}.png"]
        src = next((p for p in candidates if p.exists()), None)
        if src is None:
            raise FileNotFoundError(f"No rendered image for slide {s['slide']}")
        im = Image.open(src).convert("RGB")
        sx, sy = im.width / sw, im.height / sh
        for idx, c in enumerate(s["charts"], 1):
            px, py = int(im.width * 0.02), int(im.height * 0.02)
            box = (max(0, int(c["left"]*sx)-px), max(0, int(c["top"]*sy)-py), min(im.width, int((c["left"]+c["width"])*sx)+px), min(im.height, int((c["top"]+c["height"])*sy)+py))
            im.crop(box).save(out / f"slide_{s['slide']:03d}_chart_{idx}.png")
            made += 1
    print(f"created {made} chart crops")


if __name__ == "__main__":
    main()
