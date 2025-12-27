from services.api_service import APIService

class TrajetController:
    def get_my_trajet(self, user_id):
        return APIService.get(f"/trajet/{user_id}")

    def save_trajet(self, user_id, data):
        if self.get_my_trajet(user_id):
            return APIService.put(f"/trajet/{user_id}", data)
        return APIService.post(f"/trajet/{user_id}", data)
