from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, People, Planet, Vehicle, User, Profile
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_swapi.db'
app.config['JWT_SECRET_KEY'] = '73eeac3fa1a0ce48f381ca1e6d71f077'

db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)

@app.route('/', methods=['GET'])
def intro():
    return """
    <h1>My own SWAPI</h1>
    <p>Look inside 
        <ul>
            <li><a href='/characters'>Characters</a></li>
            <li><a href='/vehicles'>Vehicles</a></li>
            <li><a href='/planets'>Planets</a></li>
        </ul>
    </p>
    """

@app.route('/login', methods=['POST'])
def login():
    incomingUsername = request.json.get('username')
    incomingPassword = request.json.get('password')

    if not incomingUsername: return jsonify({"msg": "Username required"}), 400
    if not incomingPassword: return jsonify({"msg": "Password required"}), 400

    thisUser = User.query.filter_by(username=incomingUsername, is_active=True).first()

    if not thisUser: return jsonify({"msg": "Failed: username/password incorrect"}), 401
    if not check_password_hash(thisUser.password, incomingPassword): return jsonify({"msg": "Failed: username/password incorrect"}), 401

    expire = datetime.timedelta(hours=3)
    access_token = create_access_token(identity=thisUser.id, expires_delta=expire)

    data = {
        "access token": access_token,
        "user": thisUser.serialize()
    }

    return jsonify({"status": "All good!", "message": "Logged in", "data": data}), 200


@app.route('/register', methods=['POST'])
def register():
    incomingUsername = request.json.get('username')
    incomingPassword = request.json.get('password')

    if not incomingUsername: return jsonify({"warning": "Username required!"}), 400
    if not incomingPassword: return jsonify({"warning": "Password required!"}), 400

    newuser = User()
    newuser.username = incomingUsername
    newuser.password = generate_password_hash(incomingPassword)
    
    newprofile = Profile()
    newuser.profile = newprofile

    newuser.save()

    if newuser:
        return jsonify({"status": "Done", "message": "Regitration succesful"}), 200
    else:
        return jsonify({"status": "Incomplete", "message": "Registration failed, try again."}), 400

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    id = get_jwt_identity()
    current_user = User.query.get(id)

    return jsonify(current_user.serialize()), 200

@app.route('/characters', methods=['GET', 'POST'])
def list_and_create_people():
    if request.method == 'GET':
        people = People.query.all()
        people = list(map(lambda peop: peop.serialize(), people))

        return jsonify(people), 200

    if request.method == 'POST':
        incoming_data = request.get_json()

        people = People()
        people.name = incoming_data['name']
        people.picture = incoming_data['picture']
        people.height = incoming_data['height']
        people.mass = incoming_data['mass']
        people.hair_color = incoming_data['hair_color']
        people.skin_color = incoming_data['skin_color']
        people.eye_color = incoming_data['eye_color']
        people.birth_year = incoming_data['birth_year']
        people.gender = incoming_data['gender']
        people.planet_id = incoming_data['planet_id']
        people.description = incoming_data['description']
        people.save()

        return 'Character registered'

@app.route('/characters/<int:id>', methods=['PUT'])
def update_character(id):
    updating_char = People.query.get(id)
    
    updating_char.name = updating_char.name if request.json.get('name') is None else request.json.get('name')
    updating_char.picture = updating_char.picture if request.json.get('picture') is None else request.json.get('picture')
    updating_char.height = updating_char.height if request.json.get('height') is None else request.json.get('height')
    updating_char.mass = updating_char.mass if request.json.get('mass') is None else updating_char.mass
    updating_char.hair_color = updating_char.hair_color if request.json.get('hair_color') is None else request.json.get('hair_color')
    updating_char.skin_color = updating_char.skin_color if request.json.get('skin_color') is None else request.json.get('skin_color')
    updating_char.eye_color = updating_char.eye_color if request.json.get('eye_color') is None else request.json.get('eye_color')
    updating_char.birth_year = updating_char.birth_year if request.json.get('birth_year') is None else request.json.get('birth_year')
    updating_char.gender = updating_char.gender if request.json.get('gender') is None else request.json.get('gender')
    updating_char.planet_id = updating_char.planet_id if request.json.get('planet_id') is None else request.json.get('planet_id')
    updating_char.description = updating_char.description if request.json.get('description') is None else request.json.get('description')

    updating_char.update()
    
    return jsonify({"msg": "Information updated"})

@app.route('/planets', methods=['GET', 'POST'])
def list_and_create_planets():
    if request.method == 'GET':
        planets = Planet.query.all()
        planets = list(map(lambda planet: planet.serialize(), planets))

        return jsonify(planets), 200


    if request.method == 'POST':
        incoming_data = request.get_json()

        planet = Planet()
        planet.name = incoming_data['name']
        planet.picture = incoming_data['picture']
        planet.rotation_period = incoming_data['rotation_period']
        planet.orbital_period = incoming_data['orbital_period']
        planet.diameter = incoming_data['diameter']
        planet.climate = incoming_data['climate']
        planet.gravity = incoming_data['gravity']
        planet.terrain = incoming_data['terrain']
        planet.surface_water = incoming_data['surface_water']
        planet.population = incoming_data['population']
        planet.description = incoming_data['description']

        db.session.add(planet)
        db.session.commit()

        return 'Planet registered', 200

@app.route('/vehicles', methods=['GET', 'POST'])
def list_and_create_vehicles():
    if request.method == 'GET':
        vehicles = Vehicle.query.all()
        vehicles = list(map(lambda vehicle: vehicle.serialize(), vehicles))

        return jsonify(vehicles), 200


    if request.method == 'POST':
        incoming_data = request.get_json()

        vehicle = Vehicle()
        vehicle.name = incoming_data['name']
        vehicle.picture = incoming_data['picture']
        vehicle.model = incoming_data['model']
        vehicle.manufacturer = incoming_data['manufacturer']
        vehicle.cost_in_credits = incoming_data['cost_in_credits']
        vehicle.length = incoming_data['length']
        vehicle.max_atmosphering_speed = incoming_data['max_atmosphering_speed']
        vehicle.crew = incoming_data['crew']
        vehicle.passengers = incoming_data['passengers']
        vehicle.cargo_capacity = incoming_data['cargo_capacity']
        vehicle.consumables = incoming_data['consumables']
        vehicle.vehicle_class = incoming_data['vehicle_class']
        vehicle.description = incoming_data['description']

        db.session.add(vehicle)
        db.session.commit()

        return 'Vehicle registered', 200

if __name__ == "__main__":
    app.run()