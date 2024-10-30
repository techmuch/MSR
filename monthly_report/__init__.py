from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from datetime import datetime, timedelta
import json

class MonthlyReportGenerator:
    def __init__(self, data_path):
        self.data_path = data_path
        self.styles = getSampleStyleSheet()
        # Add custom styles
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        ))
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=20
        ))
        self.styles.add(ParagraphStyle(
            name='SubsectionTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=12
        ))

    def generate_monthly_report(self):
        with open(self.template_path, 'r') as f:
            template_str = f.read()

        with open(self.data_path, 'r') as f:
            data = json.load(f)

        # Create a Jinja2 environment
        env = Environment()

        # Add date filter to environment
        def date_filter(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d')

        env.filters['date'] = date_filter

        # Add sum extension
        env.add_extension(SumExtension)

        # Create a template from the environment
        template = env.from_string(template_str)

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

        # Group challenges by category
        challenges = {}
        for challenge in data['challenges']:
            category = challenge['category']
            if category not in challenges:
                challenges[category] = []
            challenges[category].append(challenge['description'])

        data['achievements'] = achievements
        data['challenges'] = challenges

        # Render template with data
        html_content = template.render(**data)

        # Generate HTML file
        with open("monthly_report.html", "w") as f:
            f.write(html_content)

        # Generate PDF
        c = canvas.Canvas("monthly_report.pdf")
        c.drawString(100, 750, html_content)
        c.save()

    def generate_html_report(self):
        """Generate only the HTML report without PDF"""
        with open(self.template_path, 'r') as f:
            template_str = f.read()

        with open(self.data_path, 'r') as f:
            data = json.load(f)

        # Create a Jinja2 environment
        env = Environment()

        # Add date filter to environment
        def date_filter(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d')

        env.filters['date'] = date_filter

        # Add sum extension
        env.add_extension(SumExtension)

        # Create a template from the environment
        template = env.from_string(template_str)

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

        # Group challenges by category
        challenges = {}
        for challenge in data['challenges']:
            category = challenge['category']
            if category not in challenges:
                challenges[category] = []
            challenges[category].append(challenge['description'])

        data['achievements'] = achievements
        data['challenges'] = challenges

        # Render and save HTML
        html_content = template.render(**data)
        with open("monthly_report.html", "w") as f:
            f.write(html_content)

# Example usage:
# generator = MonthlyReportGenerator('monthly_report/template.html', 'monthly_report/data.json')
# generator.generate_monthly_report()
