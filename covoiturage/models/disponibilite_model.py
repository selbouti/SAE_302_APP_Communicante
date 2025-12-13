from config.database import get_connection

class DisponibiliteModel:

    def get_indispo(self, user_id):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM Disponibilite WHERE user_id=%s", (user_id,))
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return rows

    def add_indispo(self, user_id, data):
        conn = get_connection()
        cur = conn.cursor()

        sql = """
        INSERT INTO Disponibilite (user_id, date_dispo, heure_debut, heure_fin)
        VALUES (%s,%s,%s,%s)
        """

        cur.execute(sql, (
            user_id, data["date_dispo"], data["heure_debut"], data["heure_fin"]
        ))

        conn.commit()
        cur.close()
        conn.close()

    def delete_indispo(self, dispo_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM Disponibilite WHERE id_dispo=%s", (dispo_id,))
        conn.commit()

        cur.close()
        conn.close()
