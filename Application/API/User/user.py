from flask_restful import Api, Resource, fields, marshal_with, reqparse
from Application.Validation import *
from Application.model import User,List, Card
from Application import middleware
from Application.database import db
from flask import current_app as app
from datetime import datetime, timedelta
from functools import wraps
from flask import request,jsonify,make_response




usr ={
    "public_id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "date of birth": fields.String,
    "username": fields.String,
    "role": fields.String,
}



update_usr = reqparse.RequestParser()
update_usr.add_argument('first_name', type=str,required=False)
update_usr.add_argument('last_name', type=str,required=False)
update_usr.add_argument('email', type=str,required=False)
update_usr.add_argument('date of birth', type=str,required=False)
update_usr.add_argument('username', type=str,required=False)



class UserApi(Resource):
  
  @marshal_with(usr)
  # @login_required
  @middleware.token_required
  def get(current_user,self):

    if current_user.public_id:
      user = User.query.filter_by(u_id=current_user.u_id).first()
      if user is None:
        msg="user not found"
        code=404
        error="UR001"
        raise BusinessValidationError(code,error,msg)
      else: 
        return user
    else:
      msg="Logout out, Please Signin again"
      code=401
      error="UR011"
      raise BusinessValidationError(code,error,msg)
      
  # @login_required
  @middleware.token_required
  def put(current_user,self):
    args = update_usr.parse_args()
    user = User.query.filter_by(u_id=current_user.u_id).first()
    if user is None:
      msg="user not found"
      code=404
      error="UR003"
      raise BusinessValidationError(code,error,msg)
    else:
      if args['first_name'] is not None:
        user.first_name = args['first_name']
      if args['last_name'] is not None:
        user.last_name = args['last_name']
      if args['email'] is not None:
        user.email = args['email']
      if args['date of birth'] is not None:
        user.date_of_birth = args['date of birth']
      if args['username'] is not None:
        user.username = args['username']
      db.session.commit()
      return make_response(jsonify({"message":"user updated"}),200)
  
  # @login_required
  @middleware.token_required
  def delete(current_user,self):
    user = User.query.filter_by(u_id=current_user.u_id).first()
    if user is None:
      msg="user not found"
      code=404
      error="UR003"
      raise BusinessValidationError(code,error,msg)
    else:
      try:
        user_list = List.query.filter_by(u_id=current_user.u_id).all()
        for ul in user_list:
          x = db.session.query(Card).filter_by(l_id=ul.l_id).delete()
          db.session.delete(ul)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message":"user deleted"}),200)
      except:
        db.session.rollback()
        return make_response(jsonify({"message":"user not deleted"}),500)


      
      
  

