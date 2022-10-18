from ast import arg
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from Application.Validation import *
from Application.model import *
from Application.database import db
from flask import current_app as app
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime, timedelta


login = reqparse.RequestParser()
login.add_argument('username', type=str, required=True, help='username is required')
login.add_argument('password', type=str, required=True, help='password is required')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.needs_refresh_message = (u"Session timedout, please re-login")

@login_manager.user_loader
def load_user(id):
    user  = User.query.get(int(id))
    return user

class Login(Resource):
  def post(self):
    args = login.parse_args()
    username = args['username']
    password = args['password']

    if username is None:
      msg="username is required"
      code=404
      error="LR001"
      raise BusinessValidationError(code,error,msg)
    
    if password is None:
      msg="password is required"
      code=404
      error="LR002"
      raise BusinessValidationError(code,error,msg)
    
    user = User.query.filter_by(username=username).first()
    if user is None:
      msg="username not found"
      code=404
      error="LR003"
      raise BusinessValidationError(code,error,msg)
    else:
      if check_password_hash(user.password_hash, password):
        
        token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.utcnow() + timedelta(minutes = 20)
        }, app.config['SECRET_KEY'])
        login_user(user)
        return make_response(jsonify({'token' : token}), 200)
        
      else:
        msg="password is incorrect"
        code=404
        error="LR004"
        raise BusinessValidationError(code,error,msg)
        


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
    fname = args.get('fname')
    lname = args.get('lname')
    dob = args.get('dob')
    mail = args.get('mail')
    username = args.get('username')
    password = args.get('password')
    role="user"
    # created=datetime.datetime.now().strftime("%x")
    created="2022-10-17 00:00:00"

    if fname is None:
      msg="First name is required"
      code = 400
      error = "SIGN001"
      raise BusinessValidationError(code,error,msg) 
    
    if mail is None:
      msg="Email is required"
      code = 400
      error = "SIGN002"
      raise BusinessValidationError(code,error,msg)
    
    if dob is None:
      msg="Date of birth is required"
      code = 400
      error = "SIGN003"
      raise BusinessValidationError(code,error,msg)
    
    if username is None:
      msg="Username is required"
      code = 400
      error = "SIGN004"
      raise BusinessValidationError(code,error,msg)

    if password is None:
      msg="Password is required"
      code = 400
      error = "SIGN005"
      raise BusinessValidationError(code,error,msg)

    if User.query.filter_by(email=mail).first():
      msg="Email already exists"
      code = 400
      error = "SIGN006"
      raise BusinessValidationError(code,error,msg)

 
    if User.query.filter_by(username=username).first():
      msg="Username already exists"
      code = 400
      error = "SIGN007"
      raise BusinessValidationError(code,error,msg)
    try:
      pwd =generate_password_hash(password)
      pid=str(uuid.uuid4())
      print("here2",pid,pwd,created,dob)
      new_user =User(public_id=pid,username=username,password_hash=pwd,email=mail,first_name=fname,last_name=lname,date_of_birth=created,role=role,account_created_at=created)
      print(new_user)
      db.session.add(new_user)
      db.session.commit()
      print("here3")
      return {"message":"User created successfully"}, 200
    except Exception as e:
      return {"message":e}, 500
      


