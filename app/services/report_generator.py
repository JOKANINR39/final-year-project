import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table
from datetime import datetime


def generate_pdf_report(project_name: str, scores: dict):
    os.makedirs("reports", exist_ok=True)

    file_path = f"reports/{project_name}_{datetime.utcnow().timestamp()}.pdf"

    doc = SimpleDocTemplate(file_path)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"CodeInspector Report - {project_name}", styles['Title']))
    elements.append(Spacer(1, 12))

    data = [
        ["Quality", scores["quality"]],
        ["Security", scores["security"]],
        ["Scalability", scores["scalability"]],
        ["Plagiarism", scores["plagiarism"]],
        ["Final Score", scores["final"]],
    ]

    table = Table(data)
    elements.append(table)

    doc.build(elements)

    return file_path
