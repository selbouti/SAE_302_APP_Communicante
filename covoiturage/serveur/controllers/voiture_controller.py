from flask import Blueprint, request, jsonify
from core.database import Database
from models.voiture_model import VoitureModel

voiture_bp = Blueprint('voiture', __name__, url_prefix='/api')

# =========================
#   GET : voiture utilisateur
# =========================
@voiture_bp.route('/voitures/<int:user_id>', methods=['GET'])
def get_voiture(user_id):
    voiture = VoitureModel.get_by_user(user_id)
    return jsonify(voiture), 200


# =========================
#   POST : créer / modifier voiture
# =========================
@voiture_bp.route('/voitures', methods=['POST'])
def creer_voiture():
    data = request.json

    voiture_id = VoitureModel.create(
        utilisateur_id=data['utilisateur_id'],
        marque=data['marque'],
        modele=data['modele'],
        chevaux_fiscaux=data['chevaux_fiscaux'],
        places_max=data['places_max'],
        taux_co2=data['taux_co2'],
        motorisation=data['motorisation']
    )

    return jsonify({'id': voiture_id}), 201


# =========================
#   DELETE : supprimer voiture
# =========================
@voiture_bp.route('/voitures/<int:voiture_id>', methods=['DELETE'])
def supprimer_voiture(voiture_id):
    user_id = request.args.get("user_id")

    Database.execute(
        "DELETE FROM voitures WHERE id = ? AND utilisateur_id = ?",
        (voiture_id, user_id)
    )

    return jsonify({'success': True}), 200
