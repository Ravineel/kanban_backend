from flask import request,jsonify,make_response
from flask_login import UserMixin
from .database import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
from flask import current_app as app
import uuid


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    u_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    public_id = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    date_of_birth = db.Column(db.String, nullable=False)
    role=db.Column(db.String, nullable=False)
    account_created_at = db.Column(db.String, nullable=False)
    jwt_token = db.Column(db.String, nullable=True)
    
    def get_id(self):
      return self.u_id
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# class UserSchedule(db.Model):
#     __tablename__ = 'schedule'
#     u_id = db.Column(db.Integer, db.ForeignKey('users.u_id'))
#     s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     task_name = db.Column(db.String, nullable=False)
#     frequency = db.Column(db.String, nullable=False)
#     time = db.Column(db.String, nullable=False)
#     day = db.Column(db.Integer, nullable=False)
#     month = db.Column(db.Integer, nullable=False)
#     year = db.Column(db.Integer, nullable=False)
#     isOn = db.Column(db.Integer, nullable=False, default=1)
#     webhook_url = db.Column(db.String, nullable=False, default='https://chat.googleapis.com/v1/spaces/AAAAq_LS0Zo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=j0snjacktfz17QYRygqECm9nC2-1_EtfNOvfy3nIbXE%3D')
    
        
class List(db.Model):
    __tablename__ ='list'
    l_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_id = db.Column(db.Integer, db.ForeignKey('users.u_id'))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.String,nullable=True)
    updated_at = db.Column(db.String,nullable=True)


class Card(db.Model):
    __tablename__ ='card'
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    l_id = db.Column(db.Integer, db.ForeignKey('list.l_id'))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    deadline=db.Column(db.String, nullable=False)
    completed= db.Column(db.Integer,nullable=False,default=0)
    date_of_submission = db.Column(db.String,nullable=True)
    created_at = db.Column(db.String,nullable=True)
    updated_at = db.Column(db.String,nullable=True)


