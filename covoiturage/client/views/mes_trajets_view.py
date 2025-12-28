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
        self.table.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Date', 'Voiture', 'Mode', 'Prix', 'Action'])
        layout.addWidget(self.table)
        
        refresh = QPushButton("Rafraîchir")
        refresh.clicked.connect(self.charger)
        layout.addWidget(refresh)
        
        back = QPushButton("Retour")
        back.clicked.connect(lambda: self.main_window.switch_to('home'))
        layout.addWidget(back)
        
        layout.addStretch()
        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.charger()
    
    def charger(self):
        if not self.main_window.current_user:
            return
        
        try:
            resp, status = APIService.get(f'mes_trajets/{self.main_window.current_user["id"]}')
            
            if status == 200:
                self.table.setRowCount(0)
                for t in resp:
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    
                    self.table.setItem(row, 0, QTableWidgetItem(t.get('depart', '')))
                    self.table.setItem(row, 1, QTableWidgetItem(t.get('arrivee', '')))
                    self.table.setItem(row, 2, QTableWidgetItem(t.get('date_depart', '')))
                    
                    # Voiture (marque + modele)
                    voiture = f"{t.get('marque', 'N/A')} {t.get('modele', '')}"
                    self.table.setItem(row, 3, QTableWidgetItem(voiture.strip()))
                    
                    self.table.setItem(row, 4, QTableWidgetItem(t.get('mode', '')))
                    self.table.setItem(row, 5, QTableWidgetItem(str(t.get('prix_par_place', 0))))
                    
                    btn = QPushButton("Supprimer")
                    btn.clicked.connect(lambda _, t_id=t['id']: self.supprimer(t_id))
                    self.table.setCellWidget(row, 6, btn)
        except Exception as e:
            print(f"Erreur: {e}")
    
    def supprimer(self, trajet_id):
        try:
            APIService.delete(f'trajets/{trajet_id}')
            self.charger()
        except Exception as e:
            print(f"Erreur suppression: {e}")
