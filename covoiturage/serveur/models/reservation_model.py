from core.database import Database
from models.trajet_model import TrajetModel


class ReservationModel:
    """
    Database model for managing reservations.

    This class provides methods to create, retrieve, update,
    and delete reservations associated with trips.
    """

    @staticmethod
    def create(trajet_id, passager_id, places_reservees):
        """
        Create a new reservation if enough seats are available.

        :param trajet_id: Trip identifier
        :type trajet_id: int
        :param passager_id: Passenger identifier
        :type passager_id: int
        :param places_reservees: Number of seats requested
        :type places_reservees: int
        :return: Reservation ID or None if not enough seats
        :rtype: int | None
        """
        places_dispo = TrajetModel.get_places_disponibles(trajet_id)
        if places_dispo < places_reservees:
            return None

        query = '''INSERT INTO reservations (trajet_id, passager_id, places_reservees, statut)
                   VALUES (?, ?, ?, 'en_attente')'''
        res_id = Database.insert(query, (trajet_id, passager_id, places_reservees))
        return res_id

    @staticmethod
    def get_by_passager(passager_id):
        """
        Retrieve all reservations made by a passenger.

        :param passager_id: Passenger identifier
        :type passager_id: int
        :return: List of reservations
        :rtype: list[dict]
        """
        query = '''SELECT 
                       r.id, r.trajet_id, r.places_reservees, r.statut, r.created_at,
                       t.depart, t.arrivee, t.date_depart, t.heure_depart, t.prix_par_place,
                       u.nom, u.prenom, u.telephone, v.marque, v.modele
                   FROM reservations r
                   JOIN trajets t ON r.trajet_id = t.id
                   JOIN utilisateurs u ON t.utilisateur_id = u.id
                   LEFT JOIN voitures v ON t.voiture_id = v.id
                   WHERE r.passager_id = ?'''
        res = Database.execute(query, (passager_id,))
        return [dict(r) for r in res]

    @staticmethod
    def get_by_trajet(trajet_id):
        """
        Retrieve all active reservations for a specific trip.

        Reservations with status 'refusee' are excluded.

        :param trajet_id: Trip identifier
        :type trajet_id: int
        :return: List of reservations
        :rtype: list[dict]
        """
        query = '''SELECT 
                       r.id, r.passager_id, r.places_reservees, r.statut, r.created_at,
                       t.id as trajet_id, t.depart, t.arrivee, t.date_depart, t.heure_depart, t.prix_par_place,
                       u.nom, u.prenom, u.email, u.telephone
                   FROM reservations r
                   JOIN trajets t ON r.trajet_id = t.id
                   JOIN utilisateurs u ON r.passager_id = u.id
                   WHERE r.trajet_id = ? AND r.statut != 'refusee'
                '''
        res = Database.execute(query, (trajet_id,))
        return [dict(r) for r in res]

    @staticmethod
    def accepter(reservation_id):
        """
        Accept a reservation.

        :param reservation_id: Reservation identifier
        :type reservation_id: int
        """
        Database.execute(
            'UPDATE reservations SET statut = ? WHERE id = ?',
            ('acceptee', reservation_id)
        )

    @staticmethod
    def refuser(reservation_id):
        """
        Refuse a reservation.

        :param reservation_id: Reservation identifier
        :type reservation_id: int
        """
        Database.execute(
            'UPDATE reservations SET statut = ? WHERE id = ?',
            ('refusee', reservation_id)
        )

    @staticmethod
    def annuler(reservation_id):
        """
        Cancel a reservation by deleting it.

        :param reservation_id: Reservation identifier
        :type reservation_id: int
        """
        Database.execute(
            'DELETE FROM reservations WHERE id=?',
            (reservation_id,)
        )
