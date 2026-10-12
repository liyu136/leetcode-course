from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
LESSONS_DIR = ROOT / "lessons"
OUTPUT_DIR = ROOT / "output" / "pdf"
INDIVIDUAL_DIR = OUTPUT_DIR / "individual"
COMBINED_PATH = OUTPUT_DIR / "leetcode-complete-course.pdf"

FONT_REGULAR = Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\simhei.ttf")
FONT_MONO = Path(r"C:\Windows\Fonts\consola.ttf")
FONT_MONO_BOLD = Path(r"C:\Windows\Fonts\consolab.ttf")

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 18 * mm
RIGHT_MARGIN = 18 * mm
TOP_MARGIN = 18 * mm
BOTTOM_MARGIN = 17 * mm
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN


def register_fonts() -> None:
    required = [FONT_REGULAR, FONT_BOLD, FONT_MONO, FONT_MONO_BOLD]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing fonts: {missing}")

    pdfmetrics.registerFont(TTFont("CourseSans", str(FONT_REGULAR)))
    pdfmetrics.registerFont(TTFont("CourseSansBold", str(FONT_BOLD)))
    pdfmetrics.registerFont(TTFont("CourseMono", str(FONT_MONO)))
    pdfmetrics.registerFont(TTFont("CourseMonoBold", str(FONT_MONO_BOLD)))
    pdfmetrics.registerFontFamily(
        "CourseSans",
        normal="CourseSans",
        bold="CourseSansBold",
        italic="CourseSans",
        boldItalic="CourseSansBold",
    )


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "CourseTitle",
            parent=base["Title"],
            fontName="CourseSansBold",
            fontSize=23,
            leading=31,
            textColor=colors.HexColor("#10233F"),
            spaceAfter=12,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "h2": ParagraphStyle(
            "CourseH2",
            parent=base["Heading2"],
            fontName="CourseSansBold",
            fontSize=15,
            leading=21,
            textColor=colors.HexColor("#0B6E69"),
            spaceBefore=13,
            spaceAfter=7,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "h3": ParagraphStyle(
            "CourseH3",
            parent=base["Heading3"],
            fontName="CourseSansBold",
            fontSize=12.5,
            leading=18,
            textColor=colors.HexColor("#244A73"),
            spaceBefore=10,
            spaceAfter=5,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "h4": ParagraphStyle(
            "CourseH4",
            parent=base["Heading4"],
            fontName="CourseSansBold",
            fontSize=10.8,
            leading=16,
            textColor=colors.HexColor("#394B63"),
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "body": ParagraphStyle(
            "CourseBody",
            parent=base["BodyText"],
            fontName="CourseSans",
            fontSize=9.6,
            leading=15.5,
            textColor=colors.HexColor("#1D2939"),
            spaceAfter=6,
            wordWrap="CJK",
        ),
        "bullet": ParagraphStyle(
            "CourseBullet",
            parent=base["BodyText"],
            fontName="CourseSans",
            fontSize=9.4,
            leading=14.5,
            leftIndent=14,
            firstLineIndent=-9,
            spaceAfter=3,
            wordWrap="CJK",
        ),
        "quote": ParagraphStyle(
            "CourseQuote",
            parent=base["BodyText"],
            fontName="CourseSans",
            fontSize=9.5,
            leading=15,
            textColor=colors.HexColor("#214B47"),
            leftIndent=4,
            rightIndent=4,
            spaceAfter=0,
            wordWrap="CJK",
        ),
        "code": ParagraphStyle(
            "CourseCode",
            parent=base["Code"],
            fontName="CourseMono",
            fontSize=7.7,
            leading=10.6,
            textColor=colors.HexColor("#172235"),
            backColor=colors.HexColor("#F1F4F7"),
            borderColor=colors.HexColor("#AEB9C7"),
            borderWidth=0.5,
            borderPadding=8,
            borderRadius=4,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "table_header": ParagraphStyle(
            "CourseTableHeader",
            parent=base["BodyText"],
            fontName="CourseSansBold",
            fontSize=8.2,
            leading=11.5,
            textColor=colors.white,
            alignment=TA_CENTER,
            wordWrap="CJK",
        ),
        "table_cell": ParagraphStyle(
            "CourseTableCell",
            parent=base["BodyText"],
            fontName="CourseSans",
            fontSize=8.1,
            leading=11.5,
            textColor=colors.HexColor("#263548"),
            wordWrap="CJK",
        ),
        "toc_title": ParagraphStyle(
            "CourseTOCTitle",
            parent=base["Title"],
            fontName="CourseSansBold",
            fontSize=28,
            leading=38,
            textColor=colors.HexColor("#10233F"),
            alignment=TA_CENTER,
            spaceAfter=16,
            wordWrap="CJK",
        ),
    }
    return styles


INLINE_CODE = re.compile(r"`([^`]+)`")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")


def inline_markup(text: str) -> str:
    placeholders: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        content = html.escape(match.group(1))
        token = f"@@CODE{len(placeholders)}@@"
        placeholders.append(
            f'<font name="CourseMono" color="#8A3D00" backColor="#FFF0D9">{content}</font>'
        )
        return token

    def stash_link(match: re.Match[str]) -> str:
        label = html.escape(match.group(1))
        href = html.escape(match.group(2), quote=True)
        token = f"@@CODE{len(placeholders)}@@"
        placeholders.append(f'<link href="{href}" color="#1769AA"><u>{label}</u></link>')
        return token

    text = INLINE_CODE.sub(stash_code, text)
    text = LINK.sub(stash_link, text)
    text = html.escape(text)
    text = BOLD.sub(r'<font name="CourseSansBold">\1</font>', text)
    text = ITALIC.sub(r"<i>\1</i>", text)

    for index, replacement in enumerate(placeholders):
        text = text.replace(f"@@CODE{index}@@", replacement)

    return text


def parse_table(lines: list[str], styles: dict[str, ParagraphStyle]) -> Table:
    rows: list[list[str]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)

    if not rows:
        return Table([[]])

    columns = max(len(row) for row in rows)
    for row in rows:
        row.extend([""] * (columns - len(row)))

    rendered: list[list[Paragraph]] = []
    for row_index, row in enumerate(rows):
        style = styles["table_header"] if row_index == 0 else styles["table_cell"]
        rendered.append([Paragraph(inline_markup(cell), style) for cell in row])

    lengths = []
    for col in range(columns):
        maximum = max(len(re.sub(r"[`*_]", "", row[col])) for row in rows)
        lengths.append(max(5, min(maximum, 30)))

    total = sum(lengths)
    widths = [CONTENT_WIDTH * length / total for length in lengths]

    table = Table(rendered, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#244A73")),
                ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#AAB8C8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F6FA")]),
            ]
        )
    )
    return table


def markdown_to_story(markdown: str, styles: dict[str, ParagraphStyle]) -> tuple[list, str]:
    lines = markdown.replace("\r\n", "\n").split("\n")
    story: list = []
    paragraph_lines: list[str] = []
    title = ""
    index = 0

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            joined = " ".join(line.strip() for line in paragraph_lines)
            story.append(Paragraph(inline_markup(joined), styles["body"]))
            paragraph_lines = []

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            language = stripped[3:].strip()
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index].expandtabs(4))
                index += 1
            label = f"[{language}]\n" if language and language != "text" else ""
            code = label + "\n".join(code_lines).rstrip()
            story.append(
                Preformatted(
                    code or " ",
                    styles["code"],
                    maxLineLength=94,
                    splitChars=" .,:;)]}",
                )
            )
            index += 1
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            table_lines = []
            while index < len(lines):
                candidate = lines[index].strip()
                if not (candidate.startswith("|") and candidate.endswith("|")):
                    break
                table_lines.append(candidate)
                index += 1
            story.append(parse_table(table_lines, styles))
            story.append(Spacer(1, 7))
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            title = stripped[2:].strip()
            story.append(Spacer(1, 4))
            story.append(Paragraph(inline_markup(title), styles["title"]))
            story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#55B8AE"), spaceAfter=12))
        elif stripped.startswith("## "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(stripped[3:]), styles["h2"]))
        elif stripped.startswith("### "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(stripped[4:]), styles["h3"]))
        elif stripped.startswith("#### "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(stripped[5:]), styles["h4"]))
        elif re.fullmatch(r"-{3,}", stripped):
            flush_paragraph()
            story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#CAD3DE"), spaceBefore=6, spaceAfter=7))
        elif stripped.startswith(">"):
            flush_paragraph()
            quote_lines = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip()[1:].strip())
                index += 1
            quote = Paragraph(inline_markup(" ".join(quote_lines)), styles["quote"])
            box = Table([[quote]], colWidths=[CONTENT_WIDTH - 12])
            box.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E7F7F4")),
                        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#55B8AE")),
                        ("LEFTPADDING", (0, 0), (-1, -1), 10),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ]
                )
            )
            story.append(box)
            story.append(Spacer(1, 7))
            continue
        elif re.match(r"^[-*+]\s+", stripped):
            flush_paragraph()
            content = re.sub(r"^[-*+]\s+", "", stripped)
            story.append(Paragraph("•  " + inline_markup(content), styles["bullet"]))
        elif re.match(r"^\d+\.\s+", stripped):
            flush_paragraph()
            match = re.match(r"^(\d+)\.\s+(.*)", stripped)
            assert match is not None
            story.append(Paragraph(f"{match.group(1)}.  " + inline_markup(match.group(2)), styles["bullet"]))
        elif not stripped:
            flush_paragraph()
        else:
            paragraph_lines.append(stripped)

        index += 1

    flush_paragraph()
    return story, title


