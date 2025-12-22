import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "covoiturage_app",
    "password": "MotDePasseSuperSecure123!",  # TODO: adapter
    "database": "covoiturage",
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
    

def get_trajet(self, id_trajet):
     cursor = self.conn.cursor(dictionary=True)
     cursor.execute(
        "SELECT * FROM trajet WHERE id_trajet = %s",
        (id_trajet,)
     )
     return cursor.fetchone()

def insert_reservation(self, id_trajet, id_passager, statut):
     cursor = self.conn.cursor()
     cursor.execute(
        "INSERT INTO reservation (id_trajet, id_passager, statut) VALUES (%s, %s, %s)",
        (id_trajet, id_passager, statut)
     )
     self.conn.commit()
