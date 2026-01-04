from flask import Blueprint, request, jsonify
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

