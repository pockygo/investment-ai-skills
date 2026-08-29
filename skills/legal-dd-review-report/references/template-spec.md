# Retained DOCX template contract

## Reference identity

- Asset: `assets/review-report-template.docx`
- Source name: `5-法律尽调审阅报告.docx`
- SHA-256: `32428FE9F45DAB66D09EE40A7A077E86B16EA33BEF652139DC4F47F7E532F508`
- Rendered reference page count: 11 pages in WPS PDF export
- Sections: 1
- Page: A4 portrait, 21.0 × 29.7 cm
- Margins: left/right 3.175 cm; top/bottom 2.54 cm
- Different first page: no
- Header/footer: preserve the asset's thin horizontal rule and centered PAGE field

## Visual roles

| Role | Source treatment |
|---|---|
| Company title | Centered, 22 pt, bold, on cover |
| Report title | Centered, 18 pt, regular, on cover |
| Department/date | Centered, 14 pt |
| TOC title | Centered, 16 pt, bold |
| Chapter heading | `IPO Heading 2`, bold, 14 pt, black |
| Issue heading | `IPO Heading 3`, bold |
| Block heading | `IPO Heading 4`, bold |
| Body | `IPO Normal` or source `Normal`, Song for Chinese, Times New Roman for Latin/numerals, 12 pt, 1.5 line spacing, justified |
| Table | `Table Grid`, black borders, compact 10–12 pt, repeating header |

The asset contains direct formatting in addition to named styles. Use the named `IPO` styles for generated body content and explicit cover formatting. Do not normalize the template or apply another style pack.

## Editable slots and preservation

`scripts/build_report.py` clears only the body of a working copy and rebuilds cover metadata, TOC, Chapter I, Chapter II, and Chapter III. It retains styles, section geometry, header/footer relationships, numbering resources, and page furniture. The asset itself is preserve-only and must never be overwritten.

## Fidelity gates

- Confirm the asset hash before use; redistill if it changes.
- Preserve A4 geometry, margins, header rule, footer/page number, style names, and monochrome legal-report aesthetic.
- Do not retain any source-company text from the asset in a new report.
- Update the TOC after pagination changes. If application refresh is unavailable, ensure `w:updateFields=true` and disclose deferred refresh.
- Render and inspect all pages after generation. Use the asset render as the design authority.

## Distillation evidence

The source remained unchanged. Visual inspection covered all 11 pages. Structural inspection covered body paragraphs, the tax table, header/footer, PAGEREF/PAGE fields, styles, section geometry, and package parts. The source uses custom IPO styles rather than standard Word Heading styles.

