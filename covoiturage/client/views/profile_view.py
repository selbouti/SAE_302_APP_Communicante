from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpinBox, QMessageBox
)
from controllers.profile_controller import ProfileController


class ProfileView(QWidget):

    def __init__(self, utilisateur_id, main_window=None):
        super().__init__()
        self.utilisateur_id = utilisateur_id
        self.main_window = main_window

        layout = QVBoxLayout()

        title = QLabel("Mon profil")
        title.setStyleSheet("font-size:20px;font-weight:bold;")

        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Nom")

        self.prenom = QLineEdit()
        self.prenom.setPlaceholderText("Prénom")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.telephone = QLineEdit()
        self.telephone.setPlaceholderText("Téléphone")

        self.marque = QLineEdit()
        self.marque.setPlaceholderText("Marque véhicule")

        self.modele = QLineEdit()
        self.modele.setPlaceholderText("Modèle")

        self.couleur = QLineEdit()
        self.couleur.setPlaceholderText("Couleur")

        self.plaque = QLineEdit()
        self.plaque.setPlaceholderText("Plaque")

        self.places = QSpinBox()
        self.places.setRange(1, 8)
        self.places.setPrefix("Places : ")

        save_btn = QPushButton("Enregistrer")
        back_btn = QPushButton("Retour")

        for w in [
            title, self.nom, self.prenom, self.email, self.telephone,
            self.marque, self.modele, self.couleur, self.plaque,
            self.places, save_btn, back_btn
        ]:
            layout.addWidget(w)

        self.setLayout(layout)

        save_btn.clicked.connect(self.save)
        back_btn.clicked.connect(self.go_back)

        self.load()

    def load(self):
        response = ProfileController.get_profile(self.utilisateur_id)

        if not response.get("success"):
            QMessageBox.critical(self, "Erreur", "Impossible de charger le profil")
            return

        p = response["profile"]
        self.nom.setText(p["nom"])
        self.prenom.setText(p["prenom"])
        self.email.setText(p["email"])
        self.telephone.setText(p["telephone"])

        if p.get("voiture"):
            v = p["voiture"]
            self.marque.setText(v["marque"])
            self.modele.setText(v["modele"])
            self.couleur.setText(v["couleur"])
            self.plaque.setText(v["plaque"])
            self.places.setValue(v["places_totales"])

    def save(self):
        data = {
            "nom": self.nom.text(),
            "prenom": self.prenom.text(),
            "email": self.email.text(),
            "telephone": self.telephone.text(),
            "voiture": {
                "marque": self.marque.text(),
                "modele": self.modele.text(),
                "couleur": self.couleur.text(),
                "plaque": self.plaque.text(),
                "places": self.places.value()
            }
        }

        response = ProfileController.update_profile(self.utilisateur_id, data)

        if response.get("success"):
            QMessageBox.information(self, "Succès", "Profil mis à jour ✔")
        else:
            QMessageBox.critical(self, "Erreur", "Erreur lors de la mise à jour")

    def go_back(self):
        if self.main_window:
            self.main_window.switch_to("home")
