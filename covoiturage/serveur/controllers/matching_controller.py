from flask import Blueprint, request, jsonify
from datetime import datetime
from models.trajet_model import TrajetModel

matching_bp = Blueprint('matching', __name__, url_prefix='/api')

from flask import request, jsonify

@matching_bp.route('/matching/<int:user_id>', methods=['GET'])
def get_matching(user_id):
    trajet_id = request.args.get('trajet_id', type=int)

    if not trajet_id:
        return jsonify({'error': 'trajet_id manquant'}), 400

    trajet = TrajetModel.get_trajet_by_id(trajet_id, user_id)

    if not trajet:
        return jsonify({'error': 'Aucun trajet trouvé'}), 404

    mode_inverse = 'conducteur' if trajet['mode'] == 'passager' else 'passager'

    trajets_matching = TrajetModel.search_matching(
        trajet['depart'],
        trajet['arrivee'],
        trajet['date_depart'],
        mode_inverse,
        user_id   # ✅ OBLIGATOIRE
    )

    return jsonify({
        'mon_trajet': trajet,
        'trajets_compatibles': trajets_matching,
        'mode_recherche': (
            'réservations' if trajet['mode'] == 'passager'
            else 'invitations'
        )
    }), 200


@matching_bp.route('/matching_marges/<int:user_id>', methods=['POST'])
def matching_marges(user_id):
    data = request.json or {}
    depart = (data.get("depart") or "").strip()
    arrivee = (data.get("arrivee") or "").strip()
    date = (data.get("date") or "").strip()
    heure_aller = (data.get("heure_aller") or "").strip()
    heure_retour = (data.get("heure_retour") or "").strip()

    if not all([depart, arrivee, date, heure_aller, heure_retour]):
        return jsonify({'error': 'Champs manquants'}), 400

    try:
        marge_aller = int(data.get("marge_aller", 0))
        marge_retour = int(data.get("marge_retour", 0))
    except (TypeError, ValueError):
        return jsonify({'error': 'Marges invalides'}), 400

    try:
        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(heure_aller, "%H:%M")
        datetime.strptime(heure_retour, "%H:%M")
    except ValueError:
        return jsonify({'error': 'Date ou heure invalide'}), 400

    conducteurs = TrajetModel.search_conducteurs_marges(
        depart,
        arrivee,
        date,
        heure_aller,
        marge_aller,
        heure_retour,
        marge_retour,
        user_id
    )

    if not conducteurs:
        return jsonify({
            "conducteurs": [],
            "conducteur_moins_trajets": None
        }), 200

    conducteurs = sorted(conducteurs, key=lambda c: c.get("nb_trajets", 0))
    conducteur_min = conducteurs[0]

    return jsonify({
        "conducteurs": conducteurs,
        "conducteur_moins_trajets": conducteur_min
    }), 200
