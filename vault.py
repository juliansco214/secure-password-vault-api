from flask import Blueprint, request, jsonify
from jwt_utils import jwt_required
from db import get_db_connection
from crypto_utils import encrypt_password
from crypto_utils import decrypt_password


vault_bp = Blueprint("vault", __name__)

@vault_bp.route("/vault", methods=["POST"])
@jwt_required
def add_entry():
    data = request.get_json()

    site = data.get("site")
    username = data.get("username")
    password = data.get("password")

    if not site or not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    encrypted = encrypt_password(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO vault (user_id, site, username, password_encrypted)
        VALUES (?, ?, ?, ?)
        """,
        (request.user["user_id"], site, username, encrypted)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Vault entry added"}), 201

@vault_bp.route("/vault", methods=["GET"])
@jwt_required
def list_entries():
    user_id = request.user["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, site, username, password_encrypted
        FROM vault
        WHERE user_id = ?
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    entries = []
    for row in rows:
        entries.append({
            "id": row["id"],
            "site": row["site"],
            "username": row["username"],
            "password": decrypt_password(row["password_encrypted"])
        })

    return jsonify(entries), 200
