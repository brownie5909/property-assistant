
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
import textwrap

def create_pdf_report(address, insights, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    margin = 50
    y = height - margin

    def draw_heading(text, y):
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y, text)
        return y - 24

    def draw_paragraph(text, y, font_size=10):
        c.setFont("Helvetica", font_size)
        wrap_width = 90
        for line in text.split("\n"):
            wrapped = textwrap.wrap(line, wrap_width)
            for wline in wrapped:
                if y < 50:
                    c.showPage()
                    y = height - margin
                    c.setFont("Helvetica", font_size)
                c.drawString(margin, y, wline)
                y -= 14
            y -= 6
        return y

    # Cover
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, "Buyer’s Advantage Property Report")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(margin, y, f"Address: {address}")
    y -= 40

    # Parse AI content with markdown-style headings
    lines = insights.split("\n")
    for line in lines:
        if line.strip().startswith("**") and line.strip().endswith("**"):
            y = draw_heading(line.strip(" *"), y)
        else:
            y = draw_paragraph(line, y)

    # Disclaimer
    y = 40
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(margin, y, "Disclaimer: This report is for general guidance only and not professional advice.")

    c.save()
