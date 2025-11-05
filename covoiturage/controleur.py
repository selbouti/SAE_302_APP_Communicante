# controleur.py
from modele import ModeleUtilisateurs

class ControleurApp:
    """Relie la vue et le modèle."""
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.modele = ModeleUtilisateurs()

    def aller_connexion(self):
        self.fenetre.setCurrentWidget(self.fenetre.page_connexion)

    def aller_inscription(self):
        self.fenetre.setCurrentWidget(self.fenetre.page_inscription)

    def aller_accueil(self):
        self.fenetre.setCurrentWidget(self.fenetre.page_accueil)

    def connexion_valide(self, login, mdp):
        return self.modele.verifier_connexion(login, mdp)

    def enregistrer_utilisateur(self, infos):
        return self.modele.ajouter_utilisateur(infos)
