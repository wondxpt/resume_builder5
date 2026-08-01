from __future__ import annotations

import os
import tempfile
from datetime import datetime
from typing import Any, Iterable, List, Sequence, Tuple

from fpdf import FPDF


TEMPLATES = {
    "classic": {
        "label": "Classic ATS",
        "description": "Simple ATS friendly single column resume",
        "layout": "standard",
        "hex": "#333333",
    },
    "canadian": {
        "label": "Canadian Standard",
        "description": "Professional Canadian resume format",
        "layout": "standard",
        "hex": "#1E88E5",
    },
    "corporate": {
        "label": "US Corporate",
        "description": "American corporate resume format",
        "layout": "standard",
        "hex": "#1565C0",
    },
    "modern": {
        "label": "Modern Professional",
        "description": "Modern clean professional layout",
        "layout": "two_column",
        "hex": "#00897B",
    },
    "executive": {
        "label": "Executive",
        "description": "Senior level executive resume",
        "layout": "functional",
        "hex": "#6D4C41",
    },
    "creative_photo": {
        "label": "Creative European",
        "description": "Graphic resume with photo",
        "layout": "graphic",
        "hex": "#8E24AA",
    },
}


_TEMPLATE_ALIASES = {
    "chronological": "classic",
    "classic ats": "classic",
    "standard": "classic",
    "minimal": "classic",
    "canadian standard": "canadian",
    "us corporate": "corporate",
    "corporate": "corporate",
    "modern professional": "modern",
    "two_column": "modern",
    "functional": "executive",
    "executive": "executive",
    "european": "creative_photo",
    "graphic european": "creative_photo",
    "creative_photo": "creative_photo",
}


def _hex_to_rgb(value: str) -> Tuple[int, int, int]:
    value = (value or "#000000").lstrip("#")
    if len(value) != 6:
        return (0, 0, 0)
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def clean_text(text: Any) -> str:
    if text is None:
        return ""

    text = str(text)
    replacements = {
        "\r\n": "\n",
        "\r": "\n",
        "–": "-",
        "—": "-",
        "•": "-",
        "’": "'",
        "“": '"',
        "”": '"',
        "\t": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    lines = []
    for line in text.split("\n"):
        lines.append(" ".join(line.split()))
    return "\n".join(lines).strip()


def pdf_safe_text(text: Any) -> str:
    text = clean_text(text)
    try:
        text.encode("latin-1")
        return text
    except UnicodeEncodeError:
        return text.encode("latin-1", "replace").decode("latin-1")


def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [item for item in value if item not in (None, "", [])]
    if isinstance(value, str):
        value = clean_text(value)
        if not value:
            return []
        if "," in value:
            return [part.strip() for part in value.split(",") if part.strip()]
        if "\n" in value:
            return [part.strip() for part in value.split("\n") if part.strip()]
        return [value]
    return [value]


def _normalize_languages(value: Any) -> List[str]:
    result: List[str] = []
    for item in _as_list(value):
        if isinstance(item, dict):
            name = clean_text(item.get("name", ""))
            level = clean_text(item.get("level", ""))
            if name and level:
                result.append(f"{name} — {level}")
            elif name:
                result.append(name)
        else:
            text = clean_text(item)
            if text:
                result.append(text)
    return result


def _normalize_skills(value: Any) -> List[str]:
    skills: List[str] = []
    for item in _as_list(value):
        if isinstance(item, dict):
            text = clean_text(item.get("name") or item.get("skill") or "")
        else:
            text = clean_text(item)
        if text:
            skills.append(text)
    return skills


def _contact_lines(data: Any) -> List[str]:
    lines: List[str] = []
    for attr in ("email", "phone", "location", "linkedin"):
        value = clean_text(getattr(data, attr, ""))
        if value:
            lines.append(value)
    return lines


def _resolve_template_key(value: Any) -> str:
    key = clean_text(value).lower()
    if key in TEMPLATES:
        return key
    return _TEMPLATE_ALIASES.get(key, "classic")


def _prepare_photo(photo_path: str) -> str | None:
    if not photo_path or not os.path.exists(photo_path):
        return None

    try:
        from PIL import Image, ImageDraw
    except Exception:
        return photo_path

    try:
        image = Image.open(photo_path).convert("RGBA")
        size = min(image.size)
        left = (image.width - size) // 2
        top = (image.height - size) // 2
        image = image.crop((left, top, left + size, top + size))
        image = image.resize((256, 256), Image.LANCZOS)

        mask = Image.new("L", (256, 256), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 256, 256), fill=255)
        image.putalpha(mask)

        out_path = os.path.join(tempfile.gettempdir(), "resume_builder_photo.png")
        image.save(out_path, format="PNG")
        return out_path
    except Exception:
        return photo_path


