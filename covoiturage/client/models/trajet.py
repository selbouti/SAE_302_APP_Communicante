class Trajet:
    def __init__(self, data):
        self.id = data["id"]
        self.utilisateur_id = data["utilisateur_id"]

        self.conducteur = f"{data['prenom']} {data['nom']}"
        self.depart = data["depart"]
        self.arrivee = data["arrivee"]

        self.heure_depart = data.get("heure_depart", "")
        self.heure_arrivee = data.get("heure_arrivee", "")

        self.voiture = f"{data.get('marque', '')} {data.get('modele', '')}".strip()
        self.prix = f"{data['prix_par_place']} €"
        self.places = data["places_disponibles"]

    # ----- règles métier -----

    def est_complet(self):
        return self.places <= 0
