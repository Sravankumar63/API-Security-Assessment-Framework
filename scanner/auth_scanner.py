import requests

BASE_URL = "http://127.0.0.1:5000"


def authentication_tests(add_result):
    print("[*] Testing Authentication...")
    response = requests.get(f"{BASE_URL}/data")
    if response.status_code == 401:
        add_result("Authentication", "PASS", "HIGH", "Protected endpoint rejects requests without a token.")
        print("[✔] Authentication protection is enabled.")
    else:
        add_result("Authentication", "FAIL", "HIGH", "Require authentication on protected endpoints.")
        print("[✘] Authentication Misconfiguration")
