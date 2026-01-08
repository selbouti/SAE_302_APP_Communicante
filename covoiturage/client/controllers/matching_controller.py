from services.api_service import APIService
from controllers.reservation_controller import ReservationController
from controllers.invitation_controller import InvitationController
from models.trajet import Trajet


class MatchingController:
    def __init__(self, user):
        self.user = user

    def charger_trajets_perso(self):
        return APIService.get(
            f"mes_trajets/{self.user['id']}"
        )

    def charger_matching(self, trajet_id):
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
        return ReservationController.creer_reservation(
            trajet_id,
            self.user["id"],
            1
        )

    def inviter(self, passager_id, trajet_id):
        return InvitationController.creer_invitation(
            trajet_id,
            passager_id
        )

    def rechercher_conducteurs_marges(self, data):
        return APIService.post(
            f"matching_marges/{self.user['id']}",
            data
        )
