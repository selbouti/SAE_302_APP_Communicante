from flask import Blueprint, request, jsonify
from models.voiture_model import VoitureModel

voiture_bp = Blueprint("voiture", __name__, url_prefix="/api/voiture")


# ===============================
# GET user's car
# ===============================
@voiture_bp.route("/<int:user_id>", methods=["GET"])
def get_voiture(user_id):
    """
    Retrieve the car associated with a given user.

    :param user_id: User identifier
    :type user_id: int
    :return: JSON representation of the user's car
    :rtype: flask.Response
    """
    voiture = VoitureModel.get_by_user(user_id)
    return jsonify(voiture), 200


# ===============================
# CREATE or UPDATE car
# ===============================
@voiture_bp.route("/<int:user_id>", methods=["POST", "PUT"])
def save_voiture(user_id):
    """
    Create or update the car associated with a user.

    Only one car is allowed per user. If a car already exists,
    it is removed before creating the new one.

    Expected JSON payload:
        - marque
        - modele
        - chevaux_fiscaux
        - motorisation
        - taux_co2
        - places_max

    :param user_id: User identifier
    :type user_id: int
    :return: Success or error response
    :rtype: flask.Response
    """
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

    # One car per user: delete then insert
    VoitureModel.delete_by_user(user_id)
    VoitureModel.create(user_id, data)

    return jsonify({"success": True}), 200


# ===============================
# DELETE car
# ===============================
@voiture_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_voiture(user_id):
    """
    Delete the car associated with a user.

    :param user_id: User identifier
    :type user_id: int
    :return: Success response
    :rtype: flask.Response
    """
    VoitureModel.delete_by_user(user_id)
    return jsonify({"success": True}), 200
