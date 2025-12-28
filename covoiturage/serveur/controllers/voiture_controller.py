from flask import Blueprint, request, jsonify
from models.voiture_model import VoitureModel

voiture_bp = Blueprint('voiture', __name__, url_prefix='/api')

@voiture_bp.route('/voitures/<int:user_id>', methods=['GET'])
def get_voitures(user_id):
    voitures = VoitureModel.get_by_user(user_id)
    return jsonify(voitures), 200

@voiture_bp.route('/voitures', methods=['POST'])
def creer_voiture():
    data = request.json
    voiture_id = VoitureModel.create(
        data['utilisateur_id'],
        data['marque'],
        data['modele'],
        data['couleur'],
        data['plaque'],
        data['places_totales']
    )
    return jsonify({'id': voiture_id}), 201

@voiture_bp.route('/voitures/<int:voiture_id>', methods=['DELETE'])
def supprimer_voiture(voiture_id):
    from core.database import Database
    Database.execute('DELETE FROM voitures WHERE id = ?', (voiture_id,))
    return jsonify({'success': True}), 200