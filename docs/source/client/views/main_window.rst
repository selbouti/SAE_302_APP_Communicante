MainWindow
==========

Cette page documente la classe ``MainWindow``, qui constitue
le point central de l’interface graphique de l’application.

---

Création de la fenêtre principale
---------------------------------

La fenêtre principale hérite de ``QMainWindow``.

.. code-block:: python

   class MainWindow(QMainWindow):

---

Initialisation de la fenêtre
----------------------------

Le titre, la taille et les attributs principaux sont définis
lors de l'initialisation.

.. code-block:: python

   self.setWindowTitle("Covoiturage Daily - BlaBlaCar")
   self.setGeometry(100, 100, 1000, 700)

---

Utilisateur courant
-------------------

L'utilisateur connecté est stocké dans un attribut dédié.

.. code-block:: python

   self.current_user = None

---

Gestion des vues
----------------

Les vues sont stockées dans un dictionnaire et affichées via
un ``QStackedWidget``.

.. code-block:: python

   self.views = views
   self.stack = QStackedWidget()

---

Ajout des vues au QStackedWidget
--------------------------------

Chaque vue est ajoutée dynamiquement au conteneur empilé.

.. code-block:: python

   for view in views.values():
       self.stack.addWidget(view)

---

Création de la barre de menu
----------------------------

La barre de menu est créée lors de l'initialisation.

.. code-block:: python

   self.create_menu_bar()

---

Création de la barre d’outils
-----------------------------

Une barre d’outils latérale permet une navigation rapide.

.. code-block:: python

   self.create_tool_bar()

---

Masquage initial du menu et de la toolbar
-----------------------------------------

Les barres sont masquées sur les vues de connexion.

.. code-block:: python

   self.menuBar().hide()
   self.toolbar.hide()

---

Menu Compte
-----------

Le menu Compte donne accès au profil, à la voiture
et à la déconnexion.

.. code-block:: python

   menu_compte = menubar.addMenu("Compte")

---

Action « Mon profil »
---------------------

Navigation vers la vue Profil avec un raccourci clavier.

.. code-block:: python

   self.act_profile = QAction("Mon profil", self)
   self.act_profile.setShortcut("Ctrl+P")
   self.act_profile.triggered.connect(lambda: self.switch_to("profile"))

---

Action « Ma voiture »
---------------------

Navigation vers la vue Voiture.

.. code-block:: python

   self.act_voiture = QAction("Ma voiture", self)
   self.act_voiture.setShortcut("Ctrl+V")
   self.act_voiture.triggered.connect(lambda: self.switch_to("voiture"))

---

Action « Déconnexion »
---------------------

Déconnexion de l'utilisateur courant.

.. code-block:: python

   self.act_logout = QAction("Déconnexion", self)
   self.act_logout.setShortcut("Ctrl+Q")
   self.act_logout.triggered.connect(self.logout)

---

Menu Trajets
------------

Le menu Trajets permet d’accéder aux trajets et au matching.

.. code-block:: python

   menu_trajets = menubar.addMenu("Trajets")

---

Accès aux trajets personnels
----------------------------

Affiche la vue des trajets de l'utilisateur.

.. code-block:: python

   self.act_mes_trajets = QAction("Mes trajets", self)
   self.act_mes_trajets.setShortcut("Ctrl+T")

---

Accès au matching
-----------------

Affiche la vue de matching des trajets.

.. code-block:: python

   self.act_matching = QAction("Matching", self)
   self.act_matching.setShortcut("Ctrl+M")

---

Menu Réservations
-----------------

Permet d’accéder aux réservations et invitations.

.. code-block:: python

   menu_resa = menubar.addMenu("Réservations")

---

Accès aux réservations
----------------------

Affiche les réservations de l'utilisateur.

.. code-block:: python

   self.act_resa = QAction("Mes réservations", self)
   self.act_resa.setShortcut("Ctrl+R")

---

Création de la ToolBar
---------------------

La toolbar est positionnée à gauche et utilise du texte uniquement.

.. code-block:: python

   self.toolbar = QToolBar("Navigation")
   self.toolbar.setOrientation(Qt.Vertical)
   self.toolbar.setToolButtonStyle(Qt.ToolButtonTextOnly)

---

Ajout des actions à la ToolBar
------------------------------

Les actions principales sont ajoutées à la barre d’outils.

.. code-block:: python

   self.toolbar.addAction(self.act_profile)
   self.toolbar.addAction(self.act_voiture)
   self.toolbar.addAction(self.act_mes_trajets)
   self.toolbar.addAction(self.act_matching)
   self.toolbar.addAction(self.act_resa)

---

Navigation entre les vues
-------------------------

La méthode ``switch_to`` gère le changement de vue
et l’affichage des barres.

.. code-block:: python

   self.stack.setCurrentWidget(view)

---

Masquage conditionnel du menu
-----------------------------

Le menu et la toolbar sont masqués sur login/register.

.. code-block:: python

   if view_name in ("login", "register"):
       self.menuBar().hide()
       self.toolbar.hide()

---

Déconnexion de l’utilisateur
----------------------------

La déconnexion remet l'utilisateur à ``None``.

.. code-block:: python

   self.current_user = None
   self.switch_to("login")

---

Fenêtre « À propos »
--------------------

Affiche une boîte de dialogue informative.

.. code-block:: python

   QMessageBox.information(
       self,
       "À propos",
       "Covoiturage Daily\nApplication PyQt\nProjet SAE"
   )
