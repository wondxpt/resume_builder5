"""
Canadian/US-Standard Resume PDF Generator — 6 Real Resume Formats
----------------------------------------------------------------------
Based on the three recognized resume formats used by employers and ATS
in Canada and the US (chronological, functional, combination), plus a
popular modern two-column layout, an ultra-safe minimalist variant,
and a graphic/European-style format with a photo.

All ATS-safe templates share the same foundation:
- No photo, base-14 PDF fonts only (Helvetica / Times)
- 1-inch margins (except two-column/graphic, which need slightly tighter margins)
- Clear, standard section headings
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os
import tempfile

try:
    from PIL import Image as PILImage, ImageDraw, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

DARK = HexColor("#1a1a1a")
GREY = HexColor("#555555")
WHITE = HexColor("#ffffff")

FONT_FAMILIES = {
    "Helvetica": {"regular": "Helvetica", "bold": "Helvetica-Bold", "italic": "Helvetica-Oblique"},
    "Times": {"regular": "Times-Roman", "bold": "Times-Bold", "italic": "Times-Italic"},
}


# ----------------------------------------------------------------------
# Template definitions
# ----------------------------------------------------------------------
TEMPLATES = {
    "chronological": {
        "label": "Reverse-Chronological",
        "description": "BEST FOR: USA & Canada (top pick for most applicants). The gold-standard ATS format — every major parser (Workday, Greenhouse, Taleo) reads it cleanly. Lists work experience newest-first with clear dates. Use this if you have a steady, relevant work history and no specific reason to choose another format.",
        "hex": "#2c3e50",
        "font_family": "Helvetica",
        "layout": "standard",
        "divider": True,
        "divider_thickness": 0.8,
        "banner": False,
    },
    "combination": {
        "label": "Combination (Hybrid)",
        "description": "BEST FOR: USA & Canada — the format career-advice sites now recommend for roughly 80% of applicants. Bold colored header banner + a highlighted Key Skills box, followed by a full dated work history, so it keeps ATS compatibility while still leading with your strongest skills. Ideal for career changers, e.g. a Python transition.",
        "hex": "#0f766e",
        "font_family": "Helvetica",
        "layout": "combination",
        "divider": True,
        "divider_thickness": 1.0,
        "banner": True,
    },
    "functional": {
        "label": "Functional (Skills-Based)",
        "description": "BEST FOR: USA & Canada, but only for specific situations (long employment gap, major career pivot) — most 2026 ATS platforms rank pure skills-only resumes poorly, so this version still keeps a condensed, dated Employment History section to stay ATS-safe. If you don't have a gap or pivot to explain, pick Chronological or Combination instead.",
        "hex": "#6d28d9",
        "font_family": "Helvetica",
        "layout": "functional",
        "divider": True,
        "divider_thickness": 1.0,
        "banner": False,
    },
    "two_column": {
        "label": "Modern Two-Column",
        "description": "BEST FOR: direct submissions (email, in person, networking) in USA, Canada, or Europe — NOT recommended for online ATS portals. Most ATS software reads left-to-right across the full page width, so two-column layouts often get scrambled by the parser even though they look great to a human. Bold dark sidebar with white text for contact/skills/education.",
        "hex": "#1e293b",
        "font_family": "Helvetica",
        "layout": "two_column",
        "divider": False,
        "divider_thickness": 0,
        "banner": False,
    },
    "minimal": {
        "label": "Minimalist ATS-Safe",
        "description": "BEST FOR: USA & Canada — the safest possible choice if you're applying through an older or unusually strict ATS (e.g. some government/GCJobs-style portals), or you just want zero design risk. Plain single-column layout, no lines, no color blocks — relies purely on whitespace.",
        "hex": "#3a3a3a",
        "font_family": "Helvetica",
        "layout": "standard",
        "divider": False,
        "divider_thickness": 0,
        "banner": False,
    },
    "creative_photo": {
        "label": "Creative (with Photo)",
        "description": "BEST FOR: Continental Europe (Germany, France, Spain, Italy, Portugal and similar markets), where a professional headshot is standard or expected, plus creative-industry portfolios and LinkedIn anywhere. Bold graphic sidebar with photo, vivid color, and a Europass-style language proficiency scale (A1-C2). AVOID for USA and Canada — photos and personal details on a resume there are treated as an anti-discrimination red flag and can get an application rejected outright.",
        "hex": "#9d174d",
        "font_family": "Helvetica",
        "layout": "graphic",
        "divider": False,
        "divider_thickness": 0,
        "banner": False,
    },
}

DEFAULT_TEMPLATE = "chronological"


def get_template_name(data):
    key = data.get("selected_template", DEFAULT_TEMPLATE)
    return key if key in TEMPLATES else DEFAULT_TEMPLATE


# ----------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------

def build_styles(cfg, header_align=TA_CENTER):
    accent = HexColor(cfg["hex"])
    fonts = FONT_FAMILIES[cfg["font_family"]]

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="NameHeader", fontName=fonts["bold"], fontSize=20, leading=24,
        textColor=DARK, alignment=header_align, spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name="TargetTitle", fontName=fonts["regular"], fontSize=12, leading=16,
        textColor=accent, alignment=header_align, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="ContactLine", fontName=fonts["regular"], fontSize=9.5, leading=14,
        textColor=GREY, alignment=header_align, spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeader", fontName=fonts["bold"], fontSize=11.5, leading=15,
        textColor=accent, spaceBefore=12, spaceAfter=4, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="SidebarHeader", fontName=fonts["bold"], fontSize=10.5, leading=14,
        textColor=accent, spaceBefore=10, spaceAfter=3, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="JobTitle", fontName=fonts["bold"], fontSize=10.5, leading=14,
        textColor=DARK, spaceAfter=1,
    ))
    styles.add(ParagraphStyle(
        name="JobMeta", fontName=fonts["italic"], fontSize=9.5, leading=13,
        textColor=GREY, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="CondensedJob", fontName=fonts["regular"], fontSize=9.8, leading=14,
        textColor=DARK, spaceAfter=5,
    ))
    styles.add(ParagraphStyle(
        name="ResumeBullet", fontName=fonts["regular"], fontSize=9.8,
        textColor=DARK, leftIndent=14, bulletIndent=4, spaceAfter=3, leading=13,
    ))
    styles.add(ParagraphStyle(
        name="BodyText2", fontName=fonts["regular"], fontSize=9.8,
        textColor=DARK, leading=13, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="SidebarText", fontName=fonts["regular"], fontSize=9.2,
        textColor=DARK, leading=13, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="SkillsBoxText", fontName=fonts["regular"], fontSize=9.8,
        textColor=DARK, leading=14, spaceAfter=2,
    ))
# White-text variants for colored banners / dark sidebars
    styles.add(ParagraphStyle(
        name="NameHeaderWhite", fontName=fonts["bold"], fontSize=20, leading=24,
        textColor=WHITE, alignment=TA_CENTER, spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name="TargetTitleWhite", fontName=fonts["regular"], fontSize=12, leading=16,
        textColor=WHITE, alignment=TA_CENTER, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="ContactLineWhite", fontName=fonts["regular"], fontSize=9.5, leading=14,
        textColor=HexColor("#e2e8f0"), alignment=TA_CENTER, spaceAfter=0,
    ))
    styles.add(ParagraphStyle(
        name="SidebarHeaderWhite", fontName=fonts["bold"], fontSize=10.5, leading=14,
        textColor=WHITE, spaceBefore=10, spaceAfter=3, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="SidebarTextWhite", fontName=fonts["regular"], fontSize=9.2,
        textColor=HexColor("#e2e8f0"), leading=13, spaceAfter=4,
    ))

    return styles, accent


def section_divider(cfg, accent):
    if not cfg["divider"]:
        return Spacer(1, 4)
    return HRFlowable(width="100%", thickness=cfg["divider_thickness"], color=accent, spaceAfter=6)


def _format_language(lang):
    if isinstance(lang, dict):
        name = lang.get("name", "").strip()
        level = lang.get("level", "").strip()
        return f"{name} ({level})" if level else name
    return str(lang)


def make_circular_photo(source_path, size_px=400):
    """Returns a path to a temp PNG with the photo cropped to a circle.
    Returns None if PIL is unavailable or the source can't be read."""
    if not PIL_AVAILABLE or not source_path or not os.path.isfile(source_path):
        return None
    try:
        img = PILImage.open(source_path).convert("RGBA")
        img = ImageOps.fit(img, (size_px, size_px), method=PILImage.LANCZOS)

        mask = PILImage.new("L", (size_px, size_px), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size_px, size_px), fill=255)

        circular = PILImage.new("RGBA", (size_px, size_px), (0, 0, 0, 0))
        circular.paste(img, (0, 0), mask=mask)

        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        circular.save(tmp.name, "PNG")
        return tmp.name
    except Exception:
        return None


