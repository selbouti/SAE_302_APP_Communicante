from services.api_service import APIService

class ProfileController:
    """
    Contrôleur client PROFIL
    (aucun model local, uniquement API)
    """

    @staticmethod
    def get_profile(utilisateur_id):
        data, status = APIService.get(f"profile/{utilisateur_id}")
        return data

    @staticmethod
    def update_profile(utilisateur_id, profile_data):
        data, status = APIService.post(f"profile/{utilisateur_id}", profile_data)
        return data
