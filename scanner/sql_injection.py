import requests

BASE_URL = "http://127.0.0.1:5000"


def sql_injection_scan(add_result):
    payloads = ["' OR '1'='1", "1' UNION SELECT NULL--"]
    vulnerable = False
    for payload in payloads:
        response = requests.post(f"{BASE_URL}/login", json={"username": payload, "password": payload})
        if response.status_code == 200 and "token" in response.text:
            vulnerable = True
            break
    if vulnerable:
        add_result("SQL Injection", "FAIL", "HIGH", "Use parameterized queries and strict input validation.")
    else:
        add_result("SQL Injection", "PASS", "HIGH", "No SQL injection response was observed during the test.")
