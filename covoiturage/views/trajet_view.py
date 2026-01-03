from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout, QDateEdit, QTimeEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt, QDate, QTime


class TrajetView(QWidget):
    """
    Vue simple pour créer un trajet et lister les trajets du conducteur.
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()
        form = QFormLayout()

        title = QLabel("🚌 Mes trajets")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:bold;")

        # Champs principaux
        self.date_depart = QDateEdit(QDate.currentDate())
        self.date_depart.setCalendarPopup(True)
        self.heure_depart = QTimeEdit(QTime.currentTime())

        self.date_arrivee = QDateEdit(QDate.currentDate())
        self.date_arrivee.setCalendarPopup(True)
        self.heure_arrivee = QTimeEdit(QTime.currentTime())

        self.lieu_depart = QLineEdit()
        self.lieu_arrivee = QLineEdit()

        self.km = QSpinBox()
        self.km.setRange(0, 2000)
        self.peage = QDoubleSpinBox()
        self.peage.setRange(0, 9999)
        self.peage.setDecimals(2)

        form.addRow("Date départ :", self.date_depart)
        form.addRow("Heure départ :", self.heure_depart)
        form.addRow("Date arrivée :", self.date_arrivee)
        form.addRow("Heure arrivée :", self.heure_arrivee)
        form.addRow("Lieu départ :", self.lieu_depart)
        form.addRow("Lieu arrivée :", self.lieu_arrivee)
        form.addRow("Kilométrage :", self.km)
        form.addRow("Coût péage (€) :", self.peage)

        # Boutons action
        btn_create = QPushButton("Créer le trajet")
        btn_refresh = QPushButton("Rafraîchir la liste")
        btn_back = QPushButton("⬅ Retour")

        btn_create.clicked.connect(self._create_trajet)
        btn_refresh.clicked.connect(self.refresh_table)
        btn_back.clicked.connect(self.controller.user_controller.go_home)

        actions = QHBoxLayout()
        actions.addWidget(btn_create)
        actions.addWidget(btn_refresh)
        actions.addWidget(btn_back)

        # Tableau des trajets
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Date départ", "Heure départ", "Lieu départ",
            "Lieu arrivée", "KM", "Péage"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(actions)
        layout.addWidget(self.table)
        layout.addStretch()
        self.setLayout(layout)

    def showEvent(self, event):
        """Recharge la liste à chaque affichage."""
        self.refresh_table()
        super().showEvent(event)

    def _create_trajet(self):
        # Récupération de la voiture du conducteur
        car = None
        user_ctrl = self.controller.user_controller
        if user_ctrl.current_user:
            car = user_ctrl.voiture_model.get_user_voiture(user_ctrl.current_user["id_user"])
        if not car:
            self.controller.main.show_error("Enregistrez d'abord votre voiture.")
            return

        data = {
            "voiture_id": car["id_voiture"],
            "date_depart": self.date_depart.date().toPyDate(),
            "heure_depart": self.heure_depart.time().toPyTime(),
            "date_arrivee": self.date_arrivee.date().toPyDate(),
            "heure_arrivee": self.heure_arrivee.time().toPyTime(),
            "lieu_depart": self.lieu_depart.text().strip(),
            "lieu_arrivee": self.lieu_arrivee.text().strip(),
            "kilometrage": self.km.value(),
            "cout_peage": self.peage.value(),
        }

        if not data["lieu_depart"] or not data["lieu_arrivee"]:
            self.controller.main.show_error("Renseignez les lieux de départ et d'arrivée.")
            return

        trajet_id = self.controller.create_trajet(data)
        if trajet_id:
            self.refresh_table()

    def refresh_table(self):
        trajets = self.controller.mes_trajets()
        self.table.setRowCount(len(trajets))
        for row, trajet in enumerate(trajets):
            values = [
                str(trajet["date_depart"]),
                str(trajet["heure_depart"]),
                trajet["lieu_depart"],
                trajet["lieu_arrivee"],
                str(trajet["kilometrage"]),
                str(trajet.get("cout_peage", "")),
            ]
            for col, val in enumerate(values):
                self.table.setItem(row, col, QTableWidgetItem(val))
