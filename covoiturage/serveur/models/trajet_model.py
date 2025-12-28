from core.database import Database

class TrajetModel:
    @staticmethod
    def create(utilisateur_id, voiture_id, depart, arrivee, date_depart, jour_semaine, 
               heure_depart, prix_par_place, mode):
        query = '''INSERT INTO trajets (utilisateur_id, voiture_id, depart, arrivee, date_depart, 
                   jour_semaine, heure_depart, prix_par_place, mode)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        trajet_id = Database.insert(query, (utilisateur_id, voiture_id, depart, arrivee, date_depart, 
                                            jour_semaine, heure_depart, prix_par_place, mode))
        return trajet_id
    
    @staticmethod
    def get_by_user(user_id):
        query = '''SELECT t.*, v.marque, v.modele, v.places_totales,
                   (SELECT COUNT(*) FROM reservations WHERE trajet_id = t.id) as places_reservees
                   FROM trajets t
                   LEFT JOIN voitures v ON t.voiture_id = v.id
                   WHERE t.utilisateur_id = ?'''
        trajets = Database.execute(query, (user_id,))
        return [dict(t) for t in trajets]
    
    @staticmethod
    def get_first_trajet(user_id):
        query = '''SELECT t.*, v.marque, v.modele, v.places_totales,
                   (SELECT COUNT(*) FROM reservations WHERE trajet_id = t.id) as places_reservees
                   FROM trajets t
                   LEFT JOIN voitures v ON t.voiture_id = v.id
                   WHERE t.utilisateur_id = ? LIMIT 1'''
        trajet = Database.execute_one(query, (user_id,))
        return dict(trajet) if trajet else None
    
    @staticmethod
    def search_matching(depart, arrivee, date_depart, mode_inverse):
        query = '''SELECT t.*, u.nom, u.prenom, u.email, u.telephone, v.marque, v.modele,
                   v.places_totales,
                   (v.places_totales - COALESCE(SUM(r.places_reservees), 0)) as places_disponibles
                   FROM trajets t
                   JOIN utilisateurs u ON t.utilisateur_id = u.id
                   LEFT JOIN voitures v ON t.voiture_id = v.id
                   LEFT JOIN reservations r ON t.id = r.trajet_id
                   WHERE LOWER(t.depart) LIKE LOWER(?)
                   AND LOWER(t.arrivee) LIKE LOWER(?)
                   AND t.date_depart = ?
                   AND t.mode = ?
                   GROUP BY t.id
                   HAVING places_disponibles > 0'''
        trajets = Database.execute(query, (f'%{depart}%', f'%{arrivee}%', date_depart, mode_inverse))
        return [dict(t) for t in trajets]
    
    @staticmethod
    def get_places_disponibles(trajet_id):
        """Calcule le nombre de places disponibles"""
        query = '''SELECT v.places_totales,
                   COALESCE(SUM(r.places_reservees), 0) as places_reservees
                   FROM trajets t
                   LEFT JOIN voitures v ON t.voiture_id = v.id
                   LEFT JOIN reservations r ON t.id = r.trajet_id
                   WHERE t.id = ?
                   GROUP BY t.id'''
        result = Database.execute_one(query, (trajet_id,))
        if result:
            total = result['places_totales']
            reservees = result['places_reservees']
            return total - reservees
        return 0
    
    @staticmethod
    def delete(trajet_id):
        Database.execute('DELETE FROM trajets WHERE id=?', (trajet_id,))