class ResumePDF(FPDF):
    def __init__(self) -> None:
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=14)
        self.set_margins(15, 15, 15)
        self.set_title("Resume Builder")
        self.set_author("Resume Builder")

        self._template_key = "classic"
        self._accent_rgb = (0, 0, 0)
        self._sidebar_width = 0

    def header(self) -> None:
        accent = self._accent_rgb
        template = self._template_key

        if template in ("modern", "creative_photo"):
            sidebar_w = self._sidebar_width or 66
            self.set_fill_color(*accent)
            self.rect(0, 0, sidebar_w, self.h, style="F")
            self.set_draw_color(*accent)
            self.set_line_width(0.4)
            self.line(sidebar_w, 0, sidebar_w, self.h)
            return

        if template == "corporate":
            self.set_fill_color(*accent)
            self.rect(0, 0, self.w, 12, style="F")
            self.set_y(15)
            return

        self.set_draw_color(*accent)
        self.set_line_width(0.4)
        self.line(self.l_margin, 12, self.w - self.r_margin, 12)
        self.set_y(15)

    def footer(self) -> None:
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, f"Page {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)


def _section_rule(pdf: ResumePDF, accent: Tuple[int, int, int]) -> None:
    pdf.set_draw_color(*accent)
    pdf.set_line_width(0.35)
    y = pdf.get_y() + 1
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(4)


def _section_title(
    pdf: ResumePDF,
    title: str,
    accent: Tuple[int, int, int],
    size: int = 11,
) -> None:
    pdf.set_text_color(*accent)
    pdf.set_font("Helvetica", "B", size)
    pdf.cell(0, 6, pdf_safe_text(title.upper()), ln=True)
    _section_rule(pdf, accent)
    pdf.set_text_color(0, 0, 0)


def _write_name_and_title(
    pdf: ResumePDF,
    data: Any,
    name_size: int,
    title_size: int,
    title_style: str = "",
    title_color: Tuple[int, int, int] = (70, 70, 70),
) -> None:
    name = pdf_safe_text(getattr(data, "full_name", ""))
    title = pdf_safe_text(getattr(data, "target_title", ""))

    pdf.set_font("Helvetica", "B", name_size)
    pdf.cell(0, 9, name, ln=True)

    if title:
        pdf.set_text_color(*title_color)
        pdf.set_font("Helvetica", title_style, title_size)
        pdf.cell(0, 6, title, ln=True)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(2)


def _write_contact(pdf: ResumePDF, data: Any) -> None:
    lines = _contact_lines(data)
    if not lines:
        return

    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 4.7, pdf_safe_text(" | ".join(lines)))
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)


def _write_summary(pdf: ResumePDF, data: Any, accent: Tuple[int, int, int]) -> None:
    summary = clean_text(getattr(data, "summary", ""))
    if not summary:
        return

    _section_title(pdf, "Professional Summary", accent, size=11)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, pdf_safe_text(summary))
    pdf.ln(1)


def _render_experience_item(pdf: ResumePDF, item: Any) -> None:
    if not isinstance(item, dict):
        text = clean_text(item)
        if text:
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5, pdf_safe_text(text))
            pdf.ln(1)
        return

    title = clean_text(item.get("title") or item.get("role") or "")
    company = clean_text(item.get("company") or "")
    location = clean_text(item.get("location") or "")
    start_date = clean_text(item.get("start_date") or "")
    end_date = clean_text(item.get("end_date") or "")
    bullets = _as_list(item.get("bullets"))

    if title and company:
        heading = f"{title} — {company}"
    else:
        heading = title or company

    if heading:
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(0, 5, pdf_safe_text(heading))

    meta_parts = []
    if location:
        meta_parts.append(location)
    date_range = " - ".join([part for part in [start_date, end_date] if part])
    if date_range:
        meta_parts.append(date_range)
    if meta_parts:
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(90, 90, 90)
        pdf.multi_cell(0, 4.5, pdf_safe_text(" | ".join(meta_parts)))
        pdf.set_text_color(0, 0, 0)

    if bullets:
        pdf.set_font("Helvetica", "", 9.4)
        for bullet in bullets:
            bullet_text = clean_text(bullet)
            if bullet_text:
                pdf.multi_cell(0, 4.5, pdf_safe_text(f"• {bullet_text}"))

    pdf.ln(1)


