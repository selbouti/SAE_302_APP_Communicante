from core.database import Database

class VoitureModel:
    @staticmethod
    def create(utilisateur_id, marque, modele, couleur, plaque, places_totales):
        query = '''INSERT INTO voitures (utilisateur_id, marque, modele, couleur, plaque, places_totales)
                   VALUES (?, ?, ?, ?, ?, ?)'''
        voiture_id = Database.insert(query, (utilisateur_id, marque, modele, couleur, plaque, places_totales))
        return voiture_id
    
    @staticmethod
    def get_by_user(user_id):
        query = 'SELECT * FROM voitures WHERE utilisateur_id = ?'
        voitures = Database.execute(query, (user_id,))
        return [dict(v) for v in voitures]
    
    @staticmethod
    def get_by_id(voiture_id):
        query = 'SELECT * FROM voitures WHERE id = ?'
        voiture = Database.execute_one(query, (voiture_id,))
        return dict(voiture) if voiture else None
    