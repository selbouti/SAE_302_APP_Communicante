from core.database import Database
from datetime import datetime, timedelta


class TrajetModel:
    """
    Database model for managing trips (trajets).

    This model handles trip creation from imported calendars,
    retrieval, mode switching, seat availability, and advanced
    matching with optional time margins.
    """

    @staticmethod
    def create_from_icalendar(
        utilisateur_id,
        voiture_id,
        depart,
        arrivee,
        date_depart,
        jour_semaine,
        heure_depart,
        heure_retour,
        prix_par_place,
        mode
    ):
        """
        Create a new trip from an imported iCalendar entry.

        :param utilisateur_id: User identifier
        :param voiture_id: Car identifier (or None)
        :param depart: Departure location
        :param arrivee: Arrival location
        :param date_depart: Departure date
        :param jour_semaine: Day of the week
        :param heure_depart: Departure time
        :param heure_retour: Return time
        :param prix_par_place: Price per seat
        :param mode: Trip mode (conducteur or passager)
        :return: Created trip ID
        """
        query = '''
            INSERT INTO trajets (
                utilisateur_id, voiture_id, depart, arrivee,
                date_depart, jour_semaine, heure_depart,
                heure_retour, prix_par_place, mode
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        trajet_id = Database.insert(
            query,
            (
                utilisateur_id,
                voiture_id,
                depart,
                arrivee,
                date_depart,
                jour_semaine,
                heure_depart,
                heure_retour,
                prix_par_place,
                mode
            )
        )
        return trajet_id

    @staticmethod
    def get_by_user(user_id):
        """
        Retrieve all trips created by a user.

        :param user_id: User identifier
        :return: List of trips
        """
        query = '''
            SELECT
                t.*,
                v.marque,
                v.modele,
                v.places_max,
                (
                    SELECT COUNT(*)
                    FROM reservations
                    WHERE trajet_id = t.id
                ) AS places_reservees
            FROM trajets t
            LEFT JOIN voitures v ON t.voiture_id = v.id
            WHERE t.utilisateur_id = ?
        '''
        trajets = Database.execute(query, (user_id,))
        return [dict(t) for t in trajets]

    @staticmethod
    def delete_by_user(user_id):
        """
        Delete all trips belonging to a user.

        :param user_id: User identifier
        """
        Database.execute(
            "DELETE FROM trajets WHERE utilisateur_id = ?",
            (user_id,)
        )

    @staticmethod
    def get_first_trajet(user_id):
        """
        Retrieve the first trip created by a user.

        :param user_id: User identifier
        :return: Trip data or None
        """
        query = '''
            SELECT
                t.*,
                v.marque,
                v.modele,
                v.places_max,
                (
                    SELECT COUNT(*)
                    FROM reservations
                    WHERE trajet_id = t.id
                ) AS places_reservees
            FROM trajets t
            LEFT JOIN voitures v ON t.voiture_id = v.id
            WHERE t.utilisateur_id = ?
            LIMIT 1
        '''
        trajet = Database.execute_one(query, (user_id,))
        return dict(trajet) if trajet else None

    @staticmethod
    def get_trajet_by_id(trajet_id, user_id):
        """
        Retrieve a specific trip belonging to a user.

        :param trajet_id: Trip identifier
        :param user_id: User identifier
        :return: Trip data or None
        """
        query = '''
            SELECT
                t.*,
                v.marque,
                v.modele,
                v.places_max,
                (
                    SELECT COALESCE(SUM(r.places_reservees), 0)
                    FROM reservations r
                    WHERE r.trajet_id = t.id
                    AND r.statut = 'acceptee'
                ) AS places_reservees
            FROM trajets t
            LEFT JOIN voitures v ON t.voiture_id = v.id
            WHERE t.id = ?
            AND t.utilisateur_id = ?
            LIMIT 1
        '''
        trajet = Database.execute_one(query, (trajet_id, user_id))
        return dict(trajet) if trajet else None

    @staticmethod
    def get_places_disponibles(trajet_id):
        """
        Calculate available seats for a trip.

        :param trajet_id: Trip identifier
        :return: Number of available seats
        """
        query = '''
            SELECT
                v.places_max,
                COALESCE(SUM(r.places_reservees), 0) AS places_reservees
            FROM trajets t
            LEFT JOIN voitures v ON t.voiture_id = v.id
            LEFT JOIN reservations r ON t.id = r.trajet_id
            WHERE t.id = ?
            GROUP BY t.id
        '''
        result = Database.execute_one(query, (trajet_id,))
        if result:
            return result["places_max"] - result["places_reservees"]
        return 0

    @staticmethod
    def update_mode(trajet_id, mode):
        """
        Update the mode of a trip.

        :param trajet_id: Trip identifier
        :param mode: New mode
        :return: True if successful
        """
        Database.execute(
            "UPDATE trajets SET mode = ? WHERE id = ?",
            (mode, trajet_id)
        )
        return True

    @staticmethod
    def search_matching_avance(
        depart,
        arrivee,
        date_depart,
        mode_recherche,
        user_id,
        heure_aller=None,
        marge_aller=0,
        heure_retour=None,
        marge_retour=0
    ):
        """
        Search compatible trips with optional time margins.

        :param depart: Departure location
        :param arrivee: Arrival location
        :param date_depart: Departure date
        :param mode_recherche: Target mode (conducteur or passager)
        :param user_id: Current user identifier
        :param heure_aller: Reference outbound time
        :param marge_aller: Outbound margin (minutes)
        :param heure_retour: Reference return time
        :param marge_retour: Return margin (minutes)
        :return: List of matching trips
        """
        query = '''
            SELECT
                t.*,
                u.nom,
                u.prenom,
                u.email,
                u.telephone,
                v.marque,
                v.modele,
                v.places_max,
                (
                    v.places_max - COALESCE(SUM(
                        CASE
                            WHEN r.statut = 'acceptee'
                            THEN r.places_reservees
                            ELSE 0
                        END
                    ), 0)
                ) AS places_disponibles
            FROM trajets t
            JOIN utilisateurs u ON t.utilisateur_id = u.id
            LEFT JOIN voitures v ON t.voiture_id = v.id
            LEFT JOIN reservations r ON r.trajet_id = t.id
            WHERE LOWER(t.depart) LIKE LOWER(?)
            AND LOWER(t.arrivee) LIKE LOWER(?)
            AND DATE(t.date_depart) = DATE(?)
            AND t.mode = ?
            AND t.utilisateur_id != ?
        '''

        params = [
            f"%{depart}%",
            f"%{arrivee}%",
            date_depart,
            mode_recherche,
            user_id
        ]

        if heure_aller and heure_retour:
            heure_min = (
                datetime.strptime(heure_aller, "%H:%M")
                - timedelta(minutes=marge_aller)
            ).strftime("%H:%M")

            heure_max = (
                datetime.strptime(heure_retour, "%H:%M")
                + timedelta(minutes=marge_retour)
            ).strftime("%H:%M")

            query += " AND time(t.heure_depart) BETWEEN time(?) AND time(?)"
            params.extend([heure_min, heure_max])

        query += " GROUP BY t.id"

        if mode_recherche == "conducteur":
            query += " HAVING places_disponibles > 0"

        trajets = Database.execute(query, tuple(params))
        return [dict(t) for t in trajets]
