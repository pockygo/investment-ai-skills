"""按文档顺序导出 docx 的段落（含样式与 run 结构）和表格内容，并列出填充色。

用法: python dump_docx.py <file.docx>
"""
import re
import sys
import zipfile

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def main(path: str) -> None:
    doc = Document(path)
    idx_t = 0
    for child in doc.element.body.iterchildren():
        if child.tag == f'{W}p':
            p = Paragraph(child, doc)
            runs = [r.text for r in p.runs]
            print(f'[P style={p.style.name!r} runs={len(p.runs)}] {p.text}')
            if len(runs) > 1:
                for j, rt in enumerate(runs):
                    print(f'    run{j}: {rt!r}')
        elif child.tag == f'{W}tbl':
            t = Table(child, doc)
            print(f'===== TABLE {idx_t} ({len(t.rows)}r x {len(t.columns)}c) =====')
            for r in t.rows:
                print(' || '.join(c.text.replace('\n', '\\n') for c in r.cells))
            idx_t += 1
    # 页眉页脚
    for i, sec in enumerate(doc.sections):
        for kind, part in (('header', sec.header), ('footer', sec.footer)):
            for p in part.paragraphs:
                if p.text.strip():
                    print(f'[{kind} sec{i}] {p.text}')
    xml = zipfile.ZipFile(path).read('word/document.xml').decode('utf8')
    print('shading fills:', sorted(set(re.findall(r'w:fill="([0-9A-Fa-f]{6})"', xml))))


if __name__ == '__main__':
    main(sys.argv[1])
