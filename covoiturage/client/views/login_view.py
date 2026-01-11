from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from controllers.user_controller import UserController
from views.common_style import COMMON_STYLE


class LoginView(QWidget):
    """
    User login view.

    This view allows a user to authenticate by providing
    an email address and a password.
    """

    def __init__(self, main_window):
        """
        Initialize the login view.

        :param main_window: Reference to the main application window
        """
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        """
        Build and configure the graphical user interface.
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

        # Email field
        email_label = QLabel("Adresse email")
        card_layout.addWidget(email_label)

        self.email = QLineEdit()
        self.email.setPlaceholderText("exemple@email.com")
        card_layout.addWidget(self.email)

        # Password field
        pwd_label = QLabel("Mot de passe")
        card_layout.addWidget(pwd_label)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password)

        # Buttons
        btn_row = QHBoxLayout()

        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(
            lambda: self.main_window.switch_to('login')
        )

        login_btn = QPushButton("Connexion")
        login_btn.clicked.connect(self.login)

        for btn in (cancel_btn, login_btn):
            btn.setMinimumHeight(36)

        btn_row.addWidget(cancel_btn)
        btn_row.addStretch()
        btn_row.addWidget(login_btn)

        card_layout.addLayout(btn_row)

        # Registration link
        register_label = QLabel("Première connexion ?")
        register_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(register_label)

        register_btn = QPushButton("Créer un compte")
        register_btn.clicked.connect(
            lambda: self.main_window.switch_to('register')
        )
        card_layout.addWidget(register_btn)

        layout.addWidget(card)
        layout.addStretch()
        self.setLayout(layout)

        self.setStyleSheet(COMMON_STYLE)

    def login(self):
        """
        Attempt to authenticate the user.

        Sends the entered credentials to the UserController
        and handles success or failure.
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
                self,
                "Erreur",
                resp.get('error', 'Erreur de connexion')
            )
