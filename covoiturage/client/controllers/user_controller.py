from services.api_service import APIService

class UserController:
    @staticmethod
    def register(email, password, nom, prenom, telephone):
        data = {'email': email, 'password': password, 'nom': nom, 'prenom': prenom, 'telephone': telephone}
        return APIService.post('register', data)
    
    @staticmethod
    def login(email, password):
        data = {'email': email, 'password': password}
        return APIService.post('login', data)
    
    @staticmethod
    def upload_icalendar(user_id, file_path):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            import requests
            r = requests.post(f"http://127.0.0.1:5000/api/upload_icalendar/{user_id}", files=files)
            return r.json(), r.status_code
