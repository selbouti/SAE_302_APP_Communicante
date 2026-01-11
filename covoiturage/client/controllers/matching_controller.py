from services.api_service import APIService
from controllers.reservation_controller import ReservationController
from controllers.invitation_controller import InvitationController
from models.trajet import Trajet


class MatchingController:
    """
    Client-side controller for matching trips and related actions.
    """

    def __init__(self, user):
        """
        Initialize the controller with the current user.

        :param user: current user dict
        """
        self.user = user

    def charger_trajets_perso(self):
        """
        Fetch the current user's trips.
        """
        return APIService.get(
            f"mes_trajets/{self.user['id']}"
        )

    def charger_matching(self, trajet_id):
        """
        Fetch compatible trips for a given trip.

        :param trajet_id: trip identifier
        """
        resp, status = APIService.get(
            f"matching/{self.user['id']}?trajet_id={trajet_id}"
        )

        if status != 200:
            return None, status

        resp["trajets_compatibles"] = [
            Trajet(t) for t in resp["trajets_compatibles"]
        ]

        return resp, status

    def reserver(self, trajet_id):
        """
        Create a reservation for the given trip.

        :param trajet_id: trip identifier
        """
        return ReservationController.creer_reservation(
            trajet_id,
            self.user["id"],
            1
        )

    def inviter(self, passager_id, trajet_id):
        """
        Create an invitation for a passenger on a trip.

        :param passager_id: passenger identifier
        :param trajet_id: trip identifier
        """
        return InvitationController.creer_invitation(
            trajet_id,
            passager_id
        )

    def rechercher_conducteurs_marges(self, data):
        """
        Search for drivers using time margins.

        :param data: request payload for the margins search
        """
        return APIService.post(
            f"matching_marges/{self.user['id']}",
            data
        )

    @staticmethod
    def format_time(time_str):
        """
        Normalize a time string to HH:MM.

        :param time_str: raw time string
        """
        if not time_str:
            return ""
        parts = time_str.split(":")
        if len(parts) >= 2:
            return f"{parts[0].zfill(2)}:{parts[1].zfill(2)}"
        return time_str

    @staticmethod
    def build_marges_payload(trajet, marge_aller, marge_retour):
        """
        Build a margins search payload from a trip and selected margins.

        :param trajet: trip data dict
        :param marge_aller: outbound margin (minutes)
        :param marge_retour: return margin (minutes)
        """
        if not trajet:
            return None

        heure_aller = MatchingController.format_time(
            trajet.get("heure_depart", "")
        )
        heure_retour = MatchingController.format_time(
            trajet.get("heure_retour", "")
        ) or heure_aller

        return {
            "depart": trajet.get("depart", ""),
            "arrivee": trajet.get("arrivee", ""),
            "date": trajet.get("date_depart", ""),
            "heure_aller": heure_aller,
            "marge_aller": marge_aller,
            "heure_retour": heure_retour,
            "marge_retour": marge_retour,
        }

    @staticmethod
    def format_trajet_label(trajet):
        """
        Format a trip label for combo display.

        :param trajet: trip data dict
        """
        heure = trajet.get("heure_depart", "")
        heure_txt = f" a {heure}" if heure else ""
        return (
            f"{trajet['depart']} → {trajet['arrivee']} "
            f"le {trajet['date_depart']}{heure_txt} ({trajet['mode']})"
        )

    @staticmethod
    def format_trajet_info(trajet):
        """
        Format a short trip info string for display.

        :param trajet: trip data dict
        """
        heure_depart = trajet.get("heure_depart", "")
        heure_retour = trajet.get("heure_retour", "")
        heures = ""
        if heure_depart and heure_retour:
            heures = f"{heure_depart} / {heure_retour}"
        elif heure_depart:
            heures = heure_depart
        return (
            f"{trajet['depart']} → {trajet['arrivee']} "
            f"({trajet['mode']}) {heures}".strip()
        )
