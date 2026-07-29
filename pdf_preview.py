"""
pdf_preview
-----------
Renders the first page of a generated resume PDF into a PNG so the app
can show a LIVE preview of the user's actual resume (their real name,
job title, experience, etc.) instead of just a generic template mockup.

Requires PyMuPDF:
    pip install pymupdf

If PyMuPDF isn't installed, render_pdf_first_page() returns None and the
app should fall back to the generic wireframe in template_previews.py.
"""

import os
import tempfile

try:
    import fitz  # PyMuPDF
    FITZ_AVAILABLE = True
except ImportError:
    FITZ_AVAILABLE = False

_CACHE_DIR = os.path.join(tempfile.gettempdir(), "resume_live_previews")
os.makedirs(_CACHE_DIR, exist_ok=True)

_LIVE_PREVIEW_PDF = os.path.join(_CACHE_DIR, "live_preview.pdf")
_LIVE_PREVIEW_PNG = os.path.join(_CACHE_DIR, "live_preview.png")


def render_pdf_first_page(pdf_path, dpi=130):
    """
    Renders page 1 of pdf_path to a PNG and returns the PNG path.
    Returns None if PyMuPDF isn't available, the file doesn't exist,
    or rendering fails for any reason (caller should fall back to the
    generic template wireframe in that case).
    """
    if not FITZ_AVAILABLE or not os.path.isfile(pdf_path):
        return None
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)
        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=matrix)
        pix.save(_LIVE_PREVIEW_PNG)
        doc.close()
        return _LIVE_PREVIEW_PNG
    except Exception:
        import traceback
        print("[pdf_preview] Failed to render PDF page to PNG:")
        traceback.print_exc()
        return None


def build_live_preview(resume_dict, generate_fn, template=None, dpi=130):
    """
    Convenience wrapper: generates a throwaway resume PDF from the current
    (possibly incomplete) form data using generate_fn (pass
    generate_resume_pdf from pdf_generator.py), then renders it to PNG.

    Returns the PNG path on success, or None on any failure (missing
    PyMuPDF, incomplete data that breaks layout, etc.) so the caller can
    fall back to the generic wireframe preview. Any failure is printed to
    the console so it's easy to diagnose instead of failing silently.
    """
    if not FITZ_AVAILABLE:
        print("[pdf_preview] PyMuPDF not available, skipping live preview.")
        return None
    try:
        generate_fn(resume_dict, _LIVE_PREVIEW_PDF, template=template)
        result = render_pdf_first_page(_LIVE_PREVIEW_PDF, dpi=dpi)
        if result is None:
            print("[pdf_preview] render_pdf_first_page returned None "
                  "(PDF was generated OK, but rendering it to PNG failed).")
        return result
    except Exception:
        import traceback
        print("[pdf_preview] Failed to build live preview:")
        traceback.print_exc()
        return None