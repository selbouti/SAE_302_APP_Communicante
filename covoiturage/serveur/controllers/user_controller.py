from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from models.trajet_model import TrajetModel
from models.voiture_model import VoitureModel
from services.icalendar_parser import ICalendarParser

user_bp = Blueprint("user", __name__, url_prefix="/api")


# =====================================
# REGISTER (optional car)
# =====================================
@user_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user.

    Request JSON body:
        - email (str)
        - password (str)
        - nom (str)
        - prenom (str)
        - telephone (str, optional)
        - voiture (dict, optional)

    :return: Created user data or error message
    :rtype: flask.Response
    """
    data = request.json or {}

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    nom = data.get("nom", "").strip()
    prenom = data.get("prenom", "").strip()
    telephone = data.get("telephone", "").strip()
    voiture = data.get("voiture")

    if not email or not password or not nom or not prenom:
        return jsonify({"error": "Missing required fields"}), 400

    result = UserModel.create(email, password, nom, prenom, telephone)
    if not result:
        return jsonify({"error": "Email already used"}), 400

    user_id = result["id"]

    if voiture:
        try:
            VoitureModel.create(user_id, voiture)
        except Exception as e:
            print("Car creation error:", e)

    return jsonify(result), 201


# ===================
# LOGIN
# ===================
@user_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user.

    Request JSON body:
        - email (str)
        - password (str)

    :return: Authenticated user data or error message
    :rtype: flask.Response
    """
    data = request.json or {}

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = UserModel.get_by_email(email, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify(user), 200


# ===================
# PROFILE
# ===================
@user_bp.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    """
    Retrieve a user's profile and associated car.

    :param user_id: User identifier
    :type user_id: int

    :return: User profile data
    :rtype: flask.Response
    """
    user = UserModel.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    voiture = VoitureModel.get_by_user(user_id)

    return jsonify({
        "user": user,
        "voiture": voiture
    }), 200


# =====================================
# UPLOAD CALENDAR (first import)
# =====================================
@user_bp.route("/upload_icalendar/<int:user_id>", methods=["POST"])
def upload_icalendar(user_id):
    """
    Upload an iCalendar file and generate trips.

    :param user_id: User identifier
    :type user_id: int

    :return: Import result and created trips
    :rtype: flask.Response
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "Empty file"}), 400

    user = UserModel.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

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
            dtend = e.get("dtend")

            if not dtstart:
                continue

            summary = (e.get("summary") or "").strip()
            if " - " in summary:
                depart, arrivee = summary.split(" - ", 1)
            else:
                depart, arrivee = "Départ", "Arrivée"

            trajet_id = TrajetModel.create(
                utilisateur_id=user_id,
                voiture_id=voiture_id,
                depart=depart.strip(),
                arrivee=arrivee.strip(),
                date_depart=dtstart.strftime("%Y-%m-%d"),
                jour_semaine=dtstart.strftime("%A"),
                heure_depart=dtstart.strftime("%H:%M"),
                heure_retour=dtend.strftime("%H:%M") if dtend else dtstart.strftime("%H:%M"),
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
        return jsonify({"error": str(e)}), 400


# =====================================
# UPDATE CALENDAR (reset trips)
# =====================================
@user_bp.route("/update_icalendar/<int:user_id>", methods=["POST"])
def update_icalendar(user_id):
    """
    Update calendar by resetting and recreating trips.

    :param user_id: User identifier
    :type user_id: int

    :return: Update result
    :rtype: flask.Response
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "Empty file"}), 400

    user = UserModel.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        ics_content = file.read()
        events = ICalendarParser.parse_events(ics_content)

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
                depart, arrivee = summary.split(" - ", 1)
            else:
                depart, arrivee = "Départ", "Arrivée"

            TrajetModel.create(
                utilisateur_id=user_id,
                voiture_id=voiture_id,
                depart=depart.strip(),
                arrivee=arrivee.strip(),
                date_depart=dtstart.strftime("%Y-%m-%d"),
                jour_semaine=dtstart.strftime("%A"),
                heure_depart=dtstart.strftime("%H:%M"),
                prix_par_place=5.0,
                mode=mode
            )
            count += 1

        return jsonify({"success": True, "trajets": count}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
