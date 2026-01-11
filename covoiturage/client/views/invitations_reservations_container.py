# views/reservations_invitations_container.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTabWidget
from views.reservations_view import ReservationsView
from views.invitations_view import InvitationsView
from views.common_style import COMMON_STYLE


class ReservationsInvitationsContainer(QWidget):
    """
    Container view that groups reservations and invitations.

    This view uses a tab widget to allow the user to switch between
    reservations and invitations in a single interface.
    """

    def __init__(self, main_window):
        """
        Initialize the container view.

        :param main_window: reference to the main application window
        """
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        """
        Build and configure the user interface.
        """
        layout = QVBoxLayout()

        # Main tabs
        self.tabs = QTabWidget()

        # Tab 1: Reservations
        self.reservations_view = ReservationsView(self.main_window)
        self.tabs.addTab(self.reservations_view, "Réservations")

        # Tab 2: Invitations
        self.invitations_view = InvitationsView(self.main_window)
        self.tabs.addTab(self.invitations_view, "Invitations")

        layout.addWidget(self.tabs)

        # Back button
        back = QPushButton("Retour")
        back.clicked.connect(
            lambda: self.main_window.switch_to('home')
        )
        layout.addWidget(back)

        self.setLayout(layout)
        self.setStyleSheet(COMMON_STYLE)

    def load(self):
        """
        Load data for both reservations and invitations views.
        """
        self.reservations_view.load()
        self.invitations_view.load()
