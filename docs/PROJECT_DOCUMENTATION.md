# Project Documentation

## 1. Abstract

The API Security Assessment Framework evaluates RESTful APIs using automated and manual security testing. It is built with Python and Flask and includes JWT authentication, authorization, rate limiting, and HTTP security headers. A custom Python scanner checks common API security controls and vulnerabilities, while Postman, OWASP ZAP, and Burp Suite support manual validation. HTML and PDF reports summarize findings, scores, and recommendations.

## 2. Objectives

- Develop a Flask REST API with JWT-based authentication and authorization.
- Implement an automated Python API security scanner.
- Test BOLA/IDOR, SQL Injection, XSS, Parameter Tampering, Mass Assignment, API Key Exposure, Rate Limiting, and Security Headers.
- Perform manual API testing with Postman.
- Assess the API with OWASP ZAP and inspect HTTP traffic with Burp Suite.
- Generate HTML and PDF security reports.

## 3. Environment

- Windows 11 (24H2)
- Python 3.13
- Flask
- Requests
- PyJWT
- Flask-Limiter
- Flasgger
- Postman
- OWASP ZAP 2.17.0
- Burp Suite Community Edition
- Visual Studio Code

## 4. Methodology

1. Verify the Python environment.
2. Create and activate the virtual environment.
3. Install dependencies from `requirements.txt`.
4. Start the Flask API with `python app.py`.
5. Run `python scanner/security_scanner.py` from a second terminal.
6. Execute authentication, authorization, and vulnerability checks.
7. Validate API behavior manually with Postman.
8. Run OWASP ZAP Spider/Active Scan and review alerts.
9. Intercept and inspect API requests with Burp Suite.
10. Generate HTML and PDF reports.

## 5. Documented Assessment Results

The project report records 19 tests executed, 15 passed, 4 failed, a security score of 78/100, Grade B, and overall risk High. It also records two OWASP ZAP configuration-related findings: Content Security Policy and Server header disclosure.

## 6. Learning Outcomes

The project provided practical experience in secure Flask REST API development, JWT authentication, automated API security testing, OWASP ZAP assessment, Postman testing, Burp Suite request analysis, security controls, and security report generation.

## 7. Future Scope

- CI/CD security testing
- Docker deployment
- OAuth 2.0 and MFA
- SQLMap integration
- Complete OWASP API Security Top 10 coverage
- Cloud-based assessment
- Real-time monitoring and alerting

## 8. Authorized Testing

Use the framework only against APIs and systems for which you have explicit authorization.
