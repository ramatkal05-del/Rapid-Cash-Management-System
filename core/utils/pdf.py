from django.conf import settings
from django.template.loader import render_to_string

def generate_pdf(template_src, context_dict={}):
    """
    Generates a PDF from a template and returns the bytes.
    Uses WeasyPrint if available, otherwise raises error with helpful message.
    """
    try:
        from weasyprint import HTML
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            html_string = render_to_string(template_src, context_dict)
            # WeasyPrint 60+ compatibility
            html = HTML(string=html_string)
            result = html.write_pdf()
            return result
    except TypeError as e:
        # Handle WeasyPrint version incompatibility
        raise RuntimeError(
            f"PDF generation error: {e}. "
            "Please try downgrading weasyprint: pip install weasyprint==59.0"
        )
    except (ImportError, OSError) as e:
        raise RuntimeError(
            "WeasyPrint dependencies (GTK+) are missing on this system. "
            "Please install GTK+ for Windows to enable PDF generation. "
            f"Original error: {e}"
        )
    except Exception as e:
        raise RuntimeError(f"PDF generation failed: {e}")
