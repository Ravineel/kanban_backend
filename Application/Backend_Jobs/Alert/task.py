from Application.workers import celery
from datetime import datetime
import urllib
import moment
from urllib.request import urlopen
from Application.model import *
from celery.schedules import crontab
from json import dumps
from urllib.error import HTTPError, URLError

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from Application.Backend_Jobs.Pogress_report.pdf_maker import create_pdf
from Application.Backend_Jobs.Pogress_report.send_mail import send_mail



@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.add_periodic_task(
    crontab(minute=0,hour='*',day_of_week='*'), 
    # 10,
    send_alert.s(),
    name='send daily alert'
  )
  sender.add_periodic_task(
    crontab(minute='*',hour=19,day_of_month='21',month_of_year='*'), 
    # 10,
    send_report.s(),
    name='send monthly report'
  )


def create_data():
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

    return data,lists,cards,name,email


@celery.task()
def send_report():
  data,lists,cards,name,email = create_data()
  r = create_pdf(data,lists,cards,name,email)

  if r !=-1:
    send_mail(r["file_name"],name,email,r["message"])
    return "done"
  else:
    return "error"

@celery.task()
def send_alert():
  for u in User.query.all():
    for l in List.query.filter_by(u_id=u.u_id).all():
      for c in Card.query.filter_by(l_id=l.l_id).all():

        if c.completed==0 and moment.date(c.deadline) < moment.now():
          c.completed = 1
          db.session.commit()



        if c.completed==0:
          msg = {'text': 'The task '+c.name+' is not completed yet, Please complete it as soon as possible before the deadline: '+c.deadline}
          data = dumps(msg).encode('utf-8')
          url = "https://chat.googleapis.com/v1/spaces/AAAAq_LS0Zo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=j0snjacktfz17QYRygqECm9nC2-1_EtfNOvfy3nIbXE%3D"
          headers = {'Content-Type': 'application/json'}
          req = urllib.request.Request(url,data=data,method='POST',headers=headers)
          
          try:
            with urlopen(req) as r:
              body = r.read().decode('utf-8')
             
          except Exception as e:
            print("Error Occured")
            continue
        
        if c.completed==1:
          msg = {'text': 'The task '+c.name+' is not completed yet, The deadline: '+c.deadline + ' has passed already, Please complete it as soon as possible'}
          data = dumps(msg).encode('utf-8')
          url = "https://chat.googleapis.com/v1/spaces/AAAAq_LS0Zo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=j0snjacktfz17QYRygqECm9nC2-1_EtfNOvfy3nIbXE%3D"
          headers = {'Content-Type': 'application/json'}
          req = urllib.request.Request(url,data=data,method='POST',headers=headers)
          
          try:
            with urlopen(req) as r:
              body = r.read().decode('utf-8')
           
          except Exception as e:
            print("Error Occured")
            continue
         



@celery.task()
def update_time(c_id,token):
  url = "http://localhost:5000/time_update/"+str(c_id)
  headers = {
    "Authorization": token  
  }
  req = urllib.request.Request(url, headers=headers)
  req.method = lambda:'PATCH'
  
  try:
    with urlopen(req) as r:
      body = r.read().decode('utf-8')
      return "done"
  except Exception as e:
    return "Error Occured"