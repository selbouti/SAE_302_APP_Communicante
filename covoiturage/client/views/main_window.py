from PyQt5.QtWidgets import (
    QMainWindow, QStackedWidget, QVBoxLayout,
    QWidget, QAction, QMessageBox, QToolBar
)
from PyQt5.QtCore import Qt, QSize


class MainWindow(QMainWindow):
    """
    Fenêtre principale de l'application Covoiturage Daily.

    Cette classe gère :
    - l'affichage des différentes vues via un QStackedWidget
    - la barre de menu (MenuBar)
    - la barre d'outils (ToolBar)
    - la navigation entre les vues
    - l'état de l'utilisateur connecté

    Elle constitue le point central de l'interface graphique côté client.
    """

    def __init__(self, views):
        """
        Initialise la fenêtre principale.

        :param views: dictionnaire des vues de l'application
        :type views: dict
        """
        super().__init__()
        self.setWindowTitle("Covoiturage Daily - BlaBlaCar")
        self.setGeometry(100, 100, 1000, 700)

        #: Utilisateur actuellement connecté
        self.current_user = None

        #: Dictionnaire des vues
        self.views = views

        # ---------- Widget central ----------
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        #: Widget empilé contenant toutes les vues
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.setCentralWidget(central_widget)

        for view in views.values():
            self.stack.addWidget(view)

        # ---------- Menu + Toolbar ----------
        self.create_menu_bar()
        self.create_tool_bar()

        # Cachés par défaut (login / register)
        self.menuBar().hide()
        self.toolbar.hide()

    # =====================================================
    # BARRE DE MENU
    # =====================================================
    def create_menu_bar(self):
        """
        Crée la barre de menu principale de l'application.

        Elle contient :
        - un menu Compte
        - un menu Trajets
        - un menu Réservations
        - un menu Aide

        Chaque entrée déclenche une navigation vers une vue via `switch_to`.
        """
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #8b1a1a;
                color: #ffffff;
                font-size: 15px;
                font-weight: 600;
            }
            QMenuBar::item {
                padding: 6px 12px;
            }
            QMenuBar::item:selected {
                background-color: #a32020;
            }
            QMenu {
                background-color: #ffffff;
                color: #1e1e1e;
                font-size: 14px;
            }
            QMenu::item:selected {
                background-color: #f3dede;
                color: #7a1111;
            }
        """)

        # ===== COMPTE =====
        menu_compte = menubar.addMenu("Compte")

        self.act_profile = QAction("Mon profil", self)
        self.act_profile.setShortcut("Ctrl+P")
        self.act_profile.triggered.connect(lambda: self.switch_to("profile"))

        self.act_voiture = QAction("Ma voiture", self)
        self.act_voiture.setShortcut("Ctrl+V")
        self.act_voiture.triggered.connect(lambda: self.switch_to("voiture"))

        self.act_logout = QAction("Déconnexion", self)
        self.act_logout.setShortcut("Ctrl+Q")
        self.act_logout.triggered.connect(self.logout)

        menu_compte.addAction(self.act_profile)
        menu_compte.addAction(self.act_voiture)
        menu_compte.addSeparator()
        menu_compte.addAction(self.act_logout)

        # ===== TRAJETS =====
        menu_trajets = menubar.addMenu("Trajets")

        self.act_mes_trajets = QAction("Mes trajets", self)
        self.act_mes_trajets.setShortcut("Ctrl+T")
        self.act_mes_trajets.triggered.connect(
            lambda: self.switch_to("mes_trajets")
        )

        self.act_matching = QAction("Matching", self)
        self.act_matching.setShortcut("Ctrl+M")
        self.act_matching.triggered.connect(
            lambda: self.switch_to("matching")
        )

        menu_trajets.addAction(self.act_mes_trajets)
        menu_trajets.addAction(self.act_matching)

        # ===== RÉSERVATIONS =====
        menu_resa = menubar.addMenu("Réservations")

        self.act_resa = QAction("Mes réservations", self)
        self.act_resa.setShortcut("Ctrl+R")
        self.act_resa.triggered.connect(
            lambda: self.switch_to("mes_reservations")
        )

        menu_resa.addAction(self.act_resa)

        # ===== AIDE =====
        menu_aide = menubar.addMenu("Aide")

        self.act_about = QAction("À propos", self)
        self.act_about.triggered.connect(self.show_about)

        menu_aide.addAction(self.act_about)

    # =====================================================
    # TOOLBAR
    # =====================================================
    def create_tool_bar(self):
        """
        Crée la barre d'outils (ToolBar) de navigation rapide.

        Elle permet un accès direct aux principales vues :
        - profil
        - voiture
        - trajets
        - matching
        - réservations
        - déconnexion
        """
        self.toolbar = QToolBar("Navigation")
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(24, 24))
        self.toolbar.setOrientation(Qt.Vertical)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #f7f7f7;
                spacing: 8px;
                padding: 8px;
            }
            QToolButton {
                background-color: #8b1a1a;
                color: #ffffff;
                border: 1px solid #6f1212;
                border-radius: 4px;
                padding: 8px 10px;
                font-weight: 600;
                min-width: 180px;
                max-width: 180px;
                text-align: left;
            }
            QToolButton:hover {
                background-color: #a32020;
            }
            QToolButton:pressed {
                background-color: #6b1212;
            }
        """)

        self.toolbar.addAction(self.act_profile)
        self.toolbar.addAction(self.act_voiture)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_mes_trajets)
        self.toolbar.addAction(self.act_matching)
        self.toolbar.addAction(self.act_resa)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_logout)
        self.toolbar.addAction(self.act_about)

        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

    # =====================================================
    # NAVIGATION
    # =====================================================
    def set_current_user(self, user):
        """
        Définit l'utilisateur actuellement connecté.

        :param user: informations de l'utilisateur
        :type user: dict
        """
        self.current_user = user

    def switch_to(self, view_name):
        """
        Change la vue affichée dans le QStackedWidget.

        - Masque la barre de menu et la toolbar sur login/register
        - Recharge la vue si elle possède une méthode `load` ou `refresh`

        :param view_name: nom de la vue à afficher
        :type view_name: str
        """
        if view_name in ("login", "register"):
            self.menuBar().hide()
            self.toolbar.hide()
        elif view_name == "home":
            self.menuBar().show()
            self.toolbar.hide()
        else:
            self.menuBar().show()
            self.toolbar.show()

        if view_name in self.views:
            view = self.views[view_name]

            if hasattr(view, "load"):
                view.load()
            elif hasattr(view, "refresh"):
                view.refresh()

            self.stack.setCurrentWidget(view)

    def logout(self):
        """
        Déconnecte l'utilisateur courant et redirige vers la vue de connexion.
        """
        self.current_user = None
        self.switch_to("login")

    def show_about(self):
        """
        Affiche la boîte de dialogue 'À propos' de l'application.
        """
        QMessageBox.information(
            self,
            "À propos",
            "Covoiturage Daily\n"
            "Application PyQt client/serveur\n"
            "Projet SAE"
        )