def _render_education_item(pdf: ResumePDF, item: Any) -> None:
    if not isinstance(item, dict):
        text = clean_text(item)
        if text:
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5, pdf_safe_text(text))
            pdf.ln(1)
        return

    degree = clean_text(item.get("degree") or item.get("title") or "")
    institution = clean_text(item.get("institution") or "")
    location = clean_text(item.get("location") or "")
    grad_date = clean_text(item.get("grad_date") or item.get("graduation_date") or "")

    heading = degree or institution
    if degree and institution:
        heading = f"{degree} — {institution}"

    if heading:
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(0, 5, pdf_safe_text(heading))

    meta_parts = []
    if location:
        meta_parts.append(location)
    if grad_date:
        meta_parts.append(grad_date)
    if meta_parts:
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(90, 90, 90)
        pdf.multi_cell(0, 4.5, pdf_safe_text(" | ".join(meta_parts)))
        pdf.set_text_color(0, 0, 0)

    pdf.ln(1)


def create_contact(pdf: ResumePDF, data: Any) -> None:
    _write_contact(pdf, data)


def create_experience(pdf: ResumePDF, data: Any) -> None:
    experience = _as_list(getattr(data, "experience", []))
    if not experience:
        return

    accent = getattr(pdf, "_accent_rgb", (0, 0, 0))
    _section_title(pdf, "Professional Experience", accent, size=11)
    for item in experience:
        _render_experience_item(pdf, item)


def create_education(pdf: ResumePDF, data: Any) -> None:
    education = _as_list(getattr(data, "education", []))
    if not education:
        return

    accent = getattr(pdf, "_accent_rgb", (0, 0, 0))
    _section_title(pdf, "Education", accent, size=11)
    for item in education:
        _render_education_item(pdf, item)


def create_skills(pdf: ResumePDF, data: Any) -> None:
    skills = _normalize_skills(getattr(data, "skills", []))
    if not skills:
        return

    accent = getattr(pdf, "_accent_rgb", (0, 0, 0))
    _section_title(pdf, "Skills", accent, size=11)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, pdf_safe_text(", ".join(skills)))
    pdf.ln(1)


def create_languages(pdf: ResumePDF, data: Any) -> None:
    languages = _normalize_languages(getattr(data, "languages", []))
    if not languages:
        return

    accent = getattr(pdf, "_accent_rgb", (0, 0, 0))
    _section_title(pdf, "Languages", accent, size=11)
    pdf.set_font("Helvetica", "", 10)
    for line in languages:
        pdf.multi_cell(0, 5, pdf_safe_text(line))
    pdf.ln(1)


def _sidebar_write(
    pdf: ResumePDF,
    x: float,
    y: float,
    width: float,
    text: str,
    size: int = 9,
    bold: bool = False,
    line_height: float = 4.4,
) -> float:
    pdf.set_xy(x, y)
    pdf.set_font("Helvetica", "B" if bold else "", size)
    pdf.multi_cell(width, line_height, pdf_safe_text(text))
    return pdf.get_y()


def _sidebar_section_title(
    pdf: ResumePDF,
    x: float,
    y: float,
    width: float,
    title: str,
    accent: Tuple[int, int, int],
) -> float:
    pdf.set_xy(x, y)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(width, 5, pdf_safe_text(title.upper()), ln=True)
    y = pdf.get_y()
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(0.3)
    pdf.line(x, y + 1, x + width, y + 1)
    pdf.ln(3)
    pdf.set_text_color(255, 255, 255)
    return pdf.get_y()


def _render_sidebar_profile(
    pdf: ResumePDF,
    data: Any,
    sidebar_w: float,
    with_photo: bool = False,
) -> None:
    x = 10
    y = 16
    width = sidebar_w - 20

    pdf.set_text_color(255, 255, 255)

    if with_photo:
        photo_path = _prepare_photo(getattr(data, "photo_path", ""))
        if photo_path:
            try:
                photo_size = 28
                photo_x = x + (width - photo_size) / 2
                pdf.image(photo_path, x=photo_x, y=y, w=photo_size, h=photo_size)
                y += photo_size + 8
            except Exception:
                y += 4

    full_name = clean_text(getattr(data, "full_name", ""))
    target_title = clean_text(getattr(data, "target_title", ""))

    if full_name:
        y = _sidebar_write(pdf, x, y, width, full_name, size=13, bold=True, line_height=5.2)
        y += 1

    if target_title:
        y = _sidebar_write(pdf, x, y, width, target_title, size=9, bold=False, line_height=4.5)
        y += 4

    lines = _contact_lines(data)
    if lines:
        y = _sidebar_section_title(pdf, x, y, width, "Contact", getattr(pdf, "_accent_rgb", (0, 0, 0)))
        for line in lines:
            y = _sidebar_write(pdf, x, y, width, line, size=8.7, line_height=4.2)
        y += 2

    skills = _normalize_skills(getattr(data, "skills", []))
    if skills:
        y = _sidebar_section_title(pdf, x, y, width, "Skills", getattr(pdf, "_accent_rgb", (0, 0, 0)))
        for skill in skills[:24]:
            y = _sidebar_write(pdf, x, y, width, f"• {skill}", size=8.7, line_height=4.2)
        y += 2

    languages = _normalize_languages(getattr(data, "languages", []))
    if languages:
        y = _sidebar_section_title(pdf, x, y, width, "Languages", getattr(pdf, "_accent_rgb", (0, 0, 0)))
        for line in languages:
            y = _sidebar_write(pdf, x, y, width, line, size=8.7, line_height=4.2)

    pdf.set_text_color(0, 0, 0)