def page_decorator(chapter_label: str):
    def draw(canvas, document) -> None:
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D5DDE7"))
        canvas.setLineWidth(0.5)
        canvas.line(LEFT_MARGIN, PAGE_HEIGHT - 11.5 * mm, PAGE_WIDTH - RIGHT_MARGIN, PAGE_HEIGHT - 11.5 * mm)
        canvas.setFont("CourseSans", 7.5)
        canvas.setFillColor(colors.HexColor("#68778B"))
        canvas.drawString(LEFT_MARGIN, PAGE_HEIGHT - 9 * mm, "Python 数据结构与 LeetCode")
        canvas.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, PAGE_HEIGHT - 9 * mm, chapter_label)
        canvas.line(LEFT_MARGIN, 11.5 * mm, PAGE_WIDTH - RIGHT_MARGIN, 11.5 * mm)
        canvas.drawString(LEFT_MARGIN, 7.5 * mm, "learning-log · 本地课程讲义")
        canvas.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, 7.5 * mm, f"第 {document.page} 页")
        canvas.restoreState()

    return draw


def build_lesson_pdf(source: Path, destination: Path, styles: dict[str, ParagraphStyle]) -> tuple[str, int]:
    markdown = source.read_text(encoding="utf-8")
    story, title = markdown_to_story(markdown, styles)
    chapter_match = re.match(r"(\d+)-", source.name)
    chapter = chapter_match.group(1) if chapter_match else ""
    label = f"第 {int(chapter)} 讲" if chapter else source.stem

    document = SimpleDocTemplate(
        str(destination),
        pagesize=A4,
        rightMargin=RIGHT_MARGIN,
        leftMargin=LEFT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title=title,
        author="Python 数据结构与 LeetCode 学习日志",
        subject=label,
        creator="learning-log PDF exporter",
        pageCompression=1,
    )
    decorator = page_decorator(label)
    document.build(story, onFirstPage=decorator, onLaterPages=decorator)
    pages = len(PdfReader(str(destination)).pages)
    return title, pages


