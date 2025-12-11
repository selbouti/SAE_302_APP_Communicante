#!/usr/bin/env python3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Dossiers à créer
DIRS = [
    "config",
    "controllers",
    "models",
    "views",
    "services",
    "tests",
    "resources",
]

# Fichiers à créer avec contenu de base
FILES = {
    "config/database.py": '''import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "covoiturage_app",
    "password": "MotDePasseSuperSecure123!",  # TODO: adapter
    "database": "covoiturage",
}


def get_connection():
    """
    Ouvre une connexion MySQL vers la base 'covoiturage'.
    Retourne None en cas d'échec.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("❌ Erreur de connexion MySQL :", e)
        return None
''',

    "models/user_model.py": '''from config.database import get_connection


class UserModel:
    """
    Accès aux données Utilisateur en base MySQL.
    """

    def create_user(self, data: dict) -> bool:
        """
        Crée un utilisateur en base.
        data = {
            "nom", "prenom", "login", "mot_de_passe",
            "email", "telephone", "adresse", "ville", "cp"
        }
        """
        conn = get_connection()
        if conn is None:
            return False

        # Vérifier que le login n'existe pas déjà
        if self.login_exists(data["login"], conn):
            conn.close()
            return False

        cursor = conn.cursor()
        sql = """
            INSERT INTO Utilisateur
            (nom, prenom, login, mot_de_passe, email, telephone, adresse, ville, cp)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (
            data["nom"], data["prenom"], data["login"], data["mot_de_passe"],
            data["email"], data["telephone"], data["adresse"],
            data["ville"], data["cp"]
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def authenticate(self, login: str, mdp: str) -> bool:
        """
        Vérifie si (login, mot_de_passe) correspond à un utilisateur existant.
        """
        conn = get_connection()
        if conn is None:
            return False

        cursor = conn.cursor(dictionary=True)
        sql = "SELECT id_user FROM Utilisateur WHERE login = %s AND mot_de_passe = %s"
        cursor.execute(sql, (login, mdp))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user is not None

    def login_exists(self, login: str, conn=None) -> bool:
        """
        Vérifie si un login est déjà pris.
        Si une connexion est fournie, on la réutilise (sinon on en crée une).
        """
        close_conn = False
        if conn is None:
            conn = get_connection()
            if conn is None:
                return False
            close_conn = True

        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM Utilisateur WHERE login = %s"
        cursor.execute(sql, (login,))
        (count,) = cursor.fetchone()
        cursor.close()
        if close_conn:
            conn.close()
        return count > 0
''',

    "controllers/user_controller.py": '''from models.user_model import UserModel


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
''',

    "views/login_view.py": '''from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt


class LoginPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()

        titre = QLabel("🔑 Connexion")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 18px; font-weight: bold;")

        form = QFormLayout()
        self.login = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        form.addRow("Login :", self.login)
        form.addRow("Mot de passe :", self.password)

        btn_connexion = QPushButton("Se connecter")
        btn_inscription = QPushButton("Créer un compte")

        btn_connexion.clicked.connect(self._on_login_clicked)
        btn_inscription.clicked.connect(self.controller.go_register)

        layout.addWidget(titre)
        layout.addLayout(form)
        layout.addWidget(btn_connexion)
        layout.addWidget(btn_inscription)
        layout.addStretch()
        self.setLayout(layout)

    def _on_login_clicked(self):
        login = self.login.text().strip()
        mdp = self.password.text().strip()

        if self.controller.login(login, mdp):
            self.controller.go_home()
        else:
            QMessageBox.warning(self, "Erreur", "Identifiants incorrects.")
''',

    "views/register_view.py": '''from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt


class RegisterPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()
        titre = QLabel("📝 Inscription")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 18px; font-weight: bold;")

        form = QFormLayout()
        self.nom = QLineEdit()
        self.prenom = QLineEdit()
        self.login = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.email = QLineEdit()
        self.telephone = QLineEdit()
        self.adresse = QLineEdit()
        self.ville = QLineEdit()
        self.cp = QLineEdit()

        form.addRow("Nom :", self.nom)
        form.addRow("Prénom :", self.prenom)
        form.addRow("Login :", self.login)
        form.addRow("Mot de passe :", self.password)
        form.addRow("Email :", self.email)
        form.addRow("Téléphone :", self.telephone)
        form.addRow("Adresse :", self.adresse)
        form.addRow("Ville :", self.ville)
        form.addRow("Code postal :", self.cp)

        btn_creer = QPushButton("Créer le compte")
        btn_retour = QPushButton("Retour")

        btn_creer.clicked.connect(self._on_register_clicked)
        btn_retour.clicked.connect(self.controller.go_login)

        layout.addWidget(titre)
        layout.addLayout(form)
        layout.addWidget(btn_creer)
        layout.addWidget(btn_retour)
        layout.addStretch()
        self.setLayout(layout)

    def _on_register_clicked(self):
        data = {
            "nom": self.nom.text().strip(),
            "prenom": self.prenom.text().strip(),
            "login": self.login.text().strip(),
            "mot_de_passe": self.password.text().strip(),
            "email": self.email.text().strip(),
            "telephone": self.telephone.text().strip(),
            "adresse": self.adresse.text().strip(),
            "ville": self.ville.text().strip(),
            "cp": self.cp.text().strip(),
        }

        if not all(data.values()):
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis.")
            return

        if self.controller.register(data):
            QMessageBox.information(self, "Succès", "Compte créé avec succès.")
            self.controller.go_login()
        else:
            QMessageBox.warning(self, "Erreur", "Login déjà utilisé ou erreur en base.")
''',

    "views/home_view.py": '''from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt


class HomePage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()
        titre = QLabel("🚗 Bienvenue sur l'application de covoiturage")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 18px; font-weight: bold;")

        sous_titre = QLabel("Les autres fonctionnalités (trajets, compatibilités, etc.) viendront ici.")
        sous_titre.setAlignment(Qt.AlignCenter)

        btn_deconnexion = QPushButton("Se déconnecter")
        btn_deconnexion.clicked.connect(self.controller.go_login)

        layout.addWidget(titre)
        layout.addWidget(sous_titre)
        layout.addWidget(btn_deconnexion)
        layout.addStretch()
        self.setLayout(layout)
''',

    "views/main_window.py": '''from PyQt5.QtWidgets import QStackedWidget
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
''',

    "services/matching_service.py": '''"""
Service de calcul de compatibilité de trajets (à compléter plus tard).
"""
''',

    "services/edt_parser.py": '''"""
Service de lecture / parsing des fichiers iCalendar (EDT) (à compléter).
"""
''',

    "services/bilan_service.py": '''"""
Service de calcul des coûts kilométriques et du bilan carbone (à compléter).
"""
''',

    "models/trajet_model.py": '''"""
Modèle Trajet (à compléter selon la structure de la base).
"""
''',

    "models/voiture_model.py": '''"""
Modèle Voiture (à compléter selon la structure de la base).
"""
''',

    "models/edt_model.py": '''"""
Modèle EmploiDuTemps / Disponibilités (à compléter).
"""
''',

    "controllers/trajet_controller.py": '''"""
Contrôleur pour la gestion des trajets (à compléter).
"""
''',

    "controllers/planning_controller.py": '''"""
Contrôleur pour la gestion du planning / disponibilités (à compléter).
"""
''',

    "tests/__init__.py": "",
    "resources/.gitkeep": "",
    "tests/test_user_model.py": '''"""
Tests unitaires du UserModel (à compléter).
"""
''',

    "main.py": '''import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
''',
}


def main():
    # Création des dossiers
    for d in DIRS:
        path = BASE_DIR / d
        path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Dossier OK : {path}")

    # Création des fichiers
    for rel_path, content in FILES.items():
        file_path = BASE_DIR / rel_path
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            file_path.write_text(content, encoding="utf-8")
            print(f"📄 Fichier créé : {file_path}")
        else:
            print(f"⚠️ Fichier déjà existant, ignoré : {file_path}")


if __name__ == "__main__":
    main()
