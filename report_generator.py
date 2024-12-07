import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt

def generate_report(data, output_file="Forensic_Report.pdf"):
    threats = data["Threats"]
    file_name = data["File Name"]

    # Generate bar graph
    threat_names = [t.get("Threat", "Unknown") for t in threats]
    severities = [t.get("Severity", 0) for t in threats]
    plt.figure(figsize=(8, 5))
    plt.bar(threat_names, severities, color='skyblue')
    plt.title("Threat Severity Analysis")
    plt.xlabel("Threats")
    plt.ylabel("Severity")
    plt.xticks(rotation=45)
    plt.tight_layout()
    graph_path = "threat_graph.png"
    plt.savefig(graph_path)
    plt.close()

    # Generate PDF report
    c = canvas.Canvas(output_file, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Digital Forensics Analysis Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"File Analyzed: {file_name}")

    # Add image with dynamic dimensions
    img = ImageReader(graph_path)
    img_width, img_height = img.getSize()
    aspect_ratio = img_width / img_height
    c.drawImage(graph_path, 50, 400, width=500, height=500 / aspect_ratio)

    # Add threat table
    data_table = [["Threat", "Severity", "Mitigation"]]
    for t in threats:
        data_table.append([
            t.get("Threat", "Unknown"),
            t.get("Severity", "N/A"),
            t.get("Mitigation", "N/A")
        ])

    table = Table(data_table)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))
    table.wrapOn(c, 500, 200)
    table_height = len(data_table) * 20  # Approximate height per row
    table.drawOn(c, 50, 400 - table_height - 20)

    c.save()
    os.remove(graph_path)
    print(f"Report saved to {output_file}")
