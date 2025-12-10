from database import get_connection


class ModeleUtilisateurs:
    """
    Modèle pour gérer les utilisateurs dans la base de données MySQL
    """

    def __init__(self):
        pass

    # ============================
    # ✅ CONNEXION UTILISATEUR
    # ============================
    def verifier_connexion(self, login, mot_de_passe):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
        SELECT * FROM Utilisateur
        WHERE login = %s AND mot_de_passe = %s
        """
        cursor.execute(sql, (login, mot_de_passe))
        utilisateur = cursor.fetchone()

        cursor.close()
        conn.close()

        return utilisateur  # None si échec, dict si OK

    # ============================
    # ✅ INSCRIPTION UTILISATEUR + VOITURE
    # =======
    def ajouter_utilisateur(self, infos):
        conn = get_connection()
        cursor = conn.cursor()

        # 1️⃣ Insertion Utilisateur
        sql_user = """
        INSERT INTO Utilisateur
        (login, mot_de_passe, nom, prenom, email, telephone, adresse, ville, cp)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        valeurs_user = (
            infos["login"],
            infos["mot_de_passe"],
            infos["nom"],
            infos["prenom"],
            infos["email"],
            infos["telephone"],
            infos["adresse"],
            infos["ville"],
            infos["cp"]
        )

        cursor.execute(sql_user, valeurs_user)
        id_user = cursor.lastrowid

        # 2️⃣ Insertion Voiture
        sql_voiture = """
        INSERT INTO Voiture
        (user_id, marque, modele, chevaux_fiscaux, motorisation, taux_co2, places_max)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        valeurs_voiture = (
            id_user,
            infos["marque"],
            infos["modele"],
            infos["chevaux_fiscaux"],
            infos["motorisation"],
            infos["taux_co2"],
            infos["places_max"]
        )

        cursor.execute(sql_voiture, valeurs_voiture)

        # 3️⃣ Insertion Emploi du Temps
        sql_edt = """
        INSERT INTO EmploiDuTemps (user_id, source_type, source)
        VALUES (%s,%s,%s)
        """
        cursor.execute(sql_edt, (
            id_user,
            infos["edt_source_type"],
            infos["edt_source"]
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return True

