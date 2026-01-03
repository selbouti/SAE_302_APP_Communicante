from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpinBox, QMessageBox
)
from controllers.profile_controller import ProfileController

class ProfileView(QWidget):
    def __init__(self, main_window):
        super().__init__()
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

    # 🔹 appelée uniquement après login
    def load(self):
        """Charge le profil de l'utilisateur connecté"""
        if not self.main_window.current_user:
            QMessageBox.warning(self, "Erreur", "Utilisateur non connecté")
            self.main_window.switch_to("login")  # renvoie au login
            return

        user_id = self.main_window.current_user["id"]
        response, erreur = ProfileController.get_profile(user_id)

        if erreur:
            # Affiche le message et retourne automatiquement au home ou login
            QMessageBox.critical(self, "Erreur", "Impossible de charger le profil")
            self.main_window.switch_to("home")
            return

        # Si tout va bien, on remplit le formulaire
        p = response
        self.nom.setText(p.get("nom", ""))
        self.prenom.setText(p.get("prenom", ""))
        self.email.setText(p.get("email", ""))
        self.telephone.setText(p.get("telephone", ""))

        if p.get("voiture"):
            v = p["voiture"]
            self.marque.setText(v.get("marque", ""))
            self.modele.setText(v.get("modele", ""))
            self.couleur.setText(v.get("couleur", ""))
            self.plaque.setText(v.get("plaque", ""))
            self.places.setValue(v.get("places_totales", 1))


    def go_back(self):
        self.main_window.switch_to("home")

    def save(self):
        if not self.main_window.current_user:
            QMessageBox.warning(self, "Erreur", "Utilisateur non connecté")
            return

        user_id = self.main_window.current_user["id"]

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

        response = ProfileController.update_profile(user_id, data)

        if response.get("success"):
            QMessageBox.information(self, "Succès", "Profil mis à jour ✔")
        else:
            QMessageBox.critical(self, "Erreur", "Erreur lors de la mise à jour")
