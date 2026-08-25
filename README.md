# API Security Assessment Framework

A Flask-based REST API security assessment project that combines a custom Python security scanner with manual validation using Postman, OWASP ZAP, and Burp Suite.

## Project Overview

The framework evaluates common API security controls and vulnerabilities, including:

- JWT authentication and authorization
- Broken Object Level Authorization (BOLA/IDOR)
- SQL Injection
- Cross-Site Scripting (XSS)
- Parameter Tampering
- Mass Assignment
- Rate Limiting
- API Key validation
- HTTP Security Headers
- OWASP ZAP Spider and Active Scan integration

The framework also generates HTML and PDF security assessment reports.

## Project Structure

```text
API-Security-Assessment-Framework/
├── api_server/
├── scanner/
├── reports/
├── docs/
│   ├── PROJECT_DOCUMENTATION.md
│   ├── README.md
│   └── images/
├── requirements.txt
└── README.md
```

## Requirements

- Windows 11 or compatible Windows environment
- Python 3.13
- Postman
- OWASP ZAP 2.17.0
- Burp Suite Community Edition

## Setup

```bash
cd C:\api-security-framework
py -3.13 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run the API

```bash
cd api_server
python app.py
```

The local API is available at:

```text
http://127.0.0.1:5000
```

## Run the Security Scanner

In a second terminal:

```bash
cd C:\api-security-framework
venv\Scripts\activate
cd scanner
python security_scanner.py
```

## Testing Workflow

1. Start the Flask API.
2. Execute the custom security scanner.
3. Perform manual API validation in Postman.
4. Run OWASP ZAP Spider and Active Scan.
5. Use Burp Suite to intercept and inspect API requests.
6. Review the generated HTML and PDF reports.

## Screenshots & Visual Evidence

The final project report contains visual evidence for the implementation and testing process. The repository's `docs/images/` section is reserved for the extracted screenshots and diagrams, including:

- Python and virtual-environment setup
- Flask API execution
- Custom security scanner execution and results
- Project architecture and scanner workflow
- Postman API testing
- OWASP ZAP scanning, Spider results and alerts
- Burp Suite request interception and analysis
- Generated report evidence

## Security Assessment Result

The documented assessment executed 19 tests, with 15 passing and 4 failing. The recorded security score was 78/100 with Grade B and overall risk rated High. OWASP ZAP also reported configuration-related findings involving Content Security Policy and Server header information disclosure.

## Reports

The framework produces:

- HTML security report
- PDF security report
- OWASP ZAP HTML report

## Project Classification

Intermediate-level API security assessment project completed as part of the Labmentix Cybersecurity Training Program.

## Author

Sravan Kumar Mandeti

## Disclaimer

This project is intended for authorized security testing in controlled environments. Do not use the scanner or testing tools against systems without permission.
