from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
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
        title = QLabel("Trajets compatibles")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        self.info_label = QLabel("")
        layout.addWidget(self.info_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Date', 'Heure', 'Places', 'Prix', 'Personne', 'Action'])
        layout.addWidget(self.table)
        
        refresh = QPushButton("Rafraîchir")
        refresh.clicked.connect(self.charger)
        layout.addWidget(refresh)
        
        back = QPushButton("Retour")
        back.clicked.connect(lambda: self.main_window.switch_to('home'))
        layout.addWidget(back)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def charger(self):
        # Vérifier que l'utilisateur est connecté
        if not self.main_window.current_user:
            self.info_label.setText("Veuillez vous connecter d'abord")
            return
        
        resp, status = APIService.get(f'matching/{self.main_window.current_user["id"]}')
        
        if status == 200:
            self.matching_data = resp
            mon_trajet = resp['mon_trajet']
            mode_recherche = resp['mode_recherche']
            trajets = resp['trajets_compatibles']
            
            self.info_label.setText(f"Votre trajet: {mon_trajet['depart']} → {mon_trajet['arrivee']} ({mon_trajet['mode']}) | Mode: {mode_recherche}")
            
            self.table.setRowCount(0)
            
            if len(trajets) == 0:
                self.info_label.setText(f"Votre trajet: {mon_trajet['depart']} → {mon_trajet['arrivee']} ({mon_trajet['mode']}) | Aucun trajet compatible trouvé")
                return
            
            for t in trajets:
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                self.table.setItem(row, 0, QTableWidgetItem(t['depart']))
                self.table.setItem(row, 1, QTableWidgetItem(t['arrivee']))
                self.table.setItem(row, 2, QTableWidgetItem(t['date_depart']))
                self.table.setItem(row, 3, QTableWidgetItem(t.get('heure_depart', '')))
                self.table.setItem(row, 4, QTableWidgetItem(str(t['places_disponibles'])))
                self.table.setItem(row, 5, QTableWidgetItem(str(t['prix_par_place'])))
                self.table.setItem(row, 6, QTableWidgetItem(f"{t['prenom']} {t['nom']}"))
                
                if mode_recherche == 'réservations':
                    btn = QPushButton("Réserver")
                    btn.clicked.connect(lambda _, t_id=t['id']: self.reserver(t_id))
                else:
                    btn = QPushButton("Inviter")
                    btn.clicked.connect(lambda _, p_id=t['utilisateur_id']: self.inviter(p_id, t['id']))
                
                self.table.setCellWidget(row, 7, btn)
        else:
            self.info_label.setText(f"Erreur: {resp.get('error', 'Impossible de charger les trajets')}")
    
    def reserver(self, trajet_id):
        resp, status = ReservationController.creer_reservation(trajet_id, self.main_window.current_user['id'], 1)
        if status == 201:
            QMessageBox.information(self, "Succès", "Réservation créée!")
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
