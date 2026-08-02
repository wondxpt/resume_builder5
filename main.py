import os

os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"

from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.popup import Popup
from pdf_generator import generate_resume_pdf, TEMPLATES
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image as KivyImage

from resume_data import ResumeData
from template_previews import get_preview_path

Window.size = (400, 750)

from plyer import storagepath

OUTPUT_DIR = storagepath.get_documents_dir()

LANGUAGE_OPTIONS = ["English", "French", "German", "Spanish", "Persian", "Other"]
LEVEL_OPTIONS = [
    "Native",
    "Fluent",
    "C2 - Proficient",
    "C1 - Advanced",
    "B2 - Upper Intermediate",
    "B1 - Intermediate",
    "A2 - Elementary",
    "A1 - Beginner",
]




def make_field(hint_text, multiline=False):
    return MDTextField(
        hint_text=hint_text,
        multiline=multiline,
        size_hint_y=None,
        height=48 if not multiline else 120,
    )


def make_help_text(text):
    label = MDLabel(
        text=text,
        theme_text_color="Secondary",
        font_style="Caption",
        size_hint_y=None,
        halign="left",
    )
    label.bind(
        width=lambda inst, w: setattr(label, "text_size", (w, None)),
        texture_size=lambda inst, ts: setattr(label, "height", ts[1] + 8),
    )
    return label


def color_swatch(hex_color, height=8):
    color = get_color_from_hex(hex_color)
    widget = Widget(size_hint_y=None, height=height)
    with widget.canvas:
        Color(*color)
        rect = Rectangle(pos=widget.pos, size=widget.size)

    def update_rect(instance, value):
        rect.pos = instance.pos
        rect.size = instance.size

    widget.bind(pos=update_rect, size=update_rect)
    return widget


def make_scroll_form():
    scroll = ScrollView(size_hint=(1, 1))
    form = MDBoxLayout(
        orientation="vertical",
        spacing=14,
        padding=(24, 20, 24, 20),
        size_hint_y=None,
    )
    form.bind(minimum_height=form.setter("height"))
    scroll.add_widget(form)
    return scroll, form


def nav_row(back_action=None, next_text="Next", next_action=None):
    row = MDBoxLayout(orientation="horizontal", spacing=12, size_hint_y=None, height=50)
    if back_action:
        back_btn = MDFlatButton(text="Back")
        back_btn.bind(on_press=back_action)
        row.add_widget(back_btn)
    if next_action:
        next_btn = MDRaisedButton(text=next_text)
        next_btn.bind(on_press=next_action)
        row.add_widget(next_btn)
    return row




def build_template_screen(app):
    screen = MDScreen(name="template")
    scroll, form = make_scroll_form()

    form.add_widget(
        MDLabel(
            text="Choose a Resume Template",
            font_style="H5",
            size_hint_y=None,
            height=44,
            bold=True,
        )
    )
    form.add_widget(
        make_help_text(
            "Pick a template. Simple single-column templates are safer for US/Canada ATS; "
            "the graphic template with a photo is better suited for markets like Europe or "
            "for a portfolio/LinkedIn profile. You can change this later."
        )
    )

    selected_label = MDLabel(
        text=f"Selected: {TEMPLATES[app.data.selected_template]['label']}",
        size_hint_y=None,
        height=30,
        theme_text_color="Primary",
        bold=True,
    )
    form.add_widget(selected_label)

    def select_template(key):
        def handler(instance):
            app.data.selected_template = key
            selected_label.text = f"Selected: {TEMPLATES[key]['label']}"

        return handler

    for key, cfg in TEMPLATES.items():
        card = MDBoxLayout(
            orientation="vertical",
            spacing=6,
            size_hint_y=None,
            padding=(12, 10, 12, 10),
        )
        card.bind(minimum_height=card.setter("height"))

        preview_img = KivyImage(
            source=get_preview_path(key),
            size_hint_y=None,
            height=160,
            allow_stretch=True,
            keep_ratio=True,
        )
        card.add_widget(preview_img)
        card.add_widget(
            MDLabel(text=cfg["label"], bold=True, size_hint_y=None, height=26)
        )
        card.add_widget(make_help_text(cfg["description"]))

        choose_btn = MDRaisedButton(
            text=f"Use {cfg['label']}", size_hint_y=None, height=44
        )
        choose_btn.bind(on_press=select_template(key))
        card.add_widget(choose_btn)

        form.add_widget(card)
        form.add_widget(Widget(size_hint_y=None, height=8))

    def go_next(instance):
        # The graphic/photo template gets an extra screen to upload a photo.
        if app.data.selected_template == "creative_photo":
            app.sm.current = "photo"
        else:
            app.sm.current = "personal"

    form.add_widget(nav_row(next_action=go_next))
    screen.add_widget(scroll)
    return screen


