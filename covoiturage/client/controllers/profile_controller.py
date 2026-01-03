from services.api_service import APIService

class ProfileController:
    """
    Contrôleur client PROFIL
    (aucun model local, uniquement API)
    """


    @staticmethod
    def get_profile(user_id):
        resp, status = APIService.get(f"profile/{user_id}")
        if status == 200:
            return resp, None
        return {"success": False, "message": f"Erreur {status}"}

    @staticmethod
    def update_profile(utilisateur_id, profile_data):
        data, status = APIService.post(f"profile/{utilisateur_id}", profile_data)
        return data
