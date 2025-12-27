from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

class HomeView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        user = self.main_window.current_user
        if user:
            welcome_text = f"Bienvenue {user.get('prenom', '')} {user.get('nom', '')}"
        else:
            welcome_text = "Bienvenue"
        
        layout.addWidget(QLabel(welcome_text))
        layout.addWidget(QLabel("Choisissez une action:"))
        
        btns = QHBoxLayout()
        
        btn1 = QPushButton("Voir matching")
        btn1.clicked.connect(lambda: self.main_window.switch_to('matching'))
        btns.addWidget(btn1)
        
        btn2 = QPushButton("Mes trajets")
        btn2.clicked.connect(lambda: self.main_window.switch_to('mes_trajets'))
        btns.addWidget(btn2)
        
        btn3 = QPushButton("Mes réservations")
        btn3.clicked.connect(lambda: self.main_window.switch_to('mes_reservations'))
        btns.addWidget(btn3)
        
        layout.addLayout(btns)
        
        logout = QPushButton("Déconnexion")
        logout.clicked.connect(lambda: self.main_window.switch_to('login'))
        layout.addWidget(logout)
        
        self.setLayout(layout)