def build_photo_screen(app):
    """Optional screen, only reached when the 'creative_photo' template is selected."""
    screen = MDScreen(name="photo")
    scroll, form = make_scroll_form()

    form.add_widget(
        MDLabel(
            text="Add Your Photo",
            font_style="H5",
            size_hint_y=None,
            height=40,
            bold=True,
        )
    )
    form.add_widget(
        make_help_text(
            "This template is graphic and works best with a profile photo. Choose a photo and "
            "it will be automatically cropped into a circle. If you don't want to add a photo, "
            "you can skip this step."
        )
    )

    preview = KivyImage(size_hint_y=None, height=160)
    if app.data.photo_path:
        preview.source = app.data.photo_path
    form.add_widget(preview)

    path_label = MDLabel(
        text=app.data.photo_path or "No photo selected",
        size_hint_y=None,
        height=28,
        theme_text_color="Secondary",
    )
    form.add_widget(path_label)

    def open_chooser(instance):
    chooser = FileChooserIconView(filters=["*.png", "*.jpg", "*.jpeg"])
    popup = Popup(title="Select a photo", content=chooser, size_hint=(0.9, 0.9))

    def on_selection(inst, selection):
        if selection:
            chosen_path = selection[0]
            app.data.set_photo(chosen_path)
            preview.source = chosen_path
            path_label.text = chosen_path
            popup.dismiss()

    chooser.bind(selection=on_selection)
    popup.open()

choose_btn = MDRaisedButton(text="Choose Photo", size_hint_y=None, height=48)
choose_btn.bind(on_press=open_chooser)
form.add_widget(choose_btn)

def clear_photo(instance):
    app.data.set_photo("")
    preview.source = ""
    path_label.text = "No photo selected"

clear_btn = MDFlatButton(
    text="Remove Photo",
    size_hint_y=None,
    height=44
)
    clear_btn.bind(on_press=clear_photo)
    form.add_widget(clear_btn)
    

    def go_back(instance):
        app.sm.current = "template"

    def go_next(instance):
        app.sm.current = "personal"

    form.add_widget(nav_row(back_action=go_back, next_action=go_next))
    screen.add_widget(scroll)
    return screen


def build_personal_screen(app):
    screen = MDScreen(name="personal")
    scroll, form = make_scroll_form()

    form.add_widget(
        MDLabel(
            text="Personal Information",
            font_style="H5",
            size_hint_y=None,
            height=40,
            bold=True,
        )
    )
    form.add_widget(
        make_help_text(
            "Enter your basic information. Target Job Title means the role you're applying for, "
            "e.g. 'Hairstylist' or 'Python Developer'."
        )
    )
    f_name = make_field("Full Name")
    f_title = make_field("Target Job Title (e.g. Python Developer)")
    f_location = make_field("City, Province (e.g. Toronto, ON)")
    f_email = make_field("Email")
    f_phone = make_field("Phone")
    f_linkedin = make_field("LinkedIn URL (optional)")
    f_summary = make_field("Professional Summary (3-4 sentences)", multiline=True)

    # Pre-fill from existing data (so navigating back and forth doesn't lose it)
    f_name.text = app.data.full_name
    f_title.text = app.data.target_title
    f_location.text = app.data.location
    f_email.text = app.data.email
    f_phone.text = app.data.phone
    f_linkedin.text = app.data.linkedin
    f_summary.text = app.data.summary

    for f in [f_name, f_title, f_location, f_email, f_phone, f_linkedin, f_summary]:
        form.add_widget(f)

    def go_back(instance):
        if app.data.selected_template == "creative_photo":
            app.sm.current = "photo"
        else:
            app.sm.current = "template"

    def go_next(instance):
        app.data.full_name = f_name.text.strip()
        app.data.target_title = f_title.text.strip()
        app.data.location = f_location.text.strip()
        app.data.email = f_email.text.strip()
        app.data.phone = f_phone.text.strip()
        app.data.linkedin = f_linkedin.text.strip()
        app.data.summary = f_summary.text.strip()
        app.sm.current = "experience"

    form.add_widget(nav_row(back_action=go_back, next_action=go_next))
    screen.add_widget(scroll)
    return screen


