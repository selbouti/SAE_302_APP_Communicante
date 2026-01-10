from flask import Flask
from flask_cors import CORS
from config_db.database import init_db

app = Flask(__name__)
CORS(app)

from controllers.user_controller import user_bp
from controllers.voiture_controller import voiture_bp
from controllers.trajet_controller import trajet_bp
from controllers.matching_controller import matching_bp
from controllers.reservation_controller import reservation_bp
from controllers.invitation_controller import invitation_bp
from controllers.profile_controller_api import profile_api   

app.register_blueprint(user_bp)
app.register_blueprint(voiture_bp)
app.register_blueprint(trajet_bp)
app.register_blueprint(matching_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(invitation_bp)
app.register_blueprint(profile_api)                       

if __name__ == '__main__':
    """
    Entry point of the Flask application.

    This script initializes the database, sets up the Flask application, and starts the server.
    The application uses Flask blueprints to modularize the API endpoints.

    Modules:
        - user_controller: Manages user-related operations.
        - voiture_controller: Handles car-related operations.
        - trajet_controller: Manages trip-related operations.
        - matching_controller: Handles trip matching logic.
        - reservation_controller: Manages reservation-related operations.
        - invitation_controller: Handles invitation-related operations.
        - profile_controller_api: Manages user profile operations.

    Features:
        - CORS (Cross-Origin Resource Sharing) is enabled for the application.
        - The database is initialized before the server starts.

    Server:
        - Runs on `127.0.0.1` (localhost) at port `5000`.
        - Debug mode is enabled for development purposes.
    """
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)
