from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox,
    QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from controllers.user_controller import UserController
from views.common_style import COMMON_STYLE

import os


class RegisterView(QWidget):
    """
    User registration view.

    This view allows a new user to:
    - create an account
    - optionally register a car
    - optionally import an iCalendar (.ics) file
    """

    def __init__(self, main_window):
        """
        Initialize the registration view.

        :param main_window: reference to the main application window
        """
        super().__init__()
        self.main_window = main_window
        self.ical_file = None
        self.setup_ui()

    def setup_ui(self):
        """
        Build and configure the registration user interface.
        """
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(40, 30, 40, 30)

        def styled_input():
            return QLineEdit()

        def label(text):
            return QLabel(text)

        # ---------- Titre ----------
        title = QLabel("📝 Inscription")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # ---------- Champs utilisateur ----------
        layout.addWidget(label("Nom :"))
        self.nom = styled_input()
        layout.addWidget(self.nom)

        layout.addWidget(label("Prénom :"))
        self.prenom = styled_input()
        layout.addWidget(self.prenom)

        layout.addWidget(label("Mot de passe :"))
        self.password = styled_input()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        layout.addWidget(label("Email :"))
        self.email = styled_input()
        layout.addWidget(self.email)

        layout.addWidget(label("Téléphone :"))
        self.phone = styled_input()
        layout.addWidget(self.phone)

        # ---------- Checkbox "J'ai une voiture" ----------
        self.has_car_checkbox = QCheckBox("🚗 J'ai une voiture")
        self.has_car_checkbox.stateChanged.connect(self.toggle_car_fields)
        layout.addWidget(self.has_car_checkbox)

        # ---------- Champs voiture (initialement cachés) ----------
        self.car_fields_container = QWidget()
        car_layout = QVBoxLayout()
        car_layout.setSpacing(5)

        self.marque = styled_input()
        self.marque.setPlaceholderText("Marque")
        car_layout.addWidget(self.marque)

        self.modele = styled_input()
        self.modele.setPlaceholderText("Modèle")
        car_layout.addWidget(self.modele)

        self.chevaux_fiscaux = styled_input()
        self.chevaux_fiscaux.setPlaceholderText("Chevaux fiscaux")
        car_layout.addWidget(self.chevaux_fiscaux)

        self.motorisation = styled_input()
        self.motorisation.setPlaceholderText("Motorisation")
        car_layout.addWidget(self.motorisation)

        self.taux_co2 = styled_input()
        self.taux_co2.setPlaceholderText("Taux CO2")
        car_layout.addWidget(self.taux_co2)

        self.places_max = styled_input()
        self.places_max.setPlaceholderText("Nombre de places")
        car_layout.addWidget(self.places_max)

        self.car_fields_container.setLayout(car_layout)
        self.car_fields_container.setVisible(False)  # caché par défaut
        layout.addWidget(self.car_fields_container)

        # ---------- Fichier iCalendar ----------
        layout.addWidget(label("Fichier iCalendar (optionnel) :"))
        self.file_label = QLabel("Aucun fichier sélectionné")
        layout.addWidget(self.file_label)

        browse_btn = QPushButton("📂 Parcourir...")
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn)

        # ---------- Boutons ----------
        register_btn = QPushButton("S'inscrire")
        register_btn.clicked.connect(self.register)
        layout.addWidget(register_btn)

        back_btn = QPushButton("⬅ Retour")
        back_btn.clicked.connect(lambda: self.main_window.switch_to('login'))
        layout.addWidget(back_btn)

        self.setLayout(layout)
        self.setStyleSheet(COMMON_STYLE)

    def toggle_car_fields(self, state):
        """
        Show or hide car input fields depending on the checkbox state.

        :param state: checkbox state (Qt.Checked or Qt.Unchecked)
        """
        self.car_fields_container.setVisible(state == Qt.Checked)

    def browse_file(self):
        """
        Open a file dialog to select an iCalendar (.ics) file.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner fichier iCalendar", "", "ICS Files (*.ics)"
        )
        if file_path:
            self.ical_file = file_path
            self.file_label.setText(os.path.basename(file_path))

    def register(self):
        """
        Register a new user via the UserController.

        This method:
        - collects user data
        - optionally collects car data
        - sends the registration request
        - optionally uploads an iCalendar file
        """
        # Construction des données voiture si checkbox cochée
        voiture_data = None
        if self.has_car_checkbox.isChecked():
            try:
                voiture_data = {
                    "marque": self.marque.text(),
                    "modele": self.modele.text(),
                    "chevaux_fiscaux": int(self.chevaux_fiscaux.text()) if self.chevaux_fiscaux.text() else 0,
                    "motorisation": self.motorisation.text(),
                    "taux_co2": float(self.taux_co2.text()) if self.taux_co2.text() else 0.0,
                    "places_max": int(self.places_max.text()) if self.places_max.text() else 0
                }
            except ValueError:
                QMessageBox.warning(self, "Erreur", "Veuillez remplir correctement les champs numériques de la voiture.")
                return

        # Appel au controller
        resp, status = UserController.register(
            self.email.text(),
            self.password.text(),
            self.nom.text(),
            self.prenom.text(),
            self.phone.text(),
            voiture=voiture_data
        )

        if status == 201:
            user_id = resp['id']

            if self.ical_file:
                resp2, status2 = UserController.upload_icalendar(user_id, self.ical_file)
                if status2 == 201:
                    QMessageBox.information(self, "Succès", "Inscription et trajets importés !")
                else:
                    QMessageBox.warning(self, "Avertissement", "Inscription OK mais erreur import iCalendar")
            else:
                QMessageBox.information(self, "Succès", "Inscription réussie !")

            self.main_window.switch_to('login')
        else:
            QMessageBox.warning(self, "Erreur", resp.get('error', 'Erreur lors de l’inscription'))