def build_experience_screen(app):
    screen = MDScreen(name="experience")
    scroll, form = make_scroll_form()

    form.add_widget(
        MDLabel(
            text="Work Experience",
            font_style="H5",
            size_hint_y=None,
            height=40,
            bold=True,
        )
    )
    form.add_widget(
        make_help_text(
            'Fill in each job separately. After each one, make sure to tap "+ Add This Job", '
            "otherwise it won't be saved. For achievements, write one sentence per line. "
            "If you have no work experience, just move to the next screen without filling this in. "
            "You can edit or delete any entry below at any time."
        )
    )

    count_label = MDLabel(
        text=f"{len(app.data.experience)} entries added", size_hint_y=None, height=28
    )
    form.add_widget(count_label)

    entry_list = MDBoxLayout(orientation="vertical", spacing=6, size_hint_y=None)
    entry_list.bind(minimum_height=entry_list.setter("height"))
    form.add_widget(entry_list)

    f_job_title = make_field("Job Title")
    f_company = make_field("Company Name")
    f_job_location = make_field("City, Province")
    f_start = make_field("Start Date (e.g. Jan 2022)")
    f_end = make_field("End Date (e.g. Present)")
    f_bullets = make_field("Achievements (one per line)", multiline=True)

    for f in [f_job_title, f_company, f_job_location, f_start, f_end, f_bullets]:
        form.add_widget(f)

    editing_index = {"value": None}
    
    def clear_fields():
        for f in [f_job_title, f_company, f_job_location, f_start, f_end, f_bullets]:
            f.text = ""

    def refresh_entry_list():
        entry_list.clear_widgets()
        for i, job in enumerate(app.data.experience):
            row = MDBoxLayout(
                orientation="horizontal", spacing=8, size_hint_y=None, height=40
            )
            label_text = f"{job.get('title', '')} — {job.get('company', '')}"
            row.add_widget(MDLabel(text=label_text, shorten=True, shorten_from="right"))

            edit_btn = MDFlatButton(text="Edit", size_hint_x=None, width=60)
            edit_btn.bind(on_press=lambda inst, idx=i: start_edit(idx))
            row.add_widget(edit_btn)

            delete_btn = MDFlatButton(text="Delete", size_hint_x=None, width=70)
            delete_btn.bind(on_press=lambda inst, idx=i: delete_entry(idx))
            row.add_widget(delete_btn)

            entry_list.add_widget(row)
        count_label.text = f"{len(app.data.experience)} entries added"

    def start_edit(index):
        job = app.data.experience[index]
        f_job_title.text = job.get("title", "")
        f_company.text = job.get("company", "")
        f_job_location.text = job.get("location", "")
        f_start.text = job.get("start_date", "")
        f_end.text = job.get("end_date", "")
        f_bullets.text = "\n".join(job.get("bullets", []))
        editing_index["value"] = index
        add_btn.text = "Update This Job"
        cancel_btn.opacity = 1
        cancel_btn.disabled = False

    def cancel_edit(instance):
        editing_index["value"] = None
        clear_fields()
        add_btn.text = "+ Add This Job"
        cancel_btn.opacity = 0
        cancel_btn.disabled = True

    def delete_entry(index):
        app.data.delete_experience(index)
        if editing_index["value"] == index:
            cancel_edit(None)
        refresh_entry_list()

    def add_or_update_entry(instance):
        if not f_job_title.text.strip():
            return
        if editing_index["value"] is not None:
            app.data.update_experience(
                editing_index["value"],
                f_job_title.text.strip(),
                f_company.text.strip(),
                f_job_location.text.strip(),
                f_start.text.strip(),
                f_end.text.strip(),
                f_bullets.text.strip(),
            )
        else:
            app.data.add_experience(
                f_job_title.text.strip(),
                f_company.text.strip(),
                f_job_location.text.strip(),
                f_start.text.strip(),
                f_end.text.strip(),
                f_bullets.text.strip(),
            )
        cancel_edit(None)
        refresh_entry_list()

    add_btn = MDRaisedButton(text="+ Add This Job", size_hint_y=None, height=48)
    add_btn.bind(on_press=add_or_update_entry)
    form.add_widget(add_btn)

    cancel_btn = MDFlatButton(
        text="Cancel Edit", size_hint_y=None, height=40, opacity=0, disabled=True
    )
    cancel_btn.bind(on_press=cancel_edit)
    form.add_widget(cancel_btn)

    refresh_entry_list()

    def go_back(instance):
        app.sm.current = "personal"

    def go_next(instance):
        app.sm.current = "education"

    form.add_widget(nav_row(back_action=go_back, next_action=go_next))
    screen.add_widget(scroll)
    return screen


