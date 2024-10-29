# Monthly Status Report Generator

This is a Python script that generates a monthly status report based on a JSON data file.

## Requirements

* Python 3.8+
* Jinja2 templating engine
* ReportLab library for PDF generation
* Chart.js library for chart generation

## Usage

1. Update the `monthly_report/data.json` file with the latest project data.
2. Run the `monthly_report/monthly_report.py` script to generate the report.
3. The report will be saved as a PDF file named `monthly_report.pdf`.

## Report Structure

The report includes the following sections:

* Key Achievements
* Challenges
* Planned Efforts
* Financials
* Risk Tracker
* Risk Matrix

## Customization

The report template can be customized by modifying the `monthly_report/template.html` file.

## Dependencies

The script depends on the following libraries:

* Jinja2
* ReportLab
* Chart.js

These libraries can be installed using pip:

