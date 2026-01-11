from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from controllers.reservation_controller import ReservationController
from services.api_service import APIService
from views.common_style import COMMON_STYLE


class RechercherView(QWidget):
    """
    Trip search view.

    This view allows a user to:
    - search for available trips using departure, arrival and date
    - display search results in a table
    - create a reservation for a selected trip
    """

    def __init__(self, main_window):
        """
        Initialize the trip search view.

        :param main_window: Reference to the main application window
        :type main_window: QMainWindow
        """
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        """
        Build and configure the graphical user interface.

        This method creates:
        - input fields for search criteria
        - a results table
        - action buttons
        """
        layout = QVBoxLayout()

        title = QLabel("Chercher un trajet")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        layout.addWidget(QLabel("Départ :"))
        self.depart = QLineEdit()
        layout.addWidget(self.depart)

        layout.addWidget(QLabel("Arrivée :"))
        self.arrivee = QLineEdit()
        layout.addWidget(self.arrivee)

        layout.addWidget(QLabel("Date (YYYY-MM-DD) :"))
        self.date = QLineEdit()
        layout.addWidget(self.date)

        search = QPushButton("Rechercher")
        search.clicked.connect(self.rechercher)
        layout.addWidget(search)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Départ", "Arrivée", "Date", "Heure",
            "Places", "Prix", "Conducteur", "Action"
        ])
        layout.addWidget(self.table)

        back = QPushButton("Retour")
        back.clicked.connect(lambda: self.main_window.switch_to("home"))
        layout.addWidget(back)

        self.setLayout(layout)
        self.setStyleSheet(COMMON_STYLE)

    def rechercher(self):
        """
        Search for trips using the provided criteria.

        Sends a request to the API with the departure, arrival and date,
        then displays the results in the table if successful.
        """
        data = {
            "depart": self.depart.text(),
            "arrivee": self.arrivee.text(),
            "date_depart": self.date.text()
        }

        resp, status = APIService.post("trajets/rechercher", data)

        if status == 200:
            self.table.setRowCount(0)

            for trajet in resp:
                row = self.table.rowCount()
                self.table.insertRow(row)

                self.table.setItem(row, 0, QTableWidgetItem(trajet["depart"]))
                self.table.setItem(row, 1, QTableWidgetItem(trajet["arrivee"]))
                self.table.setItem(row, 2, QTableWidgetItem(trajet["date_depart"]))
                self.table.setItem(
                    row, 3,
                    QTableWidgetItem(trajet.get("heure_depart", ""))
                )
                self.table.setItem(
                    row, 4,
                    QTableWidgetItem(str(trajet["places_disponibles"]))
                )
                self.table.setItem(
                    row, 5,
                    QTableWidgetItem(str(trajet["prix_par_place"]))
                )
                self.table.setItem(
                    row, 6,
                    QTableWidgetItem(f"{trajet['prenom']} {trajet['nom']}")
                )

                btn = QPushButton("Réserver")
                btn.clicked.connect(
                    lambda _, t_id=trajet["id"]: self.reserver(t_id)
                )
                self.table.setCellWidget(row, 7, btn)

    def reserver(self, trajet_id):
        """
        Create a reservation for the selected trip.

        :param trajet_id: Identifier of the selected trip
        :type trajet_id: int
        """
        resp, status = ReservationController.creer_reservation(
            trajet_id,
            self.main_window.current_user["id"],
            1
        )

        if status == 201:
            QMessageBox.information(
                self,
                "Succès",
                "Réservation créée !"
            )
            self.rechercher()
        else:
            QMessageBox.warning(
                self,
                "Erreur",
                resp.get("error", "Erreur")
            )
