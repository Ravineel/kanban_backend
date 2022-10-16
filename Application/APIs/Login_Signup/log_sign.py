from flask_restful import Api, Resource, fields, marshal_with, reqparse
from Application.Validation import *
from Application.models import User
from Application.database import db
from flask import current_app as app
import werkzeug
from datetime import Date
from werkzeug import generate_password_hash, check_password_hash


login = reqparse.RequestParser()
login.add_argument('username', type=str, required=True, help='username is required')
login.add_argument('password', type=str, required=True, help='password is required')

class Login(Resource):
    def post(self):
        args = login.parse_args()
        username = args['username']
        password = args['password']
        

class Signup(Resource):
  pass