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
from models import db, User, Character, Planet, Favorite
from service import Service

# import Flask-JWT-Extended library
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get('JW_TOKEN')  # Change this "super secret" with something else!
jwt = JWTManager(app)
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

@app.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email")
    password = request.json.get("password")
    # Query your User table with username and password
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        # The user was not found on the database
        return jsonify({"msg": "Bad email or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token)

# @app.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     # Access the identity of the current user with get_jwt_identity
#     current_user_id = get_jwt_identity()
#     user = User.query.get(current_user_id)
    
#     return jsonify({"email": user.email, "password": user.password }), 200

# Users endpoints
@app.route('/users', methods=['GET'])
def get_users():
    users = User.getAll()
    response_body = {
        "msg": "Hello, this is your GET /users response "
    }

    return jsonify(users), 200

@app.route('/users/<int:position>', methods=['DELETE'])
def delete_user(position):
    print("This is the position to delete: ",position)
    temp = User.deleteUser(position)
    response_body = {
        "msg": "User deleted "
    }

    return jsonify(response_body), 200

# Characters endpoints
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.getAll()
    response_body = {
        "msg": "Hello, this is your GET /characters response "
    }

    return jsonify(characters), 200

@app.route('/characters/<int:position>', methods=['DELETE'])
def delete_character(position):

    temp = Character.deleteCharacter(position)
    response_body = {
        "msg": "Character deleted "
    }

    return jsonify(response_body), 200

# Planets endpoints
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.getAll()
    response_body = {
        "msg": "Hello, this is your GET /planets response "
    }

    return jsonify(planets), 200

@app.route('/planets/<int:position>', methods=['DELETE'])
def delete_planet(position):
    print("This is the position to delete: ",position)
    temp = Planet.deletePlanet(position)
    response_body = {
        "msg": "Planet deleted "
    }

    return jsonify(response_body), 200

# Favorites endpoints
@app.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    all_favorites = Service.get_favorites(current_user_id)
    return jsonify(all_favorites), 200
    # return jsonify("hello world"), 200

@app.route('/favorites', methods=['POST'])
def add_favorite():
    request_body = request.get_json()
    # define an instance of Favorite
    favorite = Favorite(item_id=request_body["item_id"], item_type=request_body["item_type"], user_id=request_body["user_id"])
    # save it on the database table for Favorites
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify(request_body), 200

@app.route('/favorites/<int:position>', methods=['DELETE'])
def delete_favorite(position):
    favorite = Favorite.query.filter_by(item_id=position).first()
    # favorite = Favorite.query.get(position)

    if favorite is None:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite)
    db.session.commit()
    response_body = {
         "msg": "Favorite deleted successful",
    }
    return jsonify(response_body), 200

# Endpoint for populate the database
@app.route('/populate', methods=['GET'])
def populate():
    u1 = User(firstName='userF01', lastName='userL01', email='user01@example.com', password="01", is_active=False, picture="picture1.png")
    u2 = User(firstName='userF02', lastName='userL02', email='user02@example.com', password="02", is_active=False, picture="picture02.png")
    u3 = User(firstName='userF03', lastName='userL03', email='user03@example.com', password="03", is_active=False, picture="picture03.png")

    c1 = Character(name='Luke Skywalker', birth_year='19BBY', gender='male', mass="75", eye_color='blue', hair_color='blond')
    c2 = Character(name='C-3PO', birth_year='112BBY', gender='', mass="76", eye_color='yellow', hair_color='n/a')
    c3 = Character(name='R2-D2', birth_year='33BBY', gender='n/a', mass="75", eye_color='red', hair_color='n/a')
    c4 = Character(name='Darth Vader', birth_year='41.9BBY', gender='male', mass="75", eye_color='yellow', hair_color='none')
    c5 = Character(name='Leia Organa', birth_year='19BBY', gender='female', mass="75", eye_color='brown', hair_color='brown')
    c6 = Character(name='Owen Lars', birth_year='52BBY', gender='male', mass="75", eye_color='blue', hair_color='brown, grey')

    p1 = Planet(name='Tatooine', population='200000', terrain='desert', diameter='10465.0', climate='arid', orbital_period='268')
    p2 = Planet(name='Alderaan', population='2000000000', terrain='grasslands, mountains', diameter='12500.0', climate='temperate', orbital_period='268')
    p3 = Planet(name='Yavin IV', population='1000', terrain='jungle, rainforests', diameter='10200.0', climate='temperate, tropical', orbital_period='268')
    p4 = Planet(name='Hoth', population='5000', terrain='tundra, ice caves', diameter='7200.0', climate='frozen', orbital_period='268')
    p5 = Planet(name='Dagobah', population='6500', terrain='swamp, jungles', diameter='8900.0', climate='murky', orbital_period='268')
    p6 = Planet(name='Bespin', population='6000000', terrain='gas giant', diameter='118000.0', climate='temperate', orbital_period='268')

    db.session.add_all([u1, u2, u3, c1, c2, c3, c4, c5, c6, p1, p2, p3, p4, p5, p6])
    db.session.commit()

    return('Data populated')


# this only runs if `$ python src/main.py` is executed

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
