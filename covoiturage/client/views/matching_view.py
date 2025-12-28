from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QFrame
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from services.api_service import APIService
from controllers.reservation_controller import ReservationController
from controllers.invitation_controller import InvitationController

class MatchingView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.matching_data = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Les trajets disponibles")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        # Card container pour reproduire le cadre de la maquette
        card = QFrame()
        card.setObjectName("tableCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)

        # Sélecteur de trajet personnel
        select_layout = QHBoxLayout()
        select_layout.addWidget(QLabel("Choisir mon trajet:"))
        self.trajet_combo = QComboBox()
        self.trajet_combo.currentIndexChanged.connect(self.charger)
        select_layout.addWidget(self.trajet_combo)
        select_layout.addStretch()
        card_layout.addLayout(select_layout)
        
        self.info_label = QLabel("")
        self.info_label.setObjectName("infoLabel")
        card_layout.addWidget(self.info_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['Nom du conducteur', 'Heure / Lieu de départ', "Heure / Lieu d'arrivée", 'Voiture', 'Prix', 'Places', 'Action'])
        card_layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        refresh = QPushButton("Rafraîchir")
        refresh.clicked.connect(self.charger)
        btn_layout.addWidget(refresh)
        
        btn_layout.addStretch()
        back = QPushButton("Retour")
        back.clicked.connect(lambda: self.main_window.switch_to('home'))
        btn_layout.addWidget(back)
        card_layout.addLayout(btn_layout)

        layout.addWidget(card)
        layout.addStretch()
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
                color: #1e1e1e;
                font-family: "Open Sans", "Segoe UI", Arial, sans-serif;
                font-size: 14px;
            }
            QLabel#titleLabel {
                color: #7b0000;
                font-size: 24px;
                font-weight: 800;
                padding: 8px 0 16px 8px;
                text-decoration: underline;
            }
            QLabel#infoLabel {
                color: #3b3b3b;
                padding: 4px 2px 8px 2px;
            }
            QFrame#tableCard {
                background: #fdfdfd;
                border: 2px solid #4a4a4a;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #a30000;
                color: #ffffff;
                border: 1px solid #7b0000;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: 600;
                min-width: 110px;
            }
            QPushButton:hover { background-color: #b30000; }
            QPushButton:pressed { background-color: #7b0000; }
            QTableWidget {
                border: 2px solid #7b0000;
                gridline-color: #7b0000;
                selection-background-color: #ffe6e6;
                selection-color: #7b0000;
            }
            QHeaderView::section {
                background: #7b0000;
                color: #ffffff;
                padding: 10px;
                border: 1px solid #7b0000;
                font-weight: 700;
                font-size: 13px;
            }
            QTableWidget::item {
                padding-left: 6px;
                padding-right: 6px;
            }
        """)

    def showEvent(self, event):
        super().showEvent(event)
        self.charger_trajets_perso()
        self.charger()
    
    def charger(self):
        # Vérifier que l'utilisateur est connecté
        if not self.main_window.current_user:
            self.info_label.setText("Veuillez vous connecter d'abord")
            self.table.setRowCount(0)
            return

        trajet_id = self.trajet_combo.currentData()
        if trajet_id is None:
            self.info_label.setText("Ajoutez un trajet ou sélectionnez-en un pour rechercher des correspondances.")
            self.table.setRowCount(0)
            return

        resp, status = APIService.get(f'matching/{self.main_window.current_user["id"]}?trajet_id={trajet_id}')
        
        if status == 200:
            self.matching_data = resp
            mon_trajet = resp['mon_trajet']
            mode_recherche = resp['mode_recherche']
            trajets = resp['trajets_compatibles']
            
            self.info_label.setText(f"Votre trajet: {mon_trajet['depart']} → {mon_trajet['arrivee']} ({mon_trajet['mode']}) | Mode: {mode_recherche}")
            
            self.table.setRowCount(0)
            
            if len(trajets) == 0:
                self.info_label.setText(f"Votre trajet: {mon_trajet['depart']} → {mon_trajet['arrivee']} ({mon_trajet['mode']}) | Aucun trajet compatible trouvé")
                self.table.setRowCount(0)
                return
            
            for t in trajets:
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                self.table.setItem(row, 0, QTableWidgetItem(f"{t['prenom']} {t['nom']}"))
                self.table.setItem(row, 1, QTableWidgetItem(f"{t.get('heure_depart', '')} / {t['depart']}".strip()))
                self.table.setItem(row, 2, QTableWidgetItem(f"{t.get('heure_arrivee', '')} / {t['arrivee']}".strip()))
                voiture = f"{t.get('marque','')} {t.get('modele','')}".strip()
                self.table.setItem(row, 3, QTableWidgetItem(voiture))
                self.table.setItem(row, 4, QTableWidgetItem(f"{t['prix_par_place']}€")) 
                
                places_item = QTableWidgetItem(str(t['places_disponibles']))
                if t['places_disponibles'] <= 0:
                    places_item.setForeground(Qt.gray)
                self.table.setItem(row, 5, places_item)
                
                if mode_recherche == 'réservations':
                    btn = QPushButton("Réserver")
                    if t['places_disponibles'] <= 0:
                        btn.setEnabled(False)
                        btn.setStyleSheet("QPushButton { background: #d9d9d9; color: #7a7a7a; border: 1px solid #b3b3b3; }")
                    else:
                        btn.clicked.connect(lambda _, t_id=t['id']: self.reserver(t_id))
                else:
                    btn = QPushButton("Inviter")
                    btn.clicked.connect(lambda _, p_id=t['utilisateur_id']: self.inviter(p_id, t['id']))
                
                self.table.setCellWidget(row, 6, btn)
        else:
            self.table.setRowCount(0)
            if status == 404:
                self.info_label.setText("Aucun trajet trouvé pour votre profil. Ajoutez un trajet avant de rechercher des correspondances.")
            else:
                self.info_label.setText(f"Erreur: {resp.get('error', 'Impossible de charger les trajets')}")

    def charger_trajets_perso(self):
        if not self.main_window.current_user:
            self.trajet_combo.clear()
            return

        resp, status = APIService.get(f'mes_trajets/{self.main_window.current_user["id"]}')
        if status == 200:
            self.trajet_combo.blockSignals(True)
            self.trajet_combo.clear()
            for t in resp:
                label = f"{t.get('depart', '')} → {t.get('arrivee', '')} le {t.get('date_depart', '')} ({t.get('mode', '')})"
                self.trajet_combo.addItem(label, t.get('id'))
            self.trajet_combo.blockSignals(False)
        else:
            self.trajet_combo.clear()
    
    def reserver(self, trajet_id):
        resp, status = ReservationController.creer_reservation(trajet_id, self.main_window.current_user['id'], 1)
        if status == 201:
            self._show_reservation_feedback()
            self.charger()
        else:
            QMessageBox.warning(self, "Erreur", resp.get('error', 'Erreur'))
    
    def inviter(self, passager_id, trajet_id):
        resp, status = InvitationController.creer_invitation(trajet_id, passager_id)
        if status == 201:
            QMessageBox.information(self, "Succès", "Invitation envoyée!")
            self.charger()
        else:
            QMessageBox.warning(self, "Erreur", resp.get('error', 'Erreur'))

    def _show_reservation_feedback(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Réservation confirmée")
        msg.setText("Merci pour votre réservation")
        retour_btn = msg.addButton("Retour à l'accueil", QMessageBox.AcceptRole)
        msg.setStandardButtons(QMessageBox.NoButton)
        msg.setStyleSheet("""
            QMessageBox {
                background: #ffffff;
                font-family: "Open Sans", "Segoe UI", Arial, sans-serif;
                border: 2px solid #4a4a4a;
                border-radius: 8px;
            }
            QLabel {
                color: #7b0000;
                font-size: 16px;
                font-weight: 700;
            }
            QPushButton {
                background-color: #ffffff;
                color: #1e1e1e;
                border: 1px solid #9c9c9c;
                border-radius: 6px;
                padding: 8px 12px;
                min-width: 160px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #f2f2f2; }
        """)
        msg.exec_()
        if msg.clickedButton() == retour_btn:
            self.main_window.switch_to('home')
