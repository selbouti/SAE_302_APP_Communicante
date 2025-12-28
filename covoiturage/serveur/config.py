import os
from datetime import timedelta

class Config:
    DATABASE_PATH = 'covoiturage.db'
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    JWT_SECRET = os.getenv('JWT_SECRET', 'dev-secret-key')
    JWT_EXPIRATION = timedelta(hours=24)
