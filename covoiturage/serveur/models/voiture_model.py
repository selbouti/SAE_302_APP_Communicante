from core.database import Database


class VoitureModel:
    """
    Database model for car (vehicle) management.

    This class provides methods to create, retrieve, and delete
    cars associated with a specific user in the database.
    """

    @staticmethod
    def create(utilisateur_id, data):
        """
        Create a new car entry for a given user.

        :param utilisateur_id: Identifier of the car owner
        :type utilisateur_id: int
        :param data: Dictionary containing car information
        :type data: dict
        :return: Identifier of the newly created car
        :rtype: int
        """
        query = """
            INSERT INTO voitures (
                utilisateur_id,
                marque,
                modele,
                chevaux_fiscaux,
                taux_co2,
                places_totales,
                motorisation
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return Database.insert(
            query,
            (
                utilisateur_id,
                data["marque"],
                data["modele"],
                data["chevaux_fiscaux"],
                data["taux_co2"],
                data["places_max"],
                data["motorisation"]
            )
        )

    @staticmethod
    def get_by_user(user_id):
        """
        Retrieve all cars associated with a user.

        :param user_id: User identifier
        :type user_id: int
        :return: List of cars owned by the user
        :rtype: list[dict]
        """
        query = "SELECT * FROM voitures WHERE utilisateur_id = ?"
        rows = Database.execute(query, (user_id,))
        return [dict(r) for r in rows]

    @staticmethod
    def delete_by_user(user_id):
        """
        Delete all cars associated with a user.

        :param user_id: User identifier
        :type user_id: int
        """
        Database.execute(
            "DELETE FROM voitures WHERE utilisateur_id = ?",
            (user_id,)
        )