def merge_pdfs(entries: list[tuple[Path, str, int]]) -> int:
    writer = PdfWriter()
    page_offset = 0

    for pdf_path, title, page_count in entries:
        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            writer.add_page(page)
        writer.add_outline_item(title, page_number=page_offset)
        page_offset += page_count

    writer.add_metadata(
        {
            "/Title": "Python 数据结构与 LeetCode 完整课程（第 1–15 讲）",
            "/Author": "Python 数据结构与 LeetCode 学习日志",
            "/Subject": "数据结构与算法学习讲义",
        }
    )
    with COMBINED_PATH.open("wb") as stream:
        writer.write(stream)
    return page_offset


def main() -> None:
    register_fonts()
    styles = build_styles()
    sources = sorted(LESSONS_DIR.glob("[0-9][0-9]-*.md"))

    if len(sources) != 15:
        raise RuntimeError(f"Expected 15 lessons, found {len(sources)}")

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    INDIVIDUAL_DIR.mkdir(parents=True, exist_ok=True)

    entries: list[tuple[Path, str, int]] = []
    for source in sources:
        destination = INDIVIDUAL_DIR / f"{source.stem}.pdf"
        title, pages = build_lesson_pdf(source, destination, styles)
        entries.append((destination, title, pages))
        print(f"CREATED {destination.name}: {pages} pages")

    total_pages = merge_pdfs(entries)
    print(f"CREATED {COMBINED_PATH.name}: {total_pages} pages")
    print(f"OUTPUT_COUNT {len(entries) + 1}")


if __name__ == "__main__":
    main()
