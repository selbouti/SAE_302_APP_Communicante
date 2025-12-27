from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from controllers.user_controller import UserController

class LoginView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Email:"))
        self.email = QLineEdit()
        layout.addWidget(self.email)
        
        layout.addWidget(QLabel("Mot de passe:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)
        
        login_btn = QPushButton("Connexion")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)
        
        register_btn = QPushButton("S'inscrire")
        register_btn.clicked.connect(lambda: self.main_window.switch_to('register'))
        layout.addWidget(register_btn)
        
        self.setLayout(layout)
    
    def login(self):
        resp, status = UserController.login(self.email.text(), self.password.text())
        
        if status == 200:
            self.main_window.current_user = resp
            self.main_window.switch_to('home')
        else:
            QMessageBox.warning(self, "Erreur", resp.get('error', 'Erreur'))