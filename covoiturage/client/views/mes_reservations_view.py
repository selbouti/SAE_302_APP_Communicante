# ============= views/reservations_invitations_view.py =============
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QTabWidget, QMessageBox, QLabel
from controllers.reservation_controller import ReservationController
from controllers.invitation_controller import InvitationController

class ReservationsInvitationsView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Onglets principaux
        self.tabs = QTabWidget()
        
        # Onglet 1: Réservations
        self.tab_reservations = QWidget()
        self.setup_tab_reservations()
        self.tabs.addTab(self.tab_reservations, "Réservations")
        
        # Onglet 2: Invitations
        self.tab_invitations = QWidget()
        self.setup_tab_invitations()
        self.tabs.addTab(self.tab_invitations, "Invitations")
        
        layout.addWidget(self.tabs)
        
        # Bouton retour
        back = QPushButton("Retour")
        back.clicked.connect(lambda: self.main_window.switch_to('home'))
        layout.addWidget(back)
        
        self.setLayout(layout)
    
    def setup_tab_reservations(self):
        """Configure l'onglet des réservations"""
        layout = QVBoxLayout()
        
        # Sous-onglets
        sub_tabs = QTabWidget()
        
        # Réservations reçues
        widget_recues = QWidget()
        layout_recues = QVBoxLayout()
        layout_recues.addWidget(QLabel("Réservations reçues sur mes trajets"))
        
        self.table_res_recues = QTableWidget()
        self.table_res_recues.setColumnCount(8)
        self.table_res_recues.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Passager', 'Places', 'Statut', 'Date', 'Accepter', 'Refuser'])
        layout_recues.addWidget(self.table_res_recues)
        
        btn_refresh_recues = QPushButton("Rafraîchir")
        btn_refresh_recues.clicked.connect(self.charger_reservations_recues)
        layout_recues.addWidget(btn_refresh_recues)
        
        widget_recues.setLayout(layout_recues)
        sub_tabs.addTab(widget_recues, "Reçues")
        
        # Réservations faites
        widget_faites = QWidget()
        layout_faites = QVBoxLayout()
        layout_faites.addWidget(QLabel("Mes réservations"))
        
        self.table_res_faites = QTableWidget()
        self.table_res_faites.setColumnCount(7)
        self.table_res_faites.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Conducteur', 'Places', 'Statut', 'Date', 'Annuler'])
        layout_faites.addWidget(self.table_res_faites)
        
        btn_refresh_faites = QPushButton("Rafraîchir")
        btn_refresh_faites.clicked.connect(self.charger_reservations_faites)
        layout_faites.addWidget(btn_refresh_faites)
        
        widget_faites.setLayout(layout_faites)
        sub_tabs.addTab(widget_faites, "Faites")
        
        layout.addWidget(sub_tabs)
        self.tab_reservations.setLayout(layout)
    
    def setup_tab_invitations(self):
        """Configure l'onglet des invitations"""
        layout = QVBoxLayout()
        
        # Sous-onglets
        sub_tabs = QTabWidget()
        
        # Invitations reçues
        widget_recues = QWidget()
        layout_recues = QVBoxLayout()
        layout_recues.addWidget(QLabel("Invitations reçues"))
        
        self.table_inv_recues = QTableWidget()
        self.table_inv_recues.setColumnCount(7)
        self.table_inv_recues.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Conducteur', 'Statut', 'Date', 'Accepter', 'Refuser'])
        layout_recues.addWidget(self.table_inv_recues)
        
        btn_refresh_recues = QPushButton("Rafraîchir")
        btn_refresh_recues.clicked.connect(self.charger_invitations_recues)
        layout_recues.addWidget(btn_refresh_recues)
        
        widget_recues.setLayout(layout_recues)
        sub_tabs.addTab(widget_recues, "Reçues")
        
        # Invitations envoyées
        widget_envoyees = QWidget()
        layout_envoyees = QVBoxLayout()
        layout_envoyees.addWidget(QLabel("Invitations envoyées"))
        
        self.table_inv_envoyees = QTableWidget()
        self.table_inv_envoyees.setColumnCount(6)
        self.table_inv_envoyees.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Passager', 'Statut', 'Date', 'Supprimer'])
        layout_envoyees.addWidget(self.table_inv_envoyees)
        
        btn_refresh_envoyees = QPushButton("Rafraîchir")
        btn_refresh_envoyees.clicked.connect(self.charger_invitations_envoyees)
        layout_envoyees.addWidget(btn_refresh_envoyees)
        
        widget_envoyees.setLayout(layout_envoyees)
        sub_tabs.addTab(widget_envoyees, "Envoyées")
        
        layout.addWidget(sub_tabs)
        self.tab_invitations.setLayout(layout)
    
    # ===== CHARGEMENT RESERVATIONS =====
    def charger_reservations_recues(self):
        """Charge les réservations reçues"""
        reservations, erreur = ReservationController.get_reservations_recues(self.main_window.current_user['id'])
        
        if erreur:
            QMessageBox.warning(self, "Erreur", erreur)
            return
        
        self.table_res_recues.setRowCount(0)
        for res in reservations:
            row = self.table_res_recues.rowCount()
            self.table_res_recues.insertRow(row)
            
            self.table_res_recues.setItem(row, 0, QTableWidgetItem(res.depart))
            self.table_res_recues.setItem(row, 1, QTableWidgetItem(res.arrivee))
            self.table_res_recues.setItem(row, 2, QTableWidgetItem(f"{res.prenom} {res.nom}"))
            self.table_res_recues.setItem(row, 3, QTableWidgetItem(str(res.places_reservees)))
            self.table_res_recues.setItem(row, 4, QTableWidgetItem(res.statut))
            self.table_res_recues.setItem(row, 5, QTableWidgetItem(res.created_at[:10]))
            
            btn_accept = QPushButton("✓")
            btn_accept.clicked.connect(lambda _, rid=res.id: self.accepter_reservation(rid))
            self.table_res_recues.setCellWidget(row, 6, btn_accept)
            
            btn_refuse = QPushButton("✗")
            btn_refuse.clicked.connect(lambda _, rid=res.id: self.refuser_reservation(rid))
            self.table_res_recues.setCellWidget(row, 7, btn_refuse)
    
    def charger_reservations_faites(self):
        """Charge les réservations faites"""
        reservations, erreur = ReservationController.get_reservations_faites(self.main_window.current_user['id'])
        
        if erreur:
            QMessageBox.warning(self, "Erreur", erreur)
            return
        
        self.table_res_faites.setRowCount(0)
        for res in reservations:
            row = self.table_res_faites.rowCount()
            self.table_res_faites.insertRow(row)
            
            self.table_res_faites.setItem(row, 0, QTableWidgetItem(res.depart))
            self.table_res_faites.setItem(row, 1, QTableWidgetItem(res.arrivee))
            self.table_res_faites.setItem(row, 2, QTableWidgetItem(f"{res.prenom} {res.nom}"))
            self.table_res_faites.setItem(row, 3, QTableWidgetItem(str(res.places_reservees)))
            self.table_res_faites.setItem(row, 4, QTableWidgetItem(res.statut))
            self.table_res_faites.setItem(row, 5, QTableWidgetItem(res.created_at[:10]))
            
            btn_cancel = QPushButton("✗")
            btn_cancel.clicked.connect(lambda _, rid=res.id: self.annuler_reservation(rid))
            self.table_res_faites.setCellWidget(row, 6, btn_cancel)
    
    # ===== CHARGEMENT INVITATIONS =====
    def charger_invitations_recues(self):
        """Charge les invitations reçues"""
        invitations, erreur = InvitationController.get_invitations_recues(self.main_window.current_user['id'])
        
        if erreur:
            QMessageBox.warning(self, "Erreur", erreur)
            return
        
        self.table_inv_recues.setRowCount(0)
        for inv in invitations:
            row = self.table_inv_recues.rowCount()
            self.table_inv_recues.insertRow(row)
            
            self.table_inv_recues.setItem(row, 0, QTableWidgetItem(inv.depart))
            self.table_inv_recues.setItem(row, 1, QTableWidgetItem(inv.arrivee))
            self.table_inv_recues.setItem(row, 2, QTableWidgetItem(f"{inv.prenom} {inv.nom}"))
            self.table_inv_recues.setItem(row, 3, QTableWidgetItem(inv.statut))
            self.table_inv_recues.setItem(row, 4, QTableWidgetItem(inv.created_at[:10]))
            
            btn_accept = QPushButton("✓")
            btn_accept.clicked.connect(lambda _, iid=inv.id: self.accepter_invitation(iid))
            self.table_inv_recues.setCellWidget(row, 5, btn_accept)
            
            btn_refuse = QPushButton("✗")
            btn_refuse.clicked.connect(lambda _, iid=inv.id: self.refuser_invitation(iid))
            self.table_inv_recues.setCellWidget(row, 6, btn_refuse)
    
    def charger_invitations_envoyees(self):
        """Charge les invitations envoyées"""
        invitations, erreur = InvitationController.get_invitations_envoyees(self.main_window.current_user['id'])
        
        if erreur:
            QMessageBox.warning(self, "Erreur", erreur)
            return
        
        self.table_inv_envoyees.setRowCount(0)
        for inv in invitations:
            row = self.table_inv_envoyees.rowCount()
            self.table_inv_envoyees.insertRow(row)
            
            self.table_inv_envoyees.setItem(row, 0, QTableWidgetItem(inv.depart))
            self.table_inv_envoyees.setItem(row, 1, QTableWidgetItem(inv.arrivee))
            self.table_inv_envoyees.setItem(row, 2, QTableWidgetItem(f"{inv.prenom} {inv.nom}"))
            self.table_inv_envoyees.setItem(row, 3, QTableWidgetItem(inv.statut))
            self.table_inv_envoyees.setItem(row, 4, QTableWidgetItem(inv.created_at[:10]))
            
            btn_delete = QPushButton("✗")
            btn_delete.clicked.connect(lambda _, iid=inv.id: self.refuser_invitation(iid))
            self.table_inv_envoyees.setCellWidget(row, 5, btn_delete)
    
    # ===== ACTIONS =====
    def accepter_reservation(self, res_id):
        success, msg = ReservationController.accepter_reservation(res_id)
        if success:
            QMessageBox.information(self, "Succès", msg)
            self.charger_reservations_recues()
        else:
            QMessageBox.warning(self, "Erreur", msg)
    
    def refuser_reservation(self, res_id):
        success, msg = ReservationController.refuser_reservation(res_id)
        if success:
            QMessageBox.information(self, "Succès", msg)
            self.charger_reservations_recues()
        else:
            QMessageBox.warning(self, "Erreur", msg)
    
    def annuler_reservation(self, res_id):
        success, msg = ReservationController.annuler_reservation(res_id)
        if success:
            QMessageBox.information(self, "Succès", msg)
            self.charger_reservations_faites()
        else:
            QMessageBox.warning(self, "Erreur", msg)
    
    def accepter_invitation(self, inv_id):
        success, msg = InvitationController.accepter_invitation(inv_id)
        if success:
            QMessageBox.information(self, "Succès", msg)
            self.charger_invitations_recues()
        else:
            QMessageBox.warning(self, "Erreur", msg)
    
    def refuser_invitation(self, inv_id):
        success, msg = InvitationController.refuser_invitation(inv_id)
        if success:
            QMessageBox.information(self, "Succès", msg)
            self.charger_invitations_recues()
        else:
            QMessageBox.warning(self, "Erreur", msg)