from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt

from controllers.matching_controller import MatchingController


class MatchingView(QWidget):
    """
    Vue de matching des trajets compatibles.

    Cette vue permet à l'utilisateur :
    - de sélectionner un de ses trajets
    - d'afficher les trajets compatibles
    - de réserver une place ou inviter un passager
    """

    def __init__(self, main_window):
        """
        Initialise la vue Matching.

        :param main_window: fenêtre principale de l'application
        """
        super().__init__()
        self.main_window = main_window
        self.controller = None
        self.setup_ui()

    # ==================================================
    # INTERFACE UTILISATEUR
    # ==================================================
    def setup_ui(self):
        """
        Construit l'interface graphique.
        """
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(12)

        title = QLabel("🚗 Trajets compatibles")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            color:#C62828;
        """)
        layout.addWidget(title)

        # Sélecteur de trajet
        select_layout = QHBoxLayout()
        label_select = QLabel("Choisir mon trajet :")
        label_select.setStyleSheet("font-weight:bold;")

        self.trajet_combo = QComboBox()
        self.trajet_combo.currentIndexChanged.connect(self.charger)

        select_layout.addWidget(label_select)
        select_layout.addWidget(self.trajet_combo)
        layout.addLayout(select_layout)

        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("color:#444;")
        layout.addWidget(self.info_label)

        # Tableau des trajets
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "Conducteur",
            "Départ",
            "Arrivée",
            "Voiture",
            "Prix",
            "Places",
            "Action"
        ])
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #C62828;
                gridline-color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                color: #C62828;
                font-weight: bold;
                padding: 6px;
            }
        """)
        layout.addWidget(self.table)

        # Boutons
        btn_layout = QHBoxLayout()

        refresh = QPushButton("🔄 Rafraîchir")
        refresh.clicked.connect(self.charger)

        back = QPushButton("⬅ Retour")
        back.clicked.connect(lambda: self.main_window.switch_to("home"))

        for btn in (refresh, back):
            btn.setStyleSheet("""
                QPushButton {
                    background-color:#C62828;
                    color:white;
                    padding:8px;
                    border-radius:4px;
                }
                QPushButton:hover {
                    background-color:#B71C1C;
                }
            """)

        btn_layout.addWidget(refresh)
        btn_layout.addWidget(back)
        layout.addLayout(btn_layout)

    # ==================================================
    # CYCLE DE VIE
    # ==================================================
    def showEvent(self, event):
        """
        Appelé automatiquement lorsque la vue est affichée.
        """
        super().showEvent(event)

        if not self.main_window.current_user:
            self.info_label.setText("Veuillez vous connecter")
            return

        self.controller = MatchingController(
            self.main_window.current_user
        )

        self.charger_trajets_perso()
        self.charger()

    # ==================================================
    # DONNÉES
    # ==================================================
    def charger_trajets_perso(self):
        """
        Charge les trajets personnels de l'utilisateur.
        """
        self.trajet_combo.clear()
        resp, status = self.controller.charger_trajets_perso()

        if status == 200:
            for t in resp:
                label = (
                    f"{t['depart']} → {t['arrivee']} "
                    f"le {t['date_depart']} ({t['mode']})"
                )
                self.trajet_combo.addItem(label, t['id'])

    def charger(self):
        """
        Charge les trajets compatibles.
        """
        self.table.setRowCount(0)
        trajet_id = self.trajet_combo.currentData()

        if not trajet_id:
            self.info_label.setText("Sélectionnez un trajet")
            return

        data, status = self.controller.charger_matching(trajet_id)
        if status != 200:
            self.info_label.setText("Erreur de chargement")
            return

        self.afficher_trajets(data)

    # ==================================================
    # AFFICHAGE
    # ==================================================
    def afficher_trajets(self, data):
        """
        Affiche les trajets compatibles dans le tableau.

        :param data: dictionnaire retourné par le serveur
        """
        mon = data["mon_trajet"]
        trajets = data["trajets_compatibles"]
        mode = data["mode_recherche"]

        self.info_label.setText(
            f"{mon['depart']} → {mon['arrivee']} ({mon['mode']})"
        )

        for trajet in trajets:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(trajet.conducteur))
            self.table.setItem(
                row, 1,
                QTableWidgetItem(f"{trajet.heure_depart} / {trajet.depart}")
            )
            self.table.setItem(
                row, 2,
                QTableWidgetItem(f"{trajet.heure_arrivee} / {trajet.arrivee}")
            )
            self.table.setItem(row, 3, QTableWidgetItem(trajet.voiture))
            self.table.setItem(row, 4, QTableWidgetItem(trajet.prix))
            self.table.setItem(row, 5, QTableWidgetItem(str(trajet.places)))

            if mode == "réservations":
                btn = QPushButton("Réserver")
                btn.setEnabled(not trajet.est_complet())
                btn.clicked.connect(
                    lambda _, tid=trajet.id: self.reserver(tid)
                )
            else:
                btn = QPushButton("Inviter")
                btn.clicked.connect(
                    lambda _, pid=trajet.utilisateur_id,
                    tid=self.trajet_combo.currentData():
                    self.inviter(pid, tid)
                )

            btn.setStyleSheet("""
                QPushButton {
                    background-color:#C62828;
                    color:white;
                    padding:5px;
                }
                QPushButton:hover {
                    background-color:#B71C1C;
                }
            """)

            self.table.setCellWidget(row, 6, btn)

    # ==================================================
    # ACTIONS
    # ==================================================
    def reserver(self, trajet_id):
        """
        Effectue une réservation.
        """
        resp, status = self.controller.reserver(trajet_id)
        if status == 201:
            QMessageBox.information(
                self, "Succès", "Réservation confirmée"
            )
            self.charger()
        else:
            QMessageBox.warning(
                self, "Erreur", resp.get("error", "Erreur")
            )

    def inviter(self, passager_id, trajet_id):
        """
        Envoie une invitation à un utilisateur.
        """
        resp, status = self.controller.inviter(passager_id, trajet_id)
        if status == 201:
            QMessageBox.information(
                self, "Succès", "Invitation envoyée"
            )
        else:
            QMessageBox.warning(
                self, "Erreur", resp.get("error", "Erreur")
            )
