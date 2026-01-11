from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from views.common_style import COMMON_STYLE


class HomeView(QWidget):
    """
    Home view of the application.

    This view acts as the main dashboard after user authentication.
    It provides quick access to the main features of the application.
    """

    def __init__(self, main_window):
        """
        Initialize the home view.

        :param main_window: reference to the main application window
        """
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        """
        Build and configure the user interface layout.
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Main card container
        container = QFrame()
        container.setObjectName("homeCard")
        card_layout = QVBoxLayout(container)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        # Title
        title = QLabel("🚗 Covoiturage Daily")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("titleLabel")
        card_layout.addWidget(title)

        # Welcome message
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

        # Subtitle
        subtitle = QLabel("Accédez à vos fonctionnalités principales")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitleLabel")
        card_layout.addWidget(subtitle)

        # Navigation buttons
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

        btn_reservations = QPushButton(
            "Mes réservations et invitations"
        )
        btn_reservations.clicked.connect(
            lambda: self.main_window.switch_to(
                'reservations_invitations'
            )
        )
        btns.addWidget(btn_reservations)

        card_layout.addLayout(btns)

        # Logout button
        logout = QPushButton("Déconnexion")
        logout.setObjectName("logoutButton")
        logout.clicked.connect(
            lambda: self.main_window.switch_to('login')
        )
        card_layout.addWidget(logout)

        layout.addWidget(container)
        layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet(COMMON_STYLE)
