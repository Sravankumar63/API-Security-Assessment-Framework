import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

REPORT_DIR = "../reports"
os.makedirs(REPORT_DIR, exist_ok=True)


def generate_pdf_report(results):
    path = os.path.join(REPORT_DIR, "report.pdf")
    passed = sum(r["status"] == "PASS" for r in results)
    failed = sum(r["status"] == "FAIL" for r in results)
    total = len(results)
    score = int((passed / total) * 100) if total else 0
    risk = "LOW" if failed == 0 else "MEDIUM" if failed <= 2 else "HIGH"

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(path, pagesize=A4)
    story = [Paragraph("API SECURITY ASSESSMENT REPORT", styles["Title"]), Spacer(1, 12)]
    story += [Paragraph("Target: http://127.0.0.1:5000", styles["Normal"]),
              Paragraph(f"Total Tests: {total} | Passed: {passed} | Failed: {failed}", styles["Normal"]),
              Paragraph(f"Security Score: {score}/100 | Overall Risk: {risk}", styles["Normal"]), Spacer(1, 16)]

    data = [["Test", "Status", "Severity", "Recommendation"]]
    data += [[r["test"], r["status"], r["severity"], r["recommendation"]] for r in results]
    table = Table(data, repeatRows=1, colWidths=[115, 55, 55, 285])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table)
    doc.build(story)
    print(f"[✔] Professional PDF Report Generated: {path}")
    return path
