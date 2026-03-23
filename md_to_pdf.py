#!/usr/bin/env python3

from __future__ import annotations

import re
import os
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = ROOT_DIR / ".venv" / "bin" / "python"

if VENV_PYTHON.exists() and sys.prefix == sys.base_prefix:
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), str(Path(__file__).resolve()), *sys.argv[1:]])

try:
    from PIL import Image as PILImage
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (
        Image,
        Paragraph,
        Preformatted,
        SimpleDocTemplate,
        Spacer,
    )
except ModuleNotFoundError as exc:
    print(
        "Missing dependency. Install in .venv: pip install reportlab pillow",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


IMG_PATTERN = re.compile(r"!\[(.*?)\]\(([^)]+)\)")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$")
ORDERED_LIST_PATTERN = re.compile(r"^(\d+)\.\s+(.*)$")
CODE_FENCE_PATTERN = re.compile(r"^```")
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def register_fonts() -> None:
    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("Arial", str(font_dir / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(font_dir / "Arial Bold.ttf")))
    pdfmetrics.registerFont(
        TTFont("Arial-Italic", str(font_dir / "Arial Italic.ttf"))
    )
    pdfmetrics.registerFont(TTFont("CourierNew", str(font_dir / "Courier New.ttf")))


def make_styles() -> tuple[ParagraphStyle, ParagraphStyle, ParagraphStyle, dict[int, ParagraphStyle]]:
    styles = getSampleStyleSheet()

    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Arial",
        fontSize=10.5,
        leading=14,
        spaceBefore=0,
        spaceAfter=5,
    )
    quote = ParagraphStyle(
        "Quote",
        parent=body,
        fontName="Arial-Italic",
        leftIndent=12,
        textColor=colors.HexColor("#444444"),
    )
    code = ParagraphStyle(
        "Code",
        parent=body,
        fontName="CourierNew",
        fontSize=9,
        leading=11,
        leftIndent=10,
    )

    headings: dict[int, ParagraphStyle] = {}
    for level, size, before, after in [
        (1, 20, 10, 10),
        (2, 16, 8, 8),
        (3, 14, 7, 6),
        (4, 12, 6, 5),
        (5, 11, 5, 4),
        (6, 10.5, 4, 4),
    ]:
        headings[level] = ParagraphStyle(
            f"H{level}",
            parent=body,
            fontName="Arial-Bold",
            fontSize=size,
            leading=size + 3,
            spaceBefore=before,
            spaceAfter=after,
        )

    return body, quote, code, headings


def resolve_image_path(md_path: Path, rel_path: str) -> Path:
    if rel_path.startswith("/"):
        return (md_path.parents[1] / rel_path.lstrip("/")).resolve()
    return (md_path.parent / rel_path).resolve()


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def format_inline(text: str) -> str:
    text = LINK_PATTERN.sub(lambda m: f"{m.group(1)} ({m.group(2)})", text)
    parts = re.split(r"(`[^`]+`)", text)
    rendered: list[str] = []

    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) >= 2:
            rendered.append(f'<font face="CourierNew">{escape(part[1:-1])}</font>')
        else:
            rendered.append(escape(part))

    return "".join(rendered)


def add_image(
    story: list,
    md_path: Path,
    rel_path: str,
    alt: str,
    max_width: float,
    quote_style: ParagraphStyle,
    code_style: ParagraphStyle,
) -> None:
    img_path = resolve_image_path(md_path, rel_path)
    if not img_path.exists():
        story.append(
            Paragraph(format_inline(f"[missing image] {rel_path}"), code_style)
        )
        return

    with PILImage.open(img_path) as im:
        width_px, height_px = im.size

    max_height = 180 * mm
    scale = min(max_width / width_px, max_height / height_px, 1.0)
    width = width_px * scale
    height = height_px * scale

    if alt:
        story.append(Paragraph(format_inline(alt), quote_style))
    story.append(Image(str(img_path), width=width, height=height))
    story.append(Spacer(1, 4))


def add_text_line(
    story: list,
    text: str,
    body_style: ParagraphStyle,
    quote_style: ParagraphStyle,
    code_style: ParagraphStyle,
) -> None:
    stripped = text.strip()
    if not stripped:
        story.append(Spacer(1, 4))
        return

    if stripped.startswith("|") and stripped.endswith("|"):
        story.append(Preformatted(text, code_style))
        return

    if stripped.startswith("> "):
        story.append(Paragraph(format_inline(stripped[2:].strip()), quote_style))
        return

    ordered = ORDERED_LIST_PATTERN.match(stripped)
    if ordered:
        story.append(
            Paragraph(
                format_inline(ordered.group(2)),
                body_style,
                bulletText=f"{ordered.group(1)}.",
            )
        )
        return

    if stripped.startswith("- "):
        story.append(
            Paragraph(format_inline(stripped[2:].strip()), body_style, bulletText="•")
        )
        return

    story.append(Paragraph(format_inline(stripped), body_style))


def build_pdf(md_path: Path, pdf_path: Path) -> Path:
    register_fonts()
    body_style, quote_style, code_style, heading_styles = make_styles()

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title=md_path.stem,
    )
    max_width = A4[0] - doc.leftMargin - doc.rightMargin
    story: list = []
    in_code = False
    code_lines: list[str] = []

    for raw_line in md_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if CODE_FENCE_PATTERN.match(stripped):
            if in_code:
                story.append(Preformatted("\n".join(code_lines), code_style))
                story.append(Spacer(1, 4))
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        heading = HEADING_PATTERN.match(stripped)
        if heading:
            level = len(heading.group(1))
            story.append(
                Paragraph(format_inline(heading.group(2).strip()), heading_styles[level])
            )
            continue

        if stripped == "---":
            story.append(Spacer(1, 10))
            continue

        images = IMG_PATTERN.findall(line)
        if images:
            cleaned = normalize_text(IMG_PATTERN.sub("", line))
            for alt, rel_path in images:
                add_image(
                    story,
                    md_path,
                    rel_path,
                    alt,
                    max_width,
                    quote_style,
                    code_style,
                )
            if cleaned:
                add_text_line(story, cleaned, body_style, quote_style, code_style)
            continue

        add_text_line(story, line, body_style, quote_style, code_style)

    if code_lines:
        story.append(Preformatted("\n".join(code_lines), code_style))

    def add_page_number(canvas, pdf_doc) -> None:
        canvas.setFont("Arial", 9)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawRightString(A4[0] - pdf_doc.rightMargin, 10 * mm, str(canvas.getPageNumber()))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    return pdf_path


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: md_to_pdf.py INPUT_MD [OUTPUT_PDF]", file=sys.stderr)
        return 1

    md_path = Path(argv[1]).expanduser().resolve()
    if len(argv) > 2:
        pdf_path = Path(argv[2]).expanduser().resolve()
    else:
        pdf_path = md_path.with_suffix(".pdf")

    if not md_path.exists():
        print(f"Input markdown not found: {md_path}", file=sys.stderr)
        return 1

    out = build_pdf(md_path, pdf_path)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
