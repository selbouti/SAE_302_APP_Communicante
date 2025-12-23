# controllers/user_controller.py

from __future__ import annotations

from datetime import date, timedelta
from models.user_model import UserModel
from models.voiture_model import VoitureModel
from models.disponibilite_model import DisponibiliteModel
from models.edt_model import EDTModel
from services.edt_parser import EDTParser


class UserController:
    """
    Logique métier liée aux utilisateurs :
    - connexion / déconnexion
    - inscription (avec voiture + EDT)
    - navigation
    - gestion profil / voiture
    - import / mise à jour EDT
    - génération des disponibilités à partir de l'EDT
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
        self.main.show_edt_import_page()

    def go_profile(self):
        self.main.show_profile_page()

    def go_voiture(self):
        self.main.show_voiture_page()

    def go_dispo(self):
        self.main.show_dispo_page()

    # =========================
    #   AUTHENTIFICATION
    # =========================
    def login(self, login, password) -> bool:
        user = self.user_model.authenticate(login, password)
        if user:
            self.current_user = user
            self.go_home()
            return True

        self.main.show_error("Identifiants incorrects.")
        return False

    def logout(self):
        self.current_user = None
        self.main.show_message("Vous avez été déconnecté.")
        self.go_login()

    # =========================
    #   INSCRIPTION
    # =========================
    def register(self, user_data, car_data=None, edt_source=None) -> bool:
        """
        edt_source: ('file', path) ou ('url', url) ou None
        """
        try:
            user_id = self.user_model.create_user(user_data)
            if not user_id:
                self.main.show_error("Impossible de créer l'utilisateur.")
                return False

            if car_data:
                self.voiture_model.add_voiture(user_id, car_data)

            if edt_source:
                source_type, value = edt_source
                if source_type == "file":
                    cal = self.edt_parser.load_from_file(value)
                    self.edt_model.save_edt_file(user_id, value)
                    # Optionnel : pré-calculer des dispos à l'inscription
                    # (si tu veux éviter une base vide dès le début)
                    # self._recompute_all_disponibilites(cal, user_id=user_id)

                elif source_type == "url":
                    cal = self.edt_parser.load_from_url(value)
                    self.edt_model.save_edt_url(user_id, value)
                    # self._recompute_all_disponibilites(cal, user_id=user_id)

            self.main.show_message("Compte créé avec succès.")
            self.go_login()
            return True

        except Exception as e:
            print("Erreur inscription:", e)
            self.main.show_error("Erreur lors de l'inscription.")
            return False

    # =========================
    #   PROFIL
    # =========================
    def update_profile(self, data):
        if not self.current_user:
            self.main.show_error("Aucun utilisateur connecté.")
            return

        self.user_model.update_user(self.current_user["id_user"], data)
        self.main.show_message("Profil mis à jour.")

    # =========================
    #   VOITURE
    # =========================
    def save_voiture(self, data):
        if not self.current_user:
            self.main.show_error("Aucun utilisateur connecté.")
            return

        user_id = self.current_user["id_user"]
        voiture = self.voiture_model.get_user_voiture(user_id)

        try:
            if voiture:
                self.voiture_model.update_voiture(voiture["id_voiture"], data)
                self.main.show_message("Voiture mise à jour.")
            else:
                self.voiture_model.add_voiture(user_id, data)
                self.main.show_message("Voiture ajoutée.")
        except Exception as e:
            print("Erreur save_voiture:", e)
            self.main.show_error("Erreur lors de l'enregistrement de la voiture.")

    def delete_voiture(self):
        if not self.current_user:
            self.main.show_error("Aucun utilisateur connecté.")
            return

        voiture = self.voiture_model.get_user_voiture(self.current_user["id_user"])
        if not voiture:
            self.main.show_error("Aucune voiture enregistrée.")
            return

        try:
            self.voiture_model.delete_voiture(voiture["id_voiture"])
            self.main.show_message("Voiture supprimée.")
        except Exception as e:
            print("Erreur delete_voiture:", e)
            self.main.show_error("Erreur lors de la suppression de la voiture.")

    # =========================
    #   IMPORT / MISE À JOUR EDT
    # =========================
    def import_edt_file(self, file_path):
        """
        Met à jour l'EDT (remplace l'ancien) + recalcul dispo automatique.
        """
        if not self.current_user:
            self.main.show_error("Aucun utilisateur connecté.")
            return

        user_id = self.current_user["id_user"]

        try:
            cal = self.edt_parser.load_from_file(file_path)

            # IMPORTANT : save_edt_file doit remplacer l'ancien EDT côté DB
            self.edt_model.save_edt_file(user_id, file_path)

            # Recalcul dispo (évite matching faussé)
            self._recompute_all_disponibilites(cal, user_id=user_id, days_ahead=7)

            self.main.show_message("Emploi du temps mis à jour (fichier).")
        except Exception as e:
            print("Erreur import_edt_file:", e)
            self.main.show_error("Erreur lors de l'import du fichier EDT.")

    def import_edt_url(self, url):
        """
        Met à jour l'EDT (remplace l'ancien) + recalcul dispo automatique.
        """
        if not self.current_user:
            self.main.show_error("Aucun utilisateur connecté.")
            return

        user_id = self.current_user["id_user"]

        try:
            cal = self.edt_parser.load_from_url(url)

            # IMPORTANT : save_edt_url doit remplacer l'ancien EDT côté DB
            self.edt_model.save_edt_url(user_id, url)

            # Recalcul dispo (évite matching faussé)
            self._recompute_all_disponibilites(cal, user_id=user_id, days_ahead=7)

            self.main.show_message("Emploi du temps mis à jour (URL).")
        except Exception as e:
            print("Erreur import_edt_url:", e)
            self.main.show_error("Erreur lors du téléchargement de l'EDT.")

    def _recompute_all_disponibilites(self, calendar_obj, user_id: int, days_ahead: int = 7):
        """
        Recalcule toutes les disponibilités pour les N prochains jours à partir de l'EDT.
        - Supprime puis régénère les dispos pour chaque jour.
        """
        for i in range(days_ahead):
            day = date.today() + timedelta(days=i)

            events = self.edt_parser.extract_events_for_day(calendar_obj, day)

            # Nettoyage
            self.dispo_model.clear_user_dispos(user_id, day)

            # Calcul
            dispos = self.edt_parser.compute_disponibilites(events)

            # Sauvegarde
            for debut, fin in dispos:
                self.dispo_model.add_dispo(user_id, day, debut, fin)

    # =========================
    #   DISPONIBILITÉS (À LA DEMANDE)
    # =========================
    def generate_disponibilites_from_edt(self, date_dispo: date):
        """
        Génère les disponibilités d'un jour donné à partir de l'EDT enregistré en base.
        Utile quand l'utilisateur choisit une date dans la page 'Disponibilités'.
        """
        if not self.current_user:
            self.main.show_error("Aucun utilisateur connecté.")
            return

        user_id = self.current_user["id_user"]

        try:
            edt = self.edt_model.get_edt(user_id)
            if not edt:
                self.main.show_error("Aucun emploi du temps enregistré.")
                return

            if edt["source_type"] == "fichier":
                cal = self.edt_parser.load_from_file(edt["source"])
            else:
                cal = self.edt_parser.load_from_url(edt["source"])

            events = self.edt_parser.extract_events_for_day(cal, date_dispo)

            # Nettoyage anciennes dispos de ce jour
            self.dispo_model.clear_user_dispos(user_id, date_dispo)

            # Calcul + sauvegarde
            dispos = self.edt_parser.compute_disponibilites(events)
            for debut, fin in dispos:
                self.dispo_model.add_dispo(user_id, date_dispo, debut, fin)

            self.main.show_message("Disponibilités générées pour la date sélectionnée.")
        except Exception as e:
            print("Erreur generate_disponibilites_from_edt:", e)
            self.main.show_error("Erreur lors de la génération des disponibilités.")
