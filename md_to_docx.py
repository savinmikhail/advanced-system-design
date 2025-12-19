#!/usr/bin/env python3

import re
import sys
from pathlib import Path

from docx import Document
from docx.shared import Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


# Full-line markdown image: ![alt](path)
IMG_PATTERN = re.compile(r"!\[(.*?)\]\(([^)]+)\)")

# Markdown ATX heading: #, ##, ..., ###### at start of line
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$")

# TOC item inside "Оглавление" section: "- [Title](#anchor)"
TOC_ITEM_PATTERN = re.compile(r"^(\s*)[-*]\s+\[(.+?)\]\([^)]+\)\s*$")


def _add_word_toc(doc: Document) -> None:
    """
    Insert a Word auto-generated TOC field that uses Heading 1–4.
    Пользователю нужно будет обновить поля в Word (F9 / Update field).
    """
    paragraph = doc.add_paragraph()
    # TOC over Heading levels 1–4, with hyperlinks etc.
    instr = r'TOC \o "1-4" \h \z \u'

    fld_simple = OxmlElement("w:fldSimple")
    fld_simple.set(qn("w:instr"), instr)
    paragraph._p.append(fld_simple)

    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "Оглавление (обновите поля в Word)"
    r.append(t)
    fld_simple.append(r)


def md_to_docx(md_path: str, docx_path: str | None = None) -> Path:
    """
    Convert a Markdown file to DOCX, replacing full-line image markdown
    like `![alt](path)` with actual images.
    """

    md_path_obj = Path(md_path).expanduser().resolve()
    if docx_path is None:
        docx_path_obj = md_path_obj.with_suffix(".docx")
    else:
        docx_path_obj = Path(docx_path).expanduser().resolve()

    if not md_path_obj.exists():
        raise FileNotFoundError(f"Input markdown not found: {md_path_obj}")

    text = md_path_obj.read_text(encoding="utf-8")
    lines = text.splitlines()

    doc = Document()
    assets_root = md_path_obj.parent

    in_toc = False

    for line in lines:
        stripped = line.strip()

        # Headings: "# Title" -> Word "Heading 1", etc.
        heading_match = HEADING_PATTERN.match(stripped)
        if heading_match:
            hashes, title = heading_match.groups()
            level = min(len(hashes), 4)  # map 1–4, 5/6 тоже в Heading 4
            style = f"Heading {level}"
            doc.add_paragraph(title.strip(), style=style)
            # Считаем, что после "Оглавление" идут специальные строки оглавления.
            # Вместо ручного списка в DOCX вставляем авто-оглавление Word.
            if title.strip().lower() == "оглавление":
                in_toc = True
                _add_word_toc(doc)
            continue

        # Конец секции оглавления после разделителя '---'
        if in_toc and stripped == "---":
            in_toc = False
            continue

        # Строки вида "- [Блок ...](#anchor)" внутри оглавления
        toc_match = TOC_ITEM_PATTERN.match(line)
        if in_toc and toc_match:
            # В DOCX не дублируем ручное маркдаун-оглавление —
            # здесь оно заменяется авто-TOC Word.
            continue

        img_match = IMG_PATTERN.fullmatch(stripped)
        if img_match:
            alt, rel_path = img_match.groups()
            img_path = (assets_root / rel_path).resolve()

            if img_path.exists():
                if alt:
                    doc.add_paragraph(alt)
                try:
                    doc.add_picture(str(img_path), width=Inches(5))
                except Exception as exc:
                    doc.add_paragraph(f"[image error: {alt}] {rel_path} ({exc})")
            else:
                # If the image file is missing, keep the original markdown line
                doc.add_paragraph(line)
        else:
            doc.add_paragraph(line)

    doc.save(docx_path_obj)
    return docx_path_obj


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: md_to_docx.py INPUT_MD [OUTPUT_DOCX]", file=sys.stderr)
        return 1

    md_path = argv[1]
    docx_path = argv[2] if len(argv) > 2 else None

    out = md_to_docx(md_path, docx_path)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
