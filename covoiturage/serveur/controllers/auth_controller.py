from flask import Blueprint, request, jsonify
from models.user_model import UserModel

auth_bp = Blueprint("auth", __name__)
user_model = UserModel()

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = user_model.authenticate(
        data.get("login"),
        data.get("password")
    )

    if not user:
        return jsonify({"error": "Identifiants invalides"}), 401

    return jsonify(user), 200
