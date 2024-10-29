from jinja2 import Template
import json
from reportlab.pdfgen import canvas

def generate_monthly_report(template_path, data_path):
    with open(template_path, 'r') as f:
        template = Template(f.read())

    with open(data_path, 'r') as f:
        data = json.load(f)

    pdf_content = template.render(data)

    c = canvas.Canvas("monthly_report.pdf")
    c.drawString(100, 750, pdf_content)
    c.save()
