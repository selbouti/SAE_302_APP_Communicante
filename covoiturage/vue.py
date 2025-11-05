# vue.py
from PyQt5.QtWidgets import (
    QWidget, QStackedWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QFormLayout, QHBoxLayout, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt
from controleur import ControleurApp

class PageConnexion(QWidget):
    """Page de connexion utilisateur."""
    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
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

        btn_connexion.clicked.connect(self.se_connecter)
        btn_inscription.clicked.connect(self.controleur.aller_inscription)

        layout.addWidget(titre)
        layout.addLayout(form)
        layout.addWidget(btn_connexion)
        layout.addWidget(btn_inscription)
        layout.addStretch()
        self.setLayout(layout)

    def se_connecter(self):
        login = self.login.text()
        mdp = self.password.text()
        if self.controleur.connexion_valide(login, mdp):
            self.controleur.aller_accueil()
        else:
            QMessageBox.warning(self, "Erreur", "Identifiants incorrects.")


class PageInscription(QWidget):
    """Page d'inscription utilisateur."""
    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
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
        self.places = QComboBox()
        self.places.addItems([str(i) for i in range(1, 6)])
        form.addRow("Nom :", self.nom)
        form.addRow("Prénom :", self.prenom)
        form.addRow("Login :", self.login)
        form.addRow("Mot de passe :", self.password)
        form.addRow("Places voiture :", self.places)

        btn_creer = QPushButton("Créer le compte")
        btn_retour = QPushButton("Retour")

        btn_creer.clicked.connect(self.creer_compte)
        btn_retour.clicked.connect(self.controleur.aller_connexion)

        layout.addWidget(titre)
        layout.addLayout(form)
        layout.addWidget(btn_creer)
        layout.addWidget(btn_retour)
        layout.addStretch()
        self.setLayout(layout)

    def creer_compte(self):
        infos = {
            "nom": self.nom.text(),
            "prenom": self.prenom.text(),
            "login": self.login.text(),
            "mdp": self.password.text(),
            "places": int(self.places.currentText())
        }
        if self.controleur.enregistrer_utilisateur(infos):
            QMessageBox.information(self, "Succès", "Compte créé avec succès !")
            self.controleur.aller_connexion()
        else:
            QMessageBox.warning(self, "Erreur", "Login déjà existant.")


class PageAccueil(QWidget):
    """Page principale : choix de jour, covoiturages, bilan."""
    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        layout = QVBoxLayout()

        titre = QLabel("🚗 Application de Covoiturage")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

        form = QFormLayout()
        self.jour = QComboBox()
        self.jour.addItems(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"])
        form.addRow("Jour :", self.jour)

        btn_voir = QPushButton("Voir les covoiturages compatibles")
        btn_bilan = QPushButton("Voir le bilan")
        btn_deco = QPushButton("Déconnexion")

        btn_voir.clicked.connect(self.montrer_covoiturages)
        btn_bilan.clicked.connect(self.montrer_bilan)
        btn_deco.clicked.connect(self.controleur.aller_connexion)

        layout.addWidget(titre)
        layout.addLayout(form)
        layout.addWidget(btn_voir)
        layout.addWidget(btn_bilan)
        layout.addWidget(btn_deco)
        layout.addStretch()
        self.setLayout(layout)

    def montrer_covoiturages(self):
        QMessageBox.information(self, "Résultats", "Fonctionnalité à venir : affichage des covoiturages compatibles.")

    def montrer_bilan(self):
        QMessageBox.information(self, "Bilan", "Fonctionnalité à venir : affichage du bilan carbone et coûts.")


class FenetrePrincipale(QStackedWidget):
    """Gère la navigation entre les pages."""
    def __init__(self):
        super().__init__()
        self.controleur = ControleurApp(self)
        self.page_connexion = PageConnexion(self.controleur)
        self.page_inscription = PageInscription(self.controleur)
        self.page_accueil = PageAccueil(self.controleur)

        self.addWidget(self.page_connexion)
        self.addWidget(self.page_inscription)
        self.addWidget(self.page_accueil)

        self.setWindowTitle("Covoiturage - PyQt5")
        self.setMinimumSize(400, 300)
        self.setCurrentWidget(self.page_connexion)
