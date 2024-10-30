from jinja2 import Template, Environment
import json
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
from jinja2.ext import Extension
from jinja2.lexer import Token
from jinja2.utils import open_if_exists

class SumExtension(Extension):
    def filter_test(self, value):
        return value

    def sum(self, items, attribute=None):
        if attribute:
            return sum(item[attribute] for item in items)
        return sum(items)

    def __init__(self, environment):
        super(SumExtension, self).__init__(environment)
        environment.filters['sum'] = self.sum

class MonthlyReportGenerator:
    def __init__(self, template_path, data_path):
        self.template_path = template_path
        self.data_path = data_path

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
