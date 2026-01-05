from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from services.api_service import APIService

class MesTrajetsView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Mes trajets")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Date', 'Heure','Voiture', 'Mode', 'Prix', 'Changer mode', 'Supprimer'])
        layout.addWidget(self.table)
        
        refresh = QPushButton("Rafraîchir")
        refresh.clicked.connect(self.charger)
        layout.addWidget(refresh)
        
        back = QPushButton("Retour")
        back.clicked.connect(lambda: self.main_window.switch_to('home'))
        layout.addWidget(back)
        
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
                color: #b00020;
                font-size: 22px;
                font-weight: 700;
                padding: 4px 0 8px 0;
            }
            QPushButton {
                background-color: #c21807;
                color: #ffffff;
                border: 1px solid #9c1a06;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #d6281a; }
            QPushButton:pressed { background-color: #8c1505; }
            QTableWidget {
                border: 1px solid #e6e6e6;
                border-radius: 6px;
                gridline-color: #e6e6e6;
                selection-background-color: #ffe6e6;
                selection-color: #b30000;
            }
            QHeaderView::section {
                background: #f7f7f7;
                color: #b00020;
                padding: 6px;
                border: 1px solid #e6e6e6;
                font-weight: 600;
            }
        """)

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
                    est_passager = t.get('mode', '') == 'passager'
                    
                    self.table.setItem(row, 0, QTableWidgetItem(t.get('depart', '')))
                    self.table.setItem(row, 1, QTableWidgetItem(t.get('arrivee', '')))
                    self.table.setItem(row, 2, QTableWidgetItem(t.get('date_depart', '')))
                    self.table.setItem(row, 3, QTableWidgetItem(t.get('heure_depart', '')))

                    # Voiture (marque + modele) - masqué si passager
                    voiture = f"{t.get('marque', 'N/A')} {t.get('modele', '')}".strip()
                    self.table.setItem(row, 4, QTableWidgetItem('' if est_passager else voiture))

                    self.table.setItem(row, 5, QTableWidgetItem(t.get('mode', '')))
                    prix = t.get('prix_par_place', '')
                    prix_affiche = '' if est_passager else str(prix if prix is not None else '')
                    self.table.setItem(row, 6, QTableWidgetItem(prix_affiche))

                    toggle_btn = QPushButton("Basculer")
                    toggle_btn.clicked.connect(lambda _, t_id=t['id'], mode=t.get('mode', ''): self.basculer_mode(t_id, mode))
                    self.table.setCellWidget(row, 7, toggle_btn)

                    delete_btn = QPushButton("Supprimer")
                    delete_btn.clicked.connect(lambda _, t_id=t['id']: self.supprimer(t_id))
                    self.table.setCellWidget(row, 8, delete_btn)
        except Exception as e:
            print(f"Erreur: {e}")
    
    def supprimer(self, trajet_id):
        try:
            APIService.delete(f'trajets/{trajet_id}')
            self.charger()
        except Exception as e:
            print(f"Erreur suppression: {e}")

    def basculer_mode(self, trajet_id, mode_actuel):
        nouveau_mode = 'passager' if mode_actuel == 'conducteur' else 'conducteur'
        resp, status = APIService.put(f'trajets/{trajet_id}/mode', {'mode': nouveau_mode})
        if status == 200:
            self.charger()
        else:
            print(f"Erreur changement mode: {resp}")
