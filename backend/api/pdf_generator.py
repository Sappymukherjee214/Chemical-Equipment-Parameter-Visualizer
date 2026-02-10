from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os
from django.conf import settings
from .models import Dataset


def generate_pdf_report(dataset_id):
    """
    Generate a PDF report for a dataset.
    
    Args:
        dataset_id: ID of the dataset
        
    Returns:
        str: Path to generated PDF file
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id)
    except Dataset.DoesNotExist:
        raise ValueError("Dataset not found")
    
    # Create reports directory if it doesn't exist
    reports_dir = settings.REPORTS_DIR
    reports_dir.mkdir(exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"report_{dataset.id}_{timestamp}.pdf"
    filepath = os.path.join(reports_dir, filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#283593'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph("Chemical Equipment Parameter Report", title_style)
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Dataset Information
    info_heading = Paragraph("Dataset Information", heading_style)
    story.append(info_heading)
    
    info_data = [
        ['Dataset Name:', dataset.name],
        ['Uploaded By:', str(dataset.uploaded_by)],
        ['Upload Date:', dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')],
        ['Total Equipment:', str(dataset.total_equipment)],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Statistics
    summary_heading = Paragraph("Summary Statistics", heading_style)
    story.append(summary_heading)
    
    summary_data = [
        ['Parameter', 'Average Value'],
        ['Flowrate', f"{dataset.avg_flowrate:.2f}"],
        ['Pressure', f"{dataset.avg_pressure:.2f}"],
        ['Temperature', f"{dataset.avg_temperature:.2f}"],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Equipment Type Distribution
    type_heading = Paragraph("Equipment Type Distribution", heading_style)
    story.append(type_heading)
    
    type_data = [['Equipment Type', 'Count']]
    for eq_type, count in dataset.equipment_types.items():
        type_data.append([eq_type, str(count)])
    
    type_table = Table(type_data, colWidths=[3*inch, 3*inch])
    type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    story.append(type_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Equipment Details
    details_heading = Paragraph("Equipment Details", heading_style)
    story.append(details_heading)
    
    equipment_records = dataset.equipment_records.all()[:50]  # Limit to first 50
    
    details_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
    for record in equipment_records:
        details_data.append([
            record.equipment_name[:20],  # Truncate long names
            record.equipment_type[:15],
            f"{record.flowrate:.1f}",
            f"{record.pressure:.1f}",
            f"{record.temperature:.1f}"
        ])
    
    details_table = Table(details_data, colWidths=[1.8*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    story.append(details_table)
    
    if dataset.total_equipment > 50:
        note = Paragraph(
            f"<i>Note: Showing first 50 of {dataset.total_equipment} equipment records</i>",
            styles['Normal']
        )
        story.append(Spacer(1, 0.1*inch))
        story.append(note)
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    footer = Paragraph(
        f"<i>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
        styles['Normal']
    )
    story.append(footer)
    
    # Build PDF
    doc.build(story)
    
    return filepath
