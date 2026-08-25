def parse_zap_alerts(alerts, add_result):
    for alert in alerts:
        name = alert.get("alert") or alert.get("name") or "ZAP Alert"
        risk = (alert.get("riskdesc") or alert.get("risk") or "Informational").split(" ", 1)[0].upper()
        if risk not in {"HIGH", "MEDIUM", "LOW", "INFO", "INFORMATIONAL"}:
            risk = "LOW"
        add_result(
            f"ZAP : {name}",
            "FAIL",
            risk,
            alert.get("solution") or "Review the OWASP ZAP finding and apply the recommended configuration.",
        )
