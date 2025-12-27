import requests
API_URL = "http://127.0.0.1:5000/api"

class APIService:
    @staticmethod
    def post(endpoint, data):
        try:
            r = requests.post(f"{API_URL}/{endpoint}", json=data)
            return r.json(), r.status_code
        except Exception as e:
            return {'error': str(e)}, 400
    
    @staticmethod
    def get(endpoint):
        try:
            r = requests.get(f"{API_URL}/{endpoint}")
            return r.json(), r.status_code
        except Exception as e:
            return {'error': str(e)}, 400
    
    @staticmethod
    def put(endpoint, data=None):
        try:
            r = requests.put(f"{API_URL}/{endpoint}", json=data or {})
            return r.json(), r.status_code
        except Exception as e:
            return {'error': str(e)}, 400
    
    @staticmethod
    def delete(endpoint):
        try:
            r = requests.delete(f"{API_URL}/{endpoint}")
            return r.json(), r.status_code
        except Exception as e:
            return {'error': str(e)}, 400