def _header_block(data, styles, accent, banner=False):
    if banner:
        inner = [Paragraph(data.get("full_name", ""), styles["NameHeaderWhite"])]
        if data.get("target_title"):
            inner.append(Paragraph(data["target_title"], styles["TargetTitleWhite"]))
        contact_parts = [p for p in [
            data.get("location", ""), data.get("phone", ""),
            data.get("email", ""), data.get("linkedin", ""),
        ] if p]
        inner.append(Paragraph(" &nbsp;|&nbsp; ".join(contact_parts), styles["ContactLineWhite"]))

        banner_table = Table([[inner]], colWidths=[6.5 * inch])
        banner_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), accent),
            ("TOPPADDING", (0, 0), (-1, -1), 16),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))
        return [banner_table, Spacer(1, 14)]

    block = [Paragraph(data.get("full_name", ""), styles["NameHeader"])]
    if data.get("target_title"):
        block.append(Paragraph(data["target_title"], styles["TargetTitle"]))
    contact_parts = [p for p in [
        data.get("location", ""), data.get("phone", ""),
        data.get("email", ""), data.get("linkedin", ""),
    ] if p]
    block.append(Paragraph(" &nbsp;|&nbsp; ".join(contact_parts), styles["ContactLine"]))
    return block


# ----------------------------------------------------------------------
# Layout builders
# ----------------------------------------------------------------------
def _build_standard_story(data, styles, cfg, accent, condensed_experience=False, skills_box=False):
    story = []
    story.extend(_header_block(data, styles, accent, banner=cfg.get("banner", False)))

    if data.get("summary"):
        story.append(Paragraph("PROFESSIONAL SUMMARY", styles["SectionHeader"]))
        story.append(section_divider(cfg, accent))
        story.append(Paragraph(data["summary"], styles["BodyText2"]))

    if skills_box and data.get("skills"):
        story.append(Paragraph("KEY SKILLS", styles["SectionHeader"]))
        story.append(section_divider(cfg, accent))
        skills_table = Table(
            [[Paragraph(" • ".join(data["skills"]), styles["SkillsBoxText"])]],
            colWidths=[6.5 * inch],
        )
        skills_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f1f5f9")),
            ("BOX", (0, 0), (-1, -1), 0.6, accent),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]))
        story.append(skills_table)
        story.append(Spacer(1, 6))

    if data.get("experience"):
        heading = "EMPLOYMENT HISTORY" if condensed_experience else "WORK EXPERIENCE"
        story.append(Paragraph(heading, styles["SectionHeader"]))
        story.append(section_divider(cfg, accent))
        for job in data["experience"]:
            if condensed_experience:
                line = (f"<b>{job.get('title','')}</b> — {job.get('company','')}"
                        f" &nbsp;|&nbsp; {job.get('location','')} "
                        f"({job.get('start_date','')} – {job.get('end_date','')})")
                story.append(Paragraph(line, styles["CondensedJob"]))
            else:
                title_line = f"{job.get('title','')} — {job.get('company','')}"
                story.append(Paragraph(title_line, styles["JobTitle"]))
                meta_line = f"{job.get('location','')} | {job.get('start_date','')} – {job.get('end_date','')}"
                story.append(Paragraph(meta_line, styles["JobMeta"]))
                for bullet in job.get("bullets", []):
                    story.append(Paragraph(f"• {bullet}", styles["ResumeBullet"]))
                story.append(Spacer(1, 6))

    if data.get("education"):
        story.append(Paragraph("EDUCATION", styles["SectionHeader"]))
        story.append(section_divider(cfg, accent))
        for edu in data["education"]:
            line = f"{edu.get('degree','')} — {edu.get('institution','')}"
            story.append(Paragraph(line, styles["JobTitle"]))
            meta = f"{edu.get('location','')} | {edu.get('grad_date','')}"
            story.append(Paragraph(meta, styles["JobMeta"]))
        story.append(Spacer(1, 4))

    if not skills_box and data.get("skills"):
        story.append(Paragraph("SKILLS", styles["SectionHeader"]))
        story.append(section_divider(cfg, accent))
        story.append(Paragraph(" • ".join(data["skills"]), styles["BodyText2"]))

    if data.get("languages"):
        story.append(Paragraph("LANGUAGES", styles["SectionHeader"]))
        story.append(section_divider(cfg, accent))
        lang_line = " • ".join(_format_language(l) for l in data["languages"])
        story.append(Paragraph(lang_line, styles["BodyText2"]))

    return story


