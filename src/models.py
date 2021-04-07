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
    id = db.Column(Integer, primary_key=True) 
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    picture = db.Column(db.String(250), nullable=True)
    # user = relationship('Favorite', back_populates="user") # One to Many
    
    def __repr__(self):
        return '<User %r>' % self.username

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
    