def _render_single_column_template(
    pdf: ResumePDF,
    data: Any,
    template_key: str,
) -> None:
    style = {
        "classic": {
            "name_size": 18,
            "title_size": 11,
            "title_style": "",
            "title_color": (70, 70, 70),
            "accent": _hex_to_rgb(TEMPLATES["classic"]["hex"]),
        },
        "canadian": {
            "name_size": 17,
            "title_size": 10,
            "title_style": "",
            "title_color": (60, 60, 60),
            "accent": _hex_to_rgb(TEMPLATES["canadian"]["hex"]),
        },
        "corporate": {
            "name_size": 20,
            "title_size": 11,
            "title_style": "",
            "title_color": (55, 55, 55),
            "accent": _hex_to_rgb(TEMPLATES["corporate"]["hex"]),
        },
        "executive": {
            "name_size": 19,
            "title_size": 11,
            "title_style": "I",
            "title_color": (65, 65, 65),
            "accent": _hex_to_rgb(TEMPLATES["executive"]["hex"]),
        },
    }[template_key]

    pdf._template_key = template_key
    pdf._accent_rgb = style["accent"]
    pdf._sidebar_width = 0
    pdf.add_page()

    if template_key == "corporate":
        pdf.set_y(17)
    else:
        pdf.set_y(16)

    _write_name_and_title(
        pdf,
        data,
        name_size=style["name_size"],
        title_size=style["title_size"],
        title_style=style["title_style"],
        title_color=style["title_color"],
    )
    _write_contact(pdf, data)

    summary = clean_text(getattr(data, "summary", ""))
    if summary:
        _section_title(pdf, "Professional Summary", style["accent"], size=11)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, pdf_safe_text(summary))
        pdf.ln(1)

    experience = _as_list(getattr(data, "experience", []))
    if experience:
        _section_title(pdf, "Professional Experience", style["accent"], size=11)
        for item in experience:
            _render_experience_item(pdf, item)

    education = _as_list(getattr(data, "education", []))
    if education:
        _section_title(pdf, "Education", style["accent"], size=11)
        for item in education:
            _render_education_item(pdf, item)

    skills = _normalize_skills(getattr(data, "skills", []))
    if skills:
        _section_title(pdf, "Skills", style["accent"], size=11)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, pdf_safe_text(", ".join(skills)))
        pdf.ln(1)

    languages = _normalize_languages(getattr(data, "languages", []))
    if languages:
        _section_title(pdf, "Languages", style["accent"], size=11)
        pdf.set_font("Helvetica", "", 10)
        for line in languages:
            pdf.multi_cell(0, 5, pdf_safe_text(line))
        pdf.ln(1)


def _render_two_column_template(
    pdf: ResumePDF,
    data: Any,
    template_key: str,
    with_photo: bool = False,
) -> None:
    accent = _hex_to_rgb(TEMPLATES[template_key]["hex"])
    sidebar_w = 72 if with_photo else 66
    main_left = sidebar_w + 10

    pdf._template_key = template_key
    pdf._accent_rgb = accent
    pdf._sidebar_width = sidebar_w
    pdf.add_page()

    _render_sidebar_profile(pdf, data, sidebar_w=sidebar_w, with_photo=with_photo)

    pdf.set_left_margin(main_left)
    pdf.set_right_margin(12)
    pdf.set_x(main_left)
    pdf.set_y(16)

    _write_name_and_title(
        pdf,
        data,
        name_size=20 if with_photo else 19,
        title_size=11,
        title_style="",
        title_color=(55, 55, 55),
    )

    summary = clean_text(getattr(data, "summary", ""))
    if summary:
        _section_title(pdf, "Professional Summary", accent, size=11)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, pdf_safe_text(summary))
        pdf.ln(1)

    experience = _as_list(getattr(data, "experience", []))
    if experience:
        _section_title(pdf, "Professional Experience", accent, size=11)
        for item in experience:
            _render_experience_item(pdf, item)

    education = _as_list(getattr(data, "education", []))
    if education:
        _section_title(pdf, "Education", accent, size=11)
        for item in education:
            _render_education_item(pdf, item)


def create_classic(pdf: ResumePDF, data: Any) -> None:
    _render_single_column_template(pdf, data, "classic")


def create
