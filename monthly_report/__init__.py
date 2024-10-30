from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
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

        # Title
        title = Paragraph(f"Monthly Status Report - {data['month']} {data['year']}", 
                         self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 12))

        # Achievements Section
        story.append(Paragraph("Key Achievements", self.styles['SectionTitle']))
        for achievement in data['achievements']:
            p = Paragraph(f"• {achievement['category']}: {achievement['description']}", 
                         self.styles['Normal'])
            story.append(p)
        story.append(Spacer(1, 12))

        # Challenges Section
        story.append(Paragraph("Challenges", self.styles['SectionTitle']))
        for challenge in data['challenges']:
            p = Paragraph(f"• {challenge['category']}: {challenge['description']}", 
                         self.styles['Normal'])
            story.append(p)
        story.append(Spacer(1, 12))

        # Build and save the PDF
        doc.build(story)


# Example usage:
# generator = MonthlyReportGenerator('monthly_report/template.html', 'monthly_report/data.json')
# generator.generate_monthly_report()
