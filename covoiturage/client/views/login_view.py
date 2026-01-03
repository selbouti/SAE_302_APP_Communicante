from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from controllers.user_controller import UserController

class LoginView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        # En-tête
        header_layout = QHBoxLayout()
        logo = QLabel("🚗")
        logo.setObjectName("logo")
        title = QLabel("Application de covoiturage")
        title.setObjectName("titleLabel")
        header_layout.addWidget(logo)
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Card
        card = QFrame()
        card.setObjectName("loginCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        email_label = QLabel("Nom de l'utilisateur")
        email_label.setObjectName("fieldLabel")
        card_layout.addWidget(email_label)
        self.email = QLineEdit()
        self.email.setPlaceholderText("your@email.com")
        card_layout.addWidget(self.email)
        
        pwd_label = QLabel("Mot de passe")
        pwd_label.setObjectName("fieldLabel")
        card_layout.addWidget(pwd_label)
        pwd_row = QHBoxLayout()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        pwd_row.addWidget(self.password)
        pwd_row.addStretch()
        card_layout.addLayout(pwd_row)

        # Boutons action
        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.clicked.connect(lambda: self.main_window.switch_to('login'))
        btn_row.addWidget(cancel_btn)
        
        login_btn = QPushButton("Se connecter")
        login_btn.setObjectName("primaryButton")
        login_btn.clicked.connect(self.login)
        btn_row.addWidget(login_btn)
        btn_row.addStretch()
        card_layout.addLayout(btn_row)

        # Lien inscription
        register_label = QLabel("Première connexion ?")
        register_label.setObjectName("subtitle")
        card_layout.addWidget(register_label)
        register_btn = QPushButton("Créer un compte")
        register_btn.setObjectName("ghostButton")
        register_btn.clicked.connect(lambda: self.main_window.switch_to('register'))
        card_layout.addWidget(register_btn)

        layout.addWidget(card)
        layout.addStretch()
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
                color: #1e1e1e;
                font-family: "Open Sans", "Segoe UI", Arial, sans-serif;
                font-size: 14px;
            }
            QLabel#logo {
                font-size: 28px;
                padding-right: 8px;
            }
            QLabel#titleLabel {
                color: #b57b7b;
                font-size: 28px;
                font-weight: 800;
            }
            QFrame#loginCard {
                border: 2px solid #4a4a4a;
                border-radius: 10px;
                background: #fdfdfd;
            }
            QLabel#fieldLabel {
                color: #2c2c2c;
                font-weight: 700;
            }
            QLabel#subtitle {
                color: #4a4a4a;
                font-weight: 600;
                padding-top: 8px;
            }
            QLineEdit {
                border: 1px solid #9b9b9b;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton {
                border-radius: 6px;
                padding: 10px 14px;
                font-weight: 600;
            }
            QPushButton#primaryButton {
                background: #000000;
                color: #ffffff;
                border: 1px solid #000000;
                min-width: 140px;
            }
            QPushButton#primaryButton:hover { background: #2b2b2b; }
            QPushButton#cancelButton {
                background: #f0f0f0;
                color: #2c2c2c;
                border: 1px solid #c7c7c7;
                min-width: 120px;
            }
            QPushButton#ghostButton {
                background: #ffffff;
                color: #4a4a4a;
                border: 1px solid #c7c7c7;
                min-width: 140px;
            }
            QPushButton:hover { opacity: 0.9; }
        """)
    
    def login(self):
        resp, status = UserController.login(self.email.text(), self.password.text())
        
        if status == 200:
            self.main_window.current_user = resp
            self.main_window.switch_to('home')
        else:
            QMessageBox.warning(self, "Erreur", resp.get('error', 'Erreur'))