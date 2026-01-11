from flask import Blueprint, request, jsonify
from models.user_model import UserModel

auth_bp = Blueprint("auth", __name__)
user_model = UserModel()


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user.

    This endpoint receives login credentials, validates them against
    the user model, and returns the authenticated user information
    if the credentials are valid.

    Request JSON body:
        - login (str): User login or email
        - password (str): User password

    Responses:
        200 OK:
            Returns the authenticated user data as JSON.
        401 Unauthorized:
            Returned when the credentials are invalid.

    :return: JSON response with user data or error message
    :rtype: flask.Response
    """
    data = request.json

    user = user_model.authenticate(
        data.get("login"),
        data.get("password")
    )

    if not user:
        return jsonify({"error": "Identifiants invalides"}), 401

    return jsonify(user), 200
