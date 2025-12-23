# views/edt_import_view.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QLineEdit
)
from PyQt5.QtCore import Qt


class EDTImportView(QWidget):
    """
    Vue permettant de :
    - visualiser l'EDT actuel (fichier ou URL)
    - mettre à jour l'EDT via fichier .ics ou URL
    - revenir au menu principal
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.edt_file_path = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Titre
        self.title = QLabel("📅 Mettre à jour mon emploi du temps")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Infos EDT actuel
        self.current_edt_label = QLabel()
        self.current_edt_label.setAlignment(Qt.AlignCenter)
        self.current_edt_label.setStyleSheet("margin: 10px;")

        # Bouton fichier
        self.btn_file = QPushButton("Choisir un fichier .ics")
        self.btn_file.clicked.connect(self._choose_file)

        # Champ URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Ou coller ici une URL d'emploi du temps")

        self.btn_url = QPushButton("Mettre à jour via URL")
        self.btn_url.clicked.connect(self._update_from_url)

        # Bouton retour
        self.btn_back = QPushButton("Retour au menu")
        self.btn_back.clicked.connect(self.controller.go_home)

        # Ajout widgets
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.current_edt_label)
        self.layout.addWidget(self.btn_file)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.btn_url)
        self.layout.addWidget(self.btn_back)
        self.layout.addStretch()

    def showEvent(self, event):
        """
        Appelé automatiquement quand la page est affichée.
        Permet de rafraîchir l'état de l'EDT existant.
        """
        self._refresh_current_edt()
        super().showEvent(event)

    # -----------------------
    #  LOGIQUE
    # -----------------------
    def _refresh_current_edt(self):
        """Affiche l'EDT actuel s'il existe."""
        if not self.controller.current_user:
            self.current_edt_label.setText("Aucun utilisateur connecté.")
            return

        edt = self.controller.edt_model.get_edt(self.controller.current_user["id_user"])

        if not edt:
            self.current_edt_label.setText("❌ Aucun emploi du temps enregistré.")
        else:
            if edt["source_type"] == "fichier":
                self.current_edt_label.setText(f"📄 EDT actuel : fichier\n{edt['source']}")
            else:
                self.current_edt_label.setText(f"🌐 EDT actuel : URL\n{edt['source']}")

    def _choose_file(self):
        """Choisir un fichier .ics et l'importer."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choisir un fichier EDT", "", "Fichiers ICS (*.ics)"
        )

        if file_path:
            self.controller.import_edt_file(file_path)
            self._refresh_current_edt()

    def _update_from_url(self):
        """Importer l'EDT depuis une URL."""
        url = self.url_input.text().strip()
        if not url:
            self.controller.main.show_error("Veuillez entrer une URL.")
            return

        self.controller.import_edt_url(url)
        self._refresh_current_edt()
