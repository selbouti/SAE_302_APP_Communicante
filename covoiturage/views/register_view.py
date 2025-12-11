from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt


class RegisterPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()
        titre = QLabel("📝 Inscription")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 18px; font-weight: bold;")

        form = QFormLayout()
        self.nom = QLineEdit()
        self.prenom = QLineEdit()
        self.login = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.email = QLineEdit()
        self.telephone = QLineEdit()
        self.adresse = QLineEdit()
        self.ville = QLineEdit()
        self.cp = QLineEdit()

        form.addRow("Nom :", self.nom)
        form.addRow("Prénom :", self.prenom)
        form.addRow("Login :", self.login)
        form.addRow("Mot de passe :", self.password)
        form.addRow("Email :", self.email)
        form.addRow("Téléphone :", self.telephone)
        form.addRow("Adresse :", self.adresse)
        form.addRow("Ville :", self.ville)
        form.addRow("Code postal :", self.cp)

        btn_creer = QPushButton("Créer le compte")
        btn_retour = QPushButton("Retour")

        btn_creer.clicked.connect(self._on_register_clicked)
        btn_retour.clicked.connect(self.controller.go_login)

        layout.addWidget(titre)
        layout.addLayout(form)
        layout.addWidget(btn_creer)
        layout.addWidget(btn_retour)
        layout.addStretch()
        self.setLayout(layout)

    def _on_register_clicked(self):
        data = {
            "nom": self.nom.text().strip(),
            "prenom": self.prenom.text().strip(),
            "login": self.login.text().strip(),
            "mot_de_passe": self.password.text().strip(),
            "email": self.email.text().strip(),
            "telephone": self.telephone.text().strip(),
            "adresse": self.adresse.text().strip(),
            "ville": self.ville.text().strip(),
            "cp": self.cp.text().strip(),
        }

        if not all(data.values()):
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        if self.controller.register(data):
            QMessageBox.information(self, "Succès", "Compte créé avec succès.")
            self.controller.go_login()
        else:
            QMessageBox.warning(self, "Erreur", "Login déjà utilisé ou erreur en base.")
