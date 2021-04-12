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
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get('JW_TOKEN')  # Change this "super secret" with something else!
jwt = JWTManager(app)

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
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    # Query your User table with username and password
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        # The user was not found on the database
        return jsonify({"msg": "Bad email or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token})

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
    print("This is the position to delete: ",position)
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

@app.route('/favorites', methods=['POST'])
def add_favorite():
    request_body = request.get_json()
    # define an instance of Favorite
    favorite = Favorite(date=request_body["date"], item_id=request_body["item_id"], item_type=request_body["item_type"], user_id=request_body["user_id"])
    db.session.add(favorite)
    db.session.commit()
    print("Favorite added: ", request_body)
    return jsonify(request_body), 200

# @app.route('/favorite/<int:id>', methods=['DELETE'])
# def delete_favorite(id):
#     favorite = Favorite.query.get(id)

#     if favorite is None:
#         raise APIException('Favorite not found', status_code=404)

#     db.session.delete(favorite)
#     db.session.commit()
#     response_body = {
#          "msg": "Favorite delete successful",
#     }
#     return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
