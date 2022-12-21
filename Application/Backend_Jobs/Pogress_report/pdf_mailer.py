from Application.workers import celery
from datetime import datetime
import urllib
import moment
from urllib.request import urlopen
from Application.model import *
from celery.schedules import crontab
from json import dumps
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from Application.Backend_Jobs.Pogress_report.pdf_mailer import create_pdf


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.add_periodic_task(
    crontab(minute=56,hour=17,day_of_month='21',month_of_year='*'), 
    # 10,
    send_report.s(),
    name='send monthly report'
  )




@celery.task()
def send_report():
  for u in User.query.all():
    email = u.email
    name = u.first_name+" "+u.last_name
    data ={}

    for l in List.query.filter_by(u_id=u.u_id).all():
      l_id = l.l_id

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


      data[l_id]={"total":cards,"completed":completed,"incomplete":incomplete,"overdue":overdue,"late":late,"total_completed":total_completed,"total_incomplete":total_incomplete} 
      
    cards = Card.query.join(List,Card.l_id==List.l_id)\
        .add_columns(Card.c_id, Card.l_id, Card.name, Card.description, Card.deadline, Card.completed,Card.date_of_submission,Card.created_at,Card.updated_at)\
        .filter(Card.l_id==List.l_id)\
        .filter(List.u_id==u.u_id).all() 
       

    lists = List.query.filter_by(u_id=u.u_id).all()

    create_pdf(data,lists,cards,name,email)


          