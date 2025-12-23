# views/profile_view.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFormLayout
)
from PyQt5.QtCore import Qt


class ProfileView(QWidget):
    """
    Page de modification du profil utilisateur.
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()
        form = QFormLayout()

        self.title = QLabel("👤 Modifier mon profil")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:18px;font-weight:bold;")

        # Champs utilisateur
        self.nom = QLineEdit()
        self.prenom = QLineEdit()
        self.email = QLineEdit()
        self.telephone = QLineEdit()
        self.adresse = QLineEdit()
        self.ville = QLineEdit()
        self.cp = QLineEdit()

        form.addRow("Nom", self.nom)
        form.addRow("Prénom", self.prenom)
        form.addRow("Email", self.email)
        form.addRow("Téléphone", self.telephone)
        form.addRow("Adresse", self.adresse)
        form.addRow("Ville", self.ville)
        form.addRow("Code postal", self.cp)

        self.btn_save = QPushButton("💾 Enregistrer")
        self.btn_back = QPushButton("⬅ Retour")

        self.btn_save.clicked.connect(self.save)
        self.btn_back.clicked.connect(self.controller.go_home)

        layout.addWidget(self.title)
        layout.addLayout(form)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_back)
        layout.addStretch()
        self.setLayout(layout)

    def showEvent(self, event):
        """Pré-remplit les champs avec les infos actuelles."""
        user = self.controller.current_user
        if user:
            self.nom.setText(user["nom"])
            self.prenom.setText(user["prenom"])
            self.email.setText(user["email"])
            self.telephone.setText(user["telephone"])
            self.adresse.setText(user["adresse"])
            self.ville.setText(user["ville"])
            self.cp.setText(user["cp"])
        super().showEvent(event)

    def save(self):
        data = {
            "nom": self.nom.text(),
            "prenom": self.prenom.text(),
            "email": self.email.text(),
            "telephone": self.telephone.text(),
            "adresse": self.adresse.text(),
            "ville": self.ville.text(),
            "cp": self.cp.text()
        }
        self.controller.update_profile(data)