def build_education_screen(app):
    screen = MDScreen(name="education")
    scroll, form = make_scroll_form()

    form.add_widget(
        MDLabel(
            text="Education", font_style="H5", size_hint_y=None, height=40, bold=True
        )
    )
    form.add_widget(
        make_help_text(
            'Enter your degree or certificate and make sure to tap "+ Add This Education" to save it. '
            "You can add multiple entries, and edit or delete any of them below at any time."
        )
    )

    count_label = MDLabel(
        text=f"{len(app.data.education)} entries added", size_hint_y=None, height=28
    )
    form.add_widget(count_label)

    entry_list = MDBoxLayout(orientation="vertical", spacing=6, size_hint_y=None)
    entry_list.bind(minimum_height=entry_list.setter("height"))
    form.add_widget(entry_list)

    f_degree = make_field("Degree / Certificate")
    f_institution = make_field("Institution Name")
    f_edu_location = make_field("City, Province/Country")
    f_grad = make_field("Graduation Year")

    for f in [f_degree, f_institution, f_edu_location, f_grad]:
        form.add_widget(f)

    editing_index = {"value": None}

    def clear_fields():
        for f in [f_degree, f_institution, f_edu_location, f_grad]:
            f.text = ""

    def refresh_entry_list():
        entry_list.clear_widgets()
        for i, edu in enumerate(app.data.education):
            row = MDBoxLayout(
                orientation="horizontal", spacing=8, size_hint_y=None, height=40
            )
            label_text = f"{edu.get('degree', '')} — {edu.get('institution', '')}"
            row.add_widget(MDLabel(text=label_text, shorten=True, shorten_from="right"))
            edit_btn = MDFlatButton(text="Edit", size_hint_x=None, width=60)
            edit_btn.bind(on_press=lambda inst, idx=i: start_edit(idx))
            row.add_widget(edit_btn)

            delete_btn = MDFlatButton(text="Delete", size_hint_x=None, width=70)
            delete_btn.bind(on_press=lambda inst, idx=i: delete_entry(idx))
            row.add_widget(delete_btn)

            entry_list.add_widget(row)
        count_label.text = f"{len(app.data.education)} entries added"

    def start_edit(index):
        edu = app.data.education[index]
        f_degree.text = edu.get("degree", "")
        f_institution.text = edu.get("institution", "")
        f_edu_location.text = edu.get("location", "")
        f_grad.text = edu.get("grad_date", "")
        editing_index["value"] = index
        add_btn.text = "Update This Education"
        cancel_btn.opacity = 1
        cancel_btn.disabled = False

    def cancel_edit(instance):
        editing_index["value"] = None
        clear_fields()
        add_btn.text = "+ Add This Education"
        cancel_btn.opacity = 0
        cancel_btn.disabled = True

    def delete_entry(index):
        app.data.delete_education(index)
        if editing_index["value"] == index:
            cancel_edit(None)
        refresh_entry_list()

    def add_or_update_entry(instance):
        if not f_degree.text.strip():
            return
        if editing_index["value"] is not None:
            app.data.update_education(
                editing_index["value"],
                f_degree.text.strip(),
                f_institution.text.strip(),
                f_edu_location.text.strip(),
                f_grad.text.strip(),
            )
        else:
            app.data.add_education(
                f_degree.text.strip(),
                f_institution.text.strip(),
                f_edu_location.text.strip(),
                f_grad.text.strip(),
            )
        cancel_edit(None)
        refresh_entry_list()

    add_btn = MDRaisedButton(text="+ Add This Education", size_hint_y=None, height=48)
    add_btn.bind(on_press=add_or_update_entry)
    form.add_widget(add_btn)

    cancel_btn = MDFlatButton(
        text="Cancel Edit", size_hint_y=None, height=40, opacity=0, disabled=True
    )
    cancel_btn.bind(on_press=cancel_edit)
    form.add_widget(cancel_btn)

    refresh_entry_list()

    def go_back(instance):
        app.sm.current = "experience"

    def go_next(instance):
        app.sm.current = "skills"

    form.add_widget(nav_row(back_action=go_back, next_action=go_next))
    screen.add_widget(scroll)
    return screen


