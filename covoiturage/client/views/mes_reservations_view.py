from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from services.api_service import APIService
from controllers.invitation_controller import InvitationController

class MesReservationsView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Mes réservations et invitations")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        
        # Bloc réservations
        res_title = QLabel("Réservations")
        res_title.setObjectName("sectionLabel")
        layout.addWidget(res_title)

        self.res_table = QTableWidget()
        self.res_table.setColumnCount(7)
        self.res_table.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Date', 'Places', 'Prix', 'Statut', 'Action'])
        layout.addWidget(self.res_table)

        # Bloc invitations
        inv_title = QLabel("Invitations reçues")
        inv_title.setObjectName("sectionLabel")
        layout.addWidget(inv_title)

        self.inv_table = QTableWidget()
        self.inv_table.setColumnCount(6)
        self.inv_table.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Date', 'Prix', 'Statut', 'Action'])
        layout.addWidget(self.inv_table)
        
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
            QLabel#sectionLabel {
                color: #4a4a4a;
                font-size: 15px;
                font-weight: 700;
                padding: 6px 0 4px 0;
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
                selection-color: #b00020;
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
        
        user_id = self.main_window.current_user['id']
        reservations, res_status = APIService.get(f'reservations/passager/{user_id}')
        invitations, inv_status = InvitationController.invitations_received(user_id)
        
        if res_status == 200:
            self.res_table.setRowCount(0)
            # Réservations
            for r in reservations:
                row = self.res_table.rowCount()
                self.res_table.insertRow(row)
                
                self.res_table.setItem(row, 0, QTableWidgetItem(r['depart']))
                self.res_table.setItem(row, 1, QTableWidgetItem(r['arrivee']))
                self.res_table.setItem(row, 2, QTableWidgetItem(r['date_depart']))
                self.res_table.setItem(row, 3, QTableWidgetItem(str(r['places_reservees'])))
                self.res_table.setItem(row, 4, QTableWidgetItem(str(r['prix_par_place'])))
                self.res_table.setItem(row, 5, QTableWidgetItem(r['statut']))
                
                btn = QPushButton("Annuler")
                btn.clicked.connect(lambda _, r_id=r['id']: self.annuler(r_id))
                self.res_table.setCellWidget(row, 6, btn)

            # Invitations reçues
            if inv_status == 200:
                self.inv_table.setRowCount(0)
                for inv in invitations:
                    row = self.inv_table.rowCount()
                    self.inv_table.insertRow(row)
                    
                    self.inv_table.setItem(row, 0, QTableWidgetItem(inv.get('depart', '')))
                    self.inv_table.setItem(row, 1, QTableWidgetItem(inv.get('arrivee', '')))
                    self.inv_table.setItem(row, 2, QTableWidgetItem(inv.get('date_depart', '')))
                    self.inv_table.setItem(row, 3, QTableWidgetItem(str(inv.get('prix_par_place', ''))))
                    self.inv_table.setItem(row, 4, QTableWidgetItem(inv.get('statut', '')))

                    accept_btn = QPushButton("Accepter")
                    accept_btn.clicked.connect(lambda _, inv_id=inv['id']: self.accepter_inv(inv_id))
                    refuse_btn = QPushButton("Refuser")
                    refuse_btn.clicked.connect(lambda _, inv_id=inv['id']: self.refuser_inv(inv_id))

                    actions = QWidget()
                    actions_layout = QHBoxLayout(actions)
                    actions_layout.setContentsMargins(0, 0, 0, 0)
                    actions_layout.setSpacing(6)
                    actions_layout.addWidget(accept_btn)
                    actions_layout.addWidget(refuse_btn)
                    actions.setLayout(actions_layout)
                    self.inv_table.setCellWidget(row, 5, actions)
        else:
            self.res_table.setRowCount(0)
            self.inv_table.setRowCount(0)
    
    def annuler(self, reservation_id):
        APIService.delete(f'reservations/{reservation_id}/annuler')
        self.charger()

    def accepter_inv(self, invitation_id):
        InvitationController.accepter(invitation_id)
        self.charger()

    def refuser_inv(self, invitation_id):
        InvitationController.refuser(invitation_id)
        self.charger()
