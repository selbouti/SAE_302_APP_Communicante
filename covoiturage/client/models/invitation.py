class Invitation:
    """
    Client-side model representing an invitation.
    """

    def __init__(self, id, trajet_id, depart, arrivee, statut, created_at, prenom, nom):
        """
        Initialize an Invitation instance.

        :param id: Invitation identifier
        :type id: int
        :param trajet_id: Related trip identifier
        :type trajet_id: int
        :param depart: Departure location
        :type depart: str
        :param arrivee: Arrival location
        :type arrivee: str
        :param statut: Invitation status
        :type statut: str
        :param created_at: Creation timestamp
        :type created_at: str
        :param prenom: Passenger first name
        :type prenom: str
        :param nom: Passenger last name
        :type nom: str
        """
        assert isinstance(id, int)
        assert isinstance(trajet_id, int)
        assert isinstance(depart, str)
        assert isinstance(arrivee, str)
        assert isinstance(statut, str)

        self.id = id
        self.trajet_id = trajet_id
        self.depart = depart
        self.arrivee = arrivee
        self.statut = statut
        self.created_at = created_at
        self.prenom = prenom
        self.nom = nom

    def afficher(self):
        """
        Return a formatted string representation of the invitation.
        """
        return f"{self.depart} → {self.arrivee} | {self.prenom} {self.nom} | {self.statut}"