def build_skills_screen(app):
    screen = MDScreen(name="skills")
    scroll, form = make_scroll_form()

    form.add_widget(
        MDLabel(
            text="Skills & Languages",
            font_style="H5",
            size_hint_y=None,
            height=40,
            bold=True,
        )
    )
    form.add_widget(
        make_help_text(
            "Separate skills with commas. For languages, pick the language and then the "
            'proficiency level from the menus, then tap "+ Add Language".'
        )
    )

    f_skills = make_field("Skills, separated by commas", multiline=True)
    f_skills.text = ", ".join(app.data.skills)
    form.add_widget(f_skills)

    selected_language = MDRaisedButton(
        text="Select Language", size_hint_y=None, height=48
    )
    selected_level = MDRaisedButton(text="Select Level", size_hint_y=None, height=48)
    form.add_widget(selected_language)
    form.add_widget(selected_level)

    language_list = MDBoxLayout(orientation="vertical", spacing=4, size_hint_y=None)
    language_list.bind(minimum_height=language_list.setter("height"))
    form.add_widget(language_list)

    def refresh_language_list():
        language_list.clear_widgets()
        if not app.data.languages:
            language_list.add_widget(
                MDLabel(text="No languages added", size_hint_y=None, height=28)
            )
            return
        for i, l in enumerate(app.data.languages):
            row = MDBoxLayout(
                orientation="horizontal", spacing=8, size_hint_y=None, height=36
            )
            row.add_widget(MDLabel(text=f"{l['name']} - {l['level']}"))
            delete_btn = MDFlatButton(text="Delete", size_hint_x=None, width=70)
            delete_btn.bind(on_press=lambda inst, idx=i: delete_language(idx))
            row.add_widget(delete_btn)
            language_list.add_widget(row)

    def delete_language(index):
        app.data.delete_language(index)
        refresh_language_list()

    refresh_language_list()

    def set_language(value):
        selected_language.text = value
        language_menu.dismiss()

    def set_level(value):
        selected_level.text = value
        level_menu.dismiss()

    language_menu = MDDropdownMenu(
        caller=selected_language,
        items=[
            {
                "text": lang,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=lang: set_language(x),
            }
            for lang in LANGUAGE_OPTIONS
        ],
        width_mult=4,
    )

    level_menu = MDDropdownMenu(
        caller=selected_level,
        items=[
            {
                "text": lvl,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=lvl: set_level(x),
            }
            for lvl in LEVEL_OPTIONS
        ],
        width_mult=5,
    )

    selected_language.bind(on_release=lambda x: language_menu.open())
    selected_level.bind(on_release=lambda x: level_menu.open())

    def add_language(instance):
        if selected_language.text in ("Select Language", ""):
            return
        app.data.add_language(
            selected_language.text,
            selected_level.text if selected_level.text != "Select Level" else "",
        )
        refresh_language_list()
        selected_language.text = "Select Language"
        selected_level.text = "Select Level"

    add_btn = MDRaisedButton(text="+ Add Language", size_hint_y=None, height=48)
    add_btn.bind(on_press=add_language)
    form.add_widget(add_btn)

    def go_back(instance):
        app.sm.current = "education"

    def go_next(instance):
        app.data.set_skills(f_skills.text.strip())
        app.sm.current = "preview"

    form.add_widget(
        nav_row(back_action=go_back, next_text="Review & Generate", next_action=go_next)
    )
    screen.add_widget(scroll)
    return screen


