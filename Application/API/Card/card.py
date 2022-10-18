from Application.model import List,Card
from Application.database import db
from flask import request,make_response,jsonify
from flask import current_app as app
from Application.middleware import token_required
from flask_restful import Resource,reqparse,marshal_with,fields
from Application.Validation import *


mult_card = {
    "c_id": fields.Integer,
    "l_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "deadline": fields.DateTime,
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime,
    "completed": fields.Integer
}

class CardApi(Resource):

  @marshal_with(mult_card)
  @token_required
  def get(current_user,self):
    if List.query.filter_by(u_id=current_user.u_id).count() > 0:
      return make_response(jsonify({"message":"List not found"}),404)
    try:
      cards = Card.query.join(List,Card.l_id==List.l_id).filter(Card.l_id==List.l_id).filter(List.u_id==current_user.u_id).all()

      return cards,200

    except:
      raise ValidationError(404,"CR001","Card not found")

