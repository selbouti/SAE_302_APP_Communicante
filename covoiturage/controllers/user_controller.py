# controllers/user_controller.py

from models.user_model import UserModel
from models.voiture_model import VoitureModel
from models.disponibilite_model import DisponibiliteModel
from models.edt_model import EDTModel
from services.edt_parser import EDTParser


class UserController:
    """
    Logique métier liée aux utilisateurs :
    - connexion
    - inscription (avec voiture + EDT)
    - navigation
    - gestion du profil, voitures, indisponibilités
    - mise à jour EDT
    """

    def __init__(self, main_window):
        self.main = main_window
        self.user_model = UserModel()
        self.voiture_model = VoitureModel()
        self.dispo_model = DisponibiliteModel()
        self.edt_model = EDTModel()
        self.edt_parser = EDTParser()

        self.current_user = None

    # =========================
    #   NAVIGATION
    # =========================
    def go_login(self):
        self.main.show_login_page()

    def go_register(self):
        self.main.show_register_page()

    def go_home(self):
        self.main.show_home_page()

    def go_edt_import(self):
        """Afficher la page de mise à jour EDT."""
        self.main.show_edt_import_page()

    # =========================
    #   AUTHENTIFICATION
    # =========================
    def login(self, login, password) -> bool:
        user = self.user_model.authenticate(login, password)
        if user:
            self.current_user = user
            self.go_home()
            return True
        else:
            self.main.show_error("Identifiants incorrects.")
            return False

    # =========================
    #   INSCRIPTION (COMPLÈTE)
    # =========================
    def register(self, user_data: dict, car_data: dict | None, edt_source: tuple | None) -> bool:
        """
        user_data : données utilisateur
        car_data  : données voiture ou None
        edt_source: ('file', path) ou ('url', url) ou None
        """
        try:
            # 1️⃣ Création utilisateur
            user_id = self.user_model.create_user(user_data)
            if not user_id:
                self.main.show_error("Impossible de créer l'utilisateur.")
                return False

            # 2️⃣ Création voiture si existante
            if car_data:
                self.voiture_model.add_voiture(user_id, car_data)

            # 3️⃣ Import EDT si fourni
            if edt_source:
                source_type, value = edt_source

                if source_type == "file":
                    self.edt_parser.load_from_file(value)
                    self.edt_model.save_edt_file(user_id, value)

                elif source_type == "url":
                    self.edt_parser.load_from_url(value)
                    self.edt_model.save_edt_url(user_id, value)

            # 4️⃣ Fin
            self.main.show_message("Compte créé avec succès.")
            self.go_login()
            return True

        except Exception as e:
            print("Erreur lors de l'inscription :", e)
            self.main.show_error("Erreur lors de l'inscription.")
            return False

    # =========================
    #   PROFIL / VOITURE / INDISPO
    # =========================
    def update_profile(self, data):
        if not self.current_user:
            self.main.show_error("Aucun utilisateur connecté.")
            return
        self.user_model.update_user(self.current_user["id_user"], data)
        self.main.show_message("Profil mis à jour.")

    # =========================
    #   VOITURE (AJOUT / MAJ / SUPPRESSION)
    # =========================
    def save_voiture(self, data):
        """
        Ajoute ou met à jour la voiture de l'utilisateur connecté.
        """
        if not self.current_user:
            self.main.show_error("Aucun utilisateur connecté.")
            return

        user_id = self.current_user["id_user"]
        voiture = self.voiture_model.get_user_voiture(user_id)

        if voiture:
            self.voiture_model.update_voiture(voiture["id_voiture"], data)
            self.main.show_message("Voiture mise à jour.")
        else:
            self.voiture_model.add_voiture(user_id, data)
            self.main.show_message("Voiture ajoutée.")

    def delete_voiture(self):
        """
        Supprime la voiture de l'utilisateur connecté.
        """
        if not self.current_user:
            self.main.show_error("Aucun utilisateur connecté.")
            return

        voiture = self.voiture_model.get_user_voiture(self.current_user["id_user"])
        if not voiture:
            self.main.show_error("Aucune voiture enregistrée.")
            return

        self.voiture_model.delete_voiture(voiture["id_voiture"])
        self.main.show_message("Voiture supprimée.")

    def add_indispo(self, data):
        if not self.current_user:
            self.main.show_error("Aucun utilisateur connecté.")
            return
        self.dispo_model.add_indispo(self.current_user["id_user"], data)
        self.main.show_message("Indisponibilité ajoutée.")

    def delete_indispo(self, dispo_id):
        self.dispo_model.delete_indispo(dispo_id)
        self.main.show_message("Indisponibilité supprimée.")

    # =========================
    #   MISE À JOUR EDT (POST-INSCRIPTION)
    # =========================
    def import_edt_file(self, file_path):
        try:
            self.edt_parser.load_from_file(file_path)
            self.edt_model.save_edt_file(self.current_user["id_user"], file_path)
            self.main.show_message("Emploi du temps mis à jour.")
        except Exception as e:
            print("Erreur EDT fichier :", e)
            self.main.show_error("Erreur lors de l'import du fichier EDT.")

    def import_edt_url(self, url):
        try:
            self.edt_parser.load_from_url(url)
            self.edt_model.save_edt_url(self.current_user["id_user"], url)
            self.main.show_message("Emploi du temps mis à jour.")
        except Exception as e:
            print("Erreur EDT URL :", e)
            self.main.show_error("Erreur lors du téléchargement de l'EDT.")


    # =========================
    #   DÉCONNEXION
    # =========================
    def logout(self):
        """
        Déconnecte l'utilisateur et retourne à la page de login.
        """
        self.current_user = None
        self.main.show_message("Vous avez été déconnecté.")
        self.go_login()

    # =========================
    #   NAVIGATION COMPLÉMENTAIRE
    # =========================
    def go_profile(self):
        """Afficher la page de gestion du profil."""
        self.main.show_profile_page()

    def go_voiture(self):
        """Afficher la page de gestion de la voiture."""
        self.main.show_voiture_page()
    