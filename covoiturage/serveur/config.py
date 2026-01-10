import os
from datetime import timedelta

class Config:
    """
    Configuration class for the Flask application.

    This class centralizes all the configuration settings for the application, 
    including database paths, server settings, and JWT authentication parameters.

    Attributes:
        DATABASE_PATH (str): The path to the SQLite database file.
        DEBUG (bool): Enables or disables debug mode for the Flask application.
        HOST (str): The host address where the Flask application will run.
        PORT (int): The port number where the Flask application will listen.
        JWT_SECRET (str): The secret key used for signing JSON Web Tokens (JWT).
                          Defaults to 'dev-secret-key' if not set in the environment.
        JWT_EXPIRATION (timedelta): The expiration time for JWT tokens. Defaults to 24 hours.
    """
    DATABASE_PATH = 'covoiturage.db'
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    JWT_SECRET = os.getenv('JWT_SECRET', 'dev-secret-key')
    JWT_EXPIRATION = timedelta(hours=24)
