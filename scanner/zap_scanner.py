import requests

ZAP_API = "http://127.0.0.1:8080"
TARGET = "http://127.0.0.1:5000"


def run_zap_scan():
    alerts = []
    try:
        # Spider
        requests.get(f"{ZAP_API}/JSON/spider/action/scan/", params={"url": TARGET, "recurse": "true"}, timeout=5)
        # Active scan
        requests.get(f"{ZAP_API}/JSON/ascan/action/scan/", params={"url": TARGET, "recurse": "true"}, timeout=5)
        response = requests.get(f"{ZAP_API}/JSON/core/view/alerts/", params={"baseurl": TARGET}, timeout=5)
        if response.ok:
            alerts = response.json().get("alerts", [])
    except requests.RequestException:
        print("[!] OWASP ZAP is not reachable. Continuing without ZAP alerts.")
    return alerts
