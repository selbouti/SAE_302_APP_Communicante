from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame

class HomeView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        container = QFrame()
        container.setObjectName("homeCard")
        card_layout = QVBoxLayout(container)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        title = QLabel("Application de covoiturage")
        title.setObjectName("titleLabel")
        card_layout.addWidget(title)

        user = self.main_window.current_user
        welcome = QLabel()
        welcome.setObjectName("welcomeLabel")
        if user:
            welcome.setText(f"Bienvenue {user.get('prenom', '')} {user.get('nom', '')}")
        else:
            welcome.setText("Bienvenue")
        card_layout.addWidget(welcome)

        subtitle = QLabel("Accédez à vos fonctionnalités principales")
        subtitle.setObjectName("subtitleLabel")
        card_layout.addWidget(subtitle)

        btns = QHBoxLayout()
        btns.setSpacing(14)
        
        btn1 = QPushButton("Voir matching")
        btn1.clicked.connect(lambda: self.main_window.switch_to('matching'))
        btns.addWidget(btn1)
        
        btn2 = QPushButton("Mes trajets")
        btn2.clicked.connect(lambda: self.main_window.switch_to('mes_trajets'))
        btns.addWidget(btn2)
        
        btn3 = QPushButton("Mes réservations")
        btn3.clicked.connect(lambda: self.main_window.switch_to('mes_reservations'))
        btns.addWidget(btn3)
        
        card_layout.addLayout(btns)

        logout = QPushButton("Déconnexion")
        logout.setObjectName("logoutButton")
        logout.clicked.connect(lambda: self.main_window.switch_to('login'))
        card_layout.addWidget(logout)

        layout.addWidget(container)
        layout.addStretch()
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
                color: #1e1e1e;
                font-family: "Open Sans", "Segoe UI", Arial, sans-serif;
                font-size: 14px;
            }
            QFrame#homeCard {
                border: 2px solid #4a4a4a;
                border-radius: 8px;
                background: #fdfdfd;
            }
            QLabel#titleLabel {
                color: #7b0000;
                font-size: 24px;
                font-weight: 800;
                text-decoration: underline;
                padding-bottom: 6px;
            }
            QLabel#welcomeLabel {
                color: #4a4a4a;
                font-size: 16px;
                padding: 2px 0;
            }
            QLabel#subtitleLabel {
                color: #7a7a7a;
                font-size: 14px;
                padding: 0 0 12px 0;
            }
            QPushButton {
                background-color: #a30000;
                color: #ffffff;
                border: 1px solid #7b0000;
                border-radius: 6px;
                padding: 10px 14px;
                font-weight: 600;
                min-width: 150px;
            }
            QPushButton:hover { background-color: #b30000; }
            QPushButton:pressed { background-color: #7b0000; }
            QPushButton#logoutButton {
                background-color: #ffffff;
                color: #a30000;
                border: 1px solid #7b0000;
                min-width: 140px;
            }
        """)
