# reports/utils.py
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from courses.models import Grade

def generate_transcript(student):
    # Create a file-like buffer
    buffer = BytesIO()
    
    # Create the PDF object
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # center
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12
    )
    
    # Title
    elements.append(Paragraph("OFFICIAL ACADEMIC TRANSCRIPT", title_style))
    elements.append(Paragraph(f"Student: {student.user.get_full_name()}", styles['Normal']))
    elements.append(Paragraph(f"ID: {student.student_id}", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Table data
    data = [['Course Code', 'Course Name', 'Credits', 'Grade', 'Points']]
    total_points = 0
    total_credits = 0
    
    # Get all grades for this student
    grades = Grade.objects.filter(enrollment__student=student)
    
    grade_points = {'A': 4.0, 'B+': 3.5, 'B': 3.0, 'C+': 2.5, 'C': 2.0, 'D': 1.0, 'F': 0.0}
    
    for grade in grades:
        course = grade.enrollment.course
        letter = grade.letter_grade
        points = grade_points.get(letter, 0)
        credits = course.credits
        
        data.append([
            course.code,
            course.name,
            str(credits),
            letter,
            f"{points:.1f}"
        ])
        
        total_points += points * credits
        total_credits += credits
    
    # Calculate GPA
    gpa = total_points / total_credits if total_credits > 0 else 0.0
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f"Total Credits: {total_credits}", heading_style))
    elements.append(Paragraph(f"Cumulative GPA: {gpa:.2f}", heading_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF data
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf

