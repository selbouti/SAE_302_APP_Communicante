import ast
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from services.api_service import APIService
from controllers.invitation_controller import InvitationController
from controllers.message_controller import MessageController
from controllers.reservation_controller import ReservationController

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
        res_title_layout = QHBoxLayout()
        res_title_layout.addWidget(res_title)
        self.res_badge = QLabel("")
        self.res_badge.setObjectName("notifBadge")
        self.res_badge.hide()
        self.res_badge.setText("● Nouveau")
        res_title_layout.addWidget(self.res_badge)
        res_title_layout.addStretch()
        layout.addLayout(res_title_layout)

        self.res_table = QTableWidget()
        self.res_table.setColumnCount(8)
        self.res_table.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Date', 'Places', 'Prix', 'Statut', 'Nouveau', 'Action'])
        layout.addWidget(self.res_table)

        # Bloc invitations
        inv_title = QLabel("Invitations reçues")
        inv_title.setObjectName("sectionLabel")
        layout.addWidget(inv_title)

        self.inv_table = QTableWidget()
        self.inv_table.setColumnCount(9)
        self.inv_table.setHorizontalHeaderLabels(['Départ', 'Arrivée', 'Date', 'Prix', 'Statut', 'Conducteur', 'Contact', 'Nouveau', 'Action'])
        layout.addWidget(self.inv_table)

        # Bloc passagers sur mes trajets (conducteur)
        self.co_title = QLabel("Passagers sur mes trajets")
        self.co_title.setObjectName("sectionLabel")
        layout.addWidget(self.co_title)

        self.co_table = QTableWidget()
        self.co_table.setColumnCount(6)
        self.co_table.setHorizontalHeaderLabels(['Trajet', 'Passager', 'Places', 'Statut', 'Contact', 'Action'])
        layout.addWidget(self.co_table)

        refresh = QPushButton("Rafraîchir")
        refresh.clicked.connect(self.charger)
        layout.addWidget(refresh)

        clear_btn = QPushButton("Effacer notifications")
        clear_btn.clicked.connect(self.clear_notifications)
        layout.addWidget(clear_btn)
        
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
            QLabel#notifBadge {
                background: #d90429;
                color: #ffffff;
                border-radius: 10px;
                padding: 3px 8px;
                font-size: 12px;
                font-weight: 700;
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
        messages, msg_status = MessageController.list_for_user(user_id)
        co_rows = []
        # réservations sur mes trajets (si conducteur)
        res_trajets = []
        try:
            trajets, traj_status = APIService.get(f'mes_trajets/{user_id}')
            if traj_status == 200:
                for t in trajets:
                    res_trajets.append((t['id'], t.get('depart',''), t.get('arrivee',''), t.get('date_depart','')))
        except Exception:
            pass
        co_rows = []
        for t_id, dep, arr, date in res_trajets:
            res_list, st = APIService.get(f'reservations/trajet/{t_id}')
            if st == 200:
                for r in res_list:
                    co_rows.append({
                        'id': r.get('id'),
                        'trajet': f"{dep} → {arr} le {date}",
                        'passager': f"{r.get('prenom','')} {r.get('nom','')}",
                        'places': r.get('places_reservees', 0),
                        'statut': r.get('statut', ''),
                        'contact': r.get('email', '')
                    })

        new_res_ids = set()
        new_inv_ids = set()
        if msg_status == 200:
            for m in messages:
                meta = {}
                if m.get('meta'):
                    try:
                        meta = ast.literal_eval(m['meta'])
                    except Exception:
                        meta = {}
                if isinstance(meta, dict):
                    if 'reservation_id' in meta:
                        new_res_ids.add(int(meta['reservation_id']))
                    if 'invitation_id' in meta:
                        new_inv_ids.add(int(meta['invitation_id']))
            if new_res_ids:
                self.res_badge.show()
            else:
                self.res_badge.hide()

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
                new_item = QTableWidgetItem("Nouveau") if r['id'] in new_res_ids else QTableWidgetItem("")
                self.res_table.setItem(row, 6, new_item)
                
                btn = QPushButton("Annuler")
                btn.clicked.connect(lambda _, r_id=r['id']: self.annuler(r_id))
                self.res_table.setCellWidget(row, 7, btn)

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
                    self.inv_table.setItem(row, 5, QTableWidgetItem(f"{inv.get('prenom','')} {inv.get('nom','')}"))
                    self.inv_table.setItem(row, 6, QTableWidgetItem(inv.get('email','')))
                    new_item_inv = QTableWidgetItem("Nouveau") if inv.get('id') in new_inv_ids else QTableWidgetItem("")
                    self.inv_table.setItem(row, 7, new_item_inv)

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
                    self.inv_table.setCellWidget(row, 8, actions)
            # Passagers sur mes trajets (tous, avec actions si en attente)
            self.co_table.setRowCount(0)
            for co in co_rows:
                row = self.co_table.rowCount()
                self.co_table.insertRow(row)
                self.co_table.setItem(row, 0, QTableWidgetItem(co['trajet']))
                self.co_table.setItem(row, 1, QTableWidgetItem(co['passager']))
                self.co_table.setItem(row, 2, QTableWidgetItem(str(co['places'])))
                self.co_table.setItem(row, 3, QTableWidgetItem(co['statut']))
                self.co_table.setItem(row, 4, QTableWidgetItem(co['contact']))
                if co['statut'] == 'en_attente':
                    actions = QWidget()
                    actions_layout = QHBoxLayout(actions)
                    actions_layout.setContentsMargins(0, 0, 0, 0)
                    actions_layout.setSpacing(6)
                    accept_btn = QPushButton("Accepter")
                    accept_btn.clicked.connect(lambda _, r_id=co['id']: self.accepter_co(r_id))
                    refuse_btn = QPushButton("Refuser")
                    refuse_btn.clicked.connect(lambda _, r_id=co['id']: self.refuser_co(r_id))
                    actions_layout.addWidget(accept_btn)
                    actions_layout.addWidget(refuse_btn)
                    actions.setLayout(actions_layout)
                    self.co_table.setCellWidget(row, 5, actions)
                else:
                    self.co_table.setItem(row, 5, QTableWidgetItem(""))
        else:
            self.res_table.setRowCount(0)
            self.inv_table.setRowCount(0)
            self.co_table.setRowCount(0)
    
    def annuler(self, reservation_id):
        APIService.delete(f'reservations/{reservation_id}/annuler')
        self.charger()

    def accepter_inv(self, invitation_id):
        InvitationController.accepter(invitation_id)
        self.charger()

    def refuser_inv(self, invitation_id):
        InvitationController.refuser(invitation_id)
        self.charger()

    def clear_notifications(self):
        if not self.main_window.current_user:
            return
        MessageController.clear_for_user(self.main_window.current_user['id'])
        self.res_badge.hide()
        self.charger()

    def accepter_co(self, reservation_id):
        resp, status = ReservationController.accepter(reservation_id)
        if status != 200:
            QMessageBox.warning(self, "Erreur", resp.get('error', 'Impossible d\'accepter (places insuffisantes ?)'))
        self.charger()

    def refuser_co(self, reservation_id):
        ReservationController.refuser(reservation_id)
        self.charger()
