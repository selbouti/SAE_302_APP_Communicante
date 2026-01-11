from services.api_service import APIService


class TrajetController:
    """
    Handles client-side API calls related to trips (trajets).
    """

    @staticmethod
    def lister_trajets(user_id):
        """
        List all trips for a user.

        :param user_id: user identifier
        """
        return APIService.get(f"mes_trajets/{user_id}")

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
