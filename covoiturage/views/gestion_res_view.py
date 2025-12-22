# views/reservation_view.py
"""
Interface PyQt pour la gestion des réservations
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QMessageBox,
                             QDialog, QFormLayout, QSpinBox, QHeaderView)
from PyQt5.QtCore import Qt, pyqtSignal
import requests
from datetime import datetime

class ReservationView(QWidget):
    """Widget principal pour afficher et gérer les réservations"""
    
    # Signaux pour la communication
    reservation_creee = pyqtSignal(dict)
    reservation_annulee = pyqtSignal(int)
    
    def __init__(self, api_url="http://localhost:5000", id_utilisateur=None):
        """
        Initialise la vue des réservations
        
        Args:
            api_url: URL de base de l'API Flask
            id_utilisateur: ID de l'utilisateur connecté
        """
        super().__init__()
        self.api_url = api_url
        self.id_utilisateur = id_utilisateur
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        layout = QVBoxLayout()
        
        # Titre
        title = QLabel("Mes Réservations")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Boutons d'action
        button_layout = QHBoxLayout()
        
        self.btn_actualiser = QPushButton("🔄 Actualiser")
        self.btn_actualiser.clicked.connect(self.charger_reservations)
        button_layout.addWidget(self.btn_actualiser)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Tableau des réservations
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Trajet", "Places", "Statut", "Date", "Actions", ""
        ])
        
        # Ajuster la largeur des colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.table)
        
        # Message d'information
        self.label_info = QLabel("")
        self.label_info.setStyleSheet("color: #666; margin: 10px;")
        layout.addWidget(self.label_info)
        
        self.setLayout(layout)
        
        # Charger les réservations au démarrage
        if self.id_utilisateur:
            self.charger_reservations()
    
    def charger_reservations(self):
        """Charge les réservations de l'utilisateur depuis l'API"""
        if not self.id_utilisateur:
            self.afficher_erreur("Utilisateur non connecté")
            return
        
        try:
            url = f"{self.api_url}/api/passagers/{self.id_utilisateur}/reservations"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    self.afficher_reservations(data['data'])
                    self.label_info.setText(f"✓ {data['count']} réservation(s) trouvée(s)")
                else:
                    self.afficher_erreur(data.get('message', 'Erreur inconnue'))
            else:
                self.afficher_erreur(f"Erreur HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.afficher_erreur("Impossible de se connecter au serveur")
        except requests.exceptions.Timeout:
            self.afficher_erreur("Délai d'attente dépassé")
        except Exception as e:
            self.afficher_erreur(f"Erreur: {str(e)}")
    
    def afficher_reservations(self, reservations):
        """
        Affiche les réservations dans le tableau
        
        Args:
            reservations: Liste des réservations à afficher
        """
        self.table.setRowCount(0)  # Vider le tableau
        
        for reservation in reservations:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(reservation['id_reservation'])))
            
            # Trajet (afficher l'ID pour l'instant, à améliorer avec les détails)
            self.table.setItem(row, 1, QTableWidgetItem(f"Trajet #{reservation['id_trajet']}"))
            
            # Places
            self.table.setItem(row, 2, QTableWidgetItem(str(reservation['nb_places'])))
            
            # Statut avec couleur
            statut_item = QTableWidgetItem(reservation['statut'])
            if reservation['statut'] == 'confirmee':
                statut_item.setBackground(Qt.green)
            elif reservation['statut'] == 'en_attente':
                statut_item.setBackground(Qt.yellow)
            elif reservation['statut'] == 'annulee':
                statut_item.setBackground(Qt.red)
            self.table.setItem(row, 3, statut_item)
            
            # Date
            date_str = reservation.get('date_reservation', '')
            if date_str:
                try:
                    date_obj = datetime.fromisoformat(date_str)
                    date_formatted = date_obj.strftime("%d/%m/%Y %H:%M")
                except:
                    date_formatted = date_str
            else:
                date_formatted = "N/A"
            self.table.setItem(row, 4, QTableWidgetItem(date_formatted))
            
            # Bouton Annuler (seulement si pas déjà annulée)
            if reservation['statut'] != 'annulee':
                btn_annuler = QPushButton("❌ Annuler")
                btn_annuler.setStyleSheet("background-color: #ff4444; color: white;")
                btn_annuler.clicked.connect(
                    lambda checked, r_id=reservation['id_reservation']: self.annuler_reservation(r_id)
                )
                self.table.setCellWidget(row, 5, btn_annuler)
            
            # Bouton Détails
            btn_details = QPushButton("ℹ️ Détails")
            btn_details.clicked.connect(
                lambda checked, r_id=reservation['id_reservation']: self.afficher_details(r_id)
            )
            self.table.setCellWidget(row, 6, btn_details)
    
    def annuler_reservation(self, id_reservation):
        """
        Annule une réservation
        
        Args:
            id_reservation: ID de la réservation à annuler
        """
        # Demander confirmation
        reply = QMessageBox.question(
            self, 
            'Confirmation', 
            'Êtes-vous sûr de vouloir annuler cette réservation ?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        try:
            url = f"{self.api_url}/api/reservations/{id_reservation}/annuler"
            response = requests.put(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    QMessageBox.information(self, "Succès", data['message'])
                    self.reservation_annulee.emit(id_reservation)
                    self.charger_reservations()  # Recharger la liste
                else:
                    self.afficher_erreur(data.get('message', 'Erreur inconnue'))
            else:
                self.afficher_erreur(f"Erreur HTTP {response.status_code}")
                
        except Exception as e:
            self.afficher_erreur(f"Erreur: {str(e)}")
    
    def afficher_details(self, id_reservation):
        """
        Affiche les détails d'une réservation
        
        Args:
            id_reservation: ID de la réservation
        """
        try:
            url = f"{self.api_url}/api/reservations/{id_reservation}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    reservation = data['data']
                    
                    # Créer une boîte de dialogue pour afficher les détails
                    dialog = QDialog(self)
                    dialog.setWindowTitle(f"Réservation #{id_reservation}")
                    layout = QFormLayout()
                    
                    layout.addRow("ID:", QLabel(str(reservation['id_reservation'])))
                    layout.addRow("Trajet:", QLabel(f"#{reservation['id_trajet']}"))
                    layout.addRow("Passager:", QLabel(f"#{reservation['id_passager']}"))
                    layout.addRow("Places:", QLabel(str(reservation['nb_places'])))
                    layout.addRow("Statut:", QLabel(reservation['statut']))
                    
                    date_str = reservation.get('date_reservation', 'N/A')
                    layout.addRow("Date:", QLabel(date_str))
                    
                    btn_fermer = QPushButton("Fermer")
                    btn_fermer.clicked.connect(dialog.accept)
                    layout.addRow(btn_fermer)
                    
                    dialog.setLayout(layout)
                    dialog.exec_()
                else:
                    self.afficher_erreur(data.get('message', 'Erreur inconnue'))
            else:
                self.afficher_erreur(f"Erreur HTTP {response.status_code}")
                
        except Exception as e:
            self.afficher_erreur(f"Erreur: {str(e)}")
    
    def afficher_erreur(self, message):
        """
        Affiche un message d'erreur
        
        Args:
            message: Message à afficher
        """
        QMessageBox.critical(self, "Erreur", message)
        self.label_info.setText(f"❌ {message}")


class DialogReservation(QDialog):
    """Dialog pour créer une nouvelle réservation"""
    
    def __init__(self, api_url, id_trajet, id_passager, parent=None):
        """
        Initialise le dialog de réservation
        
        Args:
            api_url: URL de l'API
            id_trajet: ID du trajet à réserver
            id_passager: ID du passager
            parent: Widget parent
        """
        super().__init__(parent)
        self.api_url = api_url
        self.id_trajet = id_trajet
        self.id_passager = id_passager
        self.init_ui()
    
    def init_ui(self):
        """Initialise l'interface du dialog"""
        self.setWindowTitle("Réserver une place")
        self.setModal(True)
        
        layout = QFormLayout()
        
        # Nombre de places
        self.spin_places = QSpinBox()
        self.spin_places.setMinimum(1)
        self.spin_places.setMaximum(4)
        self.spin_places.setValue(1)
        layout.addRow("Nombre de places:", self.spin_places)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        btn_reserver = QPushButton("✓ Réserver")
        btn_reserver.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        btn_reserver.clicked.connect(self.creer_reservation)
        button_layout.addWidget(btn_reserver)
        
        btn_annuler = QPushButton("✗ Annuler")
        btn_annuler.clicked.connect(self.reject)
        button_layout.addWidget(btn_annuler)
        
        layout.addRow(button_layout)
        
        self.setLayout(layout)
    
    def creer_reservation(self):
        """Crée la réservation via l'API"""
        try:
            url = f"{self.api_url}/api/reservations"
            data = {
                "id_trajet": self.id_trajet,
                "id_passager": self.id_passager,
                "nb_places": self.spin_places.value()
            }
            
            response = requests.post(url, json=data, timeout=5)
            
            if response.status_code == 201:
                result = response.json()
                if result['success']:
                    QMessageBox.information(self, "Succès", result['message'])
                    self.accept()
                else:
                    QMessageBox.warning(self, "Erreur", result.get('message', 'Erreur inconnue'))
            else:
                QMessageBox.critical(self, "Erreur", f"Erreur HTTP {response.status_code}")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {str(e)}")


# Exemple d'utilisation
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Créer la vue avec un ID utilisateur de test
    view = ReservationView(api_url="http://localhost:5000", id_utilisateur=2)
    view.setWindowTitle("Mes Réservations")
    view.resize(900, 600)
    view.show()
    
    sys.exit(app.exec_())