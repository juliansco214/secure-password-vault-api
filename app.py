from flask import Flask, jsonify
from db import init_db
from auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return jsonify({"message": "Secure Password Vault API is running"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
