from services.api_service import APIService

class VoitureController:
    """
    Contrôleur client VOITURE
    (statique, basé uniquement sur l'API)
    """

    @staticmethod
    def get_voiture(user_id):
        resp, status = APIService.get(f"voiture/{user_id}")
        return resp, status

    @staticmethod
    def save_voiture(user_id, voiture_data):
        resp, status = APIService.post(
            f"voiture/{user_id}",
            voiture_data
        )
        return resp, status

    @staticmethod
    def delete_voiture(user_id):
        resp, status = APIService.delete(
            f"voiture/{user_id}"
        )
        return resp, status
