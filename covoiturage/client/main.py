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
from views.mes_reservations_view import ReservationsInvitationsView


def main():
    """
    Point d'entrée principal de l'application cliente PyQt.
    """
    app = QApplication(sys.argv)

    # Création temporaire de la fenêtre principale
    main_window = MainWindow({})

    # Création des vues
    views = {
        'login': LoginView(main_window),
        'register': RegisterView(main_window),
        'home': HomeView(main_window),
        'matching': MatchingView(main_window),
        'mes_trajets': MesTrajetsView(main_window),
        'profile': ProfileView(main_window),
        'mes_reservations': ReservationsInvitationsView(main_window),
        'voiture': VoitureView(main_window)
    }

    # Injection des vues
    main_window.views = views
    for view in views.values():
        main_window.stack.addWidget(view)

    # Vue de départ
    main_window.switch_to('login')

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
