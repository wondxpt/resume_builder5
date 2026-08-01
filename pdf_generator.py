from fpdf import FPDF
import os
from datetime import datetime
class ResumePDF(FPDF):
TEMPLATES = {
    "classic": {
        "label": "Classic ATS",
        "description": "Simple ATS friendly single column resume",
        "layout": "standard",
        "hex": "#333333"
    },
    "canadian": {
        "label": "Canadian Standard",
        "description": "Professional Canadian resume format",
        "layout": "standard",
        "hex": "#1E88E5"
    },
    "corporate": {
        "label": "US Corporate",
        "description": "American corporate resume format",
        "layout": "combination",
        "hex": "#1565C0"
    },
    "modern": {
        "label": "Modern Professional",
        "description": "Modern clean professional layout",
        "layout": "two_column",
        "hex": "#00897B"
    },
    "executive": {
        "label": "Executive",
        "description": "Senior level executive resume",
        "layout": "functional",
        "hex": "#6D4C41"
    },
    "creative_photo": {
        "label": "Creative European",
        "description": "Graphic resume with photo",
        "layout": "graphic",
        "hex": "#8E24AA"
    }
}

    def __init__(self):
        super().__init__(
            orientation="P",
            unit="mm",
            format="A4"
        )

        self.set_auto_page_break(
            auto=True,
            margin=15
        )

        self.set_margins(
            20,
            15,
            20
        )

    def header(self):
        pass

    def footer(self):
        self.set_y(-10)
        self.set_font(
            "Helvetica",
            "",
            8
        )

        self.cell(
            0,
            5,
            f"Page {self.page_no()}",
            align="C"
        )


# -------------------------------
# Helper Functions
# -------------------------------

