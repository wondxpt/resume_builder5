"""
ResumeData
----------
Central data model shared across all screens of the app.
Each screen reads from / writes to this single object so that
navigating back and forth between screens never loses information.
"""


class ResumeData:
    def __init__(self):
        self.selected_template = "canadian"   # chronological | combination | functional | two_column | minimal | creative_photo
        self.full_name = ""
        self.target_title = ""      # e.g. "Hairstylist | Aspiring Python Developer"
        self.location = ""          # e.g. "Toronto, ON"
        self.email = ""
        self.phone = ""
        self.linkedin = ""
        self.summary = ""
        self.photo_path = ""        # optional, used only by the "creative_photo" template

        self.experience = []        # list of dicts: title, company, location, start_date, end_date, bullets
        self.education = []         # list of dicts: degree, institution, location, grad_date
        self.skills = []            # list of strings
        self.languages = []         # list of dicts: {"name": str, "level": str}

    def add_experience(self, title, company, location, start_date, end_date, bullets_text):
        bullets = [b.strip() for b in bullets_text.split("\n") if b.strip()]
        self.experience.append({
            "title": title,
            "company": company,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "bullets": bullets,
        })

    def update_experience(self, index, title, company, location, start_date, end_date, bullets_text):
        if not (0 <= index < len(self.experience)):
            return
        bullets = [b.strip() for b in bullets_text.split("\n") if b.strip()]
        self.experience[index] = {
            "title": title,
            "company": company,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "bullets": bullets,
        }

    def delete_experience(self, index):
        if 0 <= index < len(self.experience):
            del self.experience[index]

    def add_education(self, degree, institution, location, grad_date):
        self.education.append({
            "degree": degree,
            "institution": institution,
            "location": location,
            "grad_date": grad_date,
        })

    def update_education(self, index, degree, institution, location, grad_date):
        if not (0 <= index < len(self.education)):
            return
        self.education[index] = {
            "degree": degree,
            "institution": institution,
            "location": location,
            "grad_date": grad_date,
        }

    def delete_education(self, index):
        if 0 <= index < len(self.education):
            del self.education[index]

    def set_skills(self, skills_text):
        self.skills = [s.strip() for s in skills_text.split(",") if s.strip()]

    def add_language(self, name, level):
        name = (name or "").strip()
        level = (level or "").strip()
        if not name:
            return
        self.languages.append({"name": name, "level": level})

    def delete_language(self, index):
        if 0 <= index < len(self.languages):
            del self.languages[index]

    def set_photo(self, path):
        self.photo_path = path or ""

    def to_dict(self):
        return {
            "full_name": self.full_name,
            "target_title": self.target_title,
            "selected_template": self.selected_template,
            "photo_path": self.photo_path,
            "location": self.location,
            "email": self.email,
            "phone": self.phone,
            "linkedin": self.linkedin,
            "summary": self.summary,
            "experience": self.experience,
            "education": self.education,
            "skills": self.skills,
            "languages": self.languages,
        }
    def is_ready_for_preview(self):
        """Minimum data needed before allowing PDF generation."""
        return bool(self.full_name and self.email and self.summary)
