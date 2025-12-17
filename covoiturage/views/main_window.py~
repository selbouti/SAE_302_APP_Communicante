# views/main_window.py

from PyQt5.QtWidgets import QStackedWidget, QMessageBox

from controllers.user_controller import UserController

from views.login_view import LoginPage
from views.register_view import RegisterPage
from views.home_view import HomePage
from views.edt_import_view import EDTImportView
from views.profile_view import ProfileView
from views.voiture_view import VoitureView


class MainWindow(QStackedWidget):
    """
    Fenêtre principale : un QStackedWidget qui contient
    toutes les pages de l'application.
    """

    def __init__(self):
        super().__init__()

        # ===========================
        #   Contrôleur principal
        # ===========================
        self.user_controller = UserController(self)

        # ===========================
        #   Création des vues
        # ===========================
        self.login_page = LoginPage(self.user_controller)
        self.register_page = RegisterPage(self.user_controller)
        self.home_page = HomePage(self.user_controller)
        self.edt_page = EDTImportView(self.user_controller)
        self.profile_page = ProfileView(self.user_controller)   # ✅ AJOUT
        self.voiture_page = VoitureView(self.user_controller)   # ✅ AJOUT

        # ===========================
        #   Ajout au QStackedWidget
        # ===========================
        self.addWidget(self.login_page)
        self.addWidget(self.register_page)
        self.addWidget(self.home_page)
        self.addWidget(self.edt_page)
        self.addWidget(self.profile_page)   # ✅ AJOUT
        self.addWidget(self.voiture_page)   # ✅ AJOUT

        # ===========================
        #   Paramètres fenêtre
        # ===========================
        self.setWindowTitle("Covoiturage - Application")
        self.setMinimumSize(500, 400)

        # ===========================
        #   Page de départ
        # ===========================
        self.show_login_page()

    # ======================
    #  Navigation
    # ======================
    def show_login_page(self):
        self.setCurrentWidget(self.login_page)

    def show_register_page(self):
        self.setCurrentWidget(self.register_page)

    def show_home_page(self):
        self.setCurrentWidget(self.home_page)

    def show_edt_import_page(self):
        self.setCurrentWidget(self.edt_page)

    def show_profile_page(self):          # ✅ AJOUT
        self.setCurrentWidget(self.profile_page)

    def show_voiture_page(self):          # ✅ AJOUT
        self.setCurrentWidget(self.voiture_page)

    # ======================
    #  Messages
    # ======================
    def show_error(self, message: str):
        QMessageBox.critical(self, "Erreur", message)

    def show_message(self, message: str):
        QMessageBox.information(self, "Information", message)
