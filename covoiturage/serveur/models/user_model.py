from core.database import Database
import hashlib


class UserModel:
    """
    Database model for user management.

    This class provides methods to create users, authenticate them,
    and retrieve user information from the database.
    Passwords are stored using SHA-256 hashing.
    """

    @staticmethod
    def create(email, password, nom, prenom, telephone):
        """
        Create a new user in the database.

        The password is hashed using SHA-256 before being stored.

        :param email: User email address
        :type email: str
        :param password: Plain text password
        :type password: str
        :param nom: User last name
        :type nom: str
        :param prenom: User first name
        :type prenom: str
        :param telephone: User phone number
        :type telephone: str
        :return: Dictionary containing user ID and email, or None if creation fails
        :rtype: dict | None
        """
        try:
            query = '''INSERT INTO utilisateurs (email, password, nom, prenom, telephone)
                       VALUES (?, ?, ?, ?, ?)'''
            user_id = Database.insert(
                query,
                (
                    email,
                    hashlib.sha256(password.encode()).hexdigest(),
                    nom,
                    prenom,
                    telephone
                )
            )
            return {'id': user_id, 'email': email}
        except Exception:
            return None

    @staticmethod
    def get_by_email(email, password):
        """
        Retrieve a user using email and password.

        The password is hashed before being compared with the database.

        :param email: User email address
        :type email: str
        :param password: Plain text password
        :type password: str
        :return: User data dictionary or None if authentication fails
        :rtype: dict | None
        """
        query = '''SELECT id, email, nom, prenom FROM utilisateurs
                   WHERE email=? AND password=?'''
        user = Database.execute_one(
            query,
            (
                email,
                hashlib.sha256(password.encode()).hexdigest()
            )
        )
        return dict(user) if user else None

    @staticmethod
    def get_by_id(user_id):
        """
        Retrieve a user by its unique identifier.

        :param user_id: User identifier
        :type user_id: int
        :return: User data dictionary or None if user does not exist
        :rtype: dict | None
        """
        query = 'SELECT id, email, nom, prenom, telephone FROM utilisateurs WHERE id=?'
        user = Database.execute_one(query, (user_id,))
        return dict(user) if user else None
