from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFormLayout, QComboBox
)
from PyQt5.QtCore import Qt


class VoitureView(QWidget):
    """
    Vue de gestion de la voiture de l'utilisateur.
    Permet :
    - d'ajouter une voiture
    - de modifier la voiture existante
    - de supprimer la voiture
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # ---------------- Layouts ----------------
        layout = QVBoxLayout()
        form = QFormLayout()

        # ---------------- Titre ----------------
        self.title = QLabel("🚗 Ma voiture")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:18px; font-weight:bold;")

        # ---------------- Champs ----------------
        self.marque = QLineEdit()
        self.modele = QLineEdit()
        self.chevaux = QLineEdit()
        self.places = QLineEdit()
        self.co2 = QLineEdit()

        self.motorisation = QComboBox()
        self.motorisation.addItems(
            ["thermique", "hybride", "electrique", "hydrogene"]
        )

        form.addRow("Marque :", self.marque)
        form.addRow("Modèle :", self.modele)
        form.addRow("Chevaux fiscaux :", self.chevaux)
        form.addRow("Nombre de places :", self.places)
        form.addRow("CO₂ (g/km) :", self.co2)
        form.addRow("Motorisation :", self.motorisation)

        # ---------------- Boutons ----------------
        self.btn_save = QPushButton("💾 Enregistrer")
        self.btn_delete = QPushButton("❌ Supprimer la voiture")
        self.btn_back = QPushButton("⬅ Retour")

        self.btn_save.clicked.connect(self.save)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_back.clicked.connect(self.controller.go_home)

        # ---------------- Assemblage ----------------
        layout.addWidget(self.title)
        layout.addLayout(form)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_back)
        layout.addStretch()

        self.setLayout(layout)

    # =========================
    #   ACTIONS
    # =========================
    def save(self):
        """
        Ajoute ou met à jour la voiture de l'utilisateur.
        """
        try:
            data = {
                "marque": self.marque.text(),
                "modele": self.modele.text(),
                "chevaux_fiscaux": int(self.chevaux.text()),
                "places_max": int(self.places.text()),
                "taux_co2": int(self.co2.text()),
                "motorisation": self.motorisation.currentText()
            }
            self.controller.save_voiture(data)

        except ValueError:
            self.controller.main.show_error(
                "Veuillez vérifier les champs numériques (chevaux, places, CO₂)."
            )

    def delete(self):
        """
        Supprime la voiture de l'utilisateur connecté.
        """
        self.controller.delete_voiture()

    # =========================
    #   RAFRAÎCHISSEMENT
    # =========================
    def showEvent(self, event):
        """
        Recharge les informations de la voiture
        à chaque affichage de la page.
        """
        user = self.controller.current_user
        if not user:
            return

        voiture = self.controller.voiture_model.get_user_voiture(user["id_user"])

        if voiture:
            self.marque.setText(voiture["marque"])
            self.modele.setText(voiture["modele"])
            self.chevaux.setText(str(voiture["chevaux_fiscaux"]))
            self.places.setText(str(voiture["places_max"]))
            self.co2.setText(str(voiture["taux_co2"]))
            self.motorisation.setCurrentText(voiture["motorisation"])
        else:
            self.marque.clear()
            self.modele.clear()
            self.chevaux.clear()
            self.places.clear()
            self.co2.clear()
            self.motorisation.setCurrentIndex(0)

        super().showEvent(event)
