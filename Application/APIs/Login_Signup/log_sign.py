from flask_restful import Api, Resource, fields, marshal_with, reqparse
from Application.Validation import *
from Application.models import User
from Application.database import db
from flask import current_app as app
import werkzeug
from datetime import Date
from werkzeug import generate_password_hash, check_password_hash
import uuid

login = reqparse.RequestParser()
login.add_argument('username', type=str, required=True, help='username is required')
login.add_argument('password', type=str, required=True, help='password is required')

class Login(Resource):
    def post(self):
        args = login.parse_args()
        username = args['username']
        password = args['password']
        


create_usr = reqparse.RequestParser()
create_usr.add_argument('fname', type=str, required=True, help='No first name was given!')
create_usr.add_argument('lname', type=str, required=False, help='No last name was given!')
create_usr.add_argument('mail', type=str, required=True, help='No email was given!')
create_usr.add_argument('dob', type=str, required=True, help='No date of birth was given!')
create_usr.add_argument("username", type=str, required=True, help="No username was given!")
create_usr.add_argument("password", type=str, required=True, help="No password was given!")

class Signup(Resource):

  def post(self):
    args = create_usr.parse_args()
    fname = args['fname']
    lname = args['lname']
    mail = args['mail']
    dob = args['dob']
    username = args['username']
    password = args['password']
    role="user"

    if fname is None:
      return ##return error message
    if mail is None:
      return ##return error message
    if dob is None:
      return ##return error message
    
    if username is None:
      return ##return error message

    if password is None:
      return ##return error message
    
    if User.query.filter_by(email=mail).first():
      return ##return error message
    else:
      if User.query.filter_by(username=username).first():
        return
      else:
        try:
          new_user =User(
            public_id=str(uuid.uuid4()),
            username=username,
            password=generate_password_hash(password),
            email=mail,
            first_name=fname,
            last_name=lname,
            date_of_birth=dob,
            role=role
          )
          db.session.add(new_user)
          db.session.commit()
          return ##return success message
        except:
          return ##return error message
      


