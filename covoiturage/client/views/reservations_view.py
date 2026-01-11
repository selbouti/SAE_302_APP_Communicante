# ============= views/reservations_view.py =============
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem,
    QTabWidget, QMessageBox, QLabel
)
from controllers.reservation_controller import ReservationController
from views.common_style import COMMON_STYLE


class ReservationsView(QWidget):
    """
    View for managing reservations.

    This view displays both received and made reservations.
    It allows the user to accept, refuse, or cancel reservations.
    """

    def __init__(self, main_window):
        """
        Initialize the ReservationsView.

        :param main_window: Reference to the main application window
        """
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def load(self):
        """
        Load and refresh all reservation data.
        """
        self.charger_reservations_recues()
        self.charger_reservations_faites()

    def setup_ui(self):
        """
        Initialize the user interface with tabs and tables.
        """
        layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()

        # ===== Received reservations =====
        widget_recues = QWidget()
        layout_recues = QVBoxLayout()
        layout_recues.addWidget(QLabel("Réservations reçues sur mes trajets"))

        self.table_res_recues = QTableWidget()
        self.table_res_recues.setColumnCount(8)
        self.table_res_recues.setHorizontalHeaderLabels([
            "Départ", "Arrivée", "Passager", "Places",
            "Statut", "Date", "Accepter", "Refuser"
        ])
        layout_recues.addWidget(self.table_res_recues)

        btn_refresh_recues = QPushButton("Rafraîchir")
        btn_refresh_recues.clicked.connect(self.charger_reservations_recues)
        layout_recues.addWidget(btn_refresh_recues)

        widget_recues.setLayout(layout_recues)
        self.tabs.addTab(widget_recues, "Reçues")

        # ===== Made reservations =====
        widget_faites = QWidget()
        layout_faites = QVBoxLayout()
        layout_faites.addWidget(QLabel("Mes réservations"))

        self.table_res_faites = QTableWidget()
        self.table_res_faites.setColumnCount(7)
        self.table_res_faites.setHorizontalHeaderLabels([
            "Départ", "Arrivée", "Conducteur",
            "Places", "Statut", "Date", "Annuler"
        ])
        layout_faites.addWidget(self.table_res_faites)

        btn_refresh_faites = QPushButton("Rafraîchir")
        btn_refresh_faites.clicked.connect(self.charger_reservations_faites)
        layout_faites.addWidget(btn_refresh_faites)

        widget_faites.setLayout(layout_faites)
        self.tabs.addTab(widget_faites, "Faites")

        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.setStyleSheet(COMMON_STYLE)

    # ==================================================
    # DATA LOADING
    # ==================================================
    def charger_reservations_recues(self):
        """
        Load reservations received on the user's trips.
        """
        reservations, error = ReservationController.get_reservations_recues(
            self.main_window.current_user["id"]
        )

        if error:
            QMessageBox.warning(self, "Erreur", error)
            return

        self.table_res_recues.setRowCount(0)
        for res in reservations:
            row = self.table_res_recues.rowCount()
            self.table_res_recues.insertRow(row)

            self.table_res_recues.setItem(row, 0, QTableWidgetItem(res.depart))
            self.table_res_recues.setItem(row, 1, QTableWidgetItem(res.arrivee))
            self.table_res_recues.setItem(row, 2, QTableWidgetItem(f"{res.prenom} {res.nom}"))
            self.table_res_recues.setItem(row, 3, QTableWidgetItem(str(res.places_reservees)))
            self.table_res_recues.setItem(row, 4, QTableWidgetItem(res.statut))
            self.table_res_recues.setItem(row, 5, QTableWidgetItem(res.created_at[:10]))

            btn_accept = QPushButton("✓")
            btn_accept.clicked.connect(
                lambda _, rid=res.id: self.accepter_reservation(rid)
            )
            self.table_res_recues.setCellWidget(row, 6, btn_accept)

            btn_refuse = QPushButton("✗")
            btn_refuse.clicked.connect(
                lambda _, rid=res.id: self.refuser_reservation(rid)
            )
            self.table_res_recues.setCellWidget(row, 7, btn_refuse)

    def charger_reservations_faites(self):
        """
        Load reservations made by the user.
        """
        reservations, error = ReservationController.get_reservations_faites(
            self.main_window.current_user["id"]
        )

        if error:
            QMessageBox.warning(self, "Erreur", error)
            return

        self.table_res_faites.setRowCount(0)
        for res in reservations:
            row = self.table_res_faites.rowCount()
            self.table_res_faites.insertRow(row)

            self.table_res_faites.setItem(row, 0, QTableWidgetItem(res.depart))
            self.table_res_faites.setItem(row, 1, QTableWidgetItem(res.arrivee))
            self.table_res_faites.setItem(row, 2, QTableWidgetItem(f"{res.prenom} {res.nom}"))
            self.table_res_faites.setItem(row, 3, QTableWidgetItem(str(res.places_reservees)))
            self.table_res_faites.setItem(row, 4, QTableWidgetItem(res.statut))
            self.table_res_faites.setItem(row, 5, QTableWidgetItem(res.created_at[:10]))

            btn_cancel = QPushButton("✗")
            btn_cancel.clicked.connect(
                lambda _, rid=res.id: self.annuler_reservation(rid)
            )
            self.table_res_faites.setCellWidget(row, 6, btn_cancel)

    # ==================================================
    # ACTIONS
    # ==================================================
    def accepter_reservation(self, reservation_id):
        """
        Accept a reservation.

        :param reservation_id: Reservation identifier
        """
        success, msg = ReservationController.accepter_reservation(reservation_id)
        if success:
            QMessageBox.information(self, "Succès", msg)
            self.charger_reservations_recues()
        else:
            QMessageBox.warning(self, "Erreur", msg)

    def refuser_reservation(self, reservation_id):
        """
        Refuse a reservation.

        :param reservation_id: Reservation identifier
        """
        success, msg = ReservationController.refuser_reservation(reservation_id)
        if success:
            QMessageBox.information(self, "Succès", msg)
            self.charger_reservations_recues()
        else:
            QMessageBox.warning(self, "Erreur", msg)

    def annuler_reservation(self, reservation_id):
        """
        Cancel a reservation made by the user.

        :param reservation_id: Reservation identifier
        """
        success, msg = ReservationController.annuler_reservation(reservation_id)
        if success:
            QMessageBox.information(self, "Succès", msg)
            self.charger_reservations_faites()
        else:
            QMessageBox.warning(self, "Erreur", msg)
