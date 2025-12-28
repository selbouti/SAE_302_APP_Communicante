from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from models.trajet_model import TrajetModel
from services.icalendar_parser import ICalendarParser
from werkzeug.utils import secure_filename

user_bp = Blueprint('user', __name__, url_prefix='/api')

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    result = UserModel.create(data['email'], data['password'], data['nom'], 
                              data['prenom'], data.get('telephone', ''))
    return jsonify(result) if result else jsonify({'error': 'Email déjà utilisé'}), (201 if result else 400)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = UserModel.get_by_email(data['email'], data['password'])
    return jsonify(user), (200 if user else 401)

@user_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = UserModel.get_by_id(user_id)
    return jsonify(user), (200 if user else 404)

@user_bp.route('/upload_icalendar/<int:user_id>', methods=['POST'])
def upload_icalendar(user_id):
    """Upload fichier iCalendar et crée les trajets"""
    if 'file' not in request.files:
        return jsonify({'error': 'Pas de fichier'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Fichier vide'}), 400
    
    try:
        ics_content = file.read()
        trajets_data = ICalendarParser.parse_events(ics_content)
        
        trajets_created = []
        for t in trajets_data:
            if t['dtstart']:
                trajet_id = TrajetModel.create(
                    utilisateur_id=user_id,
                    depart=t['summary'].split(' - ')[0] if ' - ' in t['summary'] else 'Départ',
                    arrivee=t['summary'].split(' - ')[1] if ' - ' in t['summary'] else 'Arrivée',
                    date_depart=t['dtstart'].strftime('%Y-%m-%d'),
                    jour_semaine=t['dtstart'].strftime('%A'),
                    heure_depart=t['dtstart'].strftime('%H:%M'),
                    places_totales=4,
                    prix_par_place=5.0,
                    mode='conducteur'  # Par défaut conducteur
                )
                trajets_created.append(trajet_id)
        
        return jsonify({'success': True, 'trajets_created': len(trajets_created)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400