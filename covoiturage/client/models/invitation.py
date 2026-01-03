class Invitation:
    """Modèle représentant une invitation"""
    def __init__(self, id, trajet_id, depart, arrivee, statut, created_at, prenom, nom):
        self.id = id
        self.trajet_id = trajet_id
        self.depart = depart
        self.arrivee = arrivee
        self.statut = statut
        self.created_at = created_at
        self.prenom = prenom
        self.nom = nom
    
    def afficher(self):
        return f"{self.depart} → {self.arrivee} | {self.prenom} {self.nom} | {self.statut}"