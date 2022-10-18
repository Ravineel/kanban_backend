import marshal
from Application.model import User,List,Card
from Application.database import db
from flask import request, jsonify, make_response,current_app as app
from Application.Validation import *
from Application.middleware import token_required
from flask_restful import Resource, reqparse, fields, marshal_with
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import moment

multlist={
  "l_id": fields.Integer,
  "u_id": fields.Integer,
  "name": fields.String,
  "description": fields.String,
  "created_at": fields.String,
  "updated_at": fields.String,

}

update_list = reqparse.RequestParser()
update_list.add_argument('name', type=str,required=False, help='name of the list')
update_list.add_argument('description', type=str, required=False,help='description of the list')
class ListAPI(Resource):

  @marshal_with(multlist)
  @token_required
  def get(current_user,self):
    if List.query.filter_by(u_id=current_user.u_id).count() == 0:
      msg = "No list found"
      code= 404
      error = "LT001"
      raise BusinessValidationError(code, error, msg)
    else:
      ulist = List.query.filter_by(u_id=current_user.u_id).all()
      return ulist,200

  @token_required
  def post(current_user,self):
    data = request.get_json()
    name = data['name']
    description = data['description']
    if name == "":
      msg = "Name cannot be empty"
      code= 404
      error = "LT003"
      raise BusinessValidationError(code, error, msg)
    else:
      create=datetime.now()
      update=datetime.now()
      new_list = List(name=name,description=description,u_id=current_user.u_id,created_at=create,updated_at=update)
      db.session.add(new_list)
      db.session.commit()
      return make_response(jsonify({"message": "List created successfully"}), 200)

  @token_required
  def put(current_user,self,l_id):
    ulist = List.query.filter_by(l_id=l_id).first()
    if not ulist:
      raise ValidationError(404, "LT001", "List not found!")
    
    try:
      args = update_list.parse_args()
      if args['name']:
        ulist.name = args['name']
      if args['description']:
        ulist.description = args['description']
      
      ulist.updated_at = moment.now().strftime("%Y-%m-%d %H:%M:%S")
      db.session.commit()
      return make_response(jsonify({"message": "List updated successfully"}), 200)
    except Exception as e:
      raise ValidationError(500, "LT002", "Error while updating list")


  @token_required
  def delete(current_user,self):
    data = request.get_json()
    l_id = data.get('l_id')
    ulist = List.query.filter_by(l_id=l_id).first()
    if not ulist:
      raise ValidationError(404, "LT001", "List not found!")
    
    
    try:
      db.session.query(Card).filter(Card.l_id == l_id).delete()
      db.session.delete(ulist)
      db.session.commit()
      return make_response(jsonify({"message": "List deleted successfully"}), 200)
    
    
    except Exception as e:
      raise ValidationError(500, "LT002", "Error while deleting list")

   