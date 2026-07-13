from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch     
from io import BytesIO

def notes_pdf_gen(notes):
    buffer= BytesIO()
    doc= SimpleDocTemplate(buffer,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,)
    styles = getSampleStyleSheet()
    notes= notes.split("\n")
    story=[]
    for line in notes:
        if not line.strip():
            continue
        if line.startswith("*"):
            style= styles["Title"]
            line=line.removeprefix("*")
            story.append(Paragraph(line, style))
            story.append(Spacer(1, 0.30 * inch))      # <-- Space after title
        elif line.startswith("##"):
            style= styles["Heading2"]
            story.append(Spacer(1, 0.18 * inch))   
            line=line.removeprefix("##")
            story.append(Paragraph(line, style))
            story.append(Spacer(1, 0.18 * inch))      # <-- Space after heading

        elif line.startswith("#"):
            story.append(Spacer(1, 0.22 * inch)) 
            style= styles["Heading1"]
            line=line.removeprefix("#")
            story.append(Paragraph(line, style))
            story.append(Spacer(1, 0.22 * inch))      # <-- Space after heading
    
        elif line.startswith("-"):
            style= styles["BodyText"]
            line= "• " + line.removeprefix("-").strip()
            story.append(Paragraph(line, style))
            story.append(Spacer(1, 0.08 * inch))      # <-- Small gap between bullets
            
        else:
            style=styles["BodyText"]
            story.append(Paragraph(line, style))
            story.append(Spacer(1, 0.12 * inch))      # <-- Gap after normal paragraph
    doc.build(story)
    buffer.seek(0)
    return buffer

    

    
    