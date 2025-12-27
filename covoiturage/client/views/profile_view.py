from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class ProfileView(QWidget):
    def __init__(self, user_controller, main_window=None):
        super().__init__()
        self.user_controller = user_controller
        self.main_window = main_window

        layout = QVBoxLayout()

        self.label = QLabel("Profil")
        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.email_input = QLineEdit()
        self.update_button = QPushButton("Mettre à jour")
        self.back_button = QPushButton("Retour")

        layout.addWidget(self.label)
        layout.addWidget(self.nom_input)
        layout.addWidget(self.prenom_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.update_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.update_button.clicked.connect(self.update_profile)
        self.back_button.clicked.connect(self.go_back)

    def load_user(self, user_id):
        response = self.user_controller.get_user(user_id)
        if response.get("success"):
            user = response["user"]
            self.nom_input.setText(user.get("nom", ""))
            self.prenom_input.setText(user.get("prenom", ""))
            self.email_input.setText(user.get("email", ""))

    def update_profile(self):
        data = {
            "nom": self.nom_input.text(),
            "prenom": self.prenom_input.text(),
            "email": self.email_input.text()
        }
        # Pour l’exemple, user_id=1
        response = self.user_controller.update_user(1, data)
        if response.get("success"):
            if self.main_window:
                self.main_window.show_message("Profil mis à jour !")
        else:
            if self.main_window:
                self.main_window.show_error(response.get("message", "Erreur"))

    def go_back(self):
        if self.main_window:
            self.main_window.show_home_page()
