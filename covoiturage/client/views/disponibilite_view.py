from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QDateEdit, QListWidget
)
from PyQt5.QtCore import QDate
from views.common_style import COMMON_STYLE


class DisponibiliteView(QWidget):
    """
    User availability view.

    This view allows the user to:
    - select a date
    - generate availabilities from their timetable (EDT)
    - display available time slots for the selected day
    - navigate back to the home view
    """

    def __init__(self, controller):
        """
        Initialize the availability view.

        :param controller: controller handling availability logic and navigation
        """
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()

        self.title = QLabel("📅 Mes disponibilités")
        self.title.setObjectName("titleLabel")

        self.date_picker = QDateEdit()
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDate(QDate.currentDate())

        self.btn_generate = QPushButton("🔄 Générer depuis l'EDT")
        self.btn_back = QPushButton("⬅ Retour")

        self.list_dispo = QListWidget()

        self.btn_generate.clicked.connect(self.generate)
        self.btn_back.clicked.connect(self.controller.go_home)

        layout.addWidget(self.title)
        layout.addWidget(self.date_picker)
        layout.addWidget(self.btn_generate)
        layout.addWidget(self.list_dispo)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)
        self.setStyleSheet(COMMON_STYLE)

    def generate(self):
        """
        Generate availabilities for the selected date from the timetable.

        This method:
        - retrieves the selected date
        - asks the controller to compute availabilities from the EDT
        - refreshes the displayed list
        """
        date_py = self.date_picker.date().toPyDate()
        self.controller.generate_disponibilites_from_edt(date_py)
        self.refresh()

    def refresh(self):
        """
        Refresh the list of displayed availabilities.

        Availabilities are fetched from the controller's availability model
        and displayed as formatted time ranges.
        """
        self.list_dispo.clear()

        dispos = self.controller.dispo_model.get_user_dispos(
            self.controller.current_user["id_user"]
        )

        for d in dispos:
            self.list_dispo.addItem(
                f"{d['date_dispo']} : {d['heure_debut']} → {d['heure_fin']}"
            )
