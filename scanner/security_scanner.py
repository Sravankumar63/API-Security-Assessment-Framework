import time
import requests
from report_generator import generate_html_report
from pdf_report import generate_pdf_report
from jwt_analyzer import analyze_jwt
from zap_scanner import run_zap_scan
from zap_parser import parse_zap_alerts
from parameter_tampering import parameter_tampering
from idor_scanner import advanced_idor
from auth_scanner import authentication_tests
from xss_scanner import xss_scan
from sql_injection import sql_injection_scan

BASE_URL = "http://127.0.0.1:5000"
results = []
scan_start = time.time()


def add_result(test_name, status, severity, recommendation):
    results.append({"test": test_name, "status": status, "severity": severity, "recommendation": recommendation})


def check_bola(token):
    advanced_idor(token, add_result)


def check_rate_limiting(token):
    print("[*] Testing Rate Limiting...")
    hit_limit = False
    for _ in range(10):
        response = requests.get(f"{BASE_URL}/data", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 429:
            hit_limit = True
            break
        time.sleep(0.1)
    add_result("Rate Limiting", "PASS" if hit_limit else "FAIL", "MEDIUM", "Rate limiting should return HTTP 429 after the configured limit.")


def check_api_key_exposure():
    response = requests.get(f"{BASE_URL}/private", headers={"x-api-key": "SECRET123"})
    add_result("API Key Exposure", "PASS" if response.status_code != 200 else "FAIL", "HIGH", "Do not expose or hardcode API keys.")


def check_security_headers():
    headers = requests.get(BASE_URL).headers
    expected = {
        "Content-Security-Policy": "Configure a restrictive CSP.",
        "X-Frame-Options": "Add clickjacking protection.",
        "X-Content-Type-Options": "Prevent MIME sniffing.",
    }
    for header, recommendation in expected.items():
        add_result(f"Security Header: {header}", "PASS" if header in headers else "FAIL", "MEDIUM", recommendation)


def check_mass_assignment(token):
    payload = {"username": "admin", "email": "admin@test.com", "role": "admin", "isAdmin": True}
    response = requests.post(f"{BASE_URL}/profile/update", json=payload, headers={"Authorization": f"Bearer {token}"})
    profile = response.json().get("profile", {}) if response.headers.get("content-type", "").startswith("application/json") else {}
    vulnerable = profile.get("role") == "admin" and profile.get("isAdmin") is True
    add_result("Mass Assignment", "FAIL" if vulnerable else "PASS", "HIGH", "Use an allow-list for writable profile fields.")


def get_token():
    response = requests.post(f"{BASE_URL}/login", json={"username": "admin", "password": "admin"})
    token = response.json().get("token") if response.ok else None
    if token:
        add_result("JWT Authentication", "PASS", "HIGH", "JWT authentication is functioning correctly.")
        status, severity, recommendation = analyze_jwt(token)
        add_result("JWT Analyzer", status, severity, recommendation)
    else:
        add_result("JWT Authentication", "FAIL", "HIGH", "Verify login and token generation.")
    return token


def wait_for_api():
    for _ in range(30):
        try:
            response = requests.get(BASE_URL, timeout=1)
            if response.status_code < 500:
                add_result("API Availability", "PASS", "INFO", "API server is reachable.")
                return
        except requests.RequestException:
            pass
        time.sleep(1)
    raise SystemExit("API is not responding. Start app.py first.")


def print_summary():
    passed = sum(r["status"] == "PASS" for r in results)
    failed = sum(r["status"] == "FAIL" for r in results)
    total = len(results)
    score = int((passed / total) * 100) if total else 0
    grade = "A+" if score >= 90 else "A" if score >= 80 else "B" if score >= 70 else "C" if score >= 60 else "D"
    risk = "LOW" if failed == 0 else "MEDIUM" if failed <= 2 else "HIGH"
    print("\n" + "=" * 70)
    print("                 API SECURITY SCAN SUMMARY")
    print("=" * 70)
    print(f"Target           : {BASE_URL}")
    print(f"Tests Executed   : {total}")
    print(f"Passed           : {passed}")
    print(f"Failed           : {failed}")
    print(f"Overall Risk     : {risk}")
    print(f"Security Score   : {score}/100")
    print(f"Security Grade   : {grade}")
    print(f"Scan Time        : {time.time() - scan_start:.2f} seconds")
    print("=" * 70)
    for result in results:
        print(f"{result['status']:4} | {result['test']} | {result['severity']}")


if __name__ == "__main__":
    wait_for_api()
    authentication_tests(add_result)
    sql_injection_scan(add_result)
    xss_scan(add_result)
    token = get_token()
    if token:
        check_bola(token)
        check_rate_limiting(token)
        check_mass_assignment(token)
        parameter_tampering(token, add_result)
    check_api_key_exposure()
    check_security_headers()

    zap_alerts = run_zap_scan()
    print(f"[✔] ZAP Alerts Found : {len(zap_alerts)}")
    parse_zap_alerts(zap_alerts, add_result)

    print_summary()
    generate_html_report(results)
    generate_pdf_report(results)
