from services.api_service import APIService

class ReservationController:
    @staticmethod
    def creer_reservation(trajet_id, passager_id, places_reservees=1):
        data = {'trajet_id': trajet_id, 'passager_id': passager_id, 'places_reservees': places_reservees}
        return APIService.post('reservations', data)
    
    @staticmethod
    def mes_reservations(passager_id):
        return APIService.get(f'reservations/passager/{passager_id}')
    
    @staticmethod
    def reservations_trajet(trajet_id):
        return APIService.get(f'reservations/trajet/{trajet_id}')
    
    @staticmethod
    def accepter(reservation_id):
        return APIService.put(f'reservations/{reservation_id}/accepter')
    
    @staticmethod
    def refuser(reservation_id):
        return APIService.put(f'reservations/{reservation_id}/refuser')
    
    @staticmethod
    def annuler(reservation_id):
        return APIService.delete(f'reservations/{reservation_id}/annuler')