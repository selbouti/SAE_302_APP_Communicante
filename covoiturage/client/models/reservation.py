# ============= models/reservation_model.py =============
class Reservation:
    """Modèle représentant une réservation"""
    def __init__(self, id, trajet_id, depart, arrivee, places_reservees, statut, created_at, prix_par_place, prenom, nom):
        self.id = id
        self.trajet_id = trajet_id
        self.depart = depart
        self.arrivee = arrivee
        self.places_reservees = places_reservees
        self.statut = statut
        self.created_at = created_at
        self.prix_par_place = prix_par_place
        self.prenom = prenom
        self.nom = nom
    
    def afficher(self):
        return f"{self.depart} → {self.arrivee} | {self.prenom} {self.nom} | {self.places_reservees} place(s) | {self.statut}"


