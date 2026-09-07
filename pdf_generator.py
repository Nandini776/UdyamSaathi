from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_pdf_report(shop_name, total_income, total_expense, net_profit, forecast_revenue, filename="business_report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # 1. Header (FIXED: Subtitle ki jagah Heading2 use kiya hai)
    story.append(Paragraph(f"<b>Micro-Enterprise Financial Project Report</b>", styles['Title']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>Enterprise Name:</b> {shop_name}", styles['Heading2']))
    story.append(Spacer(1, 15))

    # 2. Financial Metrics Table
    data = [
        ["Financial Metric", "Value (₹)"],
        ["Total Revenue (Historical)", f"Rs. {total_income:,.2f}"],
        ["Total Operating Expenses", f"Rs. {total_expense:,.2f}"],
        ["Net Operational Profit", f"Rs. {net_profit:,.2f}"],
        ["Projected 7-Day Revenue (AI Model)", f"Rs. {forecast_revenue:,.2f}"]
    ]

    t = Table(data, colWidths=[250, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 8)
    ]))
    
    story.append(t)
    story.append(Spacer(1, 20))
    
    # 3. Footer Declaration
    story.append(Paragraph("<i>Declaration: Generated via AI-Driven Hyper-Local Financial Assistant for MoSJE Scheme Credit Evaluation.</i>", styles['Normal']))

    doc.build(story)
    return filename