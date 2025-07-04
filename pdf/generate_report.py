
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import textwrap
import requests
from io import BytesIO

def create_pdf_report(address, insights, filename, image_url=None):
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

    # Draw image if available
    if image_url:
        try:
            response = requests.get(image_url)
            img = ImageReader(BytesIO(response.content))
            c.drawImage(img, margin, y - 180, width=5.5*inch, height=3*inch)
            y -= 200
        except Exception as e:
            y -= 20
            c.setFont("Helvetica-Oblique", 8)
            c.drawString(margin, y, f"(Image failed to load: {e})")
            y -= 20

    # Cover title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, "Buyer’s Advantage Property Report")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(margin, y, f"Address: {address}")
    y -= 40

    # Parse AI content
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
