"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ENDPOINTS

# OBTENER USER DEL BLOG


@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users_query = User.query.all()
        results = list(map(lambda item: item.serialize(), users_query))

        response_body = {
            "msg": "all users",
            "results": results
        }

        return jsonify(response_body), 200

    except:
        raise APIException('Personaje no encontrado', 404)


# OBTENER ALL PEOPLE

@app.route('/People', methods=['GET'])
def getPeople():
    try:
        people_list = People.query.all()
        get_people = list(map(lambda i: i.serialize(), people_list))

        response_body = {
            "msg": "all People",
            "results": get_people
        }
        return jsonify(response_body), 200

    except:
        raise APIException('Personaje no encontrado', 404)


# OBTENER ONE PEOPLE POR ID

@app.route('/People/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    try:
        people_query = People.query.filter_by(characterID=people_id).first()

        response_body = {
            "msg": "OK",
            "result": people_query.serialize(),
        }

        return jsonify(response_body), 200

    except:
        raise APIException('Personaje no encontrado', 404)

# OBTENER ALL PLANETS


@app.route('/Planets', methods=['GET'])
def getPlanets():
    try:
        planets_list = Planets.query.all()
        get_planets = list(map(lambda i: i.serialize(), planets_list))

        response_body = {
            "msg": "all planets",
            "results": get_planets
        }
        return jsonify(response_body), 200

    except:
        raise APIException('Planeta no encontrado', 404)

 # OBTENER ONE PLANET POR ID


@app.route('/Planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    try:
        planet_query = Planets.query.filter_by(planetID=planet_id).first()

        response_body = {
            "msg": "OK",
            "result": planet_query.serialize(),
        }

        return jsonify(response_body), 200

    except:
        raise APIException('Planeta no encontrado', 404)


# OBTENER FAVORITOS DE UN ID

@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def getFavoritesUser(user_id):
    try:

        favorites_query = Favorites.query.filter_by(userID=user_id).first()
        if not favorites_query:
            raise APIException('Favoritos no encontrados', 404)

        response_body = {
            "msg": "all favorites for one user",
            "results": favorites_query.serialize(),
        }
        return jsonify(response_body), 200

    except:
        raise APIException('favoritos no encontrados', 404)


# AÑADIR PLANETA FAVORITO AL USUARIO ACTUAL

@app.route('/favorito/planets/<int:planet_id>', methods=['POST'])
def add_planets_favorite(planet_id):

    request_body = request.json.get('User')

    user = User.query.get(request_body)

    if not user:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({'mensaje': 'El planeta no existe'}), 404

    favorito_existente = Favorites.query.filter_by(userID=user.id, planetID=planet_id).first()
    if favorito_existente:
        return jsonify({'mensaje': 'El planeta ya está en favoritos'}), 404
    
    

    new_favorite = Favorites(userID=user.id, planetID=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        'msg':'ok',
        "results": new_favorite.serialize()
    }

    return jsonify(response_body, {'mensaje': 'Planeta agregado a favoritos exitosamente'}), 200

   

   # AÑADIR Charater FAVORITO AL USUARIO ACTUAL
    
@app.route('/favorito/people/<int:people_id>', methods=['POST'])
def add_character_favorite(people_id):

    request_body = request.json.get('User')

    user = User.query.get(request_body)

    if not user:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    people = People.query.get(people_id)
    if not people:
        return jsonify({'mensaje': 'El personaje no existe'}), 404

    favorito_existente = Favorites.query.filter_by(userID=user.id, characterID=people_id).first()
    if favorito_existente:
        return jsonify({'mensaje': 'El personaje ya está en favoritos'}), 404

    new_favorite = Favorites(userID=user.id, characterID=people_id)
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        'msg':'ok',
        "results": new_favorite.serialize()
    }


    return jsonify(response_body,{'mensaje': 'Personaje agregado a favoritos exitosamente'}), 200


# FIN ENDPOINTS


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


