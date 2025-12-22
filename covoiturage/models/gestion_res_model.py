# models/reservation.py
"""
Modèle pour la gestion des réservations
"""
from datetime import datetime
from typing import Optional, List, Dict

class Reservation:
    """Classe représentant une réservation"""
    
    def __init__(self, id_reservation: Optional[int] = None, 
                 id_trajet: int = None,
                 id_passager: int = None,
                 nb_places: int = 1,
                 statut: str = 'en_attente',
                 date_reservation: Optional[datetime] = None):
        """
        Initialise une réservation
        
        Args:
            id_reservation: Identifiant unique de la réservation
            id_trajet: ID du trajet concerné
            id_passager: ID de l'utilisateur passager
            nb_places: Nombre de places réservées
            statut: Statut de la réservation (en_attente, confirmee, annulee)
            date_reservation: Date de création de la réservation
        """
        self.id_reservation = id_reservation
        self.id_trajet = id_trajet
        self.id_passager = id_passager
        self.nb_places = nb_places
        self.statut = statut
        self.date_reservation = date_reservation or datetime.now()
    
    def to_dict(self) -> Dict:
        """Convertit l'objet en dictionnaire pour JSON"""
        return {
            'id_reservation': self.id_reservation,
            'id_trajet': self.id_trajet,
            'id_passager': self.id_passager,
            'nb_places': self.nb_places,
            'statut': self.statut,
            'date_reservation': self.date_reservation.isoformat() if self.date_reservation else None
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Reservation':
        """Crée un objet Reservation depuis un dictionnaire"""
        return Reservation(
            id_reservation=data.get('id_reservation'),
            id_trajet=data.get('id_trajet'),
            id_passager=data.get('id_passager'),
            nb_places=data.get('nb_places', 1),
            statut=data.get('statut', 'en_attente'),
            date_reservation=datetime.fromisoformat(data['date_reservation']) 
                           if data.get('date_reservation') else None
        )


class ReservationDAO:
    """Data Access Object pour les réservations"""
    
    def __init__(self, db_connection):
        """
        Initialise le DAO avec une connexion à la base de données
        
        Args:
            db_connection: Connexion à la base de données
        """
        self.db = db_connection
    
    def creer_reservation(self, reservation: Reservation) -> Optional[int]:
        """
        Crée une nouvelle réservation en base de données
        
        Args:
            reservation: Objet Reservation à créer
            
        Returns:
            ID de la réservation créée ou None si échec
        """
        try:
            cursor = self.db.cursor()
            query = """
                INSERT INTO reservation (id_trajet, id_passager, nb_places, statut, date_reservation)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                reservation.id_trajet,
                reservation.id_passager,
                reservation.nb_places,
                reservation.statut,
                reservation.date_reservation
            ))
            self.db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erreur lors de la création de la réservation: {e}")
            self.db.rollback()
            return None
    
    def annuler_reservation(self, id_reservation: int) -> bool:
        """
        Annule une réservation (met le statut à 'annulee')
        
        Args:
            id_reservation: ID de la réservation à annuler
            
        Returns:
            True si succès, False sinon
        """
        try:
            cursor = self.db.cursor()
            query = """
                UPDATE reservation 
                SET statut = 'annulee'
                WHERE id_reservation = ?
            """
            cursor.execute(query, (id_reservation,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de l'annulation de la réservation: {e}")
            self.db.rollback()
            return False
    
    def confirmer_reservation(self, id_reservation: int) -> bool:
        """
        Confirme une réservation
        
        Args:
            id_reservation: ID de la réservation à confirmer
            
        Returns:
            True si succès, False sinon
        """
        try:
            cursor = self.db.cursor()
            query = """
                UPDATE reservation 
                SET statut = 'confirmee'
                WHERE id_reservation = ?
            """
            cursor.execute(query, (id_reservation,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la confirmation de la réservation: {e}")
            self.db.rollback()
            return False
    
    def get_reservation_by_id(self, id_reservation: int) -> Optional[Reservation]:
        """
        Récupère une réservation par son ID
        
        Args:
            id_reservation: ID de la réservation
            
        Returns:
            Objet Reservation ou None si non trouvée
        """
        try:
            cursor = self.db.cursor()
            query = """
                SELECT id_reservation, id_trajet, id_passager, nb_places, statut, date_reservation
                FROM reservation
                WHERE id_reservation = ?
            """
            cursor.execute(query, (id_reservation,))
            row = cursor.fetchone()
            
            if row:
                return Reservation(
                    id_reservation=row[0],
                    id_trajet=row[1],
                    id_passager=row[2],
                    nb_places=row[3],
                    statut=row[4],
                    date_reservation=datetime.fromisoformat(row[5]) if row[5] else None
                )
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération de la réservation: {e}")
            return None
    
    def get_reservations_by_trajet(self, id_trajet: int) -> List[Reservation]:
        """
        Récupère toutes les réservations d'un trajet
        
        Args:
            id_trajet: ID du trajet
            
        Returns:
            Liste des réservations
        """
        try:
            cursor = self.db.cursor()
            query = """
                SELECT id_reservation, id_trajet, id_passager, nb_places, statut, date_reservation
                FROM reservation
                WHERE id_trajet = ? AND statut != 'annulee'
                ORDER BY date_reservation DESC
            """
            cursor.execute(query, (id_trajet,))
            rows = cursor.fetchall()
            
            reservations = []
            for row in rows:
                reservations.append(Reservation(
                    id_reservation=row[0],
                    id_trajet=row[1],
                    id_passager=row[2],
                    nb_places=row[3],
                    statut=row[4],
                    date_reservation=datetime.fromisoformat(row[5]) if row[5] else None
                ))
            return reservations
        except Exception as e:
            print(f"Erreur lors de la récupération des réservations du trajet: {e}")
            return []
    
    def get_reservations_by_passager(self, id_passager: int) -> List[Reservation]:
        """
        Récupère toutes les réservations d'un passager
        
        Args:
            id_passager: ID du passager
            
        Returns:
            Liste des réservations
        """
        try:
            cursor = self.db.cursor()
            query = """
                SELECT id_reservation, id_trajet, id_passager, nb_places, statut, date_reservation
                FROM reservation
                WHERE id_passager = ?
                ORDER BY date_reservation DESC
            """
            cursor.execute(query, (id_passager,))
            rows = cursor.fetchall()
            
            reservations = []
            for row in rows:
                reservations.append(Reservation(
                    id_reservation=row[0],
                    id_trajet=row[1],
                    id_passager=row[2],
                    nb_places=row[3],
                    statut=row[4],
                    date_reservation=datetime.fromisoformat(row[5]) if row[5] else None
                ))
            return reservations
        except Exception as e:
            print(f"Erreur lors de la récupération des réservations du passager: {e}")
            return []
    
    def verifier_disponibilite(self, id_trajet: int, nb_places_demandees: int) -> bool:
        """
        Vérifie si le nombre de places demandées est disponible pour un trajet
        
        Args:
            id_trajet: ID du trajet
            nb_places_demandees: Nombre de places à réserver
            
        Returns:
            True si places disponibles, False sinon
        """
        try:
            cursor = self.db.cursor()
            
            # Récupérer le nombre de places total du trajet
            query_trajet = "SELECT nb_places FROM trajet WHERE id_trajet = ?"
            cursor.execute(query_trajet, (id_trajet,))
            row = cursor.fetchone()
            
            if not row:
                return False
            
            places_totales = row[0]
            
            # Calculer le nombre de places déjà réservées (statut confirmée ou en_attente)
            query_reservations = """
                SELECT COALESCE(SUM(nb_places), 0)
                FROM reservation
                WHERE id_trajet = ? AND statut IN ('confirmee', 'en_attente')
            """
            cursor.execute(query_reservations, (id_trajet,))
            places_reservees = cursor.fetchone()[0]
            
            places_disponibles = places_totales - places_reservees
            
            return places_disponibles >= nb_places_demandees
        except Exception as e:
            print(f"Erreur lors de la vérification de disponibilité: {e}")
            return False