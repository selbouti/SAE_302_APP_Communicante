from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QTableWidget,
    QTableWidgetItem
)
from controllers.trajet_controller import TrajetController
from views.common_style import COMMON_STYLE


class MesTrajetsView(QWidget):
    """
    View for listing and managing the user's trips.

    This view allows:
    - listing trips created by the user
    - distinguishing driver vs. passenger trips
    - toggling a trip mode
    - deleting a trip
    """

    def __init__(self, main_window):
        """
        Initialize the MesTrajets view.

        :param main_window: main application window
        """
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        """
        Build the view's user interface.
        """
        layout = QVBoxLayout()

        title = QLabel("Mes trajets")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            'Départ', 'Arrivée', 'Date', 'Heure', 'Retour',
            'Voiture', 'Mode', 'Prix',
            'Changer mode', 'Supprimer'
        ])
        layout.addWidget(self.table)

        refresh = QPushButton("Rafraîchir")
        refresh.clicked.connect(self.charger)
        layout.addWidget(refresh)

        back = QPushButton("Retour")
        back.clicked.connect(
            lambda: self.main_window.switch_to('home')
        )
        layout.addWidget(back)

        layout.addStretch()
        self.setLayout(layout)

        # ---------- Style ----------
        self.setStyleSheet(COMMON_STYLE)

    def showEvent(self, event):
        """
        Called automatically when the view becomes visible.

        Reloads the trip list.
        """
        super().showEvent(event)
        self.charger()

    def charger(self):
        """
        Load trips for the logged-in user from the server API.
        """
        if not self.main_window.current_user:
            return

        try:
            resp, status = TrajetController.lister_trajets(
                self.main_window.current_user["id"]
            )

            if status == 200:
                self.table.setRowCount(0)

                for t in resp:
                    row = self.table.rowCount()
                    self.table.insertRow(row)

                    est_passager = t.get('mode', '') == 'passager'

                    self.table.setItem(
                        row, 0,
                        QTableWidgetItem(t.get('depart', ''))
                    )
                    self.table.setItem(
                        row, 1,
                        QTableWidgetItem(t.get('arrivee', ''))
                    )
                    self.table.setItem(
                        row, 2,
                        QTableWidgetItem(t.get('date_depart', ''))
                    )
                    self.table.setItem(
                        row, 3,
                        QTableWidgetItem(t.get('heure_depart', ''))
                    )
                    self.table.setItem(
                        row, 4,
                        QTableWidgetItem(t.get('heure_retour', ''))
                    )

                    # Voiture masquée si passager
                    voiture = f"{t.get('marque', 'N/A')} {t.get('modele', '')}".strip()
                    self.table.setItem(
                        row, 5,
                        QTableWidgetItem('' if est_passager else voiture)
                    )

                    self.table.setItem(
                        row, 6,
                        QTableWidgetItem(t.get('mode', ''))
                    )

                    prix = t.get('prix_par_place', '')
                    prix_affiche = '' if est_passager else str(prix if prix is not None else '')
                    self.table.setItem(
                        row, 7,
                        QTableWidgetItem(prix_affiche)
                    )

                    toggle_btn = QPushButton("Basculer")
                    toggle_btn.clicked.connect(
                        lambda _, t_id=t['id'], mode=t.get('mode', ''):
                        self.basculer_mode(t_id, mode)
                    )
                    self.table.setCellWidget(row, 8, toggle_btn)

                    delete_btn = QPushButton("Supprimer")
                    delete_btn.clicked.connect(
                        lambda _, t_id=t['id']:
                        self.supprimer(t_id)
                    )
                    self.table.setCellWidget(row, 9, delete_btn)

        except Exception as e:
            print(f"Erreur chargement trajets: {e}")

    def supprimer(self, trajet_id):
        """
        Delete a trip via the server API.

        :param trajet_id: trip identifier
        """
        try:
            TrajetController.supprimer_trajet(trajet_id)
            self.charger()
        except Exception as e:
            print(f"Erreur suppression: {e}")

    def basculer_mode(self, trajet_id, mode_actuel):
        """
        Toggle a trip mode between driver and passenger.

        :param trajet_id: trip identifier
        :param mode_actuel: current trip mode
        """
        resp, status = TrajetController.basculer_mode(
            trajet_id,
            mode_actuel
        )
        if status == 200:
            self.charger()
        else:
            print(f"Erreur changement mode: {resp}")
