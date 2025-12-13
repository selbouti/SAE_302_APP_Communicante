from config.database import get_connection

class UserModel:

    def authenticate(self, login, password):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT * FROM Utilisateur
            WHERE login=%s AND mot_de_passe=%s
        """, (login, password))

        user = cur.fetchone()
        cur.close()
        conn.close()
        return user

    def create_user(self, data):
        conn = get_connection()
        cur = conn.cursor()

        sql = """
        INSERT INTO Utilisateur
        (login, mot_de_passe, nom, prenom, email, telephone, adresse, ville, cp)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cur.execute(sql, (
            data["login"], data["mot_de_passe"], data["nom"], data["prenom"],
            data["email"], data["telephone"], data["adresse"], data["ville"], data["cp"]
        ))

        conn.commit()
        uid = cur.lastrowid
        cur.close()
        conn.close()
        return uid

    def update_user(self, user_id, data):
        conn = get_connection()
        cur = conn.cursor()

        sql = """
        UPDATE Utilisateur
        SET nom=%s, prenom=%s, email=%s, telephone=%s,
            adresse=%s, ville=%s, cp=%s
        WHERE id_user=%s
        """

        cur.execute(sql, (
            data["nom"], data["prenom"], data["email"], data["telephone"],
            data["adresse"], data["ville"], data["cp"], user_id
        ))

        conn.commit()
        cur.close()
        conn.close()

    def get_user(self, user_id):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM Utilisateur WHERE id_user=%s", (user_id,))
        user = cur.fetchone()

        cur.close()
        conn.close()
        return user
