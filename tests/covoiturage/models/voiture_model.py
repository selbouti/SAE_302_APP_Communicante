from config.database import get_connection


class VoitureModel:
    """
    Modèle pour la gestion des voitures des utilisateurs.
    """

    # -----------------------------
    #  Récupérer la voiture d'un utilisateur
    # -----------------------------
    def get_user_voiture(self, user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT * FROM Voiture
            WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        voiture = cursor.fetchone()

        cursor.close()
        conn.close()
        return voiture

    # -----------------------------
    #  Ajouter une voiture
    # -----------------------------
    def add_voiture(self, user_id, data):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO Voiture
            (user_id, marque, modele, chevaux_fiscaux, motorisation, taux_co2, places_max)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            user_id,
            data["marque"],
            data["modele"],
            data["chevaux_fiscaux"],
            data["motorisation"],
            data["taux_co2"],
            data["places_max"]
        ))

        conn.commit()
        cursor.close()
        conn.close()

    # -----------------------------
    #  Mettre à jour une voiture
    # -----------------------------
    def update_voiture(self, voiture_id, data):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE Voiture
            SET marque = %s,
                modele = %s,
                chevaux_fiscaux = %s,
                motorisation = %s,
                taux_co2 = %s,
                places_max = %s
            WHERE id_voiture = %s
        """

        cursor.execute(query, (
            data["marque"],
            data["modele"],
            data["chevaux_fiscaux"],
            data["motorisation"],
            data["taux_co2"],
            data["places_max"],
            voiture_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

    # -----------------------------
    #  Supprimer une voiture
    # -----------------------------
    def delete_voiture(self, voiture_id):
        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM Voiture WHERE id_voiture = %s"
        cursor.execute(query, (voiture_id,))

        conn.commit()
        cursor.close()
        conn.close()
