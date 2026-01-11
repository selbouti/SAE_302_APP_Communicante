# ============= models/reservation_model.py =============


class Reservation:
    """
    Client-side model representing a reservation.
    """

    def __init__(
        self,
        id,
        trajet_id,
        depart,
        arrivee,
        places_reservees,
        statut,
        created_at,
        prix_par_place,
        prenom,
        nom
    ):
        """
        Initialize a Reservation instance.

        :param id: Reservation identifier
        :type id: int
        :param trajet_id: Related trip identifier
        :type trajet_id: int
        :param depart: Departure location
        :type depart: str
        :param arrivee: Arrival location
        :type arrivee: str
        :param places_reservees: Number of reserved seats
        :type places_reservees: int
        :param statut: Reservation status
        :type statut: str
        """
        assert isinstance(id, int)
        assert isinstance(trajet_id, int)
        assert isinstance(places_reservees, int)

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
        """
        Return a formatted string representation of the reservation.
        """
        return (
            f"{self.depart} → {self.arrivee} | "
            f"{self.prenom} {self.nom} | "
            f"{self.places_reservees} place(s) | {self.statut}"
        )


