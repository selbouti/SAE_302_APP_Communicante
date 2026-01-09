from core.database import Database

class VoitureModel:

    @staticmethod
    def create(utilisateur_id, data):
        query = """
            INSERT INTO voitures (
                utilisateur_id,
                marque,
                modele,
                chevaux_fiscaux,
                taux_co2,
                places_totales,
                motorisation
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return Database.insert(
            query,
            (
                utilisateur_id,
                data["marque"],
                data["modele"],
                data["chevaux_fiscaux"],
                data["taux_co2"],
                data["places_max"],
                data["motorisation"]
            )
        )

    @staticmethod
    def get_by_user(user_id):
        query = "SELECT * FROM voitures WHERE utilisateur_id = ?"
        rows = Database.execute(query, (user_id,))
        return [dict(r) for r in rows]

    @staticmethod
    def delete_by_user(user_id):
        Database.execute(
            "DELETE FROM voitures WHERE utilisateur_id = ?",
            (user_id,)
        )
