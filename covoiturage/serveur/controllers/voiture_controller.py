from flask import Blueprint, request, jsonify
from models.voiture_model import VoitureModel

voiture_bp = Blueprint("voiture", __name__, url_prefix="/api/voiture")


# ===============================
# GET voiture utilisateur
# ===============================
@voiture_bp.route("/<int:user_id>", methods=["GET"])
def get_voiture(user_id):
    voiture = VoitureModel.get_by_user(user_id)
    return jsonify(voiture), 200


# ===============================
# CREATE ou UPDATE
# ===============================
@voiture_bp.route("/<int:user_id>", methods=["POST", "PUT"])
def save_voiture(user_id):
    data = request.json or {}

    required = [
        "marque",
        "modele",
        "chevaux_fiscaux",
        "motorisation",
        "taux_co2",
        "places_max"
    ]

    if not all(k in data for k in required):
        return jsonify({"error": "Champs voiture incomplets"}), 400

    # 🧠 une seule voiture par user → delete + insert
    VoitureModel.delete_by_user(user_id)
    VoitureModel.create(user_id, data)

    return jsonify({"success": True}), 200


# ===============================
# DELETE
# ===============================
@voiture_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_voiture(user_id):
    VoitureModel.delete_by_user(user_id)
    return jsonify({"success": True}), 200
