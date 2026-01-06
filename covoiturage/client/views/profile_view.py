from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton,
    QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from controllers.profile_controller import ProfileController


class ProfileView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.edit_mode = False

        # -------- Layout principal --------
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignTop)

        # -------- Titre --------
        title = QLabel("👤 Mon profil")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            color:#C62828;
        """)
        layout.addWidget(title)

        # -------- Formulaire (COMME VoitureView) --------
        form = QFormLayout()
        form.setSpacing(8)

        self.nom = QLineEdit()
        self.prenom = QLineEdit()
        self.email = QLineEdit()
        self.telephone = QLineEdit()

        self.fields = [self.nom, self.prenom, self.email, self.telephone]

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

        form.addRow("Nom :", self.nom)
        form.addRow("Prénom :", self.prenom)
        form.addRow("Email :", self.email)
        form.addRow("Téléphone :", self.telephone)

        layout.addLayout(form)

        # -------- Boutons --------
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_edit = QPushButton("✏️ Modifier")
        self.btn_save = QPushButton("💾 Enregistrer")
        self.btn_voiture = QPushButton("🚗 Ma voiture")
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

        self.btn_voiture.setStyleSheet("""
            background-color:white;
            border:1px solid #C62828;
            padding:8px;
        """)

        self.btn_back.setStyleSheet("""
            background-color:white;
            border:1px solid #C62828;
            padding:8px;
        """)

        self.btn_save.hide()

        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_voiture)
        btn_layout.addWidget(self.btn_back)

        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)

        # -------- Signals --------
        self.btn_edit.clicked.connect(self.enable_edit)
        self.btn_save.clicked.connect(self.save)
        self.btn_voiture.clicked.connect(self.go_voiture)
        self.btn_back.clicked.connect(self.go_back)

    # -------- Chargement --------
    def load(self):
        if not self.main_window.current_user:
            self.main_window.switch_to("login")
            return

        user_id = self.main_window.current_user["id"]
        response, status = ProfileController.get_profile(user_id)

        if status != 200:
            QMessageBox.critical(self, "Erreur", "Impossible de charger le profil")
            return

        self.nom.setText(response.get("nom", ""))
        self.prenom.setText(response.get("prenom", ""))
        self.email.setText(response.get("email", ""))
        self.telephone.setText(response.get("telephone", ""))

        self.set_editable(False)

    # -------- Mode édition --------
    def enable_edit(self):
        self.set_editable(True)

    def set_editable(self, editable):
        for field in self.fields:
            field.setReadOnly(not editable)

        self.btn_edit.setVisible(not editable)
        self.btn_save.setVisible(editable)

    # -------- Sauvegarde --------
    def save(self):
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
            self.set_editable(False)
        else:
            QMessageBox.critical(self, "Erreur", "Erreur lors de la mise à jour")

    def go_voiture(self):
        self.main_window.switch_to("voiture")

    def go_back(self):
        self.main_window.switch_to("home")
