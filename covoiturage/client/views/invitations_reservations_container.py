# views/reservations_invitations_container.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTabWidget
from views.reservations_view import ReservationsView
from views.invitations_view import InvitationsView
from views.common_style import COMMON_STYLE

class ReservationsInvitationsContainer(QWidget):
    """Container for both reservations and invitations views."""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Onglets principaux
        self.tabs = QTabWidget()
        
        # Onglet 1: Réservations
        self.reservations_view = ReservationsView(self.main_window)
        self.tabs.addTab(self.reservations_view, "Réservations")
        
        # Onglet 2: Invitations
        self.invitations_view = InvitationsView(self.main_window)
        self.tabs.addTab(self.invitations_view, "Invitations")
        
        layout.addWidget(self.tabs)
        
        # Bouton retour
        back = QPushButton("Retour")
        back.clicked.connect(lambda: self.main_window.switch_to('home'))
        layout.addWidget(back)
        
        self.setLayout(layout)
        self.setStyleSheet(COMMON_STYLE)
    
    def load(self):
        """Load data for both views."""
        self.reservations_view.load()
        self.invitations_view.load()