from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt


class HomePage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()
        titre = QLabel("🚗 Bienvenue sur l'application de covoiturage")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 18px; font-weight: bold;")

        sous_titre = QLabel("Les autres fonctionnalités (trajets, compatibilités, etc.) viendront ici.")
        sous_titre.setAlignment(Qt.AlignCenter)

        btn_deconnexion = QPushButton("Se déconnecter")
        btn_deconnexion.clicked.connect(self.controller.go_login)

        layout.addWidget(titre)
        layout.addWidget(sous_titre)
        layout.addWidget(btn_deconnexion)
        layout.addStretch()
        self.setLayout(layout)
