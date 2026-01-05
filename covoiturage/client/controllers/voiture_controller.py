from services.api_service import APIService

class VoitureController:
    """
    Contrôleur client pour gérer la voiture de l'utilisateur.
    Méthodes statiques similaires au ProfileController.
    """

    @staticmethod
    def get_voiture(user_id):
        """
        Récupère la/les voitures de l'utilisateur connecté
        """
        resp, status = APIService.get(f"voitures/{user_id}")
        if status == 200:
            return resp, status
        return {"success": False, "message": f"Erreur {status}"}, status

    @staticmethod
    def save_voiture(user_id, voiture_data):
        """
        Crée ou met à jour la voiture de l'utilisateur
        """
        voiture_data["utilisateur_id"] = user_id
        resp, status = APIService.post("voitures", voiture_data)
        return resp, status

    @staticmethod
    def delete_voiture(user_id, voiture_id):
        """
        Supprime la voiture de l'utilisateur
        """
        resp, status = APIService.delete(f"voitures/{voiture_id}?user_id={user_id}")
        return resp, status
