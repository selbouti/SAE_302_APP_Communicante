from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from services.api_service import APIService

class MesTrajetsView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Mes trajets"))
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Date', 'Mode', 'Places', 'Prix', 'Action'])
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
        
        resp, status = APIService.get(f'mes_trajets/{self.main_window.current_user["id"]}')
        
        if status == 200:
            self.table.setRowCount(0)
            for t in resp:
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                self.table.setItem(row, 0, QTableWidgetItem(t['depart']))
                self.table.setItem(row, 1, QTableWidgetItem(t['arrivee']))
                self.table.setItem(row, 2, QTableWidgetItem(t['date_depart']))
                self.table.setItem(row, 3, QTableWidgetItem(t['mode']))
                self.table.setItem(row, 4, QTableWidgetItem(str(t['places_disponibles'])))
                self.table.setItem(row, 5, QTableWidgetItem(str(t['prix_par_place'])))
                
                btn = QPushButton("Supprimer")
                btn.clicked.connect(lambda _, t_id=t['id']: self.supprimer(t_id))
                self.table.setCellWidget(row, 6, btn)
    
    def supprimer(self, trajet_id):
        APIService.delete(f'trajets/{trajet_id}')
        self.charger()