def clean_text(text):
    """
    Removes unsupported characters
    for PDF generation
    """

    if not text:
        return ""

    replacements = {
        "–": "-",
        "—": "-",
        "•": "-",
        "’": "'",
        "“": '"',
        "”": '"'
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def add_title(pdf, text):

    pdf.set_font(
        "Helvetica",
        "B",
        13
    )

    pdf.cell(
        0,
        8,
        clean_text(text),
        ln=True
    )

    pdf.ln(2)


def add_section(pdf, title):

    pdf.set_font(
        "Helvetica",
        "B",
        11
    )

    pdf.cell(
        0,
        7,
        clean_text(title),
        ln=True
    )

    pdf.set_font(
        "Helvetica",
        "",
        10
    )


def add_text(pdf, text):

    if not text:
        return

    pdf.set_font(
        "Helvetica",
        "",
        10
    )

    pdf.multi_cell(
        0,
        5,
        clean_text(text)
    )

    pdf.ln(2)


def add_line(pdf):

    pdf.cell(
        0,
        1,
        "",
        border="B",
        ln=True
    )

    pdf.ln(3)

def create_contact(pdf, data):

    pdf.set_font(
        "Helvetica",
        "",
        10
    )

    contact = []

    if data.email:
        contact.append(data.email)

    if data.phone:
        contact.append(data.phone)

    if data.location:
        contact.append(data.location)

    if hasattr(data, "linkedin"):
        if data.linkedin:
            contact.append(data.linkedin)


    pdf.multi_cell(
        0,
        5,
        clean_text(
            " | ".join(contact)
        )
    )

    pdf.ln(5)
    

def create_experience(pdf, data):

    if not data.experience:
        return


    add_section(
        pdf,
        "PROFESSIONAL EXPERIENCE"
    )


    pdf.multi_cell(
        0,
        5,
        clean_text(
            data.experience
        )
    )

    pdf.ln(4)


def create_education(pdf, data):

    if not data.education:
        return


    add_section(
        pdf,
        "EDUCATION"
    )


    pdf.multi_cell(
        0,
        5,
        clean_text(
            data.education
        )
    )

    pdf.ln(4)

def create_skills(pdf, data):

    if not data.skills:
        return


    add_section(
        pdf,
        "SKILLS"
    )


    pdf.multi_cell(
        0,
        5,
        clean_text(
            data.skills
        )
    )

    pdf.ln(4)


def create_languages(pdf, data):

    if not hasattr(data, "languages"):
        return


    if not data.languages:
        return


    add_section(
        pdf,
        "LANGUAGES"
    )


    pdf.multi_cell(
        0,
        5,
        clean_text(
            data.languages
        )
    )

    pdf.ln(4)
    # -------------------------------
# TEMPLATE 1
# Classic ATS Resume
# -------------------------------

def create_classic(pdf, data):

    pdf.add_page()

    pdf.set_font(
        "Helvetica",
        "B",
        18
    )

    pdf.cell(
        0,
        10,
        clean_text(data.full_name),
        ln=True
    )

    pdf.set_font(
        "Helvetica",
        "",
        11
    )

    pdf.cell(
        0,
        6,
        clean_text(data.target_title),
        ln=True
    )

    pdf.ln(4)

    create_contact(pdf, data)

    add_line(pdf)


    if data.summary:
        add_section(pdf, "PROFESSIONAL SUMMARY")
        add_text(pdf, data.summary)


    create_experience(pdf, data)
    create_education(pdf, data)
    create_skills(pdf, data)
    create_languages(pdf, data)



def create_canadian(pdf, data):

    pdf.add_page()

    pdf.set_font(
        "Helvetica",
        "B",
        16
    )

    pdf.cell(
        0,
        8,
        clean_text(data.full_name),
        ln=True
    )

    pdf.set_font(
        "Helvetica",
        "",
        10
    )

    pdf.cell(
        0,
        6,
        clean_text(data.target_title),
        ln=True
    )


    pdf.ln(3)

    create_contact(pdf, data)

    add_line(pdf)


    if data.summary:

        add_section(
            pdf,
            "SUMMARY"
        )

        add_text(
            pdf,
            data.summary
        )


    create_experience(
        pdf,
        data
    )

    create_education(
        pdf,
        data
    )

    create_skills(
        pdf,
        data
    )

    create_languages(
        pdf,
        data
    )



def create_corporate(pdf, data):

    pdf.add_page()


    pdf.set_font(
        "Helvetica",
        "B",
        20
    )

    pdf.cell(
        0,
        10,
        clean_text(data.full_name),
        ln=True
    )


    pdf.set_font(
        "Helvetica",
        "",
        11
    )

    pdf.cell(
        0,
        6,
        clean_text(data.target_title),
        ln=True
    )

    pdf.ln(5)


    create_contact(
        pdf,
        data
    )

    add_line(pdf)


    if data.summary:

        add_section(
            pdf,
            "EXECUTIVE SUMMARY"
        )

        add_text(
            pdf,
            data.summary
        )


    create_experience(
        pdf,
        data
    )

    create_education(
        pdf,
        data
    )

    create_skills(
        pdf,
        data
    )

    create_languages(
        pdf,
        data
    )



def create_modern(pdf, data):

    pdf.add_page()


    pdf.set_font(
        "Helvetica",
        "B",
        22
    )

    pdf.cell(
        0,
        12,
        clean_text(data.full_name),
        ln=True
    )


    pdf.set_font(
        "Helvetica",
        "",
        12
    )

    pdf.cell(
        0,
        7,
        clean_text(data.target_title),
        ln=True
    )


    pdf.ln(6)


    create_contact(
        pdf,
        data
    )


    add_line(pdf)


    if data.summary:

        add_section(
            pdf,
            "PROFILE"
        )

        add_text(
            pdf,
            data.summary
        )


    create_experience(
        pdf,
        data
    )

    create_education(
        pdf,
        data
    )

    create_skills(
        pdf,
        data
    )

    create_languages(
        pdf,
        data
    )


def create_executive(pdf, data):

    pdf.add_page()


    pdf.set_font(
        "Helvetica",
        "B",
        20
    )

    pdf.cell(
        0,
        10,
        clean_text(data.full_name),
        ln=True
    )


    pdf.set_font(
        "Helvetica",
        "I",
        11
    )

    pdf.cell(
        0,
        7,
        clean_text(data.target_title),
        ln=True
    )


    pdf.ln(5)


    create_contact(
        pdf,
        data
    )


    add_line(pdf)


    if data.summary:

        add_section(
            pdf,
            "CAREER PROFILE"
        )

        add_text(
            pdf,
            data.summary
        )


    create_experience(
        pdf,
        data
    )

    create_education(
        pdf,
        data
    )

    create_skills(
        pdf,
        data
    )

    create_languages(
        pdf,
        data
    )



def create_european(pdf, data):

    pdf.add_page()


    pdf.set_font(
        "Helvetica",
        "B",
        18
    )

    pdf.cell(
        0,
        10,
        clean_text(data.full_name),
        ln=True
    )


    pdf.set_font(
        "Helvetica",
        "",
        11
    )

    pdf.cell(
        0,
        7,
        clean_text(data.target_title),
        ln=True
    )


    pdf.ln(5)


    create_contact(
        pdf,
        data
    )


    add_line(pdf)


    if data.summary:

        add_section(
            pdf,
            "ABOUT ME"
        )

        add_text(
            pdf,
            data.summary
        )


    create_experience(
        pdf,
        data
    )

    create_education(
        pdf,
        data
    )

    create_skills(
        pdf,
        data
    )

    create_languages(
        pdf,
        data
    )
    

def generate_resume_pdf(data, output_path):

    pdf = ResumePDF()


    template = "classic"


    if hasattr(data, "selected_template"):
        template = data.selected_template.lower()


    # Template mapping

    if template in [
        "classic",
        "classic ats"
    ]:

        create_classic(
            pdf,
            data
        )


    elif template in [
        "canadian",
        "canadian standard"
    ]:

        create_canadian(
            pdf,
            data
        )


    elif template in [
        "corporate",
        "us corporate"
    ]:

        create_corporate(
            pdf,
            data
        )


    elif template in [
        "modern",
        "modern professional"
    ]:

        create_modern(
            pdf,
            data
        )


    elif template in [
        "executive"
    ]:

        create_executive(
            pdf,
            data
        )


    elif template in [
        "european",
        "graphic european"
    ]:

        create_european(
            pdf,
            data
        )


    else:

        create_classic(
            pdf,
            data
        )


    # Save PDF

    pdf.output(
        output_path
    )


    return output_path
