from services.api_service import APIService
from models.invitation import Invitation

class InvitationController:
    """
    Manages the logic for invitations on the client side.
    """

    @staticmethod
    def creer_invitation(trajet_id, passager_id):
        """
        Create an invitation for a passenger to join a trip.

        Args:
            trajet_id (int): The ID of the trip.
            passager_id (int): The ID of the passenger.

        Returns:
            tuple: The response from the API and the HTTP status code.
        """
        data = {
            'trajet_id': trajet_id,
            'passager_id': passager_id
        }
        return APIService.post('invitations', data)
    
    @staticmethod
    def get_invitations_recues(user_id):
        """
        Retrieve invitations received by a user (passenger mode).

        Args:
            user_id (int): The ID of the user.

        Returns:
            tuple: A list of Invitation objects and None if successful, 
                   or None and an error message if an error occurs.
        """
        resp, status = APIService.get(f'invitations/received/{user_id}')
        
        if status == 200:
            invitations = [
                Invitation(
                    i['id'], i['trajet_id'], i['depart'], i['arrivee'],
                    i['statut'], i['created_at'], i['prenom'], i['nom']
                )
                for i in resp
            ]
            return invitations, None
        return None, f"Error {status}"
    
    @staticmethod
    def get_invitations_envoyees(user_id):
        """
        Retrieve invitations sent by a user (driver mode).

        Args:
            user_id (int): The ID of the user.

        Returns:
            tuple: A list of Invitation objects and None if successful, 
                   or None and an error message if an error occurs.
        """
        resp, status = APIService.get(f'invitations/sent/{user_id}')
        
        if status == 200:
            invitations = [
                Invitation(
                    i['id'], i['trajet_id'], i['depart'], i['arrivee'],
                    i['statut'], i['created_at'], i['prenom'], i['nom']
                )
                for i in resp
            ]
            return invitations, None
        return None, f"Error {status}"
    
    @staticmethod
    def accepter_invitation(invitation_id):
        """
        Accept an invitation.

        Args:
            invitation_id (int): The ID of the invitation.

        Returns:
            tuple: True and a success message if successful, 
                   or False and an error message if an error occurs.
        """
        resp, status = APIService.put(f'invitations/{invitation_id}/accepter')
        
        if status == 200:
            return True, "Invitation accepted"
        return False, f"Error {status}"
    
    @staticmethod
    def refuser_invitation(invitation_id):
        """
        Decline an invitation.

        Args:
            invitation_id (int): The ID of the invitation.

        Returns:
            tuple: True and a success message if successful, 
                   or False and an error message if an error occurs.
        """
        resp, status = APIService.put(f'invitations/{invitation_id}/refuser')
        
        if status == 200:
            return True, "Invitation declined"
        return False, f"Error {status}"
