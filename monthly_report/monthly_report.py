from jinja2 import Template
import json
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta

def generate_monthly_report(template_path, data_path):
    with open(template_path, 'r') as f:
        template = Template(f.read())

    with open(data_path, 'r') as f:
        data = json.load(f)

    # Add date filter to template
    def date_filter(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d')

    template.filters['date'] = date_filter

    pdf_content = template.render(data)

    c = canvas.Canvas("monthly_report.pdf")
    c.drawString(100, 750, pdf_content)
    c.save()
