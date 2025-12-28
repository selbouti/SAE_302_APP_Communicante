from flask import Blueprint, request, jsonify
from models.trajet_model import TrajetModel

matching_bp = Blueprint('matching', __name__, url_prefix='/api')

@matching_bp.route('/matching/<int:user_id>', methods=['GET'])
def get_matching(user_id):
    trajet = TrajetModel.get_first_trajet(user_id)
    
    if not trajet:
        return jsonify({'error': 'Aucun trajet trouvé'}), 404
    
    mode_inverse = 'conducteur' if trajet['mode'] == 'passager' else 'passager'
    
    trajets_matching = TrajetModel.search_matching(
        trajet['depart'],
        trajet['arrivee'],
        trajet['date_depart'],
        mode_inverse
    )
    
    return jsonify({
        'mon_trajet': dict(trajet),
        'trajets_compatibles': trajets_matching,
        'mode_recherche': 'réservations' if trajet['mode'] == 'passager' else 'invitations'
    }), 200
