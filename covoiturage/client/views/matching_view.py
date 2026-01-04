from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt

from controllers.matching_controller import MatchingController


class MatchingView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.controller = None
        self.setup_ui()

    # ---------------- UI ---------------- #

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Les trajets disponibles")
        layout.addWidget(title)

        select_layout = QHBoxLayout()
        select_layout.addWidget(QLabel("Choisir mon trajet :"))
        self.trajet_combo = QComboBox()
        self.trajet_combo.currentIndexChanged.connect(self.charger)
        select_layout.addWidget(self.trajet_combo)
        layout.addLayout(select_layout)

        self.info_label = QLabel("")
        layout.addWidget(self.info_label)

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
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        refresh = QPushButton("Rafraîchir")
        refresh.clicked.connect(self.charger)
        btn_layout.addWidget(refresh)

        back = QPushButton("Retour")
        back.clicked.connect(lambda: self.main_window.switch_to("home"))
        btn_layout.addWidget(back)

        layout.addLayout(btn_layout)

    # ---------------- LIFE CYCLE ---------------- #

    def showEvent(self, event):
        super().showEvent(event)

        if not self.main_window.current_user:
            self.info_label.setText("Veuillez vous connecter")
            return

        self.controller = MatchingController(
            self.main_window.current_user
        )

        self.charger_trajets_perso()
        self.charger()

    # ---------------- DATA ---------------- #

    def charger_trajets_perso(self):
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

    # ---------------- DISPLAY ---------------- #

    def afficher_trajets(self, data):
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
                    lambda _, pid=trajet.utilisateur_id, tid=self.trajet_combo.currentData():
                    self.inviter(pid, tid)
                )

            self.table.setCellWidget(row, 6, btn)

    # ---------------- ACTIONS ---------------- #

    def reserver(self, trajet_id):
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
        resp, status = self.controller.inviter(passager_id, trajet_id)
        if status == 201:
            QMessageBox.information(
                self, "Succès", "Invitation envoyée"
            )
        else:
            QMessageBox.warning(
                self, "Erreur", resp.get("error", "Erreur")
            )
