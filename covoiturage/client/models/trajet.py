class Trajet:
    """
    Client-side trip model for matching results.
    """

    def __init__(self, data):
        """
        Build a Trajet instance from API data.

        :param data: trip data dict
        """
        self.id = data["id"]
        self.utilisateur_id = data["utilisateur_id"]

        self.conducteur = f"{data['prenom']} {data['nom']}"
        self.depart = data["depart"]
        self.arrivee = data["arrivee"]

        self.heure_depart = data.get("heure_depart", "")
        self.heure_retour = data.get("heure_retour", "")

        self.voiture = f"{data.get('marque', '')} {data.get('modele', '')}".strip()
        self.prix = f"{data['prix_par_place']} €"
        self.places = data["places_disponibles"]

    # ----- règles métier -----

    def est_complet(self):
        """
        Return True when there are no available seats.
        """
        return self.places <= 0
