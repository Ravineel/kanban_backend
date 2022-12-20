from Application.model import List,Card
from Application.database import db
from flask import request,make_response,jsonify
from flask import current_app as app
from Application.middleware import token_required
from flask_restful import Resource,reqparse,marshal_with,fields
from Application.Validation import *
from datetime import datetime, timedelta
import moment
from Application.Backend_Jobs.Alert.task import update_time

mult_card = {
    "c_id": fields.Integer,
    "l_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "deadline": fields.String,
    "completed": fields.Integer,
    "date_of_submission": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String
}

class CardApi(Resource):

  @marshal_with(mult_card)
  @token_required
  def get(current_user,self):
    print(current_user.u_id)
    if List.query.filter_by(u_id=current_user.u_id).count() == 0:
      raise ValidationError(404,"LT001","No list found")
    try:

      # for l in List.query.filter_by(u_id=current_user.u_id).all():
      #   for c in Card.query.filter_by(l_id=l.l_id).all():
      #     job = update_time.delay(c.c_id,request.headers['Authorization'])
      #     r = job.wait()

      cards = Card.query.join(List,Card.l_id==List.l_id)\
        .add_columns(Card.c_id, Card.l_id, Card.name, Card.description, Card.deadline, Card.completed,Card.date_of_submission,Card.created_at,Card.updated_at)\
        .filter(Card.l_id==List.l_id)\
        .filter(List.u_id==current_user.u_id).all()      

      return cards,200
    except Exception as e:
      print(e)
      raise ValidationError(404,"CR001","Card not found")

  @token_required
  def post(current_user,self):
    data = request.get_json()
    if not data:
      raise ValidationError(400,"CR002","No data provided")
    if not data.get("l_id"):
      raise ValidationError(400,"CR003","List id not provided")
    if not data.get("name"):
      raise ValidationError(400,"CR004","Card name not provided")
    if not data.get("description"):
      raise ValidationError(400,"CR005","Card description not provided")
    if not data.get("deadline"):
      raise ValidationError(400,"CR006","Card deadline not provided")
    completed=0
    create = datetime.now()
    update = datetime.now()
    data["deadline"] = moment.date(data["deadline"]).add(hours=23,minutes=59,seconds=59).format('YYYY-MM-DD HH:mm:ss')
    
    try:
      card = Card(l_id=data["l_id"],name=data["name"],description=data["description"],deadline=data["deadline"],created_at=create,updated_at=update,completed=completed)
      db.session.add(card)
      db.session.commit()
      return make_response(jsonify({"message":"Card created successfully"}),200)
    except:
      raise ValidationError(500,"CR007","Card creation failed")

  @token_required
  def put(current_user,self,c_id):
    data = request.get_json()
    if not data:
      raise ValidationError(400,"CR008","No data provided")
    card = Card.query.filter_by(c_id=c_id).first()
    if data.get("l_id"):
      card.l_id = data["l_id"]
    if  data.get("name"):
      card.name=data["name"]
    if  data.get("description"):
      card.description=data["description"]
    if  data.get("deadline"):
      card.deadline=data["deadline"]
    card.updated_at = datetime.now()

    try:
      db.session.commit()
      return make_response(jsonify({"message":"Card updated successfully"}),200)
    except:
      raise ValidationError(500,"CR013","Card updation failed")    


  @token_required
  def delete(current_user,self,c_id):
    try:
      card = Card.query.filter_by(c_id=c_id).first()
      db.session.delete(card)
      db.session.commit()
      return make_response(jsonify({"message":"Card deleted successfully"}),200)
    except:
      raise ValidationError(500,"CR014","Card deletion failed")

  @token_required
  def patch(current_user,self,c_id):
    try:
      card = Card.query.filter_by(c_id=c_id).first()
      if card.completed == 0 and moment.date(card.deadline)  < moment.now():
        card.completed=1
      db.session.commit()
      return make_response(jsonify({"message":"Card updated successfully"}),200)
    except:
      raise ValidationError(500,"CR013","Card updation failed")
class CardCompleteApi(Resource):

  @token_required
  def put(current_user,self,c_id):
    try:
      card = Card.query.filter_by(c_id=c_id).first()
      
      if moment.date(card.deadline)  < moment.now():
        card.completed=3
        msg= "Card completed successfully but deadline has passed"
      else:
        card.completed=2
        msg= "Card completed successfully"
      card.updated_at=datetime.now()
      db.session.commit()
      return make_response(jsonify({"message":msg}),200)
    except:
      raise ValidationError(500,"CR015","Card completion failed")
  
  