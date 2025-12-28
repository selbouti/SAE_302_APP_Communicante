from core.database import Database
import hashlib

class UserModel:
    @staticmethod
    def create(email, password, nom, prenom, telephone):
        try:
            query = '''INSERT INTO utilisateurs (email, password, nom, prenom, telephone)
                       VALUES (?, ?, ?, ?, ?)'''
            user_id = Database.insert(query, (email, hashlib.sha256(password.encode()).hexdigest(), 
                                              nom, prenom, telephone))
            return {'id': user_id, 'email': email}
        except:
            return None
    
    @staticmethod
    def get_by_email(email, password):
        query = '''SELECT id, email, nom, prenom FROM utilisateurs 
                   WHERE email=? AND password=?'''
        user = Database.execute_one(query, (email, hashlib.sha256(password.encode()).hexdigest()))
        return dict(user) if user else None
    
    @staticmethod
    def get_by_id(user_id):
        query = 'SELECT id, email, nom, prenom, telephone FROM utilisateurs WHERE id=?'
        user = Database.execute_one(query, (user_id,))
        return dict(user) if user else None