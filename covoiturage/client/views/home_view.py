from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt


class HomeView(QWidget):
    """
    Vue d'accueil de l'application.
    """

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # ================= CARD =================
        container = QFrame()
        container.setObjectName("homeCard")
        card_layout = QVBoxLayout(container)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        # ================= TITRE =================
        title = QLabel("🚗 Covoiturage Daily")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("titleLabel")
        card_layout.addWidget(title)

        # ================= BIENVENUE =================
        user = self.main_window.current_user
        welcome = QLabel()
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setObjectName("welcomeLabel")

        if user:
            welcome.setText(
                f"Bienvenue {user.get('prenom', '')} {user.get('nom', '')}"
            )
        else:
            welcome.setText("Bienvenue")

        card_layout.addWidget(welcome)

        subtitle = QLabel("Accédez à vos fonctionnalités principales")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitleLabel")
        card_layout.addWidget(subtitle)

        # ================= BOUTONS =================
        btns = QHBoxLayout()
        btns.setSpacing(14)

        btn_profile = QPushButton("Mon profil")
        btn_profile.clicked.connect(
            lambda: self.main_window.switch_to('profile')
        )
        btns.addWidget(btn_profile)

        btn_matching = QPushButton("Matching")
        btn_matching.clicked.connect(
            lambda: self.main_window.switch_to('matching')
        )
        btns.addWidget(btn_matching)

        btn_trajets = QPushButton("Mes trajets")
        btn_trajets.clicked.connect(
            lambda: self.main_window.switch_to('mes_trajets')
        )
        btns.addWidget(btn_trajets)

        btn_reservations = QPushButton("Mes réservations")
        btn_reservations.clicked.connect(
            lambda: self.main_window.switch_to('mes_reservations')
        )
        btns.addWidget(btn_reservations)

        card_layout.addLayout(btns)

        # ================= LOGOUT =================
        logout = QPushButton("Déconnexion")
        logout.setObjectName("logoutButton")
        logout.clicked.connect(
            lambda: self.main_window.switch_to('login')
        )
        card_layout.addWidget(logout)

        layout.addWidget(container)
        layout.addStretch()
        self.setLayout(layout)

        # ================= STYLE =================
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: "Segoe UI", Arial, sans-serif;
                font-size: 14px;
                color: #1e1e1e;
            }

            QFrame#homeCard {
                border: 2px solid #C62828;
                border-radius: 10px;
                background-color: #fdfdfd;
            }

            QLabel#titleLabel {
                color: #C62828;
                font-size: 26px;
                font-weight: bold;
                padding-bottom: 8px;
            }

            QLabel#welcomeLabel {
                color: #444;
                font-size: 16px;
                font-weight: 600;
            }

            QLabel#subtitleLabel {
                color: #777;
                font-size: 14px;
                padding-bottom: 16px;
            }

            QPushButton {
                background-color: #C62828;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 14px;
                font-weight: bold;
                min-width: 140px;
            }

            QPushButton:hover {
                background-color: #B71C1C;
            }

            QPushButton#logoutButton {
                background-color: white;
                color: #C62828;
                border: 1px solid #C62828;
                margin-top: 16px;
            }

            QPushButton#logoutButton:hover {
                background-color: #f8f8f8;
            }
        """)
