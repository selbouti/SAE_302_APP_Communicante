#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication

from views.main_window import MainWindow
from views.login_view import LoginView
from views.register_view import RegisterView
from views.home_view import HomeView
from views.matching_view import MatchingView
from views.mes_trajets_view import MesTrajetsView
from views.voiture_view import VoitureView
from views.profile_view import ProfileView
from views.invitations_reservations_container import ReservationsInvitationsContainer


def main():
    """
    Entry point for the PyQt client application.

    This function initializes the PyQt application, creates the main window,
    and sets up all the views used in the application. It also manages the
    injection of views into the main window's stack and sets the initial view
    to the login screen.

    Views:
        - LoginView: Handles user authentication.
        - RegisterView: Handles user registration.
        - HomeView: Displays the home screen after login.
        - MatchingView: Manages trip matching functionality.
        - MesTrajetsView: Displays the user's trips.
        - ProfileView: Allows the user to view and edit their profile.
        - ReservationsInvitationsContainer: Manages reservations and invitations.
        - VoitureView: Handles car-related operations.

    Workflow:
        1. Initialize the QApplication.
        2. Create the MainWindow instance.
        3. Instantiate all views and inject them into the main window.
        4. Set the initial view to the login screen.
        5. Start the PyQt event loop.

    Exits:
        The application exits when the PyQt event loop ends.
    """
    app = QApplication(sys.argv)

    # Temporary creation of the main window
    main_window = MainWindow({})

    # Create views
    views = {
        'login': LoginView(main_window),
        'register': RegisterView(main_window),
        'home': HomeView(main_window),
        'matching': MatchingView(main_window),
        'mes_trajets': MesTrajetsView(main_window),
        'profile': ProfileView(main_window),
        'reservations_invitations': ReservationsInvitationsContainer(main_window),
        'voiture': VoitureView(main_window)
    }

    # Inject views into the main window
    main_window.views = views
    for view in views.values():
        main_window.stack.addWidget(view)

    # Set the initial view
    main_window.switch_to('login')

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
