from core.database import Database
from models.trajet_model import TrajetModel

class ReservationModel:
    @staticmethod
    def create(trajet_id, passager_id, places_reservees):
        # Vérifier les places disponibles
        places_dispo = TrajetModel.get_places_disponibles(trajet_id)
        if places_dispo < places_reservees:
            return None
        
        query = '''INSERT INTO reservations (trajet_id, passager_id, places_reservees, statut)
                   VALUES (?, ?, ?, 'en_attente')'''
        res_id = Database.insert(query, (trajet_id, passager_id, places_reservees))
        return res_id
    
    @staticmethod
    def get_by_passager(passager_id):
        query = '''SELECT r.id, r.trajet_id, r.places_reservees, r.statut, r.created_at,
                   t.depart, t.arrivee, t.date_depart, t.heure_depart, t.prix_par_place,
                   u.nom, u.prenom, u.telephone, v.marque, v.modele
                   FROM reservations r
                   JOIN trajets t ON r.trajet_id = t.id
                   JOIN utilisateurs u ON t.utilisateur_id = u.id
                   LEFT JOIN voitures v ON t.voiture_id = v.id
                   WHERE r.passager_id = ?'''
        res = Database.execute(query, (passager_id,))
        return [dict(r) for r in res]
    
    @staticmethod
    def get_by_trajet(trajet_id):
        query = '''SELECT r.id, r.passager_id, r.places_reservees, r.statut, r.created_at,
                   u.nom, u.prenom, u.email, u.telephone
                   FROM reservations r
                   JOIN utilisateurs u ON r.passager_id = u.id
                   WHERE r.trajet_id = ?'''
        res = Database.execute(query, (trajet_id,))
        return [dict(r) for r in res]
    
    @staticmethod
    def accepter(reservation_id):
        Database.execute('UPDATE reservations SET statut = ? WHERE id = ?', ('acceptee', reservation_id))
    
    @staticmethod
    def refuser(reservation_id):
        Database.execute('UPDATE reservations SET statut = ? WHERE id = ?', ('refusee', reservation_id))

