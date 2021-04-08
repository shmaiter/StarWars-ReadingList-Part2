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
    favorites = db.relationship('Favorite', lazy=True) # One to Many
    
    def __repr__(self):
        return '<User %r>' % self.firstName

    def serialize(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "picture": self.picture,
            "favorites": self.favorites
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
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    birthYear = db.Column(db.String(25))
    gender = db.Column(db.String(25))
    description = db.Column(db.String(300))
    # favorite_id = db.Column(db.Integer, ForeignKey('favorite.id'))
    
    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "birthYear": self.birthYear,
            "gender": self.gender,
            "description": self.description
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
    name = db.Column(db.String(50))
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(25))
    climate = db.Column(db.String(25))
    description = db.Column(db.String(300))
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
            "description": self.description
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    item_id = db.Column(db.Integer, unique=False, nullable=False)
    item_type = db.Column(db.String(80), unique=False, nullable=False)

    # character = db.relationship('Character', back_populates="favorite") # One to Many
    # planet = db.relationship('Planet', back_populates="favorite") # One to Many
    
    def __repr__(self):
        return '<Favorite %r>' % self.date

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "user_id": self.user_id,
            "item_id": self.item_id,
            "item_type": self.item_type
            # do not serialize the password, its a security breach
        }