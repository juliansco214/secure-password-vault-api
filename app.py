import os
from flask import request
from jwt_utils import jwt_required
from flask import Flask, jsonify
from db import init_db
from auth import auth_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET", "dev-only-secret-change-me")

app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return jsonify({"message": "Secure Password Vault API is running"})

@app.route("/me", methods=["GET"])
@jwt_required
def me():
    return jsonify({
        "user_id": request.user["user_id"],
        "username": request.user["username"]
    }), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)


