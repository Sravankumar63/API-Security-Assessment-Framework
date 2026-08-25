import requests

BASE_URL = "http://127.0.0.1:5000"


def parameter_tampering(token, add_result):
    response = requests.post(
        f"{BASE_URL}/product/update",
        json={"price": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code == 403:
        add_result("Parameter Tampering", "PASS", "HIGH", "Server validates sensitive parameters.")
    else:
        add_result("Parameter Tampering", "FAIL", "HIGH", "Validate sensitive parameters server-side.")
