# views/login_view.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout,
    QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt


class LoginPage(QWidget):
    """
    Page de connexion.
    Elle appelle les méthodes du UserController : login(), go_register()
    """

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

        if not login or not mdp:
            # On laisse le contrôleur gérer les messages via main.show_error
            self.controller.main.show_error("Veuillez renseigner login et mot de passe.")
            return

        self.controller.login(login, mdp)
