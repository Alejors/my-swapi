from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    profile = db.relationship("Profile", backref="user", uselist=False)

    def serialize(self):
        return{
            'id': self.id,
            'username': self.username,
            'is active': self.is_active
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="unknown")
    lastname = db.Column(db.String(100), default="unknown")
    fav_char = db.relationship('People', secondary="favorite_characters")
    fav_plan = db.relationship("Planet", secondary="favorite_planets")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def get_fav_chars(self):
        return (list(map(lambda char: char.name, self.fav_char)))

    def get_fav_plans(self):
        return (list(map(lambda plan: plan.name, self.fav_plan)))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "user id": self.user_id,
            "username": self.user.username,
            "active": self.user.is_active,
            "liked characters": self.get_fav_chars(),
            "liked planets": self.get_fav_plans()
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Favorite_characters(db.Model):
    __tablename__ = 'favorite_characters'
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), primary_key=True) 
    character_id = db.Column(db.Integer, db.ForeignKey('people.id'), primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Favorite_planets(db.Model):
    __tablename__ = 'favorite_planets'
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), primary_key=True) 
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    picture = db.Column(db.String(250), default="https://dummyimage.com/300X200/dbdbdb/000")
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(100))
    skin_color = db.Column(db.String(100))
    eye_color = db.Column(db.String(100))
    birth_year = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), default="")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "height": self.height,
            "mass": self.mass,
            "hair color": self.hair_color,
            "skin color": self.skin_color,
            "eye color": self.eye_color,
            "birth year": self.birth_year,
            "gender": self.gender,
            "picture": self.picture,
            "homeplanet": "unknown" if self.planet is None else self.planet.name
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique = True, default="unknown")
    description = db.Column(db.Text)
    picture = db.Column(db.String(250), default="https://dummyimage.com/300X200/dbdbdb/000")
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    climate = db.Column(db.String(100), default="unknown")
    gravity = db.Column(db.String(100), default="unknown")
    terrain = db.Column(db.String(100), default="unknown")
    surface_water = db.Column(db.Integer)
    population = db.Column(db.Integer)
    characters_born = db.relationship('People', backref='planet')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "rotation period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface water": self.surface_water,
            "population": self.population,
            "picture": self.picture
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    picture = db.Column(db.String(250), default="https://dummyimage.com/300X200/dbdbdb/000")
    model = db.Column(db.String(100), unique=True)
    manufacturer = db.Column(db.String(100))
    cost_in_credits = db.Column(db.Integer)
    length = db.Column(db.Float)
    max_atmosphering_speed = db.Column(db.Integer)
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    cargo_capacity = db.Column(db.Integer)
    consumables = db.Column(db.String(100))
    vehicle_class = db.Column(db.String(100))
    # users_liked = db.relationship("Profile", secondary="favorite_vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "picture": self.picture,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost in credits": self.cost_in_credits,
            "length": self.length,
            "max atmosphering speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "vehicle class": self.vehicle_class
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
