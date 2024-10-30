from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
# from reportlab.graphics.charts.scatter import ScatterPlot
from reportlab.graphics.charts.lineplots import ScatterPlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
import json
import os

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

    def _add_title_page(self, story, data):
        """Add the title page to the report"""
        # Add logo if it exists
        if os.path.exists(data['logo_path']):
            img = Image(data['logo_path'])
            img.drawHeight = 1.5*inch
            img.drawWidth = 1.5*inch
            story.append(img)
            story.append(Spacer(1, 12))

        # Title
        story.append(Paragraph(f"{data['project_name']}", self.styles['CustomTitle']))
        story.append(Paragraph(f"Monthly Report - {data['month']} {data['year']}", self.styles['SectionTitle']))
        story.append(Spacer(1, 30))

        # Version
        story.append(Paragraph(f"Version: {data['version']}", self.styles['Normal']))
        story.append(Spacer(1, 30))

        # Authors
        story.append(Paragraph("Authors:", self.styles['SubsectionTitle']))
        for author in data['authors']:
            author_text = (
                f"<b>{author['name']}</b><br/>"
                f"Title: {author['title']}<br/>"
                f"Role: {author['role']}<br/>"
                f"Email: {author['contact_info']['email']}<br/>"
                f"Phone: {author['contact_info']['phone']}"
            )
            story.append(Paragraph(author_text, self.styles['Normal']))
            story.append(Spacer(1, 12))

    def _add_project_summary(self, story, data):
        """Add the project summary section"""
        story.append(Paragraph("Project Summary", self.styles['SectionTitle']))
        
        summary_text = (
            f"<b>Description:</b> {data['project_description']}<br/><br/>"
            f"<b>Start Date:</b> {data['project_start_date']}<br/>"
            f"<b>End Date:</b> {data['project_end_date']}<br/>"
            f"<b>Expected Duration:</b> {data['expected_duration']} months"
        )
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(Spacer(1, 20))

    def _create_risk_matrix(self, risks):
        """Create a risk matrix visualization"""
        drawing = Drawing(400, 400)
        
        # Create scatter plot
        scatter = ScatterPlot()
        scatter.x = 50
        scatter.y = 50
        scatter.width = 300
        scatter.height = 300
        
        # Add data points
        scatter.data = [[(risk['likelihood'], risk['impact']) for risk in risks]]
        scatter.xValueAxis.valueMin = 0
        scatter.xValueAxis.valueMax = 5
        scatter.xValueAxis.valueStep = 1
        scatter.yValueAxis.valueMin = 0
        scatter.yValueAxis.valueMax = 5
        scatter.yValueAxis.valueStep = 1
        
        # Labels
        scatter.xValueAxis.labels.fontSize = 10
        scatter.yValueAxis.labels.fontSize = 10
        scatter.xValueAxis.title = "Likelihood"
        scatter.yValueAxis.title = "Impact"
        
        drawing.add(scatter)
        return drawing

    def _create_financial_chart(self, accounts):
        """Create a financial bar chart"""
        drawing = Drawing(500, 250)
        
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 175
        bc.width = 400
        
        # Prepare data
        expected = []
        actual = []
        labels = []
        
        for account in accounts:
            labels.append(account['account_name'])
            expected.append(sum(exp['amount'] for exp in account['expected_expenditures']))
            actual.append(sum(exp['amount'] for exp in account['actual_expenditures']))
        
        bc.data = [expected, actual]
        bc.categoryAxis.categoryNames = labels
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = -8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 30
        
        # Add legend
        bc.bars[0].fillColor = colors.blue
        bc.bars[1].fillColor = colors.red
        drawing.add(bc)
        
        return drawing

    def generate_monthly_report(self):
        """Generate PDF report using ReportLab"""
        with open(self.data_path, 'r') as f:
            data = json.load(f)

        doc = SimpleDocTemplate(
            "monthly_report.pdf",
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        story = []

        # Title Page
        self._add_title_page(story, data)
        story.append(PageBreak())

        # Project Summary
        self._add_project_summary(story, data)
        story.append(PageBreak())

        # Achievements Section
        story.append(Paragraph("Key Achievements", self.styles['SectionTitle']))
        for achievement in data['achievements']:
            p = Paragraph(f"• {achievement['category']}: {achievement['description']}", 
                         self.styles['Normal'])
            story.append(p)
        story.append(Spacer(1, 20))

        # Plans Section (30/60/90 day outlook)
        story.append(Paragraph("Project Plans", self.styles['SectionTitle']))
        
        # Calculate dates
        now = datetime.now()
        thirty_days = now + timedelta(days=30)
        sixty_days = now + timedelta(days=60)
        ninety_days = now + timedelta(days=90)

        # 30-day plans
        story.append(Paragraph("30-Day Outlook", self.styles['SubsectionTitle']))
        for effort in data['roadmap']:
            start_date = datetime.strptime(effort['steps'][0]['start_date'], '%Y-%m-%d')
            if start_date >= now and start_date < thirty_days:
                p = Paragraph(f"• {effort['description']}", self.styles['Normal'])
                story.append(p)
        story.append(Spacer(1, 12))

        # 60-day plans
        story.append(Paragraph("60-Day Outlook", self.styles['SubsectionTitle']))
        for effort in data['roadmap']:
            start_date = datetime.strptime(effort['steps'][0]['start_date'], '%Y-%m-%d')
            if start_date >= thirty_days and start_date < sixty_days:
                p = Paragraph(f"• {effort['description']}", self.styles['Normal'])
                story.append(p)
        story.append(Spacer(1, 12))

        # 90-day plans
        story.append(Paragraph("90-Day Outlook", self.styles['SubsectionTitle']))
        for effort in data['roadmap']:
            start_date = datetime.strptime(effort['steps'][0]['start_date'], '%Y-%m-%d')
            if start_date >= sixty_days and start_date < ninety_days:
                p = Paragraph(f"• {effort['description']}", self.styles['Normal'])
                story.append(p)
        story.append(Spacer(1, 20))

        # Challenges Section
        story.append(Paragraph("Challenges", self.styles['SectionTitle']))
        for challenge in data['challenges']:
            p = Paragraph(f"• {challenge['category']}: {challenge['description']}", 
                         self.styles['Normal'])
            story.append(p)
        story.append(Spacer(1, 20))

        # Risks Section
        story.append(Paragraph("Risk Assessment", self.styles['SectionTitle']))
        for risk in data['risks']:
            risk_text = (
                f"• <b>{risk['description']}</b><br/>"
                f"  Likelihood: {risk['likelihood']}, Impact: {risk['impact']}<br/>"
                f"  Mitigation: {risk['mitigation_plan']}<br/>"
                f"  Expected Effect: {risk['expected_effect']}"
            )
            story.append(Paragraph(risk_text, self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Risk Matrix
        story.append(Paragraph("Risk Matrix", self.styles['SubsectionTitle']))
        risk_matrix = self._create_risk_matrix(data['risks'])
        story.append(risk_matrix)
        story.append(Spacer(1, 20))

        # Financials Section
        story.append(Paragraph("Financial Report", self.styles['SectionTitle']))
        financial_text = (
            f"Planned Expenditures: ${data['planned_expenditures']:,.2f}<br/>"
            f"Actual Expenditures: ${data['actual_expenditures']:,.2f}"
        )
        story.append(Paragraph(financial_text, self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Financial Chart
        story.append(Paragraph("Expenditures by Account", self.styles['SubsectionTitle']))
        financial_chart = self._create_financial_chart(data['financials']['accounts'])
        story.append(financial_chart)
        story.append(Spacer(1, 20))

        # Recipients Section
        story.append(Paragraph("Report Recipients", self.styles['SectionTitle']))
        for recipient in data['recipients']:
            recipient_text = (
                f"<b>{recipient['name']}</b><br/>"
                f"Title: {recipient['title']}<br/>"
                f"Role: {recipient['role']}<br/>"
                f"Email: {recipient['contact_info']['email']}<br/>"
                f"Phone: {recipient['contact_info']['phone']}"
            )
            story.append(Paragraph(recipient_text, self.styles['Normal']))
            story.append(Spacer(1, 12))

        # Build and save the PDF
        doc.build(story)


# Example usage:
# generator = MonthlyReportGenerator('monthly_report/template.html', 'monthly_report/data.json')
# generator.generate_monthly_report()
