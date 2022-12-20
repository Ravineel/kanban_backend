from Application.model import List,Card
from Application.database import db
from flask import request,make_response,jsonify
from flask import current_app as app
from Application.middleware import token_required
from flask_restful import Resource,reqparse,marshal_with,fields
from Application.Validation import *
from datetime import datetime, timedelta
import moment
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

sdata= {
  "l_id":fields.Integer,
  "completed": fields.Integer,
  "incomplete": fields.Integer,
  "overdue": fields.Integer,
  "late": fields.Integer,
  "total_completed": fields.Integer,
  "total_incomplete": fields.Integer
}
class SummaryApi(Resource):
  
  @token_required
  @marshal_with(sdata)
  def get(current_user,self, l_id):
    if List.query.filter_by(l_id=l_id).count() == 0:
      raise ValidationError(404,"LT001","No list found")
    try:
      cards = Card.query.filter_by(l_id=l_id).count()
      cards2 = Card.query.filter_by(l_id=l_id).all()
      completed = Card.query.filter_by(l_id=l_id).filter_by(completed=2).count()
      incomplete = Card.query.filter_by(l_id=l_id).filter_by(completed=0).count()
      overdue = Card.query.filter_by(l_id=l_id).filter_by(completed=1).count()
      late = Card.query.filter_by(l_id=l_id).filter_by(completed=3).count()
    
      fig = plt.figure()
      plt.bar("Total Cards",cards,color="blue")
      plt.bar("Incomplete",incomplete,color="yellow")
      plt.bar("Completed",completed,color="green")
      plt.bar("Overdue",overdue,color="red")
      plt.bar("Late",late,color="orange")
      plt.title("Summary")
      g= ["total cards","incomplete","completed","overdue","late Submissions"]
      plt.legend(g)
      plt.savefig('./assets/img/summary_'+str(l_id)+'.png')
      plt.close()
   
      x=[]
      y=[]
      names=[]
      for card in cards2:
          if card.completed == 2:
            x.append(card.c_id)
            names.append(card.name)
            y.append(card.date_of_submission)
   
      plt.plot(y,names, color="green", marker="o")
      print(y)
      print(x)
      x=[]
      y=[]
      names=[]
      for card in cards2:
          if card.completed == 3:
            x.append(card.c_id)
            names.append(card.name)
            y.append(card.date_of_submission) 
      plt.plot(y,names, color="red", marker="o")
      plt.title("Cards Trend For Completeion")
      plt.legend(["completed","late Submissions"])
      plt.savefig('./assets/img/trend_'+str(l_id)+'.png')

      total_completed = completed+late
      total_incomplete = incomplete+overdue


      data ={"l_id":l_id,"completed":completed,"incomplete":incomplete,"overdue":overdue,"late":late,"total_completed":total_completed,"total_incomplete":total_incomplete} 
      return data,200 
    except Exception as e:
      raise ValidationError(404,"CR001","error occured")
