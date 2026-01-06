from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QMessageBox, QHBoxLayout
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
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignTop)

        form = QFormLayout()
        form.setSpacing(8)

        title = QLabel("🚗 Ma voiture")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:20px; font-weight:bold; color:#C62828;")

        self.marque = QLineEdit()
        self.modele = QLineEdit()
        self.chevaux = QLineEdit()
        self.places = QLineEdit()
        self.co2 = QLineEdit()
        self.plaque = QLineEdit()

        self.motorisation = QComboBox()
        self.motorisation.addItems(
            ["thermique", "hybride", "electrique", "hydrogene"]
        )

        # Liste des champs pour gestion lecture seule
        self.fields = [
            self.marque, self.modele, self.chevaux,
            self.places, self.co2, self.plaque
        ]

        for field in self.fields:
            field.setReadOnly(True)
            field.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #C62828;
                    border-radius: 4px;
                }
                QLineEdit:read-only {
                    background-color: #F5F5F5;
                }
            """)

        self.motorisation.setEnabled(False)
        self.motorisation.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #C62828;
                border-radius: 4px;
            }
        """)

        form.addRow("Marque :", self.marque)
        form.addRow("Modèle :", self.modele)
        form.addRow("Chevaux fiscaux :", self.chevaux)
        form.addRow("Nombre de places :", self.places)
        form.addRow("CO₂ (g/km) :", self.co2)
        form.addRow("Plaque :", self.plaque)
        form.addRow("Motorisation :", self.motorisation)

        # ---------------- Boutons ----------------
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_edit = QPushButton("✏️ Modifier")
        self.btn_save = QPushButton("💾 Enregistrer")
        self.btn_delete = QPushButton("❌ Supprimer")
        self.btn_back = QPushButton("⬅ Retour")

        self.btn_edit.setStyleSheet("""
            background-color:#C62828;
            color:white;
            padding:8px;
        """)

        self.btn_save.setStyleSheet("""
            background-color:#2E7D32;
            color:white;
            padding:8px;
        """)

        self.btn_delete.setStyleSheet("""
            background-color:#C62828;
            color:white;
            padding:8px;
        """)

        self.btn_back.setStyleSheet("""
            background-color:white;
            border:1px solid #C62828;
            padding:8px;
        """)

        self.btn_save.hide()  # 🔒 caché tant que pas en mode édition

        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_back)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)

        # ---------------- Signals ----------------
        self.btn_edit.clicked.connect(self.enable_edit)
        self.btn_save.clicked.connect(self.save)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_back.clicked.connect(self.go_back)

    # ---------------- Edition ----------------
    def enable_edit(self):
        for field in self.fields:
            field.setReadOnly(False)
        self.motorisation.setEnabled(True)

        self.btn_edit.hide()
        self.btn_save.show()

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

            if status in (200, 201):
                QMessageBox.information(self, "Succès", "Voiture enregistrée ✔")

                # 🔒 Rebloquer après sauvegarde
                for field in self.fields:
                    field.setReadOnly(True)
                self.motorisation.setEnabled(False)

                self.btn_save.hide()
                self.btn_edit.show()
            else:
                QMessageBox.critical(self, "Erreur", "Erreur lors de l'enregistrement")

        except ValueError:
            QMessageBox.warning(
                self, "Erreur",
                "Vérifiez les champs numériques (chevaux, places, CO₂)."
            )

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
        self.main_window.switch_to("profile")

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
            self.co2.setText(str(v.get("taux_co2", "")))
            self.motorisation.setCurrentText(
                v.get("motorisation", "thermique")
            )
            self.plaque.setText(v.get("plaque", ""))
        else:
            self.clear_fields()

    def clear_fields(self):
        for field in self.fields:
            field.clear()
        self.motorisation.setCurrentIndex(0)
