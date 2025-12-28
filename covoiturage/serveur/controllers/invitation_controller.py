from flask import Blueprint, request, jsonify
from models.invitation_model import InvitationModel

invitation_bp = Blueprint('invitation', __name__, url_prefix='/api')

@invitation_bp.route('/invitations', methods=['POST'])
def creer_invitation():
    data = request.json
    try:
        inv_id = InvitationModel.create(data['trajet_id'], data['passager_id'])
        return jsonify({'id': inv_id, 'statut': 'en_attente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@invitation_bp.route('/invitations/received/<int:passager_id>', methods=['GET'])
def invitations_received(passager_id):
    invitations = InvitationModel.get_invitations_received(passager_id)
    return jsonify(invitations), 200

@invitation_bp.route('/invitations/sent/<int:conducteur_id>', methods=['GET'])
def invitations_sent(conducteur_id):
    invitations = InvitationModel.get_invitations_sent(conducteur_id)
    return jsonify(invitations), 200

@invitation_bp.route('/invitations/<int:invitation_id>/accepter', methods=['PUT'])
def accepter_invitation(invitation_id):
    InvitationModel.accepter(invitation_id)
    return jsonify({'success': True}), 200

@invitation_bp.route('/invitations/<int:invitation_id>/refuser', methods=['PUT'])
def refuser_invitation(invitation_id):
    InvitationModel.refuser(invitation_id)
    return jsonify({'success': True}), 200