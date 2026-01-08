from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from controllers.user_controller import UserController
from views.common_style import COMMON_STYLE


class LoginView(QWidget):
    """
    Vue de connexion utilisateur.
    """

    def __init__(self, main_window):
        """
        Initialise la vue de connexion.

        :param main_window: Fenêtre principale
        """
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        """
        Construit l'interface graphique.
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # ================= HEADER =================
        title = QLabel("🚗 Covoiturage Daily")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        subtitle = QLabel("Connexion à votre compte")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # ================= CARD =================
        card = QFrame()
        card.setObjectName("loginCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        # Email
        email_label = QLabel("Email")
        card_layout.addWidget(email_label)

        self.email = QLineEdit()
        self.email.setPlaceholderText("exemple@email.com")
        card_layout.addWidget(self.email)

        # Mot de passe
        pwd_label = QLabel("Mot de passe")
        card_layout.addWidget(pwd_label)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password)

        # Boutons
        btn_row = QHBoxLayout()

        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(lambda: self.main_window.switch_to('login'))

        login_btn = QPushButton("Se connecter")
        login_btn.clicked.connect(self.login)

        for btn in (cancel_btn, login_btn):
            btn.setMinimumHeight(36)

        btn_row.addWidget(cancel_btn)
        btn_row.addStretch()
        btn_row.addWidget(login_btn)

        card_layout.addLayout(btn_row)

        # Inscription
        register_label = QLabel("Première connexion ?")
        register_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(register_label)

        register_btn = QPushButton("Créer un compte")
        register_btn.clicked.connect(lambda: self.main_window.switch_to('register'))
        card_layout.addWidget(register_btn)

        layout.addWidget(card)
        layout.addStretch()
        self.setLayout(layout)

        self.setStyleSheet(COMMON_STYLE)

    def login(self):
        """
        Tente une connexion utilisateur.
        """
        resp, status = UserController.login(
            self.email.text(),
            self.password.text()
        )

        if status == 200:
            self.main_window.current_user = resp
            self.main_window.switch_to('home')
        else:
            QMessageBox.warning(
                self, "Erreur",
                resp.get('error', 'Erreur de connexion')
            )
