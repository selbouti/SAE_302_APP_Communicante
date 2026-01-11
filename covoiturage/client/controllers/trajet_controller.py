from services.api_service import APIService


class TrajetController:
    """
    Handles client-side API calls related to trips (trajets).
    """

    @staticmethod
    def get_my_trajet(user_id):
        """
        Fetch the user's main trip.

        :param user_id: user identifier
        """
        return APIService.get(f"/trajet/{user_id}")

    @staticmethod
    def save_trajet(user_id, data):
        """
        Create or update a trip for a user.

        :param user_id: user identifier
        :param data: trip payload
        """
        if TrajetController.get_my_trajet(user_id):
            return APIService.put(f"/trajet/{user_id}", data)
        return APIService.post(f"/trajet/{user_id}", data)

    @staticmethod
    def lister_trajets(user_id):
        """
        List all trips for a user.

        :param user_id: user identifier
        """
        return APIService.get(f"mes_trajets/{user_id}")

    @staticmethod
    def supprimer_trajet(trajet_id):
        """
        Delete a trip by its identifier.

        :param trajet_id: trip identifier
        """
        return APIService.delete(f"trajets/{trajet_id}")

    @staticmethod
    def basculer_mode(trajet_id, mode_actuel):
        """
        Toggle a trip mode between driver and passenger.

        :param trajet_id: trip identifier
        :param mode_actuel: current trip mode
        """
        nouveau_mode = "passager" if mode_actuel == "conducteur" else "conducteur"
        return APIService.put(
            f"trajets/{trajet_id}/mode",
            {"mode": nouveau_mode}
        )
