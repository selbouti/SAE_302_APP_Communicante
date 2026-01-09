import requests  # Obligatoire pour les requêtes HTTP

API_URL = "http://localhost:5000/api"  # adapte si ton serveur tourne ailleurs


class UserController:
    @staticmethod
    def register(email, password, nom, prenom, telephone, voiture=None):
        data = {
            "email": email,
            "password": password,
            "nom": nom,
            "prenom": prenom,
            "telephone": telephone
        }
        if voiture:
            data["voiture"] = voiture
        try:
            resp = requests.post(f"{API_URL}/register", json=data)
            return resp.json(), resp.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    @staticmethod
    def upload_icalendar(user_id, file_path):
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                resp = requests.post(f"{API_URL}/upload_icalendar/{user_id}", files=files)
                return resp.json(), resp.status_code
        except FileNotFoundError:
            return {"error": "Fichier non trouvé"}, 400
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    @staticmethod
    def login(email, password):
        data = {"email": email, "password": password}
        try:
            resp = requests.post(f"{API_URL}/login", json=data)
            return resp.json(), resp.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_profile(user_id):
        try:
            resp = requests.get(f"{API_URL}/profile/{user_id}")
            return resp.json(), resp.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    @staticmethod
    def update_calendar(user_id, file_path):
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                resp = requests.post(f"{API_URL}/update_calendar/{user_id}", files=files)
                return resp.json(), resp.status_code
        except FileNotFoundError:
            return {"error": "Fichier non trouvé"}, 400
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