def _build_functional_story(data, styles, cfg, accent):
    story = []
    story.extend(_header_block(data, styles, accent, banner=False))

    if data.get("summary"):
        story.append(Paragraph("PROFESSIONAL SUMMARY", styles["SectionHeader"]))
        story.append(section_divider(cfg, accent))
        story.append(Paragraph(data["summary"], styles["BodyText2"]))

    if data.get("skills"):
        story.append(Paragraph("CORE SKILLS", styles["SectionHeader"]))
        story.append(section_divider(cfg, accent))
        skills_table = Table(
            [[Paragraph(" • ".join(data["skills"]), styles["SkillsBoxText"])]],
            colWidths=[6.5 * inch],
        )
        skills_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f5f3ff")),
            ("BOX", (0, 0), (-1, -1), 0.6, accent),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]))
        story.append(skills_table)
        story.append(Spacer(1, 8))

    if data.get("experience"):
        story.append(Paragraph("EMPLOYMENT HISTORY", styles["SectionHeader"]))
        story.append(section_divider(cfg, accent))
        for job in data["experience"]:
            line = (f"<b>{job.get('title','')}</b> — {job.get('company','')}"
                    f" &nbsp;|&nbsp; {job.get('location','')} "
                    f"({job.get('start_date','')} – {job.get('end_date','')})")
            story.append(Paragraph(line, styles["CondensedJob"]))

    if data.get("education"):
        story.append(Paragraph("EDUCATION", styles["SectionHeader"]))
        story.append(section_divider(cfg, accent))
        for edu in data["education"]:
            line = f"{edu.get('degree','')} — {edu.get('institution','')}"
            story.append(Paragraph(line, styles["JobTitle"]))
            meta = f"{edu.get('location','')} | {edu.get('grad_date','')}"
            story.append(Paragraph(meta, styles["JobMeta"]))
        story.append(Spacer(1, 4))

    if data.get("languages"):
        story.append(Paragraph("LANGUAGES", styles["SectionHeader"]))
        story.append(section_divider(cfg, accent))
        lang_line = " • ".join(_format_language(l) for l in data["languages"])
        story.append(Paragraph(lang_line, styles["BodyText2"]))

    return story


