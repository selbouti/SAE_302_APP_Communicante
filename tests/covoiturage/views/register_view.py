# views/register_view.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout,
    QLineEdit, QPushButton, QCheckBox, QComboBox, QFileDialog
)
from PyQt5.QtCore import Qt


class RegisterPage(QWidget):
    """
    Page d'inscription complète :
    - Informations utilisateur
    - Informations voiture
    - Import EDT (fichier .ics ou URL)
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()

        titre = QLabel("📝 Inscription")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 18px; font-weight: bold;")

        form = QFormLayout()

        # ----------- Champs utilisateur -----------
        self.nom = QLineEdit()
        self.prenom = QLineEdit()
        self.login = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.email = QLineEdit()
        self.telephone = QLineEdit()
        self.adresse = QLineEdit()
        self.ville = QLineEdit()
        self.cp = QLineEdit()

        form.addRow("Nom :", self.nom)
        form.addRow("Prénom :", self.prenom)
        form.addRow("Login :", self.login)
        form.addRow("Mot de passe :", self.password)
        form.addRow("Email :", self.email)
        form.addRow("Téléphone :", self.telephone)
        form.addRow("Adresse :", self.adresse)
        form.addRow("Ville :", self.ville)
        form.addRow("Code postal :", self.cp)

        # ----------- Possède une voiture ? -----------
        self.has_car = QCheckBox("Je possède une voiture")
        self.has_car.stateChanged.connect(self._toggle_car_fields)
        form.addRow(self.has_car)

        # ----------- Champs voiture -----------
        self.marque = QLineEdit()
        self.modele = QLineEdit()
        self.chevaux = QLineEdit()
        self.taux_co2 = QLineEdit()
        self.places = QLineEdit()

        self.motorisation = QComboBox()
        self.motorisation.addItems(["thermique", "hybride", "hydrogene", "electrique"])

        form.addRow("Marque :", self.marque)
        form.addRow("Modèle :", self.modele)
        form.addRow("Chevaux fiscaux :", self.chevaux)
        form.addRow("Motorisation :", self.motorisation)
        form.addRow("Taux CO2 (g/km) :", self.taux_co2)
        form.addRow("Places :", self.places)

        # Masquer les champs voiture au départ
        self._toggle_car_fields()

        # ----------- Import EDT -----------
        self.edt_file_path = None
        self.edt_url = QLineEdit()

        btn_import_file = QPushButton("Importer un fichier .ics")
        btn_import_file.clicked.connect(self._choose_file)

        form.addRow("Emploi du temps (fichier) :", btn_import_file)
        form.addRow("Emploi du temps (URL) :", self.edt_url)

        # ----------- Boutons -----------
        btn_creer = QPushButton("Créer le compte")
        btn_retour = QPushButton("Retour")

        btn_creer.clicked.connect(self._on_register_clicked)
        btn_retour.clicked.connect(self.controller.go_login)

        layout.addWidget(titre)
        layout.addLayout(form)
        layout.addWidget(btn_creer)
        layout.addWidget(btn_retour)
        layout.addStretch()

        self.setLayout(layout)

    def _toggle_car_fields(self):
        """Affiche ou masque les champs voiture."""
        visible = self.has_car.isChecked()
        for widget in [
            self.marque, self.modele, self.chevaux,
            self.motorisation, self.taux_co2, self.places
        ]:
            widget.setVisible(visible)

    def _choose_file(self):
        """Choisir un fichier .ics"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choisir un fichier EDT", "", "Fichiers ICS (*.ics)"
        )
        if file_path:
            self.edt_file_path = file_path

    def _on_register_clicked(self):
        user_data = {
            "nom": self.nom.text().strip(),
            "prenom": self.prenom.text().strip(),
            "login": self.login.text().strip(),
            "mot_de_passe": self.password.text().strip(),
            "email": self.email.text().strip(),
            "telephone": self.telephone.text().strip(),
            "adresse": self.adresse.text().strip(),
            "ville": self.ville.text().strip(),
            "cp": self.cp.text().strip(),
        }

        if not all(user_data.values()):
            self.controller.main.show_error("Tous les champs utilisateur doivent être remplis.")
            return

        car_data = None
        if self.has_car.isChecked():
            car_data = {
                "marque": self.marque.text().strip(),
                "modele": self.modele.text().strip(),
                "chevaux_fiscaux": self.chevaux.text().strip(),
                "motorisation": self.motorisation.currentText(),
                "taux_co2": self.taux_co2.text().strip(),
                "places_max": self.places.text().strip(),
            }
            if not all(car_data.values()):
                self.controller.main.show_error("Tous les champs voiture doivent être remplis.")
                return

        # Détection source EDT
        edt_source = None
        if self.edt_file_path:
            edt_source = ("file", self.edt_file_path)
        elif self.edt_url.text().strip():
            edt_source = ("url", self.edt_url.text().strip())

        # Appel contrôleur
        self.controller.register(user_data, car_data, edt_source)
