# controllers/reservation_controller.py
"""
Contrôleur API pour la gestion des réservations
"""
import sys
import os

# Ajouter le chemin racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from flask import Flask, request, jsonify
from models.gestion_res_model import Reservation, ReservationDAO
from typing import Dict, Any

class ReservationController:
    """Contrôleur pour gérer les endpoints de réservation"""
    
    def __init__(self, app: Flask, db_connection):
        """
        Initialise le contrôleur avec l'application Flask et la connexion BD
        
        Args:
            app: Application Flask
            db_connection: Connexion à la base de données
        """
        self.app = app
        self.dao = ReservationDAO(db_connection)
        self._register_routes()
    
    def _register_routes(self):
        """Enregistre toutes les routes de l'API"""
        self.app.add_url_rule('/api/reservations', 
                            view_func=self.creer_reservation, 
                            methods=['POST'])
        
        self.app.add_url_rule('/api/reservations/<int:id_reservation>', 
                            view_func=self.get_reservation, 
                            methods=['GET'])
        
        self.app.add_url_rule('/api/reservations/<int:id_reservation>/annuler', 
                            view_func=self.annuler_reservation, 
                            methods=['PUT'])
        
        self.app.add_url_rule('/api/reservations/<int:id_reservation>/confirmer', 
                            view_func=self.confirmer_reservation, 
                            methods=['PUT'])
        
        self.app.add_url_rule('/api/trajets/<int:id_trajet>/reservations', 
                            view_func=self.get_reservations_trajet, 
                            methods=['GET'])
        
        self.app.add_url_rule('/api/passagers/<int:id_passager>/reservations', 
                            view_func=self.get_reservations_passager, 
                            methods=['GET'])
    
    def creer_reservation(self) -> tuple[Dict[str, Any], int]:
        """
        POST /api/reservations
        Crée une nouvelle réservation
        
        Body JSON attendu:
        {
            "id_trajet": 1,
            "id_passager": 2,
            "nb_places": 1
        }
        
        Returns:
            Réponse JSON avec la réservation créée et code HTTP
        """
        try:
            data = request.get_json()
            
            # Validation des données
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Données manquantes'
                }), 400
            
            id_trajet = data.get('id_trajet')
            id_passager = data.get('id_passager')
            nb_places = data.get('nb_places', 1)
            
            if not id_trajet or not id_passager:
                return jsonify({
                    'success': False,
                    'message': 'id_trajet et id_passager sont requis'
                }), 400
            
            # Vérifier la disponibilité des places
            if not self.dao.verifier_disponibilite(id_trajet, nb_places):
                return jsonify({
                    'success': False,
                    'message': 'Pas assez de places disponibles'
                }), 400
            
            # Créer la réservation
            reservation = Reservation(
                id_trajet=id_trajet,
                id_passager=id_passager,
                nb_places=nb_places,
                statut='en_attente'
            )
            
            id_reservation = self.dao.creer_reservation(reservation)
            
            if id_reservation:
                reservation.id_reservation = id_reservation
                return jsonify({
                    'success': True,
                    'message': 'Réservation créée avec succès',
                    'data': reservation.to_dict()
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'message': 'Erreur lors de la création de la réservation'
                }), 500
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erreur serveur: {str(e)}'
            }), 500
    
    def get_reservation(self, id_reservation: int) -> tuple[Dict[str, Any], int]:
        """
        GET /api/reservations/<id>
        Récupère une réservation par son ID
        
        Args:
            id_reservation: ID de la réservation
            
        Returns:
            Réponse JSON avec la réservation et code HTTP
        """
        try:
            reservation = self.dao.get_reservation_by_id(id_reservation)
            
            if reservation:
                return jsonify({
                    'success': True,
                    'data': reservation.to_dict()
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Réservation non trouvée'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erreur serveur: {str(e)}'
            }), 500
    
    def annuler_reservation(self, id_reservation: int) -> tuple[Dict[str, Any], int]:
        """
        PUT /api/reservations/<id>/annuler
        Annule une réservation
        
        Args:
            id_reservation: ID de la réservation à annuler
            
        Returns:
            Réponse JSON avec le résultat et code HTTP
        """
        try:
            success = self.dao.annuler_reservation(id_reservation)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Réservation annulée avec succès'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Réservation non trouvée ou déjà annulée'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erreur serveur: {str(e)}'
            }), 500
    
    def confirmer_reservation(self, id_reservation: int) -> tuple[Dict[str, Any], int]:
        """
        PUT /api/reservations/<id>/confirmer
        Confirme une réservation
        
        Args:
            id_reservation: ID de la réservation à confirmer
            
        Returns:
            Réponse JSON avec le résultat et code HTTP
        """
        try:
            success = self.dao.confirmer_reservation(id_reservation)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Réservation confirmée avec succès'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Réservation non trouvée'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erreur serveur: {str(e)}'
            }), 500
    
    def get_reservations_trajet(self, id_trajet: int) -> tuple[Dict[str, Any], int]:
        """
        GET /api/trajets/<id>/reservations
        Récupère toutes les réservations d'un trajet
        
        Args:
            id_trajet: ID du trajet
            
        Returns:
            Réponse JSON avec la liste des réservations et code HTTP
        """
        try:
            reservations = self.dao.get_reservations_by_trajet(id_trajet)
            
            return jsonify({
                'success': True,
                'data': [r.to_dict() for r in reservations],
                'count': len(reservations)
            }), 200
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erreur serveur: {str(e)}'
            }), 500
    
    def get_reservations_passager(self, id_passager: int) -> tuple[Dict[str, Any], int]:
        """
        GET /api/passagers/<id>/reservations
        Récupère toutes les réservations d'un passager
        
        Args:
            id_passager: ID du passager
            
        Returns:
            Réponse JSON avec la liste des réservations et code HTTP
        """
        try:
            reservations = self.dao.get_reservations_by_passager(id_passager)
            
            return jsonify({
                'success': True,
                'data': [r.to_dict() for r in reservations],
                'count': len(reservations)
            }), 200
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erreur serveur: {str(e)}'
            }), 500


# Exemple d'utilisation
"""if __name__ == '__main__':
    from flask import Flask
    import sqlite3
    
    app = Flask(__name__)
    db = sqlite3.connect('covoiturage.db', check_same_thread=False)
    
    controller = ReservationController(app, db)
    
    app.run(debug=True, port=5000)"""