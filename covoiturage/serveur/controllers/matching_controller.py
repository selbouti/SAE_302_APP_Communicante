from flask import Blueprint, request, jsonify
from datetime import datetime
from models.trajet_model import TrajetModel

matching_bp = Blueprint("matching", __name__, url_prefix="/api")

# ==================================================
# MATCHING SIMPLE (à partir d’un trajet existant)
# ==================================================
@matching_bp.route("/matching/<int:user_id>", methods=["GET"])
def get_matching(user_id):
    trajet_id = request.args.get("trajet_id", type=int)

    if not trajet_id:
        return jsonify({"error": "trajet_id manquant"}), 400

    trajet = TrajetModel.get_trajet_by_id(trajet_id, user_id)
    if not trajet:
        return jsonify({"error": "Aucun trajet trouvé"}), 404

    # 🔁 conducteur ↔ passager
    mode_recherche = (
        "conducteur" if trajet["mode"] == "passager" else "passager"
    )

    trajets_matching = TrajetModel.search_matching_avance(
        depart=trajet["depart"],
        arrivee=trajet["arrivee"],
        date_depart=trajet["date_depart"],
        mode_recherche=mode_recherche,
        user_id=user_id
    )

    return jsonify({
        "mon_trajet": trajet,
        "trajets_compatibles": trajets_matching,
        "mode_recherche": (
            "réservations" if trajet["mode"] == "passager"
            else "invitations"
        )
    }), 200


# ==================================================
# MATCHING AVEC MARGES HORAIRES
# ==================================================
@matching_bp.route("/matching_marges/<int:user_id>", methods=["POST"])
def matching_marges(user_id):
    data = request.json or {}

    depart = (data.get("depart") or "").strip()
    arrivee = (data.get("arrivee") or "").strip()
    date = (data.get("date") or "").strip()
    heure_aller = (data.get("heure_aller") or "").strip()
    heure_retour = (data.get("heure_retour") or "").strip()

    if not all([depart, arrivee, date, heure_aller, heure_retour]):
        return jsonify({"error": "Champs manquants"}), 400

    try:
        marge_aller = int(data.get("marge_aller", 0))
        marge_retour = int(data.get("marge_retour", 0))
    except ValueError:
        return jsonify({"error": "Marges invalides"}), 400

    try:
        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(heure_aller, "%H:%M")
        datetime.strptime(heure_retour, "%H:%M")
    except ValueError:
        return jsonify({"error": "Date ou heure invalide"}), 400

    # 🔁 conducteur ↔ passager (logique identique au matching simple)
    mode_utilisateur = data.get("mode")  # "conducteur" ou "passager"
    if mode_utilisateur not in ["conducteur", "passager"]:
        return jsonify({"error": "Mode invalide"}), 400

    mode_recherche = (
        "conducteur" if mode_utilisateur == "passager" else "passager"
    )

    trajets = TrajetModel.search_matching_avance(
        depart=depart,
        arrivee=arrivee,
        date_depart=date,
        mode_recherche=mode_recherche,
        user_id=user_id,
        heure_aller=heure_aller,
        marge_aller=marge_aller,
        heure_retour=heure_retour,
        marge_retour=marge_retour
    )

    return jsonify({
        "mode_recherche": mode_recherche,
        "trajets_compatibles": trajets
    }), 200
