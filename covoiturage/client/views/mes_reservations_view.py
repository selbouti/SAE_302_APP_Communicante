from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from services.api_service import APIService

class MesReservationsView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Mes réservations et invitations"))
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Date', 'Places', 'Prix', 'Type', 'Statut', 'Action'])
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
        if not self.main_window.current_user:
            return
        
        user_id = self.main_window.current_user['id']
        resp, status = APIService.get(f'reservations/passager/{user_id}')
        
        if status == 200:
            self.table.setRowCount(0)
            for r in resp:
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                self.table.setItem(row, 0, QTableWidgetItem(r['depart']))
                self.table.setItem(row, 1, QTableWidgetItem(r['arrivee']))
                self.table.setItem(row, 2, QTableWidgetItem(r['date_depart']))
                self.table.setItem(row, 3, QTableWidgetItem(str(r['places_reservees'])))
                self.table.setItem(row, 4, QTableWidgetItem(str(r['prix_par_place'])))
                self.table.setItem(row, 5, QTableWidgetItem("Réservation"))
                self.table.setItem(row, 6, QTableWidgetItem(r['statut']))
                
                btn = QPushButton("Annuler")
                btn.clicked.connect(lambda _, r_id=r['id']: self.annuler(r_id))
                self.table.setCellWidget(row, 7, btn)
    
    def annuler(self, reservation_id):
        APIService.delete(f'reservations/{reservation_id}/annuler')
        self.charger()