import requests  # Required for HTTP requests

API_URL = "http://localhost:5000/api"


class UserController:
    """
    Client-side controller responsible for user-related API interactions.
    """

    @staticmethod
    def register(email, password, nom, prenom, telephone, voiture=None):
        """
        Register a new user.

        :param email: User email address
        :param password: User password
        :param nom: Last name
        :param prenom: First name
        :param telephone: Phone number
        :param voiture: Optional car data
        :return: API response and HTTP status code
        """
        assert isinstance(email, str) and email, "email must be a non-empty string"
        assert isinstance(password, str) and password, "password must be a non-empty string"
        assert isinstance(nom, str), "nom must be a string"
        assert isinstance(prenom, str), "prenom must be a string"
        assert isinstance(telephone, str), "telephone must be a string"

        data = {
            "email": email,
            "password": password,
            "nom": nom,
            "prenom": prenom,
            "telephone": telephone
        }

        if voiture is not None:
            assert isinstance(voiture, dict), "voiture must be a dictionary"
            data["voiture"] = voiture

        try:
            resp = requests.post(f"{API_URL}/register", json=data)
            return resp.json(), resp.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    @staticmethod
    def login(email, password):
        """
        Authenticate a user.

        :param email: User email
        :param password: User password
        :return: API response and HTTP status code
        """
        assert isinstance(email, str) and email, "email must be a non-empty string"
        assert isinstance(password, str) and password, "password must be a non-empty string"

        data = {"email": email, "password": password}

        try:
            resp = requests.post(f"{API_URL}/login", json=data)
            return resp.json(), resp.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_profile(user_id):
        """
        Retrieve a user profile.

        :param user_id: User identifier
        :return: API response and HTTP status code
        """
        assert isinstance(user_id, int), "user_id must be an integer"

        try:
            resp = requests.get(f"{API_URL}/profile/{user_id}")
            return resp.json(), resp.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    @staticmethod
    def upload_icalendar(user_id, file_path):
        """
        Upload an iCalendar (.ics) file for a user.

        :param user_id: User identifier
        :param file_path: Path to the .ics file
        :return: API response and HTTP status code
        """
        assert isinstance(user_id, int), "user_id must be an integer"
        assert isinstance(file_path, str) and file_path, "file_path must be a valid string"

        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                resp = requests.post(
                    f"{API_URL}/upload_icalendar/{user_id}",
                    files=files
                )
                return resp.json(), resp.status_code
        except FileNotFoundError:
            return {"error": "File not found"}, 400
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    @staticmethod
    def update_calendar(user_id, file_path):
        """
        Update the user's calendar file.

        :param user_id: User identifier
        :param file_path: Path to the calendar file
        :return: API response and HTTP status code
        """
        assert isinstance(user_id, int), "user_id must be an integer"
        assert isinstance(file_path, str) and file_path, "file_path must be a valid string"

        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                resp = requests.post(
                    f"{API_URL}/update_calendar/{user_id}",
                    files=files
                )
                return resp.json(), resp.status_code
        except FileNotFoundError:
            return {"error": "File not found"}, 400
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500
