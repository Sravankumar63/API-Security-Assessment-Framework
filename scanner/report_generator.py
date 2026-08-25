import os
from datetime import datetime

REPORT_DIR = "../reports"
os.makedirs(REPORT_DIR, exist_ok=True)


def generate_html_report(results):
    passed = sum(r["status"] == "PASS" for r in results)
    failed = sum(r["status"] == "FAIL" for r in results)
    total = len(results)
    score = int((passed / total) * 100) if total else 0
    risk = "LOW" if failed == 0 else "MEDIUM" if failed <= 2 else "HIGH"

    rows = "".join(
        f"<tr><td>{r['test']}</td><td>{r['status']}</td><td>{r['severity']}</td><td>{r['recommendation']}</td></tr>"
        for r in results
    )
    html = f"""<!doctype html><html><head><meta charset='utf-8'><title>API Security Report</title>
    <style>body{{font-family:Arial;background:#f5f5f5;padding:30px}}.card{{background:white;padding:20px;margin-bottom:20px}}
    table{{width:100%;border-collapse:collapse}}th,td{{padding:8px;border:1px solid #ddd}}th{{background:#003366;color:white}}</style></head>
    <body><div class='card'><h1>API SECURITY ASSESSMENT REPORT</h1>
    <p><b>Target:</b> http://127.0.0.1:5000</p><p><b>Date:</b> {datetime.now()}</p>
    <p><b>Total Tests:</b> {total} &nbsp; <b>Passed:</b> {passed} &nbsp; <b>Failed:</b> {failed}</p>
    <p><b>Security Score:</b> {score}/100 &nbsp; <b>Overall Risk:</b> {risk}</p></div>
    <div class='card'><h2>Detailed Findings</h2><table><tr><th>Test</th><th>Status</th><th>Severity</th><th>Recommendation</th></tr>{rows}</table></div></body></html>"""
    path = os.path.join(REPORT_DIR, "report.html")
    with open(path, "w", encoding="utf-8") as file:
        file.write(html)
    print(f"[✔] Professional HTML Report Generated: {path}")
    return path
