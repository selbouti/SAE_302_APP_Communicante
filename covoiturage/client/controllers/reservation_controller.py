from services.api_service import APIService
from models.reservation import Reservation

class ReservationController:
    """
    Handles the logic for managing reservations on the client side.

    This class provides static methods to interact with the reservation-related
    API endpoints, including creating, retrieving, accepting, refusing, and canceling reservations.
    """

    @staticmethod
    def creer_reservation(trajet_id, passager_id, places=1):
        """
        Create a new reservation for a trip.

        Args:
            trajet_id (int): The ID of the trip.
            passager_id (int): The ID of the passenger making the reservation.
            places (int, optional): The number of seats reserved (default is 1).

        Returns:
            tuple: A tuple containing the API response (dict) and the HTTP status code (int).
        """
        data = {
            'trajet_id': trajet_id,
            'passager_id': passager_id,
            'places_reservees': places
        }
        return APIService.post('reservations', data)
    
    @staticmethod
    def get_reservations_recues(user_id):
        """
        Retrieve reservations received by the user (driver mode).

        Args:
            user_id (int): The ID of the user (driver).

        Returns:
            tuple: A tuple containing a list of `Reservation` objects and None if successful,
                   or None and an error message if an error occurs.
        """
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
        """
        Retrieve reservations made by the user (passenger mode).

        Args:
            user_id (int): The ID of the user (passenger).

        Returns:
            tuple: A tuple containing a list of `Reservation` objects and None if successful,
                   or None and an error message if an error occurs.
        """
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
        """
        Accept a reservation.

        Args:
            reservation_id (int): The ID of the reservation to accept.

        Returns:
            tuple: A tuple containing True and a success message if successful,
                   or False and an error message if an error occurs.
        """
        resp, status = APIService.put(f'reservations/{reservation_id}/accepter')
        
        if status == 200:
            return True, "Réservation acceptée"
        return False, f"Erreur {status}"
    
    @staticmethod
    def refuser_reservation(reservation_id):
        """
        Refuse a reservation.

        Args:
            reservation_id (int): The ID of the reservation to refuse.

        Returns:
            tuple: A tuple containing True and a success message if successful,
                   or False and an error message if an error occurs.
        """
        resp, status = APIService.put(f'reservations/{reservation_id}/refuser')
        
        if status == 200:
            return True, "Réservation refusée"
        return False, f"Erreur {status}"
    
    @staticmethod
    def annuler_reservation(reservation_id):
        """
        Cancel a reservation.

        Args:
            reservation_id (int): The ID of the reservation to cancel.

        Returns:
            tuple: A tuple containing True and a success message if successful,
                   or False and an error message if an error occurs.
        """
        resp, status = APIService.delete(f'reservations/{reservation_id}')
        if status == 200:
            return True, "Réservation annulée"
        return False, f"Erreur {status}"