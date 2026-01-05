from services.api_service import APIService

class ProfileController:
    """
    Contrôleur client PROFIL
    (aucun modèle local, uniquement API)
    """

    @staticmethod
    def get_profile(user_id):
        resp, status = APIService.get(f"profile/{user_id}")
        return resp, status

    @staticmethod
    def update_profile(user_id, profile_data):
        resp, status = APIService.post(f"profile/{user_id}", profile_data)
        return resp, status
