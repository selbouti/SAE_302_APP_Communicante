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
    def get_trajet_by_id(trajet_id, user_id):
        query = '''
            SELECT 
                t.*,
                v.marque,
                v.modele,
                v.couleur,
                v.plaque,
                v.places_totales,
                (
                    SELECT COALESCE(SUM(r.places_reservees), 0)
                    FROM reservations r
                    WHERE r.trajet_id = t.id
                    AND r.statut = 'acceptee'
                ) AS places_reservees
            FROM trajets t
            LEFT JOIN voitures v ON t.voiture_id = v.id
            WHERE t.id = ?
            AND t.utilisateur_id = ?
            LIMIT 1
        '''
        trajet = Database.execute_one(query, (trajet_id, user_id))
        return dict(trajet) if trajet else None

    @staticmethod
    def search_matching(depart, arrivee, date_depart, mode_inverse, user_id):
        base_query = '''
            SELECT
                t.*,
                u.nom, u.prenom, u.email, u.telephone,
                v.marque, v.modele, v.places_totales,
                (v.places_totales - COALESCE(SUM(
                    CASE
                        WHEN r.statut = 'acceptee' THEN r.places_reservees
                        ELSE 0
                    END
                ), 0)) AS places_disponibles
            FROM trajets t
            JOIN utilisateurs u ON t.utilisateur_id = u.id
            LEFT JOIN voitures v ON t.voiture_id = v.id
            LEFT JOIN reservations r ON t.id = r.trajet_id
            WHERE LOWER(t.depart) LIKE LOWER(?)
            AND LOWER(t.arrivee) LIKE LOWER(?)
            AND DATE(t.date_depart) = DATE(?)
            AND t.mode = ?
            AND t.utilisateur_id != ?
            GROUP BY t.id
        '''
        
        # Ajouter HAVING seulement si on cherche des trajets en mode passager
        if mode_inverse == 'conducteur':
            base_query += ' HAVING places_disponibles > 0'
        
        trajets = Database.execute(
            base_query,
            (f'%{depart}%', f'%{arrivee}%', date_depart, mode_inverse, user_id)
        )
        
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

    @staticmethod
    def update_mode(trajet_id, mode):
        """Met à jour le mode (conducteur/passager) pour un trajet."""
        Database.execute('UPDATE trajets SET mode=? WHERE id=?', (mode, trajet_id))
        return True
