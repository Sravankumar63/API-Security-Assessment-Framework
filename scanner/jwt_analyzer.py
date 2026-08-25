import base64
import json


def analyze_jwt(token):
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return "FAIL", "HIGH", "JWT must contain three segments."
        payload = parts[1] + "=" * (-len(parts[1]) % 4)
        claims = json.loads(base64.urlsafe_b64decode(payload).decode())
        if "exp" not in claims:
            return "FAIL", "HIGH", "JWT should contain an expiration claim."
        return "PASS", "HIGH", "JWT contains an expiration claim."
    except Exception:
        return "FAIL", "HIGH", "Unable to parse JWT safely."
