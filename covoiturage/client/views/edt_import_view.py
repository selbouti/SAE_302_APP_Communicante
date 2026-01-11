# views/edt_import_view.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QLineEdit
)
from PyQt5.QtCore import Qt
from views.common_style import COMMON_STYLE


class EDTImportView(QWidget):
    """
    Timetable (EDT) import view.

    This view allows the user to:
    - display the currently registered timetable (file or URL)
    - update the timetable using a .ics file
    - update the timetable using a URL
    - return to the main menu
    """

    def __init__(self, controller):
        """
        Initialize the EDT import view.

        :param controller: main user controller handling EDT logic
        """
        super().__init__()
        self.controller = controller
        self.edt_file_path = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title
        self.title = QLabel("📅 Mettre à jour mon emploi du temps")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("titleLabel")

        # Current EDT info
        self.current_edt_label = QLabel()
        self.current_edt_label.setAlignment(Qt.AlignCenter)

        # File import
        self.btn_file = QPushButton("Choisir un fichier .ics")
        self.btn_file.clicked.connect(self._choose_file)

        # URL import
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(
            "Ou coller ici une URL d'emploi du temps"
        )

        self.btn_url = QPushButton("Mettre à jour via URL")
        self.btn_url.clicked.connect(self._update_from_url)

        # Back button
        self.btn_back = QPushButton("Retour au menu")
        self.btn_back.clicked.connect(self.controller.go_home)

        # Layout
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.current_edt_label)
        self.layout.addWidget(self.btn_file)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.btn_url)
        self.layout.addWidget(self.btn_back)
        self.layout.addStretch()

        self.setStyleSheet(COMMON_STYLE)

    def showEvent(self, event):
        """
        Triggered automatically when the view is displayed.

        Refreshes the current timetable information.
        """
        self._refresh_current_edt()
        super().showEvent(event)

    def _refresh_current_edt(self):
        """
        Display the current timetable if it exists.
        """
        if not self.controller.current_user:
            self.current_edt_label.setText(
                "Aucun utilisateur connecté."
            )
            return

        edt = self.controller.edt_model.get_edt(
            self.controller.current_user["id_user"]
        )

        if not edt:
            self.current_edt_label.setText(
                "❌ Aucun emploi du temps enregistré."
            )
        else:
            if edt["source_type"] == "fichier":
                self.current_edt_label.setText(
                    f"📄 EDT actuel : fichier\n{edt['source']}"
                )
            else:
                self.current_edt_label.setText(
                    f"🌐 EDT actuel : URL\n{edt['source']}"
                )

    def _choose_file(self):
        """
        Open a file dialog to select a .ics file and import it.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir un fichier EDT",
            "",
            "Fichiers ICS (*.ics)"
        )

        if file_path:
            self.controller.import_edt_file(file_path)
            self._refresh_current_edt()

    def _update_from_url(self):
        """
        Import the timetable from a URL.
        """
        url = self.url_input.text().strip()
        if not url:
            self.controller.main.show_error(
                "Veuillez entrer une URL."
            )
            return

        self.controller.import_edt_url(url)
        self._refresh_current_edt()
