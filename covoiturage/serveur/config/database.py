import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "covoiturage_app",
    "password": "MotDePasseSuperSecure123!",  # TODO: adapter
    "database": "covoiturage_2",
}


def get_connection():
    """
    Ouvre une connexion MySQL vers la base 'covoiturage'.
    Retourne None en cas d'échec.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(" Erreur de connexion MySQL :", e)
        return None
    