def _build_two_column_story(data, styles, cfg, accent):
    story = []
    story.extend(_header_block(data, styles, accent, banner=False))
    story.append(Spacer(1, 6))

    # --- Sidebar (left) — bold dark background with white text ---
    sidebar = []
    if data.get("skills"):
        sidebar.append(Paragraph("SKILLS", styles["SidebarHeaderWhite"]))
        for s in data["skills"]:
            sidebar.append(Paragraph(f"• {s}", styles["SidebarTextWhite"]))
        sidebar.append(Spacer(1, 6))

    if data.get("education"):
        sidebar.append(Paragraph("EDUCATION", styles["SidebarHeaderWhite"]))
        for edu in data["education"]:
            sidebar.append(Paragraph(f"<b>{edu.get('degree','')}</b>", styles["SidebarTextWhite"]))
            sidebar.append(Paragraph(edu.get("institution", ""), styles["SidebarTextWhite"]))
            sidebar.append(Paragraph(edu.get("grad_date", ""), styles["SidebarTextWhite"]))
            sidebar.append(Spacer(1, 4))

    if data.get("languages"):
        sidebar.append(Paragraph("LANGUAGES", styles["SidebarHeaderWhite"]))
        for l in data["languages"]:
            sidebar.append(Paragraph(_format_language(l), styles["SidebarTextWhite"]))

    # --- Main column (right) ---
    main = []
    if data.get("summary"):
        main.append(Paragraph("PROFESSIONAL SUMMARY", styles["SectionHeader"]))
        main.append(Paragraph(data["summary"], styles["BodyText2"]))

    if data.get("experience"):
        main.append(Paragraph("WORK EXPERIENCE", styles["SectionHeader"]))
        for job in data["experience"]:
            title_line = f"{job.get('title','')} — {job.get('company','')}"
            main.append(Paragraph(title_line, styles["JobTitle"]))
            meta_line = f"{job.get('location','')} | {job.get('start_date','')} – {job.get('end_date','')}"
            main.append(Paragraph(meta_line, styles["JobMeta"]))
            for bullet in job.get("bullets", []):
                main.append(Paragraph(f"• {bullet}", styles["ResumeBullet"]))
            main.append(Spacer(1, 6))
            layout_table = Table(
        [[sidebar, main]],
        colWidths=[2.1 * inch, 4.4 * inch],
    )
    layout_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), accent),
        ("LEFTPADDING", (0, 0), (0, -1), 12),
        ("RIGHTPADDING", (0, 0), (0, -1), 12),
        ("TOPPADDING", (0, 0), (0, -1), 10),
        ("BOTTOMPADDING", (0, 0), (0, -1), 10),
        ("LEFTPADDING", (1, 0), (1, -1), 16),
        ("TOPPADDING", (1, 0), (1, -1), 4),
    ]))
    story.append(layout_table)
    return story


