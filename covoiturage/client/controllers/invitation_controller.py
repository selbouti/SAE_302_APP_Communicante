from services.api_service import APIService
from models.invitation import Invitation

class InvitationController:
    """Contrôle la logique des invitations côté client"""
    
    @staticmethod
    def creer_invitation(trajet_id, passager_id):
        """Créer une invitation"""
        data = {
            'trajet_id': trajet_id,
            'passager_id': passager_id
        }
        return APIService.post('invitations', data)
    
    @staticmethod
    def get_invitations_recues(user_id):
        """Récupérer les invitations reçues (mode passager)"""
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
        return None, f"Erreur {status}"
    
    @staticmethod
    def get_invitations_envoyees(user_id):
        """Récupérer les invitations envoyées (mode conducteur)"""
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
        return None, f"Erreur {status}"
    
    @staticmethod
    def accepter_invitation(invitation_id):
        """Accepter une invitation"""
        resp, status = APIService.put(f'invitations/{invitation_id}/accepter')
        
        if status == 200:
            return True, "Invitation acceptée"
        return False, f"Erreur {status}"
    
    @staticmethod
    def refuser_invitation(invitation_id):
        """Refuser une invitation"""
        resp, status = APIService.put(f'invitations/{invitation_id}/refuser')
        
        if status == 200:
            return True, "Invitation refusée"
        return False, f"Erreur {status}"
