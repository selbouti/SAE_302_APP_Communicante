import unittest
from unittest.mock import patch
from controllers.invitation_controller import InvitationController
from controllers.reservation_controller import ReservationController

class TestInvitationController(unittest.TestCase):
    """Unit tests for InvitationController"""

    @patch('services.api_service.APIService.post')
    def test_creer_invitation(self, mock_post):
        # Mock API response
        mock_post.return_value = ({"success": True, "message": "Invitation created"}, 201)
        
        # Call the method
        response, status = InvitationController.creer_invitation(1, 2)
        
        # Assertions
        self.assertEqual(status, 201)
        self.assertTrue(response["success"])
        self.assertEqual(response["message"], "Invitation created")

    @patch('client.services.api_service.APIService.get')
    def test_get_invitations_recues(self, mock_get):
        # Mock API response
        mock_get.return_value = ([
            {"id": 1, "trajet_id": 1, "depart": "Paris", "arrivee": "Lyon", "statut": "pending",
             "created_at": "2026-01-10", "prenom": "John", "nom": "Doe"}
        ], 200)
        
        # Call the method
        invitations, error = InvitationController.get_invitations_recues(1)
        
        # Assertions
        self.assertIsNone(error)
        self.assertEqual(len(invitations), 1)
        self.assertEqual(invitations[0].depart, "Paris")
        self.assertEqual(invitations[0].arrivee, "Lyon")

class TestReservationController(unittest.TestCase):
    """Unit tests for ReservationController"""

    @patch('client.services.api_service.APIService.get')
    def test_get_reservations_recues(self, mock_get):
        # Mock API response
        mock_get.return_value = ([
            {"id": 1, "trajet_id": 1, "depart": "Paris", "arrivee": "Lyon", "places_reservees": 2,
             "statut": "pending", "created_at": "2026-01-10", "prix_par_place": 20, "prenom": "Jane", "nom": "Smith"}
        ], 200)
        
        # Call the method
        reservations, error = ReservationController.get_reservations_recues(1)
        
        # Assertions
        self.assertIsNone(error)
        self.assertEqual(len(reservations), 1)
        self.assertEqual(reservations[0].depart, "Paris")
        self.assertEqual(reservations[0].arrivee, "Lyon")
        self.assertEqual(reservations[0].places_reservees, 2)

    @patch('client.services.api_service.APIService.put')
    def test_accepter_reservation(self, mock_put):
        # Mock API response
        mock_put.return_value = ({"success": True, "message": "Reservation accepted"}, 200)
        
        # Call the method
        success, message = ReservationController.accepter_reservation(1)
        
        # Assertions
        self.assertTrue(success)
        self.assertEqual(message, "Reservation accepted")

if __name__ == '__main__':
    unittest.main()