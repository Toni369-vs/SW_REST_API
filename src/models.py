from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites_user = db.relationship("Favorites", backref="users")
    

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            
        }
    

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"))
    planetID = db.Column(db.Integer, db.ForeignKey("planets.planetID"))
    characterID = db.Column(db.Integer, db.ForeignKey("people.characterID"))
   
    

    def serialize(self):
        return {
            "id": self.id,
            "userID": self.userID,
            "planetID": self.planetID,
            "characterID": self.characterID
        }

              


# TABLAS STAR WARS   


class People(db.Model):
    characterID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    eyed_color = db.Column(db.String(80), nullable = False)
    birth_year = db.Column(db.String(80), nullable = False)
    height = db.Column(db.Integer, nullable = False)
    mass = db.Column(db.Integer, nullable = False)
    url = db.Column(db.String(200), nullable = False)
    homeworld = db.Column(db.String(200), nullable = False)
    favorites_people = db.relationship("Favorites", backref="people")

    def __repr__(self):
        return '<People %r>' % self.characterID


    def serialize(self):
        return {
            'characterID' : self.characterID,
            'name' : self.name,
            'eyed_color' : self.eyed_color,
            'birth_year' : self.birth_year,
            'height' : self.height,
            'mass' : self.mass,
            'url' : self.url,
            'homeworld' : self.homeworld
        }    



class Planets(db.Model):
    planetID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    rotated_period  = db.Column(db.String(80), nullable = False)
    diameter = db.Column(db.Integer, nullable = False)
    climate = db.Column(db.String(80), nullable = False)
    orbital_period = db.Column(db.Integer, nullable = False)
    url = db.Column(db.String(200), nullable = False)
    favorites_planets = db.relationship("Favorites", backref="planets")

    def __repr__(self):
        return '<Planets %r>' % self.planetID
    
    def serialize(self):
        return {
            'planetID' : self.planetID,
            'name': self.name,
            'rotated_period' : self.rotated_period,
            'diameter': self.diameter,
            'climate': self.climate,
            'orbital_period': self.orbital_period, 
        }
    


