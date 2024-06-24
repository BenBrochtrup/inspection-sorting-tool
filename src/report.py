import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

# Order of the rows in the final report
order_map = {
    'Helmet': 1,
    'Boots': 2,
    'Hood (1)': 3,
    'Hood (2)': 4,
    'Gloves (1)': 5,
    'Gloves (2)': 6,
    'Coat (1)': 7,
    'Coat (2)': 8,
    'Pants (1)': 9,
    'Pants (2)': 10
}

def sort_final_dataframe(df):
    df_map = df.copy()
    df_map['TypeOrder'] = df_map['Type'].map(order_map)
    df_sorted_map = df_map.sort_values('TypeOrder').drop(columns='TypeOrder')
    return df_sorted_map

def dataframe_to_pdf(dataframe, output_pdf_path, assignee_first, assignee_last, employee_id):
    # Create the output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Columns to include in the table
    columns = ['Type', 'Make', 'Model', 'Year of Equipment Item', 'Equipment Item Serial Number', 'Size', 'Purchase Date']

    dataframe = dataframe[columns]
    dataframe = sort_final_dataframe(dataframe)

    # Create a PDF document
    doc = SimpleDocTemplate(output_pdf_path, pagesize=landscape(letter), topMargin=30)
    elements = []

    # Add title to the PDF
    styles = getSampleStyleSheet()
    custom_title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=16,  # Set the font size smaller than the default
        leading=20,  # Adjust line height if necessary
        spaceAfter=12  # Space after the title
    )
    elements.append(Paragraph('APPLETON FIRE DEPARTMENT', custom_title_style))
    elements.append(Paragraph('PERSONAL PROTECTIVE EQUIPMENT (PPE) INSPECTION', custom_title_style))

    # Define custom styles for the fields
    field_title_style = ParagraphStyle(
        'FieldTitle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        spaceAfter=6,
        leftIndent=6,
    )

    field_value_style = ParagraphStyle(
        'FieldValue',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        spaceAfter=12,
        leftIndent=6,
    )

    # Define the field values (can be dynamically assigned as per your data)
    last_name = str(assignee_last)
    first_name = str(assignee_first)
    employee_id = str(employee_id)

    # Create the fields in two columns
    data = [
        [Paragraph("Last Name:", field_title_style), Paragraph(last_name, field_value_style),
         Paragraph("Insp. Date:", field_title_style), Paragraph("________________________", field_value_style)],
        [Paragraph("First Name:", field_title_style), Paragraph(first_name, field_value_style),
         Paragraph("Inspected By:", field_title_style), Paragraph("________________________", field_value_style)],
        [Paragraph("Employee ID:", field_title_style), Paragraph(employee_id, field_value_style)],
    ]

    # Create a table for the fields
    field_table = Table(data, colWidths=[120, 150, 120, 200])

    # Add style to the field table
    field_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    # Add the field table to the elements
    elements.append(field_table)
    elements.append(Spacer(1, 12))

    # Convert the DataFrame to a list of lists for the Table
    data = [dataframe.columns.tolist()] + dataframe.values.tolist()

    # Create a Table
    table = Table(data)

    # Add style to the Table
    # Add style to the Table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    # Add the Table to the elements
    elements.append(table)

    # Add Comments section
    comments_title = Paragraph("Comments:", field_title_style)
    comments_box = Table([[""]], colWidths=[600], rowHeights=[100])  # Define the box size

    # Add style to the comments box to create an outline
    comments_box.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))

    comments_section = Table([
        [comments_title, comments_box]
    ], colWidths=[80, 600])

    # Add style to left-align the Comments section
    comments_section.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    # Add the comments section to the elements
    elements.append(comments_section)

    # Build the PDF
    doc.build(elements)