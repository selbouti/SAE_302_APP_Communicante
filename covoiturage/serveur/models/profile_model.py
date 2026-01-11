from core.database import Database


class ProfileModel:
    """
    Data access layer for user profile management.

    This model provides methods to retrieve and update user profile
    information, as well as to create or update the user's car data.
    """

    @staticmethod
    def get_profile(utilisateur_id):
        """
        Retrieve a user's profile information.

        :param utilisateur_id: User identifier
        :type utilisateur_id: int
        :return: Dictionary containing profile data or an error message
        :rtype: dict
        """
        user = Database.execute_one("""
            SELECT nom, prenom, email, telephone
            FROM utilisateurs
            WHERE id = ?
        """, (utilisateur_id,))

        if not user:
            return {"success": False, "message": "Utilisateur introuvable"}

        return {
            "success": True,
            "profile": {
                "nom": user["nom"],
                "prenom": user["prenom"],
                "email": user["email"],
                "telephone": user["telephone"]
            }
        }

    @staticmethod
    def update_profile(utilisateur_id, nom, prenom, email, telephone):
        """
        Update a user's profile information.

        :param utilisateur_id: User identifier
        :type utilisateur_id: int
        :param nom: Last name
        :type nom: str
        :param prenom: First name
        :type prenom: str
        :param email: Email address
        :type email: str
        :param telephone: Phone number
        :type telephone: str
        """
        Database.execute("""
            UPDATE utilisateurs
            SET nom=?, prenom=?, email=?, telephone=?
            WHERE id=?
        """, (nom, prenom, email, telephone, utilisateur_id))

    @staticmethod
    def save_voiture(utilisateur_id, voiture):
        """
        Create or update the car associated with a user.

        If a car already exists for the user, it is updated.
        Otherwise, a new car entry is created.

        :param utilisateur_id: User identifier
        :type utilisateur_id: int
        :param voiture: Car data
        :type voiture: dict
        """
        exists = Database.execute_one(
            "SELECT id FROM voitures WHERE utilisateur_id=?",
            (utilisateur_id,)
        )

        if exists:
            Database.execute("""
                UPDATE voitures
                SET marque=?, modele=?, couleur=?, plaque=?, places_totales=?
                WHERE utilisateur_id=?
            """, (
                voiture["marque"],
                voiture["modele"],
                voiture["couleur"],
                voiture["plaque"],
                voiture["places"],
                utilisateur_id
            ))
        else:
            Database.execute("""
                INSERT INTO voitures
                (utilisateur_id, marque, modele, couleur, plaque, places_totales)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                utilisateur_id,
                voiture["marque"],
                voiture["modele"],
                voiture["couleur"],
                voiture["plaque"],
                voiture["places"]
            ))
