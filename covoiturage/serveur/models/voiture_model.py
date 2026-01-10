from core.database import Database

class VoitureModel:
    """
    A model class for managing cars (voitures) in the database.
    Provides methods to create, retrieve, and delete cars associated with a user.
    """

    @staticmethod
    def create(utilisateur_id, data):
        """
        Create a new car entry in the database for a specific user.

        Args:
            utilisateur_id (int): The ID of the user who owns the car.
            data (dict): A dictionary containing the car details:
                - marque (str): The brand of the car.
                - modele (str): The model of the car.
                - chevaux_fiscaux (float): The fiscal horsepower of the car.
                - taux_co2 (float): The CO2 emission rate of the car.
                - places_max (int): The total number of seats in the car.
                - motorisation (str): The type of motorization (e.g., electric, diesel).

        Returns:
            int: The ID of the newly created car entry.
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
        Retrieve all cars associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[dict]: A list of dictionaries, each containing the details of a car.
        """
        query = "SELECT * FROM voitures WHERE utilisateur_id = ?"
        rows = Database.execute(query, (user_id,))
        return [dict(r) for r in rows]

    @staticmethod
    def delete_by_user(user_id):
        """
        Delete all cars associated with a specific user.

        Args:
            user_id (int): The ID of the user whose cars should be deleted.
        """
        Database.execute(
            "DELETE FROM voitures WHERE utilisateur_id = ?",
            (user_id,)
        )
