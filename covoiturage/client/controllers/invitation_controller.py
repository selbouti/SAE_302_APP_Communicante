from services.api_service import APIService

class InvitationController:
    @staticmethod
    def creer_invitation(trajet_id, passager_id):
        data = {'trajet_id': trajet_id, 'passager_id': passager_id}
        return APIService.post('invitations', data)
    
    @staticmethod
    def invitations_received(passager_id):
        return APIService.get(f'invitations/received/{passager_id}')
    
    @staticmethod
    def invitations_sent(conducteur_id):
        return APIService.get(f'invitations/sent/{conducteur_id}')
    
    @staticmethod
    def accepter(invitation_id):
        return APIService.put(f'invitations/{invitation_id}/accepter')
    
    @staticmethod
    def refuser(invitation_id):
        return APIService.put(f'invitations/{invitation_id}/refuser')