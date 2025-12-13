from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt


class LoginPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()

        titre = QLabel("🔑 Connexion")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 18px; font-weight: bold;")

        form = QFormLayout()
        self.login = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        form.addRow("Login :", self.login)
        form.addRow("Mot de passe :", self.password)

        btn_connexion = QPushButton("Se connecter")
        btn_inscription = QPushButton("Créer un compte")

        btn_connexion.clicked.connect(self._on_login_clicked)
        btn_inscription.clicked.connect(self.controller.go_register)

        layout.addWidget(titre)
        layout.addLayout(form)
        layout.addWidget(btn_connexion)
        layout.addWidget(btn_inscription)
        layout.addStretch()
        self.setLayout(layout)

    def _on_login_clicked(self):
        login = self.login.text().strip()
        mdp = self.password.text().strip()

        if self.controller.login(login, mdp):
            self.controller.go_home()
        else:
            QMessageBox.warning(self, "Erreur", "Identifiants incorrects.")