def _build_graphic_story(data, styles, cfg, accent):
    story = []

    # --- Sidebar (left): photo, contact, skills, languages, education ---
    sidebar = [Spacer(1, 4)]

    circ_path = make_circular_photo(data.get("photo_path", ""))
    if circ_path:
        img = Image(circ_path, width=1.3 * inch, height=1.3 * inch)
        img.hAlign = "CENTER"
        sidebar.append(img)
        sidebar.append(Spacer(1, 10))

    if data.get("skills"):
        sidebar.append(Paragraph("SKILLS", styles["SidebarHeaderWhite"]))
        for s in data["skills"]:
            sidebar.append(Paragraph(f"■ {s}", styles["SidebarTextWhite"]))
        sidebar.append(Spacer(1, 6))

    if data.get("languages"):
        sidebar.append(Paragraph("LANGUAGES", styles["SidebarHeaderWhite"]))
        for l in data["languages"]:
            sidebar.append(Paragraph(f"■ {_format_language(l)}", styles["SidebarTextWhite"]))
        sidebar.append(Spacer(1, 6))

    if data.get("education"):
        sidebar.append(Paragraph("EDUCATION", styles["SidebarHeaderWhite"]))
        for edu in data["education"]:
            sidebar.append(Paragraph(f"<b>{edu.get('degree','')}</b>", styles["SidebarTextWhite"]))
            sidebar.append(Paragraph(edu.get("institution", ""), styles["SidebarTextWhite"]))
            sidebar.append(Paragraph(edu.get("grad_date", ""), styles["SidebarTextWhite"]))
            sidebar.append(Spacer(1, 4))

    # --- Main column (right): name, title, contact, summary, experience ---
    name_style_left = ParagraphStyle("NameLeft", parent=styles["NameHeader"], alignment=TA_LEFT)
    title_style_left = ParagraphStyle("TitleLeft", parent=styles["TargetTitle"], alignment=TA_LEFT)
    contact_style_left = ParagraphStyle("ContactLeft", parent=styles["ContactLine"], alignment=TA_LEFT)

    main = [Paragraph(data.get("full_name", ""), name_style_left)]
    if data.get("target_title"):
        main.append(Paragraph(data["target_title"], title_style_left))
    contact_parts = [p for p in [
        data.get("location", ""), data.get("phone", ""),
        data.get("email", ""), data.get("linkedin", ""),
    ] if p]
    main.append(Paragraph(" &nbsp;|&nbsp; ".join(contact_parts), contact_style_left))
    main.append(Spacer(1, 8))

    if data.get("summary"):
        main.append(Paragraph("PROFILE", styles["SectionHeader"]))
        main.append(Paragraph(data["summary"], styles["BodyText2"]))
        main.append(Spacer(1, 4))

    if data.get("experience"):
        main.append(Paragraph("EXPERIENCE", styles["SectionHeader"]))
        for job in data["experience"]:
            title_line = f"{job.get('title','')} — {job.get('company','')}"
            main.append(Paragraph(title_line, styles["JobTitle"]))
            meta_line = f"{job.get('location','')} | {job.get('start_date','')} – {job.get('end_date','')}"
            main.append(Paragraph(meta_line, styles["JobMeta"]))
            for bullet in job.get("bullets", []):
                main.append(Paragraph(f"■ {bullet}", styles["ResumeBullet"]))
            main.append(Spacer(1, 6))

    layout_table = Table([[sidebar, main]], colWidths=[2.0 * inch, 4.5 * inch])
    layout_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), accent),
        ("LEFTPADDING", (0, 0), (0, -1), 12),
        ("RIGHTPADDING", (0, 0), (0, -1), 12),
        ("TOPPADDING", (0, 0), (0, -1), 14),
        ("BOTTOMPADDING", (0, 0), (0, -1), 14),
        ("LEFTPADDING", (1, 0), (1, -1), 18),
        ("TOPPADDING", (1, 0), (1, -1), 4),
    ]))
    story.append(layout_table)
    return story


