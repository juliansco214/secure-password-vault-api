from functools import wraps
from flask import request, jsonify, current_app
import jwt

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header:
            return jsonify({"error": "Missing Authorization header"}), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Invalid Authorization header format"}), 401

        token = auth_header.split(" ", 1)[1].strip()
        if not token:
            return jsonify({"error": "Missing token"}), 401

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        # Attach payload to request context for handlers to use
        request.user = payload
        return fn(*args, **kwargs)

    return wrapper
