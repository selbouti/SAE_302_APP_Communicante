from models.user_model import UserModel


class UserController:
    """
    Logique métier liée aux utilisateurs (authentification, inscription, navigation).
    """

    def __init__(self, main_window):
        self.main_window = main_window   # Fenêtre principale (QStackedWidget)
        self.model = UserModel()

    # --- navigation entre pages ---
    def go_login(self):
        self.main_window.show_login_page()

    def go_register(self):
        self.main_window.show_register_page()

    def go_home(self):
        self.main_window.show_home_page()

    # --- logique métier ---
    def login(self, login: str, mdp: str) -> bool:
        return self.model.authenticate(login, mdp)

    def register(self, data: dict) -> bool:
        """
        data contient les champs du formulaire d'inscription.
        Retourne True si OK, False si login déjà utilisé ou erreur.
        """
        return self.model.create_user(data)
