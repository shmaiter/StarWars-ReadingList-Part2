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
from models import db, User, Character, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

# Users endpoints
@app.route('/users', methods=['GET'])
def handle_users():
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
def handle_characters():
    characters = Character.getAll()
    response_body = {
        "msg": "Hello, this is your GET /characters response "
    }

    return jsonify(characters), 200

# Planets endpoints
@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planet.getAll()
    response_body = {
        "msg": "Hello, this is your GET /planets response "
    }

    return jsonify(planets), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
