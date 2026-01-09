from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from models.trajet_model import TrajetModel
from models.voiture_model import VoitureModel
from services.icalendar_parser import ICalendarParser

user_bp = Blueprint("user", __name__, url_prefix="/api")


# =====================================
# REGISTER (avec voiture optionnelle)
# =====================================
@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json or {}

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    nom = data.get("nom", "").strip()
    prenom = data.get("prenom", "").strip()
    telephone = data.get("telephone", "").strip()
    voiture = data.get("voiture")  # optionnel

    if not email or not password or not nom or not prenom:
        return jsonify({"error": "Champs requis manquants"}), 400

    result = UserModel.create(email, password, nom, prenom, telephone)
    if not result:
        return jsonify({"error": "Email déjà utilisé"}), 400

    user_id = result["id"]

    # ✅ Enregistrer la voiture si fournie
    if voiture:
        try:
            VoitureModel.create(user_id, voiture)
        except Exception as e:
            print("Erreur voiture register:", e)

    return jsonify(result), 201


# ===================
# LOGIN
# ===================
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"error": "Email et mot de passe requis"}), 400

    user = UserModel.get_by_email(email, password)
    if not user:
        return jsonify({"error": "Identifiants invalides"}), 401

    return jsonify(user), 200


# ===================
# PROFIL
# ===================
@user_bp.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    user = UserModel.get_by_id(user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    voiture = VoitureModel.get_by_user(user_id)

    return jsonify({
        "user": user,
        "voiture": voiture
    }), 200


# =====================================
# UPLOAD CALENDRIER (première fois)
# =====================================
@user_bp.route("/upload_icalendar/<int:user_id>", methods=["POST"])
def upload_icalendar(user_id):

    if "file" not in request.files:
        return jsonify({"error": "Pas de fichier envoyé"}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "Fichier vide"}), 400

    user = UserModel.get_by_id(user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    try:
        ics_content = file.read()
        events = ICalendarParser.parse_events(ics_content)

        voiture = VoitureModel.get_by_user(user_id)
        mode = "conducteur" if voiture else "passager"
        voiture_id = voiture["id"] if voiture else None

        created = 0
        ids = []

        for e in events:
            dtstart = e.get("dtstart")
            dtend = e.get("dtend")  # <-- ajouter cette ligne

            if not dtstart:
                continue

            summary = (e.get("summary") or "").strip()

            if " - " in summary:
                depart, arrivee = [x.strip() for x in summary.split(" - ", 1)]
            else:
                depart, arrivee = "Départ", "Arrivée"

            trajet_id = TrajetModel.create(
                utilisateur_id=user_id,
                voiture_id=voiture_id,
                depart=depart,
                arrivee=arrivee,
                date_depart=dtstart.strftime("%Y-%m-%d"),
                jour_semaine=dtstart.strftime("%A"),
                heure_depart=dtstart.strftime("%H:%M"),
                heure_retour=(dtend.strftime("%H:%M") if dtend else dtstart.strftime("%H:%M")),
                prix_par_place=5.0,
                mode=mode
            )


            if trajet_id:
                created += 1
                ids.append(trajet_id)

        return jsonify({
            "success": True,
            "mode": mode,
            "trajets_created": created,
            "trajets_ids": ids
        }), 201

    except Exception as e:
        print("UPLOAD ICS ERROR:", e)
        return jsonify({"error": str(e)}), 400


# =====================================
# UPDATE CALENDRIER (reset trajets)
# =====================================
@user_bp.route("/update_icalendar/<int:user_id>", methods=["POST"])
def update_icalendar(user_id):

    if "file" not in request.files:
        return jsonify({"error": "Pas de fichier envoyé"}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "Fichier vide"}), 400

    user = UserModel.get_by_id(user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    try:
        ics_content = file.read()
        events = ICalendarParser.parse_events(ics_content)

        # 🔥 supprimer anciens trajets
        TrajetModel.delete_by_user(user_id)

        voiture = VoitureModel.get_by_user(user_id)
        mode = "conducteur" if voiture else "passager"
        voiture_id = voiture["id"] if voiture else None

        count = 0

        for e in events:
            dtstart = e.get("dtstart")
            if not dtstart:
                continue

            summary = (e.get("summary") or "").strip()

            if " - " in summary:
                depart, arrivee = [x.strip() for x in summary.split(" - ", 1)]
            else:
                depart, arrivee = "Départ", "Arrivée"

            TrajetModel.create(
                utilisateur_id=user_id,
                voiture_id=voiture_id,
                depart=depart,
                arrivee=arrivee,
                date_depart=dtstart.strftime("%Y-%m-%d"),
                jour_semaine=dtstart.strftime("%A"),
                heure_depart=dtstart.strftime("%H:%M"),
                prix_par_place=5.0,
                mode=mode
            )
            count += 1

        return jsonify({"success": True, "trajets": count}), 200

    except Exception as e:
        print("UPDATE ICS ERROR:", e)
        return jsonify({"error": str(e)}), 400

