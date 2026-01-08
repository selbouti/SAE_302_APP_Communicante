from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QGroupBox,
    QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt

from controllers.matching_controller import MatchingController
from views.common_style import COMMON_STYLE


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
        layout.setContentsMargins(20, 16, 20, 16)

        title = QLabel("Trajets compatibles")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        # Sélecteur de trajet
        select_layout = QHBoxLayout()
        label_select = QLabel("Choisir mon trajet :")

        self.trajet_combo = QComboBox()
        self.trajet_combo.currentIndexChanged.connect(self.on_trajet_change)

        select_layout.addWidget(label_select)
        select_layout.addWidget(self.trajet_combo)
        layout.addLayout(select_layout)

        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)

        # Bloc marges
        marges_box = QGroupBox("Recherche avec marges")
        marges_layout = QVBoxLayout(marges_box)
        marges_layout.setSpacing(10)

        form_marges = QFormLayout()
        form_marges.setSpacing(8)

        self.date_value = QLabel("-")
        self.heure_aller_value = QLabel("-")
        self.heure_retour_value = QLabel("-")

        self.marge_aller = QComboBox()
        self.marge_retour = QComboBox()
        self._populate_marges()

        form_marges.addRow("Date :", self.date_value)
        form_marges.addRow("Heure aller :", self.heure_aller_value)
        form_marges.addRow("Marge aller :", self.marge_aller)
        form_marges.addRow("Heure retour :", self.heure_retour_value)
        form_marges.addRow("Marge retour :", self.marge_retour)
        marges_layout.addLayout(form_marges)

        self.btn_marges = QPushButton("Rechercher avec marges")
        self.btn_marges.clicked.connect(self.charger_marges)
        marges_layout.addWidget(self.btn_marges)

        self.info_marges_label = QLabel("")
        self.info_marges_label.setAlignment(Qt.AlignCenter)
        marges_layout.addWidget(self.info_marges_label)
        layout.addWidget(marges_box)

        # Tableau des trajets
        self.table = QTableWidget(0, 7)
        self.standard_headers = [
            "Conducteur",
            "Départ",
            "Arrivée",
            "Voiture",
            "Prix",
            "Places",
            "Action"
        ]
        self.marges_headers = [
            "Conducteur",
            "Aller",
            "Retour",
            "Places",
            "Trajets",
            "Action"
        ]
        self._set_table_headers(self.standard_headers)
        layout.addWidget(self.table)

        # Boutons
        btn_layout = QHBoxLayout()

        refresh = QPushButton("🔄 Rafraîchir")
        refresh.clicked.connect(self.charger)

        back = QPushButton("⬅ Retour")
        back.clicked.connect(lambda: self.main_window.switch_to("home"))

        btn_layout.addWidget(refresh)
        btn_layout.addWidget(back)
        layout.addLayout(btn_layout)
        self.setStyleSheet(COMMON_STYLE)

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
        self.on_trajet_change()

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
                heure = t.get("heure_depart", "")
                heure_txt = f" a {heure}" if heure else ""
                label = (
                    f"{t['depart']} → {t['arrivee']} "
                    f"le {t['date_depart']}{heure_txt} ({t['mode']})"
                )
                self.trajet_combo.addItem(label, t)

        if self.trajet_combo.count() == 0:
            self.info_label.setText("Aucun trajet disponible")
        else:
            self._sync_trajet_fields()

    def on_trajet_change(self):
        self._sync_trajet_fields()
        self.charger()

    def charger(self):
        """
        Charge les trajets compatibles.
        """
        self._set_table_headers(self.standard_headers)
        self.table.setRowCount(0)
        self.info_marges_label.setText("")
        trajet = self._current_trajet()
        trajet_id = trajet.get("id") if trajet else None

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

        heure_depart = mon.get("heure_depart", "")
        heure_retour = mon.get("heure_retour", "")
        heures = ""
        if heure_depart and heure_retour:
            heures = f"{heure_depart} / {heure_retour}"
        elif heure_depart:
            heures = heure_depart

        self.info_label.setText(
            f"{mon['depart']} → {mon['arrivee']} "
            f"({mon['mode']}) {heures}".strip()
        )

        for trajet in trajets:
            row = self.table.rowCount()
            self.table.insertRow(row)

            depart_txt = (
                f"{trajet.heure_depart} / {trajet.depart}"
                if trajet.heure_depart else trajet.depart
            )
            self.table.setItem(row, 0, QTableWidgetItem(trajet.conducteur))
            self.table.setItem(row, 1, QTableWidgetItem(depart_txt))
            self.table.setItem(row, 2, QTableWidgetItem(trajet.arrivee))
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
                    tid=self._current_trajet_id():
                    self.inviter(pid, tid)
                )

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

    def charger_marges(self):
        self._set_table_headers(self.marges_headers)
        self.table.setRowCount(0)
        self.info_marges_label.setText("")
        self.info_label.setText("")

        trajet = self._current_trajet()
        if not trajet:
            self.info_marges_label.setText("Sélectionnez un trajet")
            return

        heure_aller = self._format_time(trajet.get("heure_depart", ""))
        heure_retour = self._format_time(trajet.get("heure_retour", "")) or heure_aller
        data = {
            "depart": trajet.get("depart", ""),
            "arrivee": trajet.get("arrivee", ""),
            "date": trajet.get("date_depart", ""),
            "heure_aller": heure_aller,
            "marge_aller": self.marge_aller.currentData(),
            "heure_retour": heure_retour,
            "marge_retour": self.marge_retour.currentData(),
        }

        resp, status = self.controller.rechercher_conducteurs_marges(data)
        if status != 200:
            self.info_marges_label.setText(
                resp.get("error", "Erreur de chargement")
            )
            return

        conducteurs = resp.get("conducteurs", [])
        conducteur_min = resp.get("conducteur_moins_trajets")
        conducteur_min_id = (
            conducteur_min.get("conducteur_id") if conducteur_min else None
        )

        if conducteur_min:
            self.info_marges_label.setText(
                f"Conducteur recommande : {conducteur_min.get('prenom', '')} "
                f"{conducteur_min.get('nom', '')} "
                f"({conducteur_min.get('nb_trajets', 0)} trajets)"
            )
        else:
            self.info_marges_label.setText("Aucun conducteur compatible")

        for c in conducteurs:
            row = self.table.rowCount()
            self.table.insertRow(row)

            nom = f"{c.get('prenom', '')} {c.get('nom', '')}".strip()
            if c.get("conducteur_id") == conducteur_min_id:
                nom = f"{nom} (recommande)"

            self.table.setItem(row, 0, QTableWidgetItem(nom))
            self.table.setItem(
                row, 1, QTableWidgetItem(c.get("heure_aller", ""))
            )
            self.table.setItem(
                row, 2, QTableWidgetItem(c.get("heure_retour", ""))
            )
            self.table.setItem(
                row, 3, QTableWidgetItem(str(c.get("places_dispo", 0)))
            )
            self.table.setItem(
                row, 4, QTableWidgetItem(str(c.get("nb_trajets", 0)))
            )

            btn = QPushButton("Choisir")
            btn.clicked.connect(
                lambda _, tid=c.get("trajet_id"):
                self.reserver_marge(tid)
            )
            self.table.setCellWidget(row, 5, btn)

    def reserver_marge(self, trajet_id):
        if not trajet_id:
            QMessageBox.warning(self, "Erreur", "Trajet invalide")
            return

        resp, status = self.controller.reserver(trajet_id)
        if status != 201:
            QMessageBox.warning(
                self,
                "Erreur",
                resp.get("error", "Erreur reservation")
            )
            return

        QMessageBox.information(
            self,
            "Succès",
            "Réservation confirmée"
        )
        self.charger_marges()

    def _populate_marges(self):
        self.marge_aller.clear()
        self.marge_retour.clear()
        options = [
            ("15 min", 15),
            ("30 min", 30),
            ("1h", 60),
            ("2h", 120),
            ("3h", 180),
        ]
        for label, minutes in options:
            self.marge_aller.addItem(label, minutes)
            self.marge_retour.addItem(label, minutes)

    def _set_table_headers(self, headers):
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

    def _current_trajet(self):
        trajet = self.trajet_combo.currentData()
        if isinstance(trajet, dict):
            return trajet
        return None

    def _current_trajet_id(self):
        trajet = self._current_trajet()
        return trajet.get("id") if trajet else None

    def _sync_trajet_fields(self):
        trajet = self._current_trajet()
        if not trajet:
            self.date_value.setText("-")
            self.heure_aller_value.setText("-")
            self.heure_retour_value.setText("-")
            return

        date_str = trajet.get("date_depart", "") or "-"
        self.date_value.setText(date_str)

        aller_str = self._format_time(trajet.get("heure_depart", "")) or "-"
        retour_str = self._format_time(trajet.get("heure_retour", "")) or aller_str
        self.heure_aller_value.setText(aller_str)
        self.heure_retour_value.setText(retour_str)

    def _format_time(self, time_str):
        if not time_str:
            return ""
        parts = time_str.split(":")
        if len(parts) >= 2:
            return f"{parts[0].zfill(2)}:{parts[1].zfill(2)}"
        return time_str
