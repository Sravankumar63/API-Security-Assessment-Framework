import requests

BASE_URL = "http://127.0.0.1:5000"


def xss_scan(add_result):
    payload = "<script>alert(1)</script>"
    response = requests.get(f"{BASE_URL}/", params={"q": payload})
    if payload in response.text:
        add_result("Cross-Site Scripting (XSS)", "FAIL", "MEDIUM", "Encode output and validate untrusted input.")
    else:
        add_result("Cross-Site Scripting (XSS)", "PASS", "MEDIUM", "Reflected XSS payload was not returned by the API.")
