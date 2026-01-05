from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
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

        save_btn = QPushButton("Enregistrer")
        voiture_btn = QPushButton("🚗 Ma voiture")
        back_btn = QPushButton("Retour")

        for w in [
            title,
            self.nom,
            self.prenom,
            self.email,
            self.telephone,
            save_btn,
            voiture_btn,
            back_btn
        ]:
            layout.addWidget(w)

        self.setLayout(layout)

        save_btn.clicked.connect(self.save)
        voiture_btn.clicked.connect(self.go_voiture)
        back_btn.clicked.connect(self.go_back)

    # ----------------------------
    # Chargement du profil
    # ----------------------------
    def load(self):
        if not self.main_window.current_user:
            QMessageBox.warning(self, "Erreur", "Utilisateur non connecté")
            self.main_window.switch_to("login")
            return

        user_id = self.main_window.current_user["id"]
        response, status = ProfileController.get_profile(user_id)

        if status != 200:
            QMessageBox.critical(self, "Erreur", "Impossible de charger le profil")
            self.main_window.switch_to("home")
            return

        self.nom.setText(response.get("nom", ""))
        self.prenom.setText(response.get("prenom", ""))
        self.email.setText(response.get("email", ""))
        self.telephone.setText(response.get("telephone", ""))

    # ----------------------------
    # Actions
    # ----------------------------
    def save(self):
        if not self.main_window.current_user:
            QMessageBox.warning(self, "Erreur", "Utilisateur non connecté")
            return

        user_id = self.main_window.current_user["id"]

        data = {
            "nom": self.nom.text(),
            "prenom": self.prenom.text(),
            "email": self.email.text(),
            "telephone": self.telephone.text()
        }

        response, status = ProfileController.update_profile(user_id, data)

        if status == 200:
            QMessageBox.information(self, "Succès", "Profil mis à jour ✔")
        else:
            QMessageBox.critical(self, "Erreur", "Erreur lors de la mise à jour")

    def go_voiture(self):
        """Redirection vers la vue voiture"""
        self.main_window.switch_to("voiture")

    def go_back(self):
        self.main_window.switch_to("home")
