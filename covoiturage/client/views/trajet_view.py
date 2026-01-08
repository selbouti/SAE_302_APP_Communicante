from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QMessageBox
from services.api_service import APIService
from views.common_style import COMMON_STYLE

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
        
        layout.addWidget(QLabel("Heure départ (HH:MM):"))
        self.heure = QLineEdit()
        layout.addWidget(self.heure)

        layout.addWidget(QLabel("Heure retour (HH:MM):"))
        self.heure_retour = QLineEdit()
        layout.addWidget(self.heure_retour)
        
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
        self.setStyleSheet(COMMON_STYLE)
    
    def publier(self):
        try:
            data = {
                'utilisateur_id': self.main_window.current_user['id'],
                'depart': self.depart.text(),
                'arrivee': self.arrivee.text(),
                'date_depart': self.date.text(),
                'jour_semaine': self.jour.text(),
                'heure_depart': self.heure.text(),
                'heure_retour': self.heure_retour.text(),
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
