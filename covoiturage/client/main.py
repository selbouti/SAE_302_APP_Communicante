#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication

from views.main_window import MainWindow
from views.login_view import LoginView
from views.register_view import RegisterView
from views.home_view import HomeView
from views.matching_view import MatchingView
from views.mes_trajets_view import MesTrajetsView

from views.mes_reservations_view import MesReservationsView
from views.profile_view import ProfileView

from views.mes_reservations_view import ReservationsInvitationsView


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Fenêtre principale
    main_window = MainWindow({})

    # ⚠️ ID utilisateur temporaire (après login plus tard)
    USER_ID = 1

    # Dictionnaire des vues
    views = {
        'login': LoginView(main_window),
        'register': RegisterView(main_window),
        'home': HomeView(main_window),
        'matching': MatchingView(main_window),
        'mes_trajets': MesTrajetsView(main_window),

        'mes_reservations': MesReservationsView(main_window),
        'profile': ProfileView(USER_ID, main_window),# ✅ CORRIGÉ
        'mes_reservations': ReservationsInvitationsView(main_window)
    }

    # Injection des vues dans la fenêtre principale
    main_window.views = views
    for view in views.values():
        main_window.stack.addWidget(view)

    # Vue de départ
    main_window.switch_to('login')

    main_window.show()
    sys.exit(app.exec_())
