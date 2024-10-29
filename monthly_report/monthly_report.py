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

    # Calculate dates
    now = datetime.now()
    thirty_days = now + timedelta(days=30)
    sixty_days = now + timedelta(days=60)
    ninety_days = now + timedelta(days=90)

    # Pass dates to template
    data['now'] = now.strftime('%Y-%m-%d')
    data['thirty_days'] = thirty_days.strftime('%Y-%m-%d')
    data['sixty_days'] = sixty_days.strftime('%Y-%m-%d')
    data['ninety_days'] = ninety_days.strftime('%Y-%m-%d')

    # Calculate effort start and planned completion dates
    for effort in data['roadmap']:
        effort['start_date'] = min(step['start_date'] for step in effort['steps'])
        effort['planned_completion_date'] = max(step['planned_completion_date'] for step in effort['steps'])

    # Group achievements by category
    achievements = {}
    for achievement in data['achievements']:
        category = achievement['category']
        if category not in achievements:
            achievements[category] = []
        achievements[category].append(achievement['description'])

    data['achievements'] = achievements

    pdf_content = template.render(data)

    c = canvas.Canvas("monthly_report.pdf")
    c.drawString(100, 750, pdf_content)
    c.save()
