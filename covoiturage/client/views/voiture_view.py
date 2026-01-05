from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt
from controllers.voiture_controller import VoitureController

class VoitureView(QWidget):
    """
    Vue de gestion de la voiture de l'utilisateur.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # ---------------- Layout ----------------
        layout = QVBoxLayout()
        form = QFormLayout()

        title = QLabel("🚗 Ma voiture")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:bold;")

        self.marque = QLineEdit()
        self.modele = QLineEdit()
        self.chevaux = QLineEdit()
        self.places = QLineEdit()
        self.co2 = QLineEdit()
        self.plaque = QLineEdit()

        self.motorisation = QComboBox()
        self.motorisation.addItems(["thermique", "hybride", "electrique", "hydrogene"])

        form.addRow("Marque :", self.marque)
        form.addRow("Modèle :", self.modele)
        form.addRow("Chevaux fiscaux :", self.chevaux)
        form.addRow("Nombre de places :", self.places)
        form.addRow("CO₂ (g/km) :", self.co2)
        form.addRow("Plaque d'immatriculation :", self.plaque)
        form.addRow("Motorisation :", self.motorisation)

        self.btn_save = QPushButton("💾 Enregistrer")
        self.btn_delete = QPushButton("❌ Supprimer")
        self.btn_back = QPushButton("⬅ Retour")

        self.btn_save.clicked.connect(self.save)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_back.clicked.connect(self.go_back)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_back)
        layout.addStretch()

        self.setLayout(layout)

    # ---------------- Actions ----------------
    def save(self):
        if not self.main_window.current_user:
            QMessageBox.warning(self, "Erreur", "Utilisateur non connecté")
            return

        try:
            data = {
                "marque": self.marque.text(),
                "modele": self.modele.text(),
                "chevaux_fiscaux": int(self.chevaux.text()),
                "places_max": int(self.places.text()),
                "taux_co2": int(self.co2.text()),
                "motorisation": self.motorisation.currentText(),
                "plaque": self.plaque.text()
            }
            user_id = self.main_window.current_user["id"]
            resp, status = VoitureController.save_voiture(user_id, data)

            if status == 201:
                QMessageBox.information(self, "Succès", "Voiture enregistrée ✔")
            else:
                QMessageBox.critical(self, "Erreur", resp.get("error", "Erreur lors de l'enregistrement"))

        except ValueError:
            QMessageBox.warning(self, "Erreur", "Vérifiez les champs numériques (chevaux, places, CO₂).")

    def delete(self):
        if not self.main_window.current_user:
            QMessageBox.warning(self, "Erreur", "Utilisateur non connecté")
            return

        user_id = self.main_window.current_user["id"]
        resp, status = VoitureController.delete_voiture(user_id)

        if status == 200:
            QMessageBox.information(self, "Succès", "Voiture supprimée ✔")
            self.clear_fields()
        else:
            QMessageBox.critical(self, "Erreur", "Erreur lors de la suppression")

    def go_back(self):
        self.main_window.switch_to("home")

    # ---------------- Rafraîchissement ----------------
    def showEvent(self, event):
        super().showEvent(event)
        if not self.main_window.current_user:
            return

        user_id = self.main_window.current_user["id"]
        resp, status = VoitureController.get_voiture(user_id)

        if status == 200 and resp:
            v = resp[0]
            self.marque.setText(v.get("marque", ""))
            self.modele.setText(v.get("modele", ""))
            self.chevaux.setText(str(v.get("chevaux_fiscaux", "")))
            self.places.setText(str(v.get("places_totales", "")))
            #self.places.setText(str(v.get("places_totales", "")))
            self.co2.setText(str(v.get("taux_co2", "")))
            self.motorisation.setCurrentText(v.get("motorisation", "thermique"))
            self.plaque.setText(v.get("plaque", ""))
        else:
            self.clear_fields()

    def clear_fields(self):
        self.marque.clear()
        self.modele.clear()
        self.chevaux.clear()
        self.places.clear()
        self.co2.clear()
        self.motorisation.setCurrentIndex(0)
