from PyQt5.QtWidgets import QStackedWidget
from controllers.user_controller import UserController
from views.login_view import LoginPage
from views.register_view import RegisterPage
from views.home_view import HomePage


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Crée le controller utilisateur et lui passe la fenêtre
        self.user_controller = UserController(self)

        # Crée les pages
        self.login_page = LoginPage(self.user_controller)
        self.register_page = RegisterPage(self.user_controller)
        self.home_page = HomePage(self.user_controller)

        # Ajoute les pages au QStackedWidget
        self.addWidget(self.login_page)
        self.addWidget(self.register_page)
        self.addWidget(self.home_page)

        # Réglages de la fenêtre
        self.setWindowTitle("Covoiturage - Application")
        self.setMinimumSize(500, 400)

        self.show_login_page()

    # Méthodes utilisées par le contrôleur
    def show_login_page(self):
        self.setCurrentWidget(self.login_page)

    def show_register_page(self):
        self.setCurrentWidget(self.register_page)

    def show_home_page(self):
        self.setCurrentWidget(self.home_page)
