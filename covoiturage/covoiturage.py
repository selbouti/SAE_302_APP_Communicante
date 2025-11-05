# nom_projet.py
"""
Application graphique de covoiturage
Auteur : Ton Nom
Date : 2025-11-05
"""

import sys
from PyQt5.QtWidgets import QApplication
from vue import FenetrePrincipale

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetrePrincipale()
    fenetre.show()
    sys.exit(app.exec_())
