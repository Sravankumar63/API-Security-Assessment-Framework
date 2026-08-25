from flask import Flask, request, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"

users = {
    "admin": {
        "username": "admin",
        "email": "admin@test.com",
        "role": "user",
    }
}

limiter = Limiter(key_func=get_remote_address, default_limits=["5 per minute"])
limiter.init_app(app)


@app.after_request
def set_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self';"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Server"] = ""
    return response


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = data["user"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired!"}), 401
        except Exception as exc:
            return jsonify({"message": f"Invalid Token : {exc}"}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@app.route("/")
def home():
    return "<h1>API Security Testing Framework</h1><p>Use Postman or security_scanner.py</p>"


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if data and data.get("username") == "admin" and data.get("password") == "admin":
        token = jwt.encode(
            {"user": "admin", "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"token": token})
    return make_response("Invalid Credentials", 401)


@app.route("/data")
@limiter.limit("5 per minute")
@token_required
def get_data(current_user):
    return jsonify({"message": "Sensitive Information", "user": current_user})


@app.route("/users/<int:user_id>")
@token_required
def get_user(current_user, user_id):
    if user_id == 1:
        return jsonify({"user_id": 1, "name": "admin"})
    return jsonify({"message": "Unauthorized Access"}), 403


@app.route("/private")
def private_data():
    return jsonify({"message": "Private Data"}), 401


@app.route("/profile/update", methods=["POST"])
@token_required
def update_profile(current_user):
    data = request.get_json(silent=True) or {}
    if current_user not in users:
        return jsonify({"message": "User not found"}), 404
    for field in ("username", "email"):
        if field in data:
            users[current_user][field] = data[field]
    return jsonify({"message": "Profile Updated Successfully", "profile": users[current_user]})


@app.route("/product/update", methods=["POST"])
@token_required
def update_product(current_user):
    data = request.get_json(silent=True) or {}
    # Price is intentionally server-controlled for the parameter-tampering test.
    if "price" in data:
        return jsonify({"message": "Sensitive parameter cannot be modified"}), 403
    return jsonify({"message": "Product updated"})


if __name__ == "__main__":
    app.run(debug=True)
