class Trajet:
    """
    Client-side model representing a trip used in matching results.
    """

    def __init__(self, data):
        """
        Build a Trajet instance from API data.

        :param data: Trip data dictionary
        :type data: dict
        """
        assert isinstance(data, dict)
        assert "id" in data
        assert "utilisateur_id" in data

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

    def est_complet(self):
        """
        Return True if no seats are available.
        """
        return self.places <= 0

