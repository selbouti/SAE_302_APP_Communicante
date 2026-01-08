from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton,
    QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from controllers.user_controller import UserController

import os


class RegisterView(QWidget):
    """
    Vue d'inscription des utilisateurs.

    Cette vue permet :
    - la création d'un compte utilisateur
    - la saisie des informations personnelles
    - l'import optionnel d'un fichier iCalendar (.ics)
    """

    def __init__(self, main_window):
        """
        Initialise la vue d'inscription.

        :param main_window: fenêtre principale de l'application
        """
        super().__init__()
        self.main_window = main_window
        self.ical_file = None
        self.setup_ui()

    def setup_ui(self):
        """
        Construit l'interface graphique de la vue d'inscription.
        """
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(40, 30, 40, 30)

        # ---------- Titre ----------
        title = QLabel("📝 Inscription")
        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            color:#C62828;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # ---------- Champs ----------
        def styled_input():
            field = QLineEdit()
            field.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #C62828;
                    border-radius: 4px;
                }
            """)
            return field

        def label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("font-weight:bold;")
            return lbl

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

        layout.addWidget(label("Fichier iCalendar (optionnel) :"))
        self.file_label = QLabel("Aucun fichier sélectionné")
        self.file_label.setStyleSheet("color:gray;")
        layout.addWidget(self.file_label)

        browse_btn = QPushButton("📂 Parcourir...")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #C62828;
                padding: 8px;
                font-weight:bold;
            }
            QPushButton:hover {
                background-color: #C62828;
                color: white;
            }
        """)
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn)

        # ---------- Boutons ----------
        register_btn = QPushButton("S'inscrire")
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #C62828;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B71C1C;
            }
        """)
        register_btn.clicked.connect(self.register)
        layout.addWidget(register_btn)

        back_btn = QPushButton("⬅ Retour")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #C62828;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C62828;
                color: white;
            }
        """)
        back_btn.clicked.connect(
            lambda: self.main_window.switch_to('login')
        )
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def browse_file(self):
        """
        Ouvre une boîte de dialogue pour sélectionner
        un fichier iCalendar (.ics).
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner fichier iCalendar",
            "",
            "ICS Files (*.ics)"
        )
        if file_path:
            self.ical_file = file_path
            self.file_label.setText(os.path.basename(file_path))

    def register(self):
        """
        Enregistre un nouvel utilisateur via l'API serveur.
        """
        resp, status = UserController.register(
            self.email.text(),
            self.password.text(),
            self.nom.text(),
            self.prenom.text(),
            self.phone.text()
        )

        if status == 201:
            user_id = resp['id']

            if self.ical_file:
                resp2, status2 = UserController.upload_icalendar(
                    user_id, self.ical_file
                )
                if status2 == 201:
                    QMessageBox.information(
                        self, "Succès",
                        "Inscription et trajets importés !"
                    )
                else:
                    QMessageBox.warning(
                        self, "Avertissement",
                        "Inscription OK mais erreur import iCalendar"
                    )
            else:
                QMessageBox.information(
                    self, "Succès",
                    "Inscription réussie !"
                )

            self.main_window.switch_to('login')
        else:
            QMessageBox.warning(
                self, "Erreur",
                resp.get('error', 'Erreur lors de l’inscription')
            )
