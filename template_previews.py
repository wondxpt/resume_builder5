"""
template_previews
------------------
Generates small schematic "wireframe" preview thumbnails (PNG) for each
resume template, so the user can see the shape of the layout (where the
header, sidebar, photo, and text blocks go) before choosing it.

These are NOT full PDF renders — they're lightweight PIL drawings that
mimic the structure and accent color of each layout. This keeps the
dependency list small (just Pillow, which the project already needs for
the circular photo crop) and is fast enough to generate on the fly.

Usage:
    from template_previews import get_preview_path
    path = get_preview_path("combination")   # returns a cached PNG path
"""

import os
import tempfile
from PIL import Image, ImageDraw

W, H = 240, 320
MARGIN = 14
LINE_GREY = (210, 210, 210)
TEXT_GREY = (150, 150, 150)
PAGE_BG = (255, 255, 255)
PAGE_BORDER = (225, 225, 225)

_CACHE_DIR = os.path.join(tempfile.gettempdir(), "resume_template_previews")
os.makedirs(_CACHE_DIR, exist_ok=True)


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def _new_page():
    img = Image.new("RGB", (W, H), PAGE_BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W - 1, H - 1], outline=PAGE_BORDER, width=2)
    return img, draw


def _text_lines(draw, x, y, width, count, gap=10, thickness=3, color=LINE_GREY, shrink_last=0.6):
    """Draws count horizontal bars to represent lines of body text."""
    for i in range(count):
        w = width if i < count - 1 else int(width * shrink_last)
        draw.rectangle([x, y, x + w, y + thickness], fill=color)
        y += gap
    return y


def _section_block(draw, x, y, width, accent, label_w=60, lines=3):
    """A section header (short accent bar) followed by a few text lines."""
    draw.rectangle([x, y, x + label_w, y + 5], fill=accent)
    y += 12
    y = _text_lines(draw, x, y, width, lines)
    return y + 8


# ----------------------------------------------------------------------
# Layout drawers — one per TEMPLATES["layout"] value
# ----------------------------------------------------------------------

def _draw_standard(draw, accent, banner=False, skills_box=False):
    x = MARGIN
    y = MARGIN
    width = W - 2 * MARGIN

    if banner:
        draw.rectangle([0, 0, W, 46], fill=accent)
        draw.rectangle([x + 40, 14, x + width - 40, 20], fill=(255, 255, 255))
        draw.rectangle([x + 60, 26, x + width - 60, 30], fill=(255, 255, 255))
        y = 58
    else:
        draw.rectangle([x + 50, y, x + width - 50, y + 10], fill=(30, 30, 30))
        y += 18
        draw.rectangle([x + 70, y, x + width - 70, y + 6], fill=accent)
        y += 20

    if skills_box:
        draw.rectangle([x, y, x + width, y + 26], fill=(244, 246, 248), outline=accent, width=1)
        y += 34

    y = _section_block(draw, x, y, width, accent, lines=3)
    y = _section_block(draw, x, y, width, accent, lines=2)
    y = _section_block(draw, x, y, width, accent, lines=1)
    return


def _draw_functional(draw, accent):
    x = MARGIN
    y = MARGIN
    width = W - 2 * MARGIN

    draw.rectangle([x + 50, y, x + width - 50, y + 10], fill=(30, 30, 30))
    y += 18
    draw.rectangle([x + 70, y, x + width - 70, y + 6], fill=accent)
    y += 20

    # Prominent skills box near the top
    draw.rectangle([x, y, x + width, y + 34], fill=(246, 244, 253), outline=accent, width=1)
    y += 44

    y = _section_block(draw, x, y, width, accent, lines=1)
    y = _section_block(draw, x, y, width, accent, lines=1)
    y = _section_block(draw, x, y, width, accent, lines=2)
    return


def _draw_two_column(draw, accent):
    sidebar_w = 70
    draw.rectangle([0, 0, sidebar_w, H], fill=accent)

    # sidebar content (white-ish lines)
    sx, sy = 10, 16
    for _ in range(3):
        draw.rectangle([sx, sy, sx + sidebar_w - 20, sy + 4], fill=(255, 255, 255))
        sy += 10
    sy += 14
    for _ in range(4):
        draw.rectangle([sx, sy, sx + sidebar_w - 20, sy + 4], fill=(230, 230, 230))
        sy += 10
# main column
    x = sidebar_w + 14
    y = 16
    width = W - x - MARGIN
    draw.rectangle([x, y, x + width - 30, y + 8], fill=(30, 30, 30))
    y += 22
    y = _section_block(draw, x, y, width, accent, lines=3)
    y = _section_block(draw, x, y, width, accent, lines=2)
    return


def _draw_graphic(draw, accent):
    sidebar_w = 76
    draw.rectangle([0, 0, sidebar_w, H], fill=accent)

    # circular photo placeholder
    cx, cy, r = sidebar_w // 2, 34, 20
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 255), outline=(255, 255, 255))

    sx, sy = 10, 66
    for _ in range(3):
        draw.rectangle([sx, sy, sx + sidebar_w - 20, sy + 4], fill=(255, 255, 255))
        sy += 10
    sy += 14
    for _ in range(3):
        draw.rectangle([sx, sy, sx + sidebar_w - 20, sy + 4], fill=(235, 235, 235))
        sy += 10

    x = sidebar_w + 14
    y = 16
    width = W - x - MARGIN
    draw.rectangle([x, y, x + width - 30, y + 8], fill=(30, 30, 30))
    y += 22
    y = _section_block(draw, x, y, width, accent, lines=3)
    y = _section_block(draw, x, y, width, accent, lines=2)
    return


_LAYOUT_DRAWERS = {
    "standard": lambda draw, accent, cfg: _draw_standard(
        draw, accent, banner=cfg.get("banner", False), skills_box=(cfg.get("layout") == "combination")
    ),
    "combination": lambda draw, accent, cfg: _draw_standard(draw, accent, banner=True, skills_box=True),
    "functional": lambda draw, accent, cfg: _draw_functional(draw, accent),
    "two_column": lambda draw, accent, cfg: _draw_two_column(draw, accent),
    "graphic": lambda draw, accent, cfg: _draw_graphic(draw, accent),
}


def generate_preview(template_key, cfg):
    """Builds (or returns a cached) PNG wireframe preview for one template."""
    cache_path = os.path.join(_CACHE_DIR, f"{template_key}.png")
    if os.path.isfile(cache_path):
        return cache_path

    accent = _hex_to_rgb(cfg["hex"])
    img, draw = _new_page()

    layout = cfg["layout"]
    drawer = _LAYOUT_DRAWERS.get(layout, _LAYOUT_DRAWERS["standard"])
    drawer(draw, accent, cfg)

    img.save(cache_path, "PNG")
    return cache_path


def get_preview_path(template_key):
    from pdf_generator import TEMPLATES
    cfg = TEMPLATES[template_key]
    return generate_preview(template_key, cfg)


def generate_all_previews():
    from pdf_generator import TEMPLATES
    paths = {}
    for key, cfg in TEMPLATES.items():
        paths[key] = generate_preview(key, cfg)
    return paths


if __name__ == "__main__":
    paths = generate_all_previews()
    for k, p in paths.items():
        print(k, "->", p)