from services.api_service import APIService


class VoitureController:
    """
    Client-side controller responsible for car (vehicle) management.

    This controller communicates exclusively with the REST API to
    retrieve, create, update, or delete the user's car.
    """

    @staticmethod
    def get_voiture(user_id):
        """
        Retrieve the car associated with a user.

        :param user_id: User identifier
        :type user_id: int
        :return: API response and HTTP status code
        :rtype: tuple
        """
        assert isinstance(user_id, int), "user_id must be an integer"

        resp, status = APIService.get(f"voiture/{user_id}")
        return resp, status

    @staticmethod
    def save_voiture(user_id, voiture_data):
        """
        Create or update the user's car.

        :param user_id: User identifier
        :type user_id: int
        :param voiture_data: Car data payload
        :type voiture_data: dict
        :return: API response and HTTP status code
        :rtype: tuple
        """
        assert isinstance(user_id, int), "user_id must be an integer"
        assert isinstance(voiture_data, dict), "voiture_data must be a dictionary"

        resp, status = APIService.post(
            f"voiture/{user_id}",
            voiture_data
        )
        return resp, status

    @staticmethod
    def delete_voiture(user_id):
        """
        Delete the car associated with a user.

        :param user_id: User identifier
        :type user_id: int
        :return: API response and HTTP status code
        :rtype: tuple
        """
        assert isinstance(user_id, int), "user_id must be an integer"

        resp, status = APIService.delete(
            f"voiture/{user_id}"
        )
        return resp, status
