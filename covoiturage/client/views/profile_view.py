from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton,
    QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from controllers.profile_controller import ProfileController
from views.common_style import COMMON_STYLE


class ProfileView(QWidget):
    """
    User profile view.

    This view allows the user to:
    - display personal information
    - edit profile data
    - navigate to vehicle management
    """

    def __init__(self, main_window):
        """
        Initialize the Profile view.

        :param main_window: Main application window
        """
        super().__init__()
        self.main_window = main_window

        # ================== Layout principal ==================
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignTop)

        # ================== Titre ==================
        title = QLabel("👤 Mon profil")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        # ================== Formulaire ==================
        form = QFormLayout()
        form.setSpacing(8)

        self.nom = QLineEdit()
        self.prenom = QLineEdit()
        self.email = QLineEdit()
        self.telephone = QLineEdit()

        self.fields = [
            self.nom, self.prenom,
            self.email, self.telephone
        ]

        for field in self.fields:
            field.setReadOnly(True)

        form.addRow("Nom :", self.nom)
        form.addRow("Prénom :", self.prenom)
        form.addRow("Email :", self.email)
        form.addRow("Téléphone :", self.telephone)

        layout.addLayout(form)

        # ================== Boutons ==================
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_edit = QPushButton("✏️ Modifier")
        self.btn_save = QPushButton("💾 Enregistrer")
        self.btn_voiture = QPushButton("🚗 Ma voiture")
        self.btn_back = QPushButton("⬅ Retour")

        # Mode lecture seule par défaut
        self.btn_save.hide()

        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_voiture)
        btn_layout.addWidget(self.btn_back)

        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet(COMMON_STYLE)

        # ================== Connexions ==================
        self.btn_edit.clicked.connect(self.enable_edit)
        self.btn_save.clicked.connect(self.save)
        self.btn_voiture.clicked.connect(self.go_voiture)
        self.btn_back.clicked.connect(self.go_back)

    # ==================================================
    # CHARGEMENT DU PROFIL
    # ==================================================
    def load(self):
        """
        Load the user profile data from the server.

        Redirects to the login view if no user is connected.
        """
        if not self.main_window.current_user:
            self.main_window.switch_to("login")
            return

        user_id = self.main_window.current_user["id"]
        response, status = ProfileController.get_profile(user_id)

        if status != 200:
            QMessageBox.critical(
                self, "Erreur", "Impossible de charger le profil"
            )
            return

        # Remplissage des champs
        self.nom.setText(response["user"].get("nom", ""))
        self.prenom.setText(response["user"].get("prenom", ""))
        self.email.setText(response["user"].get("email", ""))
        self.telephone.setText(response["user"].get("telephone", ""))

        self.set_editable(False)

    # ==================================================
    # MODE ÉDITION
    # ==================================================
    def enable_edit(self):
        """
        Enable edit mode for profile fields.
        """
        self.set_editable(True)

    def set_editable(self, editable):
        """
        Enable or disable editing of profile fields.

        :param editable: True to enable editing, False otherwise
        """
        for field in self.fields:
            field.setReadOnly(not editable)

        self.btn_edit.setVisible(not editable)
        self.btn_save.setVisible(editable)

    # ==================================================
    # SAUVEGARDE
    # ==================================================
    def save(self):
        """
        Save profile updates to the server.
        """
        user_id = self.main_window.current_user["id"]

        data = {
            "nom": self.nom.text(),
            "prenom": self.prenom.text(),
            "email": self.email.text(),
            "telephone": self.telephone.text()
        }

        response, status = ProfileController.update_profile(user_id, data)

        if status == 200:
            QMessageBox.information(
                self, "Succès", "Profil mis à jour ✔"
            )
            self.set_editable(False)
        else:
            QMessageBox.critical(
                self, "Erreur", "Erreur lors de la mise à jour"
            )

    # ==================================================
    # NAVIGATION
    # ==================================================
    def go_voiture(self):
        """
        Navigate to the vehicle management view.
        """
        self.main_window.switch_to("voiture")

    def go_back(self):
        """
        Return to the home view.
        """
        self.main_window.switch_to("home")
