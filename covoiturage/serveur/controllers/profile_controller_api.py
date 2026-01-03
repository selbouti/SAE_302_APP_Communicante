from flask import Blueprint, request, jsonify
from models.profile_model import ProfileModel

profile_api = Blueprint("profile_api", __name__, url_prefix="/api")

@profile_api.route("/profile/<int:utilisateur_id>", methods=["GET"])
def get_profile(utilisateur_id):
    profile = ProfileModel.get_profile(utilisateur_id)

    if not profile:
        return jsonify({"success": False, "message": "Profil introuvable"}), 404

    return jsonify({"success": True, "profile": profile})


@profile_api.route("/profile/<int:utilisateur_id>", methods=["POST"])
def update_profile(utilisateur_id):
    data = request.json

    ProfileModel.update_profile(
        utilisateur_id,
        data["nom"],
        data["prenom"],
        data["email"],
        data["telephone"]
    )

    if data.get("voiture"):
        ProfileModel.save_voiture(utilisateur_id, data["voiture"])

    return jsonify({"success": True})
