from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, People, Planet, Vehicle

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_swapi.db'

db.init_app(app)
Migrate(app, db)

@app.route('/', methods=['GET'])
def intro():
    return """
    <h1>My own SWAPI</h1>
    <p>Look inside 
        <ul>
            <li><a href='/characters'>characters</a></li>
            <li><a href='/planets'>planets</a></li>
            <li><a href='/vehicles'>vehicles</a></li>
        </ul>
    </p>
    """

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

        db.session.add(people)
        db.session.commit()

        return 'Character registered'

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

        db.session.add(vehicle)
        db.session.commit()

        return 'Vehicle registered', 200

if __name__ == "__main__":
    app.run()