from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from controllers.reservation_controller import ReservationController
from services.api_service import APIService

class RechercherView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Chercher un trajet"))
        
        layout.addWidget(QLabel("Départ:"))
        self.depart = QLineEdit()
        layout.addWidget(self.depart)
        
        layout.addWidget(QLabel("Arrivée:"))
        self.arrivee = QLineEdit()
        layout.addWidget(self.arrivee)
        
        layout.addWidget(QLabel("Date (YYYY-MM-DD):"))
        self.date = QLineEdit()
        layout.addWidget(self.date)
        
        search = QPushButton("Rechercher")
        search.clicked.connect(self.rechercher)
        layout.addWidget(search)
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Date', 'Heure', 'Places', 'Prix', 'Conducteur', 'Action'])
        layout.addWidget(self.table)
        
        back = QPushButton("Retour")
        back.clicked.connect(lambda: self.main_window.switch_to('home'))
        layout.addWidget(back)
        
        self.setLayout(layout)
    
    def rechercher(self):
        data = {'depart': self.depart.text(), 'arrivee': self.arrivee.text(), 'date_depart': self.date.text()}
        resp, status = APIService.post('trajets/rechercher', data)
        
        if status == 200:
            self.table.setRowCount(0)
            for t in resp:
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                self.table.setItem(row, 0, QTableWidgetItem(t['depart']))
                self.table.setItem(row, 1, QTableWidgetItem(t['arrivee']))
                self.table.setItem(row, 2, QTableWidgetItem(t['date_depart']))
                self.table.setItem(row, 3, QTableWidgetItem(t.get('heure_depart', '')))
                self.table.setItem(row, 4, QTableWidgetItem(str(t['places_disponibles'])))
                self.table.setItem(row, 5, QTableWidgetItem(str(t['prix_par_place'])))
                self.table.setItem(row, 6, QTableWidgetItem(f"{t['prenom']} {t['nom']}"))
                
                btn = QPushButton("Réserver")
                btn.clicked.connect(lambda _, t_id=t['id']: self.reserver(t_id))
                self.table.setCellWidget(row, 7, btn)
    
    def reserver(self, trajet_id):
        resp, status = ReservationController.creer_reservation(trajet_id, self.main_window.current_user['id'], 1)
        
        if status == 201:
            QMessageBox.information(self, "Succès", "Réservation créée!")
            self.rechercher()
        else:
            QMessageBox.warning(self, "Erreur", resp.get('error', 'Erreur'))
