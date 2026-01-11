import os
from datetime import timedelta


class Config:
    """
    Configuration class for the Flask application.

    This class centralizes all configuration settings used by the server-side
    Flask application of the carpooling project.

    It includes:
    - database configuration
    - server network settings
    - debug mode
    - JWT authentication parameters

    All attributes are class-level constants and can be accessed directly
    without instantiating the class.
    """

    #: Path to the SQLite database file
    DATABASE_PATH = 'covoiturage.db'

    #: Enable or disable Flask debug mode
    DEBUG = True

    #: Host address on which the Flask server will run
    HOST = '0.0.0.0'

    #: Port number used by the Flask server
    PORT = 5000

    #: Secret key used to sign JSON Web Tokens (JWT)
    #: Can be overridden using the environment variable ``JWT_SECRET``
    JWT_SECRET = os.getenv('JWT_SECRET', 'dev-secret-key')

    #: Expiration duration for JWT tokens (default: 24 hours)
    JWT_EXPIRATION = timedelta(hours=24)
