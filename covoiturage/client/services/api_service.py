import requests
API_URL = "http://127.0.0.1:5000/api"

class APIService:
    """
    A service class to handle HTTP requests to the API.
    Provides static methods for making POST, GET, PUT, and DELETE requests.
    """

    @staticmethod
    def post(endpoint, data):
        """
        Sends a POST request to the specified API endpoint.

        Args:
            endpoint (str): The API endpoint to send the request to (e.g., 'users/create').
            data (dict): The data to include in the request body.

        Returns:
            tuple: A tuple containing the JSON response (dict) and the HTTP status code (int).
                   If an error occurs, returns an error message and a 400 status code.
        """
        try:
            r = requests.post(f"{API_URL}/{endpoint}", json=data)
            return r.json(), r.status_code
        except Exception as e:
            return {'error': str(e)}, 400
    
    @staticmethod
    def get(endpoint):
        """
        Sends a GET request to the specified API endpoint.

        Args:
            endpoint (str): The API endpoint to send the request to (e.g., 'users/1').

        Returns:
            tuple: A tuple containing the JSON response (dict) and the HTTP status code (int).
                   If an error occurs, returns an error message and a 400 status code.
        """
        try:
            r = requests.get(f"{API_URL}/{endpoint}")
            return r.json(), r.status_code
        except Exception as e:
            return {'error': str(e)}, 400
    
    @staticmethod
    def put(endpoint, data=None):
        """
        Sends a PUT request to the specified API endpoint.

        Args:
            endpoint (str): The API endpoint to send the request to (e.g., 'users/1/update').
            data (dict, optional): The data to include in the request body. Defaults to an empty dictionary.

        Returns:
            tuple: A tuple containing the JSON response (dict) and the HTTP status code (int).
                   If an error occurs, returns an error message and a 400 status code.
        """
        try:
            r = requests.put(f"{API_URL}/{endpoint}", json=data or {})
            return r.json(), r.status_code
        except Exception as e:
            return {'error': str(e)}, 400
    
    @staticmethod
    def delete(endpoint):
        """
        Sends a DELETE request to the specified API endpoint.

        Args:
            endpoint (str): The API endpoint to send the request to (e.g., 'users/1/delete').

        Returns:
            tuple: A tuple containing the JSON response (dict) and the HTTP status code (int).
                   If an error occurs, returns an error message and a 400 status code.
        """
        try:
            r = requests.delete(f"{API_URL}/{endpoint}")
            return r.json(), r.status_code
        except Exception as e:
            return {'error': str(e)}, 400