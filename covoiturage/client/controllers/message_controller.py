from services.api_service import APIService

class MessageController:
    @staticmethod
    def list_for_user(user_id):
        return APIService.get(f'messages/{user_id}')

    @staticmethod
    def clear_for_user(user_id):
        return APIService.delete(f'messages/{user_id}')
