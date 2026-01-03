# ============= controllers/reservation_controller.py =============
from flask import Blueprint, request, jsonify
from models.reservation_model import ReservationModel

reservation_bp = Blueprint('reservation', __name__, url_prefix='/api')

@reservation_bp.route('/reservations', methods=['POST'])
def creer_reservation():
    """Créer une réservation"""
    data = request.json
    try:
        res_id = ReservationModel.create(data['trajet_id'], data['passager_id'], 
                                         data.get('places_reservees', 1))
        if res_id:
            return jsonify({'id': res_id, 'statut': 'en_attente'}), 201
        else:
            return jsonify({'error': 'Places insuffisantes'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@reservation_bp.route('/reservations/recues/<int:conducteur_id>', methods=['GET'])
def reservations_recues(conducteur_id):
    """Réservations reçues sur mes trajets (je suis conducteur)"""
    reservations = ReservationModel.get_by_trajet(conducteur_id)
    return jsonify(reservations), 200

@reservation_bp.route('/reservations/faites/<int:passager_id>', methods=['GET'])
def reservations_faites(passager_id):
    """Réservations que j'ai faites (je suis passager)"""
    reservations = ReservationModel.get_by_passager(passager_id)
    return jsonify(reservations), 200

@reservation_bp.route('/reservations/<int:reservation_id>/accepter', methods=['PUT'])
def accepter_reservation(reservation_id):
    """Accepter une réservation"""
    ReservationModel.accepter(reservation_id)
    return jsonify({'success': True}), 200

@reservation_bp.route('/reservations/<int:reservation_id>/refuser', methods=['PUT'])
def refuser_reservation(reservation_id):
    """Refuser une réservation"""
    ReservationModel.refuser(reservation_id)
    return jsonify({'success': True}), 200

@reservation_bp.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def annuler_reservation(reservation_id):
    """Annuler une réservation"""
    ReservationModel.annuler(reservation_id)
    return jsonify({'success': True}), 200