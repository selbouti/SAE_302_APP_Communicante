from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QComboBox,
    QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from controllers.voiture_controller import VoitureController
from views.common_style import COMMON_STYLE


class VoitureView(QWidget):
    """
    View for managing the user's car.

    This view allows the user to:
    - display car information
    - edit car details
    - delete the car
    - return to the profile view

    By default, all fields are read-only.
    """

    def __init__(self, main_window):
        """
        Initialize the car management view.

        :param main_window: Reference to the main application window
        """
        super().__init__()
        self.main_window = main_window

        # ================== Main layout ==================
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignTop)

        form = QFormLayout()
        form.setSpacing(8)

        title = QLabel("🚗 Ma voiture")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("titleLabel")

        # ================== Fields ==================
        self.marque = QLineEdit()
        self.modele = QLineEdit()
        self.chevaux = QLineEdit()
        self.places = QLineEdit()
        self.co2 = QLineEdit()

        self.motorisation = QComboBox()
        self.motorisation.addItems(
            ["thermique", "hybride", "electrique", "hydrogene"]
        )

        self.fields = [
            self.marque, self.modele,
            self.chevaux, self.places,
            self.co2
        ]

        for field in self.fields:
            field.setReadOnly(True)

        self.motorisation.setEnabled(False)

        form.addRow("Marque :", self.marque)
        form.addRow("Modèle :", self.modele)
        form.addRow("Chevaux fiscaux :", self.chevaux)
        form.addRow("Nombre de places :", self.places)
        form.addRow("CO₂ (g/km) :", self.co2)
        form.addRow("Motorisation :", self.motorisation)

        # ================== Buttons ==================
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_edit = QPushButton("✏️ Modifier")
        self.btn_save = QPushButton("💾 Enregistrer")
        self.btn_delete = QPushButton("❌ Supprimer")
        self.btn_back = QPushButton("⬅ Retour")

        self.btn_save.hide()

        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_back)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet(COMMON_STYLE)

        # ================== Signals ==================
        self.btn_edit.clicked.connect(self.enable_edit)
        self.btn_save.clicked.connect(self.save)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_back.clicked.connect(self.go_back)

    # ==================================================
    # EDIT MODE
    # ==================================================
    def enable_edit(self):
        """
        Enable edit mode.

        Makes all fields editable and shows the save button.
        """
        for field in self.fields:
            field.setReadOnly(False)

        self.motorisation.setEnabled(True)
        self.btn_edit.hide()
        self.btn_save.show()

    # ==================================================
    # ACTIONS
    # ==================================================
    def save(self):
        """
        Save or update the car via the server API.
        """
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
            }

            user_id = self.main_window.current_user["id"]
            _, status = VoitureController.save_voiture(user_id, data)

            if status in (200, 201):
                QMessageBox.information(self, "Succès", "Voiture enregistrée ✔")

                for field in self.fields:
                    field.setReadOnly(True)

                self.motorisation.setEnabled(False)
                self.btn_save.hide()
                self.btn_edit.show()
            else:
                QMessageBox.critical(self, "Erreur", "Erreur lors de l'enregistrement")

        except ValueError:
            QMessageBox.warning(
                self,
                "Erreur",
                "Vérifiez les champs numériques (chevaux, places, CO₂)."
            )

    def delete(self):
        """
        Delete the user's car.
        """
        if not self.main_window.current_user:
            QMessageBox.warning(self, "Erreur", "Utilisateur non connecté")
            return

        user_id = self.main_window.current_user["id"]
        _, status = VoitureController.delete_voiture(user_id)

        if status == 200:
            QMessageBox.information(self, "Succès", "Voiture supprimée ✔")
            self.clear_fields()
        else:
            QMessageBox.critical(self, "Erreur", "Erreur lors de la suppression")

    def go_back(self):
        """
        Return to the profile view.
        """
        self.main_window.switch_to("profile")

    # ==================================================
    # REFRESH
    # ==================================================
    def showEvent(self, event):
        """
        Automatically reload car data when the view is shown.
        """
        super().showEvent(event)

        if not self.main_window.current_user:
            return

        user_id = self.main_window.current_user["id"]
        resp, status = VoitureController.get_voiture(user_id)

        if status == 200 and resp:
            car = resp[0]
            self.marque.setText(car.get("marque", ""))
            self.modele.setText(car.get("modele", ""))
            self.chevaux.setText(str(car.get("chevaux_fiscaux", "")))
            self.places.setText(str(car.get("places_max", "")))
            self.co2.setText(str(car.get("taux_co2", "")))
            self.motorisation.setCurrentText(
                car.get("motorisation", "thermique")
            )
        else:
            self.clear_fields()

    def clear_fields(self):
        """
        Clear all car input fields.
        """
        for field in self.fields:
            field.clear()
        self.motorisation.setCurrentIndex(0)
