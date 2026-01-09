from core.database import Database

class TrajetModel:
    @staticmethod
    def create(
        utilisateur_id,
        voiture_id,
        depart,
        arrivee,
        date_depart,
        jour_semaine,
        heure_depart,
        heure_retour,
        prix_par_place,
        mode
    ):
        query = '''INSERT INTO trajets (utilisateur_id, voiture_id, depart, arrivee, date_depart, 
                   jour_semaine, heure_depart, heure_retour, prix_par_place, mode)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        trajet_id = Database.insert(
            query,
            (
                utilisateur_id,
                voiture_id,
                depart,
                arrivee,
                date_depart,
                jour_semaine,
                heure_depart,
                heure_retour,
                prix_par_place,
                mode
            )
        )
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
    def delete_by_user(user_id):
  	 Database.execute("DELETE FROM trajets WHERE utilisateur_id = ?", (user_id,))


    
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

    @staticmethod
    def _time_to_minutes(time_str):
        try:
            parts = time_str.split(":")
            if len(parts) < 2:
                return None
            hours = int(parts[0])
            minutes = int(parts[1])
        except (ValueError, AttributeError):
            return None

        if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
            return None
        return hours * 60 + minutes

    @staticmethod
    def _minutes_to_time_str(minutes):
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"

    @staticmethod
    def _time_window(time_str, margin_minutes):
        base = TrajetModel._time_to_minutes(time_str)
        if base is None:
            return None, None
        start = max(0, base - margin_minutes)
        end = min(23 * 60 + 59, base + margin_minutes)
        return (
            TrajetModel._minutes_to_time_str(start),
            TrajetModel._minutes_to_time_str(end),
        )

    @staticmethod
    def count_trajets_by_users(user_ids):
        if not user_ids:
            return {}

        placeholders = ",".join(["?"] * len(user_ids))
        query = f'''
            SELECT utilisateur_id, COUNT(*) as nb
            FROM trajets
            WHERE utilisateur_id IN ({placeholders})
            AND mode = 'conducteur'
            GROUP BY utilisateur_id
        '''
        rows = Database.execute(query, tuple(user_ids))
        return {row["utilisateur_id"]: row["nb"] for row in rows}

    @staticmethod
    def search_conducteurs_marges(
        depart,
        arrivee,
        date_depart,
        heure_aller,
        marge_aller,
        heure_retour,
        marge_retour,
        user_id
    ):
        start_aller, end_aller = TrajetModel._time_window(
            heure_aller, marge_aller
        )
        start_retour, end_retour = TrajetModel._time_window(
            heure_retour, marge_retour
        )
        if not start_aller or not start_retour:
            return []

        target_aller = TrajetModel._time_to_minutes(heure_aller)
        target_retour = TrajetModel._time_to_minutes(heure_retour)
        if target_aller is None or target_retour is None:
            return []

        base_query = '''
            SELECT
                t.id as trajet_id,
                t.utilisateur_id,
                t.heure_depart,
                t.heure_retour,
                u.nom,
                u.prenom,
                v.places_totales,
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
            WHERE t.mode = 'conducteur'
            AND DATE(t.date_depart) = DATE(?)
            AND LOWER(t.depart) LIKE LOWER(?)
            AND LOWER(t.arrivee) LIKE LOWER(?)
            AND t.utilisateur_id != ?
            GROUP BY t.id
            HAVING places_disponibles > 0
        '''

        trajets = Database.execute(
            base_query,
            (
                date_depart,
                f'%{depart}%',
                f'%{arrivee}%',
                user_id,
            )
        )

        start_aller_min = TrajetModel._time_to_minutes(start_aller)
        end_aller_min = TrajetModel._time_to_minutes(end_aller)
        start_retour_min = TrajetModel._time_to_minutes(start_retour)
        end_retour_min = TrajetModel._time_to_minutes(end_retour)
        if None in (
            start_aller_min,
            end_aller_min,
            start_retour_min,
            end_retour_min
        ):
            return []

        best_by_user = {}
        for trajet in trajets:
            data = dict(trajet)
            uid = data.get("utilisateur_id")
            if uid is None:
                continue

            aller_min = TrajetModel._time_to_minutes(
                data.get("heure_depart", "")
            )
            retour_min = TrajetModel._time_to_minutes(
                data.get("heure_retour", "") or data.get("heure_depart", "")
            )
            if aller_min is None or retour_min is None:
                continue
            if not (start_aller_min <= aller_min <= end_aller_min):
                continue
            if not (start_retour_min <= retour_min <= end_retour_min):
                continue

            delta = abs(aller_min - target_aller) + abs(retour_min - target_retour)
            if uid not in best_by_user or delta < best_by_user[uid]["delta"]:
                best_by_user[uid] = {"data": data, "delta": delta}

        user_ids = list(best_by_user.keys())
        counts = TrajetModel.count_trajets_by_users(user_ids)

        results = []
        for uid, payload in best_by_user.items():
            data = payload["data"]
            results.append({
                "conducteur_id": uid,
                "nom": data.get("nom", ""),
                "prenom": data.get("prenom", ""),
                "trajet_id": data.get("trajet_id"),
                "heure_aller": data.get("heure_depart", ""),
                "heure_retour": data.get("heure_retour", ""),
                "nb_trajets": counts.get(uid, 0),
                "places_dispo": data.get("places_disponibles", 0),
            })

        return results
