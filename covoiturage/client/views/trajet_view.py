from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QMessageBox
from services.api_service import APIService

class TrajetView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Publier un trajet")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        layout.addWidget(QLabel("Départ:"))
        self.depart = QLineEdit()
        layout.addWidget(self.depart)
        
        layout.addWidget(QLabel("Arrivée:"))
        self.arrivee = QLineEdit()
        layout.addWidget(self.arrivee)
        
        layout.addWidget(QLabel("Date (YYYY-MM-DD):"))
        self.date = QLineEdit()
        layout.addWidget(self.date)
        
        layout.addWidget(QLabel("Jour de semaine (lundi, mardi...):"))
        self.jour = QLineEdit()
        layout.addWidget(self.jour)
        
        layout.addWidget(QLabel("Heure (HH:MM):"))
        self.heure = QLineEdit()
        layout.addWidget(self.heure)
        
        layout.addWidget(QLabel("Places:"))
        self.places = QSpinBox()
        self.places.setValue(1)
        self.places.setMinimum(1)
        self.places.setMaximum(10)
        layout.addWidget(self.places)
        
        layout.addWidget(QLabel("Prix par place (€):"))
        self.prix = QLineEdit()
        layout.addWidget(self.prix)
        
        btn = QPushButton("Publier")
        btn.clicked.connect(self.publier)
        layout.addWidget(btn)
        
        back = QPushButton("Retour")
        back.clicked.connect(lambda: self.main_window.switch_to('home'))
        layout.addWidget(back)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
                color: #1e1e1e;
                font-family: "Helvetica Neue", Arial, sans-serif;
                font-size: 14px;
            }
            QLabel#titleLabel {
                color: #b30000;
                font-size: 22px;
                font-weight: 700;
                padding: 4px 0 8px 0;
            }
            QLabel {
                color: #4a4a4a;
            }
            QLineEdit, QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                padding: 8px;
                background: #ffffff;
            }
            QPushButton {
                background-color: #c1121f;
                color: #ffffff;
                border: 1px solid #a00f1b;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #d90429; }
            QPushButton:pressed { background-color: #9b0d16; }
        """)
    
    def publier(self):
        try:
            data = {
                'utilisateur_id': self.main_window.current_user['id'],
                'depart': self.depart.text(),
                'arrivee': self.arrivee.text(),
                'date_depart': self.date.text(),
                'jour_semaine': self.jour.text(),
                'heure_depart': self.heure.text(),
                'places_totales': self.places.value(),
                'prix_par_place': float(self.prix.text())
            }
            resp, status = APIService.post('trajets', data)
            
            if status == 201:
                QMessageBox.information(self, "Succès", "Trajet publié!")
                self.main_window.switch_to('home')
            else:
                QMessageBox.warning(self, "Erreur", resp.get('error', 'Erreur'))
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Prix invalide")
