from core.database import Database

class ProfileModel:

    @staticmethod
    def get_profile(utilisateur_id):
        user = Database.execute_one("""
            SELECT id, nom, prenom, email, telephone
            FROM utilisateurs
            WHERE id = ?
        """, (utilisateur_id,))

        if not user:
            return None

        voiture = Database.execute_one("""
            SELECT marque, modele, couleur, plaque, places_totales
            FROM voitures
            WHERE utilisateur_id = ?
        """, (utilisateur_id,))

        return {
            "id": user["id"],
            "nom": user["nom"],
            "prenom": user["prenom"],
            "email": user["email"],
            "telephone": user["telephone"],
            "voiture": dict(voiture) if voiture else None
        }

    @staticmethod
    def update_profile(utilisateur_id, nom, prenom, email, telephone):
        Database.execute("""
            UPDATE utilisateurs
            SET nom=?, prenom=?, email=?, telephone=?
            WHERE id=?
        """, (nom, prenom, email, telephone, utilisateur_id))

    @staticmethod
    def save_voiture(utilisateur_id, voiture):
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
