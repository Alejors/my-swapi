from flask import Flask, request, jsonify
from flask_migrate import Migrate
from .models import db, People, Planet, Vehicle, User, Profile, Favorite_characters, Favorite_planets
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

    expire = datetime.timedelta(hours=1)
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

@app.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile_consult_or_update():
    if request.method == 'GET':
        id = get_jwt_identity()
        current_user = Profile.query.get(id)

        return jsonify(current_user.serialize()), 200

    if request.method == 'PUT':
        id = get_jwt_identity()
        current_user = Profile.query.get(id)
        
        current_user.name = current_user.name if request.json.get('name') is None else request.json.get('name')
        current_user.lastname = current_user.lastname if request.json.get('lastname') is None else request.json.get('lastname')
        
        current_user.update()

        return jsonify({"msg": "Information updated"}), 200

@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    users_list = list(map(lambda user: user.serialize(), users))

    return jsonify(users_list),200

@app.route('/users/favorites', methods=['GET'])
@jwt_required()
def user_favorites():
    current_user = get_jwt_identity()
    usersProfile = Profile.query.get(current_user)
    data = {
        "favorite characters": usersProfile.get_fav_chars(),
        "favorite planets": usersProfile.get_fav_plans()
    }

    return jsonify({"msg":"Success", "data": data}),200

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

@app.route('/characters/<int:id>', methods=['GET'])
def list_single_character(id):
    
    character = People.query.get(id)

    return jsonify(character.serialize()), 200

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

        planet.save()

        return 'Planet registered', 200

@app.route('/planets/<int:id>', methods=['GET'])
def list_single_planet(id):
    
    planet = Planet.query.get(id)

    return jsonify(planet.serialize()), 200

@app.route('/planets/<int:id>', methods=['PUT'])
def update_planet(id):
    updatingplanet = Planet.query.get(id)
    
    updatingplanet.name = updatingplanet.name if request.json.get('name') is None else request.json.get('name')
    updatingplanet.picture = updatingplanet.picture if request.json.get('picture') is None else request.json.get('picture')
    updatingplanet.rotation_period = updatingplanet.rotation_period if request.json.get('rotation_period') is None else request.json.get('rotation_period')
    updatingplanet.orbital_period = updatingplanet.orbital_period if request.json.get('orbital_period') is None else request.json.get('orbital_period')
    updatingplanet.diameter = updatingplanet.diameter if request.json.get('diameter') is None else request.json.get('diameter')
    updatingplanet.climate = updatingplanet.climate if request.json.get('climate') is None else request.json.get('climate')
    updatingplanet.gravity = updatingplanet.gravity if request.json.get('gravity') is None else request.json.get('gravity')
    updatingplanet.terrain = updatingplanet.terrain if request.json.get('terrain') is None else request.json.get('terrain')
    updatingplanet.surface_water = updatingplanet.surface_water if request.json.get('surface_water') is None else request.json.get('surface_water')
    updatingplanet.population = updatingplanet.population if request.json.get('population') is None else request.json.get('population')
    updatingplanet.description = updatingplanet.description if request.json.get('description') is None else request.json.get('description')

    updatingplanet.update()

    return jsonify({"msg": "Information updated"})

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

        vehicle.save()

        return 'Vehicle registered', 200

@app.route('/vehicles/<int:id>', methods=['PUT'])
def update_vehicle(id):
    updatingvehicle = Vehicle.query.get(id)

    updatingvehicle.name = updatingvehicle.name if request.json.get('name') is None else request.json.get('name')
    updatingvehicle.picture = updatingvehicle.picture if request.json.get('picture') is None else request.json.get('picture')
    updatingvehicle.model = updatingvehicle.model if request.json.get('model') is None else request.json.get('model')
    updatingvehicle.manufacturer = updatingvehicle.manufacturer if request.json.get('manufacturer') is None else request.json.get('manufacturer')
    updatingvehicle.cost_in_credits = updatingvehicle.cost_in_credits if request.json.get('cost_in_credits') is None else request.json.get('cost_in_credits')
    updatingvehicle.length = updatingvehicle.length if request.json.get('length') is None else request.json.get('length')
    updatingvehicle.max_atmosphering_speed = updatingvehicle.max_atmosphering_speed if request.json.get('max_atmosphering_speed') is None else request.json.get('max_atmosphering_speed')
    updatingvehicle.crew = updatingvehicle.crew if request.json.get('crew') is None else request.json.get('crew')
    updatingvehicle.passengers = updatingvehicle.passengers if request.json.get('passengers') is None else request.json.get('passengers')
    updatingvehicle.cargo_capacity = updatingvehicle.cargo_capacity if request.json.get('cargo_capacity') is None else request.json.get('cargo_capacity')
    updatingvehicle.consumables = updatingvehicle.consumables if request.json.get('consumables') is None else request.json.get('consumables')
    updatingvehicle.vehicle_class = updatingvehicle.vehicle_class if request.json.get('vehicle_class') is None else request.json.get('vehicle_class')
    updatingvehicle.description = updatingvehicle.description if request.json.get('description') is None else request.json.get('description')

    updatingvehicle.update()

    return jsonify({"msg": "Information updated"})

@app.route('/favorite/people/<int:id>', methods=['POST', 'DELETE'])
@jwt_required()
def add_or_delete_favorite_character(id):
    if request.method == 'POST':
        current_user = get_jwt_identity()
        usersProfile = Profile.query.get(current_user)

        favorite = Favorite_characters()
        favorite.character_id = id
        favorite.profile_id = usersProfile.id
        favorite.save()

        return jsonify({"msg":"insertion ok"})
    
    if request.method == 'DELETE':
        current_user = get_jwt_identity()
        usersProfile = Profile.query.get(current_user)

        favorites = Favorite_characters.query.filter_by(profile_id = usersProfile.id, character_id = id).first()
        favorites.delete()

        return "favorite deleted"

@app.route('/favorite/planets/<int:id>', methods=['POST', 'DELETE'])
@jwt_required()
def add_or_delete_favorite_planet(id):
    if request.method == 'POST':
        current_user = get_jwt_identity()
        usersProfile = Profile.query.get(current_user)

        favorite = Favorite_planets()
        favorite.planet_id = id
        favorite.profile_id = usersProfile.id
        favorite.save()

        return jsonify({"msg":"insertion ok"})
    
    if request.method == 'DELETE':
        current_user = get_jwt_identity()
        usersProfile = Profile.query.get(current_user)

        favorites = Favorite_planets.query.filter_by(profile_id = usersProfile.id, planet_id = id).first()
        favorites.delete()

        return "favorite deleted"

if __name__ == "__main__":
    app.run()