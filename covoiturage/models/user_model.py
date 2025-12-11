from config.database import get_connection


class UserModel:
    """
    Accès aux données Utilisateur en base MySQL.
    """

    def create_user(self, data: dict) -> bool:
        """
        Crée un utilisateur en base.
        data = {
            "nom", "prenom", "login", "mot_de_passe",
            "email", "telephone", "adresse", "ville", "cp"
        }
        """
        conn = get_connection()
        if conn is None:
            return False

        # Vérifier que le login n'existe pas déjà
        if self.login_exists(data["login"], conn):
            conn.close()
            return False

        cursor = conn.cursor()
        sql = """
            INSERT INTO Utilisateur
            (nom, prenom, login, mot_de_passe, email, telephone, adresse, ville, cp)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (
            data["nom"], data["prenom"], data["login"], data["mot_de_passe"],
            data["email"], data["telephone"], data["adresse"],
            data["ville"], data["cp"]
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def authenticate(self, login: str, mdp: str) -> bool:
        """
        Vérifie si (login, mot_de_passe) correspond à un utilisateur existant.
        """
        conn = get_connection()
        if conn is None:
            return False

        cursor = conn.cursor(dictionary=True)
        sql = "SELECT id_user FROM Utilisateur WHERE login = %s AND mot_de_passe = %s"
        cursor.execute(sql, (login, mdp))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user is not None

    def login_exists(self, login: str, conn=None) -> bool:
        """
        Vérifie si un login est déjà pris.
        Si une connexion est fournie, on la réutilise (sinon on en crée une).
        """
        close_conn = False
        if conn is None:
            conn = get_connection()
            if conn is None:
                return False
            close_conn = True

        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM Utilisateur WHERE login = %s"
        cursor.execute(sql, (login,))
        (count,) = cursor.fetchone()
        cursor.close()
        if close_conn:
            conn.close()
        return count > 0
