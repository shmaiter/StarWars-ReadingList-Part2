from flask_sqlalchemy import SQLAlchemy
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
# from eralchemy import render_er

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) 
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    picture = db.Column(db.String(250), nullable=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True) # One to Many
    
    def __repr__(self):
        return '<User %r>' % self.firstName

    def serialize(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "picture": self.picture
            # do not serialize the password, its a security breach
        }

    def getAll():
        all_users = User.query.all()
        all_users = list(map(lambda x: x.serialize(), all_users))
        return all_users

    def deleteUser(id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    gender = db.Column(db.String(25))
    hair_color = db.Column(db.String(25))
    eye_color = db.Column(db.String(25))
    birth_year = db.Column(db.String(25))
    mass = db.Column(db.Float)
    # favorite_id = db.Column(db.Integer, ForeignKey('favorite.id'))
    
    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "mass": self.mass
            # do not serialize the password, its a security breach
        }

    def getAll():
        all_characters = Character.query.all()
        all_characters = list(map(lambda x: x.serialize(), all_characters))
        return all_characters

    def deleteCharacter(id):
        character = Character.query.get(id)
        db.session.delete(character)
        db.session.commit()

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    population = db.Column(db.String(25))
    terrain = db.Column(db.String(25))
    climate = db.Column(db.String(25))
    diameter = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    # favorite_id = db.Column(db.Integer, ForeignKey('favorite.id'))
    
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period
            # do not serialize the password, its a security breach
        }

    def getAll():
        all_planets = Planet.query.all()
        all_planets = list(map(lambda x: x.serialize(), all_planets))
        return all_planets

    def deletePlanet(id):
        planet = Planet.query.get(id)
        db.session.delete(planet)
        db.session.commit()

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(25))
    item_id = db.Column(db.Integer, unique=False, nullable=False)
    item_type = db.Column(db.String(80), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

    # character = db.relationship('Character', back_populates="favorite") # One to Many
    # planet = db.relationship('Planet', back_populates="favorite") # One to Many
    
    # def __repr__(self):
    #     return '<Favorite %r>' % self.date

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "item_id": self.item_id,
            "item_type": self.item_type,
            "user_id": self.user_id
            # do not serialize the password, its a security breach
        }

    # def deleteFavorite(id):
    #     favorite = Favorite.query.get(id)
    #     db.session.delete(favorite)
    #     db.session.commit()