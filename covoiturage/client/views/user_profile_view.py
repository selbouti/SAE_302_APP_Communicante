from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class UserProfileView(QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Page de gestion du profil"))
        layout.addWidget(QLabel("(Formulaires à compléter par la suite)"))

        self.setLayout(layout)
