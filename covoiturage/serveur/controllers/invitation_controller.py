from flask import Blueprint, request, jsonify
from models.invitation_model import InvitationModel

invitation_bp = Blueprint('invitation', __name__, url_prefix='/api')

@invitation_bp.route('/invitations', methods=['POST'])
def creer_invitation():
    """
    Create a new invitation for a passenger to join a trip.

    Request Body (JSON):
        - trajet_id (int): The ID of the trip.
        - passager_id (int): The ID of the passenger.

    Returns:
        - 201 Created: A JSON object containing the invitation ID and its status.
        - 400 Bad Request: A JSON object containing the error message if an exception occurs.
    """
    data = request.json
    try:
        inv_id = InvitationModel.create(data['trajet_id'], data['passager_id'])
        return jsonify({'id': inv_id, 'statut': 'en_attente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@invitation_bp.route('/invitations/received/<int:passager_id>', methods=['GET'])
def invitations_received(passager_id):
    """
    Retrieve all invitations received by a passenger.

    Args:
        passager_id (int): The ID of the passenger.

    Returns:
        - 200 OK: A JSON array of invitations received by the passenger.
    """
    invitations = InvitationModel.get_invitations_received(passager_id)
    return jsonify(invitations), 200

@invitation_bp.route('/invitations/sent/<int:conducteur_id>', methods=['GET'])
def invitations_sent(conducteur_id):
    """
    Retrieve all invitations sent by a driver.

    Args:
        conducteur_id (int): The ID of the driver.

    Returns:
        - 200 OK: A JSON array of invitations sent by the driver.
    """
    invitations = InvitationModel.get_invitations_sent(conducteur_id)
    return jsonify(invitations), 200

@invitation_bp.route('/invitations/<int:invitation_id>/accepter', methods=['PUT'])
def accepter_invitation(invitation_id):
    """
    Accept an invitation.

    Args:
        invitation_id (int): The ID of the invitation to accept.

    Returns:
        - 200 OK: A JSON object indicating success.
    """
    InvitationModel.accepter(invitation_id)
    return jsonify({'success': True}), 200

@invitation_bp.route('/invitations/<int:invitation_id>/refuser', methods=['PUT'])
def refuser_invitation(invitation_id):
    """
    Decline an invitation.

    Args:
        invitation_id (int): The ID of the invitation to decline.

    Returns:
        - 200 OK: A JSON object indicating success.
    """
    InvitationModel.refuser(invitation_id)
    return jsonify({'success': True}), 200