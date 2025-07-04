from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_pdf_report(address, insights, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    margin = 50
    y = height - margin

    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, "Buyer’s Advantage Property Report")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(margin, y, f"Address: {address}")
    y -= 20

    c.setFont("Helvetica", 11)
    text_object = c.beginText(margin, y)
    text_object.setLeading(14)

    for line in insights.split('\n'):
        text_object.textLine(line)

    c.drawText(text_object)

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(margin, 30, "Disclaimer: This report is for general guidance only and not professional advice.")

    c.save()
