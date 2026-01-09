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
    Vue de gestion de la voiture de l'utilisateur.

    Cette vue permet :
    - d'afficher les informations du véhicule associé à l'utilisateur
    - de modifier ces informations après activation du mode édition
    - de supprimer la voiture
    - de revenir à la vue Profil

    Par défaut, les champs sont en lecture seule.
    """

    def __init__(self, main_window):
        """
        Initialise la vue Voiture.

        :param main_window: fenêtre principale de l'application
        :type main_window: MainWindow
        """
        super().__init__()
        self.main_window = main_window

        # ================== Layout principal ==================
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignTop)

        form = QFormLayout()
        form.setSpacing(8)

        title = QLabel("🚗 Ma voiture")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("titleLabel")

        # ================== Champs ==================
        self.marque = QLineEdit()
        self.modele = QLineEdit()
        self.chevaux = QLineEdit()
        self.places = QLineEdit()
        self.co2 = QLineEdit()

        self.motorisation = QComboBox()
        self.motorisation.addItems(
            ["thermique", "hybride", "electrique", "hydrogene"]
        )

        #: Liste des champs pour gérer le mode lecture seule
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

        # ================== Boutons ==================
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_edit = QPushButton("✏️ Modifier")
        self.btn_save = QPushButton("💾 Enregistrer")
        self.btn_delete = QPushButton("❌ Supprimer")
        self.btn_back = QPushButton("⬅ Retour")

        # Bouton sauvegarde masqué tant que pas en édition
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

        # ================== Connexions ==================
        self.btn_edit.clicked.connect(self.enable_edit)
        self.btn_save.clicked.connect(self.save)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_back.clicked.connect(self.go_back)

    # ==================================================
    # MODE ÉDITION
    # ==================================================
    def enable_edit(self):
        """
        Active le mode édition.

        Les champs deviennent modifiables
        et le bouton Enregistrer apparaît.
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
        Enregistre ou met à jour la voiture via l'API serveur.
        """
        if not self.main_window.current_user:
            QMessageBox.warning(
                self, "Erreur", "Utilisateur non connecté"
            )
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
            resp, status = VoitureController.save_voiture(user_id, data)

            if status in (200, 201):
                QMessageBox.information(
                    self, "Succès", "Voiture enregistrée ✔"
                )

                # Repasser en lecture seule
                for field in self.fields:
                    field.setReadOnly(True)

                self.motorisation.setEnabled(False)
                self.btn_save.hide()
                self.btn_edit.show()

            else:
                QMessageBox.critical(
                    self, "Erreur", "Erreur lors de l'enregistrement"
                )

        except ValueError:
            QMessageBox.warning(
                self,
                "Erreur",
                "Vérifiez les champs numériques (chevaux, places, CO₂)."
            )

    def delete(self):
        """
        Supprime la voiture associée à l'utilisateur.
        """
        if not self.main_window.current_user:
            QMessageBox.warning(
                self, "Erreur", "Utilisateur non connecté"
            )
            return

        user_id = self.main_window.current_user["id"]
        resp, status = VoitureController.delete_voiture(user_id)

        if status == 200:
            QMessageBox.information(
                self, "Succès", "Voiture supprimée ✔"
            )
            self.clear_fields()
        else:
            QMessageBox.critical(
                self, "Erreur", "Erreur lors de la suppression"
            )

    def go_back(self):
        """
        Retourne vers la vue Profil utilisateur.
        """
        self.main_window.switch_to("profile")

    # ==================================================
    # RAFRAÎCHISSEMENT
    # ==================================================
    def showEvent(self, event):
        """
        Recharge automatiquement les données de la voiture
        lorsque la vue devient visible.
        """
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
            self.places.setText(str(v.get("places_max", "")))
            self.co2.setText(str(v.get("taux_co2", "")))
            self.motorisation.setCurrentText(
                v.get("motorisation", "thermique")
            )
        else:
            self.clear_fields()

    def clear_fields(self):
        """
        Vide tous les champs de la vue.
        """
        for field in self.fields:
            field.clear()
        self.motorisation.setCurrentIndex(0)
