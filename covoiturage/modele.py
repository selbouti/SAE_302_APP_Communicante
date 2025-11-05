# modele.py
class ModeleUtilisateurs:
    """Gère les utilisateurs (simulation mémoire, remplaçable par une base de données)."""
    def __init__(self):
        self.utilisateurs = {}

    def ajouter_utilisateur(self, infos):
        login = infos["login"]
        if login in self.utilisateurs:
            return False
        self.utilisateurs[login] = infos
        return True

    def verifier_connexion(self, login, mdp):
        utilisateur = self.utilisateurs.get(login)
        if utilisateur and utilisateur["mdp"] == mdp:
            return True
        return False
