from services.api_service import APIService
from models.reservation import Reservation

class ReservationController:
    """Contrôle la logique des réservations côté client"""
    
    @staticmethod
    def creer_reservation(trajet_id, passager_id, places=1):
        """Créer une réservation"""
        data = {
            'trajet_id': trajet_id,
            'passager_id': passager_id,
            'places_reservees': places
        }
        return APIService.post('reservations', data)
    
    @staticmethod
    def get_reservations_recues(user_id):
        """Récupérer les réservations reçues (mode conducteur)"""
        resp, status = APIService.get(f'reservations/recues/{user_id}')
        
        if status == 200:
            reservations = [
                Reservation(
                    r['id'], r['trajet_id'], r['depart'], r['arrivee'],
                    r['places_reservees'], r['statut'], r['created_at'],
                    r['prix_par_place'], r['prenom'], r['nom']
                )
                for r in resp
            ]
            return reservations, None
        return None, f"Erreur {status}"
    
    @staticmethod
    def get_reservations_faites(user_id):
        """Récupérer les réservations faites (mode passager)"""
        resp, status = APIService.get(f'reservations/faites/{user_id}')
        
        if status == 200:
            reservations = [
                Reservation(
                    r['id'], r['trajet_id'], r['depart'], r['arrivee'],
                    r['places_reservees'], r['statut'], r['created_at'],
                    r['prix_par_place'], r['prenom'], r['nom']
                )
                for r in resp
            ]
            return reservations, None
        return None, f"Erreur {status}"
    
    @staticmethod
    def accepter_reservation(reservation_id):
        """Accepter une réservation"""
        resp, status = APIService.put(f'reservations/{reservation_id}/accepter')
        
        if status == 200:
            return True, "Réservation acceptée"
        return False, f"Erreur {status}"
    
    @staticmethod
    def refuser_reservation(reservation_id):
        """Refuser une réservation"""
        resp, status = APIService.put(f'reservations/{reservation_id}/refuser')
        
        if status == 200:
            return True, "Réservation refusée"
        return False, f"Erreur {status}"
    
    @staticmethod
    # Dans reservation_controller.py côté client:
    @staticmethod
    def annuler_reservation(reservation_id):
        """Annuler une réservation"""
        resp, status = APIService.delete(f'reservations/{reservation_id}')  # ← Sans /annuler
        if status == 200:
            return True, "Réservation annulée"
        return False, f"Erreur {status}"