from services.api_service import APIService


class ProfileController:
    """
    Client-side controller responsible for user profile management.

    This controller communicates exclusively with the server REST API
    and does not rely on any local model.
    """

    @staticmethod
    def get_profile(user_id: int):
        """
        Retrieve a user's profile from the API.

        :param user_id: Unique user identifier
        :type user_id: int
        :return: API response and HTTP status code
        :rtype: tuple
        """
        assert isinstance(user_id, int), "user_id must be an integer"
        assert user_id > 0, "user_id must be positive"

        return APIService.get(f"profile/{user_id}")

    @staticmethod
    def update_profile(user_id: int, profile_data: dict):
        """
        Update a user's profile through the API.

        :param user_id: Unique user identifier
        :type user_id: int
        :param profile_data: Profile data to update
        :type profile_data: dict
        :return: API response and HTTP status code
        :rtype: tuple
        """
        assert isinstance(user_id, int), "user_id must be an integer"
        assert isinstance(profile_data, dict), "profile_data must be a dictionary"

        return APIService.post(f"profile/{user_id}", profile_data)