def build_preview_screen(app):
    screen = MDScreen(name="preview")
    scroll, form = make_scroll_form()

    form.add_widget(
        MDLabel(
            text="Review & Generate",
            font_style="H5",
            size_hint_y=None,
            height=40,
            bold=True,
        )
    )
    form.add_widget(
        make_help_text(
            "Check this summary before generating the PDF. If the Experience or Education count "
            "is zero, you probably forgot to tap the Add button — go back and fix it."
        )
    )

    preview_caption = MDLabel(
        text="", size_hint_y=None, height=22, theme_text_color="Secondary"
    )
    form.add_widget(preview_caption)
    template_preview_img = KivyImage(
        source=get_preview_path(app.data.selected_template),
        size_hint_y=None,
        height=280,
        allow_stretch=True,
        keep_ratio=True,
    )
    form.add_widget(template_preview_img)

    def open_fullscreen_preview(instance):
        popup_image = KivyImage(
            source=template_preview_img.source,
            allow_stretch=True,
            keep_ratio=True,
        )
        close_btn = MDFlatButton(text="Close", size_hint_y=None, height=48)
        popup_box = MDBoxLayout(orientation="vertical", spacing=8, padding=8)
        popup_box.add_widget(popup_image)
        popup_box.add_widget(close_btn)

        popup = Popup(
            title="Resume Preview",
            content=popup_box,
            size_hint=(0.95, 0.95),
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    fullscreen_btn = MDFlatButton(text="View Full Screen", size_hint_y=None, height=44)
    fullscreen_btn.bind(on_press=open_fullscreen_preview)
    form.add_widget(fullscreen_btn)
    change_template_btn = MDRaisedButton(
        text="Change Template", size_hint_y=None, height=48
    )
    form.add_widget(change_template_btn)

    def pick_template(key):
        def handler(*args):
            app.data.selected_template = key
            template_menu.dismiss()
            refresh_summary()

        return handler

    template_menu = MDDropdownMenu(
        caller=change_template_btn,
        items=[
            {
                "text": cfg["label"],
                "viewclass": "OneLineListItem",
                "on_release": pick_template(key),
            }
            for key, cfg in TEMPLATES.items()
        ],
        width_mult=5,
    )
    change_template_btn.bind(on_release=lambda x: template_menu.open())

    template_label = MDLabel(text="", size_hint_y=None, height=26, bold=True)
    form.add_widget(template_label)

    summary_label = MDLabel(text="", size_hint_y=None, halign="left")
    summary_label.bind(
        texture_size=lambda inst, val: setattr(summary_label, "height", val[1])
    )
    form.add_widget(summary_label)

    status_label = MDLabel(text="", size_hint_y=None, height=40)
    form.add_widget(status_label)

    def refresh_summary():
        d = app.data
        tpl = TEMPLATES[d.selected_template]
        template_label.text = f"Template: {tpl['label']}"

        live_png = None


        missing = []
        if not d.full_name:
            missing.append("Full Name")
        if not d.email:
            missing.append("Email")
        if not d.summary:
            missing.append("Professional Summary")

        if live_png:
            preview_caption.text = "This is exactly what your PDF will look like:"
            template_preview_img.source = live_png
        elif missing:
            preview_caption.text = (
                "Fill in "
                + ", ".join(missing)
                + " (on the Personal Information screen) "
                "to see your actual resume here."
            )
            template_preview_img.source = get_preview_path(d.selected_template)
        else:
            preview_caption.text = "Layout preview:"
            template_preview_img.source = get_preview_path(d.selected_template)
        template_preview_img.reload()

        warnings = []
        if len(d.experience) == 0:
            warnings.append(
                '⚠ No work experience added — did you forget to tap "+ Add This Job"?'
            )
        if len(d.education) == 0:
            warnings.append(
                '⚠ No education added — did you forget to tap "+ Add This Education"?'
            )
        if d.selected_template == "creative_photo" and not d.photo_path:
            warnings.append("⚠ This template is designed for a photo — none was added.")
        summary_label.text = "\n".join(warnings)

    def generate_pdf(instance):
        if not app.data.is_ready_for_preview():
            status_label.text = "Please fill in name, email, and summary first."
            status_label.theme_text_color = "Error"
            return
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        safe_name = (app.data.full_name or "resume").replace(" ", "_")
        output_path = os.path.join(OUTPUT_DIR, f"{safe_name}_Resume.pdf")
        try:
            generate_resume_pdf(app.data.to_dict(), output_path)
            status_label.text = f"Saved to: {output_path}"
            status_label.theme_text_color = "Primary"
        except Exception as e:
            status_label.text = f"Error: {e}"
            status_label.theme_text_color = "Error"

    gen_btn = MDRaisedButton(text="Generate PDF Resume", size_hint_y=None, height=52)
    gen_btn.bind(on_press=generate_pdf)
    form.add_widget(gen_btn)

    def go_back(instance):
        app.sm.current = "skills"

    form.add_widget(nav_row(back_action=go_back))

    screen.bind(on_pre_enter=lambda inst: refresh_summary())
    screen.add_widget(scroll)
    return screen



class ResumeBuilderApp(MDApp):
    def build(self):
        self.title = "Canadian Resume Builder"
        self.theme_cls.primary_palette = "Blue"
        self.data = ResumeData()

        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(build_template_screen(self))
        self.sm.add_widget(build_photo_screen(self))
        self.sm.add_widget(build_personal_screen(self))
        self.sm.add_widget(build_experience_screen(self))
        self.sm.add_widget(build_education_screen(self))
        self.sm.add_widget(build_skills_screen(self))
        self.sm.add_widget(build_preview_screen(self))
        self.sm.current = "template"

        return self.sm


if __name__ == "__main__":
    ResumeBuilderApp().run()
