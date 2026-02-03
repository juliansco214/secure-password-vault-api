import os
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

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
