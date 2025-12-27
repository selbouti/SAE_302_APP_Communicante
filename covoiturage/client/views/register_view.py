from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog
from controllers.user_controller import UserController
import os

class RegisterView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.ical_file = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Email:"))
        self.email = QLineEdit()
        layout.addWidget(self.email)
        
        layout.addWidget(QLabel("Mot de passe:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)
        
        layout.addWidget(QLabel("Nom:"))
        self.nom = QLineEdit()
        layout.addWidget(self.nom)
        
        layout.addWidget(QLabel("Prénom:"))
        self.prenom = QLineEdit()
        layout.addWidget(self.prenom)
        
        layout.addWidget(QLabel("Téléphone:"))
        self.phone = QLineEdit()
        layout.addWidget(self.phone)
        
        layout.addWidget(QLabel("Fichier iCalendar (optionnel):"))
        self.file_label = QLabel("Aucun fichier sélectionné")
        layout.addWidget(self.file_label)
        
        browse_btn = QPushButton("Parcourir...")
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn)
        
        register_btn = QPushButton("S'inscrire")
        register_btn.clicked.connect(self.register)
        layout.addWidget(register_btn)
        
        back_btn = QPushButton("Retour")
        back_btn.clicked.connect(lambda: self.main_window.switch_to('login'))
        layout.addWidget(back_btn)
        
        self.setLayout(layout)
    
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner fichier iCalendar", "", "ICS Files (*.ics)")
        if file_path:
            self.ical_file = file_path
            self.file_label.setText(os.path.basename(file_path))
    
    def register(self):
        resp, status = UserController.register(self.email.text(), self.password.text(), 
                                               self.nom.text(), self.prenom.text(), self.phone.text())
        
        if status == 201:
            user_id = resp['id']
            
            # Uploader fichier iCalendar si fourni
            if self.ical_file:
                resp2, status2 = UserController.upload_icalendar(user_id, self.ical_file)
                if status2 == 201:
                    QMessageBox.information(self, "Succès", "Inscription et trajets importés!")
                else:
                    QMessageBox.warning(self, "Avertissement", "Inscription OK mais erreur import iCalendar")
            else:
                QMessageBox.information(self, "Succès", "Inscription réussie!")
            
            self.main_window.switch_to('login')
        else:
            QMessageBox.warning(self, "Erreur", resp.get('error', 'Erreur'))