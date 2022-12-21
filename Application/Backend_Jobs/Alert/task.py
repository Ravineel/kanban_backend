from Application.workers import celery
from datetime import datetime
import urllib
import moment
from urllib.request import urlopen
from Application.model import *
from celery.schedules import crontab
from json import dumps

from urllib.error import HTTPError, URLError


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.add_periodic_task(
    crontab(minute=0,hour=17,day_of_week='*'), 
    # 10,
    send_alert.s(),
    name='send daily alert'
  )
  

# @celery.task()
# def check():
#   msg= {'text': 'Hello World'}
#   data = dumps(msg).encode('utf-8')
#   print(data)

#   url = "https://chat.googleapis.com/v1/spaces/AAAAq_LS0Zo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=j0snjacktfz17QYRygqECm9nC2-1_EtfNOvfy3nIbXE%3D"
#   headers = {'Content-Type': 'application/json'}
#   req = urllib.request.Request(url,data=data,method='POST',headers=headers)
  
#   try:
#     with urlopen(req) as r:
#       print("r",r)
#       body = r.read().decode('utf-8')
#       print(body)
#   except HTTPError as e:
#     print("http error ",e.status, e.reason)
#   except URLError as e:
#     print("url error ",e.reason)
#   except TimeoutError:
#     print("Timeout")
#   except Exception as e:
#     print(e.reason)

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