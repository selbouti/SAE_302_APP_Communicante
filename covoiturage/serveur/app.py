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
from controllers.profile_controller_api import profile_api   # ✅ AJOUT

app.register_blueprint(user_bp)
app.register_blueprint(voiture_bp)
app.register_blueprint(trajet_bp)
app.register_blueprint(matching_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(invitation_bp)
app.register_blueprint(profile_api)                       # ✅ AJOUT

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)