# ----------------------------------------------------------------------
# Main entry point
# ----------------------------------------------------------------------

def generate_resume_pdf(data: dict, output_path: str, template: str = None):
    """
    data expects:
    {
        "full_name", "target_title", "location", "email", "phone", "linkedin",
        "summary",
        "experience": [{"title","company","location","start_date","end_date","bullets":[...]}],
        "education": [{"degree","institution","location","grad_date"}],
        "skills": [str, ...],
        "languages": [str, ...] or [{"name","level"}, ...],
        "photo_path": optional str, used only by the "creative_photo" template,
        "selected_template": one of TEMPLATES keys (optional, used if template arg not given)
    }
    """
    template_key = template if template in TEMPLATES else get_template_name(data)
    cfg = TEMPLATES[template_key]
    layout = cfg["layout"]

    header_align = TA_CENTER
    styles, accent = build_styles(cfg, header_align)

    if layout in ("two_column", "graphic"):
        margins = dict(topMargin=0.7 * inch, bottomMargin=0.7 * inch,
                        leftMargin=0.7 * inch, rightMargin=0.7 * inch)
    else:
        margins = dict(topMargin=1.0 * inch, bottomMargin=1.0 * inch,
                        leftMargin=1.0 * inch, rightMargin=1.0 * inch)

    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        title=f"{data.get('full_name', 'Resume')} - Resume",
        **margins,
    )

    if layout == "combination":
        story = _build_standard_story(data, styles, cfg, accent, condensed_experience=False, skills_box=True)
    elif layout == "functional":
        story = _build_functional_story(data, styles, cfg, accent)
    elif layout == "two_column":
        story = _build_two_column_story(data, styles, cfg, accent)
    elif layout == "graphic":
        story = _build_graphic_story(data, styles, cfg, accent)
    else:  # "standard" (chronological, minimal)
        story = _build_standard_story(data, styles, cfg, accent, condensed_experience=False, skills_box=False)

    doc.build(story)
    return output_path


if __name__ == "__main__":
    sample_data = {
        "full_name": "Abbas Shiri",
        "target_title": "Hairstylist | Aspiring Python Developer",
        "location": "Toronto, ON",
        "email": "abbas.shiri@email.com",
        "phone": "+1 (416) 555-0123",
        "linkedin": "linkedin.com/in/abbasshiri",
        "photo_path": "/tmp/test_photo.jpg",
        "summary": (
            "Detail-oriented hairstylist and salon owner with 11+ years of experience "
            "delivering high-quality client service and managing daily salon operations. "
            "Currently building Python development skills to transition into tech."
        ),
        "experience": [
            {
                "title": "Owner & Senior Hairstylist",
                "company": "Wondxpt Hair Salon",
                "location": "Shiraz, Iran",
                "start_date": "Mar 2013",
                "end_date": "Present",
                "bullets": [
                    "Managed all aspects of daily salon operations, including scheduling, inventory, and client relations",
                    "Delivered personalized hairstyling services to a loyal client base of 200+ regular customers",
                    "Trained and supervised 3 junior stylists, improving team service consistency",
                    "Maintained a 95%+ client retention rate through consistent quality and communication",
                ],
            },
        ],
        "education": [
            {
                "degree": "Bachelor of Business Administration",
                "institution": "Shiraz Azad University",
                "location": "Shiraz, Iran",
                "grad_date": "2012",
            }
        ],
        "skills": [
            "Client Relationship Management", "Team Leadership", "Scheduling & Operations",
            "Python (Learning)", "Problem Solving", "Adaptability",
        ],
        "languages": [
            {"name": "Persian", "level": "Native"},
            {"name": "English", "level": "Intermediate-Advanced"},
        ],
    }

    for key in TEMPLATES:
        out = f"/mnt/user-data/outputs/sample_{key}.pdf"
        generate_resume_pdf(sample_data, out, template=key)
        print(f"Generated: {out}")