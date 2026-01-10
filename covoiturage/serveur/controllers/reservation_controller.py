# ============= controllers/reservation_controller.py =============
from flask import Blueprint, request, jsonify
from models.reservation_model import ReservationModel

reservation_bp = Blueprint('reservation', __name__, url_prefix='/api')

@reservation_bp.route('/reservations', methods=['POST'])
def creer_reservation():
    """
    Create a new reservation for a trip.

    Request Body (JSON):
        - trajet_id (int): The ID of the trip.
        - passager_id (int): The ID of the passenger making the reservation.
        - places_reservees (int, optional): The number of seats reserved (default is 1).

    Returns:
        - 201 Created: A JSON object containing the reservation ID and its status.
        - 400 Bad Request: A JSON object containing an error message if the reservation fails.
    """
    data = request.json
    try:
        res_id = ReservationModel.create(data['trajet_id'], data['passager_id'], 
                                         data.get('places_reservees', 1))
        if res_id:
            return jsonify({'id': res_id, 'statut': 'en_attente'}), 201
        else:
            return jsonify({'error': 'Insufficient seats available'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@reservation_bp.route('/reservations/recues/<int:conducteur_id>', methods=['GET'])
def reservations_recues(conducteur_id):
    """
    Retrieve reservations received for trips where the user is the driver.

    Args:
        conducteur_id (int): The ID of the driver.

    Returns:
        - 200 OK: A JSON array of reservations received for the driver's trips.
    """
    reservations = ReservationModel.get_by_trajet(conducteur_id)
    return jsonify(reservations), 200

@reservation_bp.route('/reservations/faites/<int:passager_id>', methods=['GET'])
def reservations_faites(passager_id):
    """
    Retrieve reservations made by the user as a passenger.

    Args:
        passager_id (int): The ID of the passenger.

    Returns:
        - 200 OK: A JSON array of reservations made by the passenger.
    """
    reservations = ReservationModel.get_by_passager(passager_id)
    return jsonify(reservations), 200

@reservation_bp.route('/reservations/<int:reservation_id>/accepter', methods=['PUT'])
def accepter_reservation(reservation_id):
    """
    Accept a reservation.

    Args:
        reservation_id (int): The ID of the reservation to accept.

    Returns:
        - 200 OK: A JSON object indicating success.
    """
    ReservationModel.accepter(reservation_id)
    return jsonify({'success': True}), 200

@reservation_bp.route('/reservations/<int:reservation_id>/refuser', methods=['PUT'])
def refuser_reservation(reservation_id):
    """
    Decline a reservation.

    Args:
        reservation_id (int): The ID of the reservation to decline.

    Returns:
        - 200 OK: A JSON object indicating success.
    """
    ReservationModel.refuser(reservation_id)
    return jsonify({'success': True}), 200

@reservation_bp.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def annuler_reservation(reservation_id):
    """
    Cancel a reservation.

    Args:
        reservation_id (int): The ID of the reservation to cancel.

    Returns:
        - 200 OK: A JSON object indicating success.
    """
    ReservationModel.annuler(reservation_id)
    return jsonify({'success': True}), 200