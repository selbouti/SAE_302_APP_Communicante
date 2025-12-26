from flask import Flask
from config.database import get_connection
from controllers.gestion_res_controller import ReservationController

def create_app():
    """
    Crée et configure l'application Flask.
    """
    app = Flask(__name__)

    # Configuration de la base de données
    db_connection = get_connection()

    # Enregistrement des contrôleurs
    ReservationController(app, db_connection)

    return app

def main():
    """
    Point d'entrée principal de l'application.
    """
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
