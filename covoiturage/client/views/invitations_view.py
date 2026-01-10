# ============= views/invitations_view.py =============
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QTabWidget, QMessageBox, QLabel
from controllers.invitation_controller import InvitationController
from views.common_style import COMMON_STYLE

class InvitationsView(QWidget):
    """
    A view for managing invitations.
    
    This widget displays and manages both received and sent invitations.
    It allows users to accept, refuse, or delete invitations.
    """
    
    def __init__(self, main_window):
        """
        Initialize the InvitationsView.
        
        Args:
            main_window: The main application window reference
        """
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        
    def load(self):
        """Load and refresh all invitation data."""
        self.charger_invitations_recues()
        self.charger_invitations_envoyees()
    
    def setup_ui(self):
        """Initialize the user interface with tabs and tables."""
        layout = QVBoxLayout()
        
        # Onglets pour invitations
        self.tabs = QTabWidget()
        
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
        self.tabs.addTab(widget_recues, "Reçues")
        
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
        self.tabs.addTab(widget_envoyees, "Envoyées")
        
        layout.addWidget(self.tabs)
    
        
        self.setLayout(layout)
        self.setStyleSheet(COMMON_STYLE)
    
    # ===== LOADING INVITATIONS =====
    def charger_invitations_recues(self):
        """
        Load and display received invitations.
        
        Fetches invitations sent to the user from the controller and populates
        the table with accept/refuse action buttons.
        """
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
        """
        Load and display sent invitations.
        
        Fetches invitations sent by the current user from the controller and
        populates the table with delete action buttons.
        """
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
    def accepter_invitation(self, inv_id):
        """
        Accept a received invitation.
        
        Args:
            inv_id: The ID of the invitation to accept
        """
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