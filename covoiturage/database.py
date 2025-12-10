# database.py
import mysql.connector

def get_connection():
    """
    Retourne une connexion MySQL à la base covoiturage
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # mets ton mot de passe MySQL si tu en as un
        database="covoiturage"
    )
