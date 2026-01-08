from flask import Blueprint, request, jsonify
from models.trajet_model import TrajetModel

trajet_bp = Blueprint('trajet', __name__, url_prefix='/api')

@trajet_bp.route('/mes_trajets/<int:user_id>', methods=['GET'])
def mes_trajets(user_id):
    trajets = TrajetModel.get_by_user(user_id)
    return jsonify(trajets), 200

@trajet_bp.route('/trajets', methods=['POST'])
def creer_trajet():
    data = request.json
    trajet_id = TrajetModel.create(
        data['utilisateur_id'],
        data['voiture_id'],
        data['depart'],
        data['arrivee'],
        data['date_depart'],
        data['jour_semaine'],
        data['heure_depart'],
        data.get('heure_retour'),
        data['prix_par_place'],
        data['mode']
    )
    return jsonify({'id': trajet_id}), 201

@trajet_bp.route('/trajets/<int:trajet_id>', methods=['DELETE'])
def supprimer_trajet(trajet_id):
    TrajetModel.delete(trajet_id)
    return jsonify({'success': True}), 200

@trajet_bp.route('/trajets/<int:trajet_id>/places', methods=['GET'])
def get_places_disponibles(trajet_id):
    places = TrajetModel.get_places_disponibles(trajet_id)
    return jsonify({'places_disponibles': places}), 200

@trajet_bp.route('/trajets/<int:trajet_id>/mode', methods=['PUT'])
def changer_mode(trajet_id):
    data = request.json or {}
    mode = data.get('mode')
    if mode not in ('conducteur', 'passager'):
        return jsonify({'error': 'Mode invalide'}), 400
    
    TrajetModel.update_mode(trajet_id, mode)
    return jsonify({'success': True, 'mode': mode}), 200

# ============= controllers/matching_controller.py (MODIFIED) =============
