import requests

BASE_URL = "http://127.0.0.1:5000"


def advanced_idor(token, add_result):
    response = requests.get(f"{BASE_URL}/users/2", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 403:
        add_result("Advanced IDOR (BOLA)", "PASS", "HIGH", "Unauthorized object access is blocked.")
    else:
        add_result("Advanced IDOR (BOLA)", "FAIL", "HIGH", "Enforce object-level authorization.")
