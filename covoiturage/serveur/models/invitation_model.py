from core.database import Database

class InvitationModel:
    @staticmethod
    def create(trajet_id, passager_id):
        query = '''INSERT INTO invitations (trajet_id, passager_id, statut)
                   VALUES (?, ?, 'en_attente')'''
        inv_id = Database.insert(query, (trajet_id, passager_id))
        return inv_id
    
    @staticmethod
    def get_invitations_received(passager_id):
        query = '''SELECT i.id, i.trajet_id, i.statut, i.created_at,
                   t.depart, t.arrivee, t.date_depart, t.heure_depart, t.prix_par_place,
                   u.nom, u.prenom, u.email, u.telephone
                   FROM invitations i
                   JOIN trajets t ON i.trajet_id = t.id
                   JOIN utilisateurs u ON t.utilisateur_id = u.id
                   WHERE i.passager_id = ?'''
        invs = Database.execute(query, (passager_id,))
        return [dict(i) for i in invs]

    @staticmethod
    def get_invitations_sent(conducteur_id):
        """Invitations que j'ai envoyées (je suis conducteur)"""
        query = '''SELECT i.id, i.trajet_id, i.statut, i.created_at,
                   t.depart, t.arrivee, t.date_depart, t.heure_depart,
                   u.nom, u.prenom, u.email, u.telephone
                   FROM invitations i
                   JOIN trajets t ON i.trajet_id = t.id
                   JOIN utilisateurs u ON i.passager_id = u.id
                   WHERE t.utilisateur_id = ? AND t.mode = 'conducteur'
                   ORDER BY i.created_at DESC'''
        invs = Database.execute(query, (conducteur_id,))
        return [dict(i) for i in invs]
    
    @staticmethod
    def accepter(invitation_id):
        Database.execute('UPDATE invitations SET statut = ? WHERE id = ?', ('acceptee', invitation_id))
    
    @staticmethod
    def refuser(invitation_id):
        Database.execute('UPDATE invitations SET statut = ? WHERE id = ?', ('refusee', invitation_id))