from Application.workers import celery
from datetime import datetime
from urllib import request,parse
from urllib.request import urlopen
from Application.model import *
from celery.schedules import crontab


# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#   sender.add_periodic_task(
#     crontab(hour=2, minute=50,day_of_week='*'), 
#     send_alert.s("https://chat.googleapis.com/v1/spaces/AAAAq_LS0Zo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=j0snjacktfz17QYRygqECm9nC2-1_EtfNOvfy3nIbXE%3D"),
#     name='send daily alert'
#   )
  
# @celery.task()
# def send_alert(wurl):
#   print("hi")
#   for u in User.query.all():
#     for l in List.query.filter_by(u_id=u.u_id).all():
#       for c in Card.query.filter_by(l_id=l.l_id).all():
#         if c.completed==0:
#           msg = "The task"+c.name+" is not completed yet, Please complete it as soon as possible before the deadline: "+c.deadline
#           url = wurl
#           req = request.Request(url, data=bytes(parse.urlencode({'text': msg}), encoding='utf-8'), method='POST')
#           try:
#             with urlopen(req) as r:
#               body = r.read().decode('utf-8')
#               print(body)
#           except Exception as e:
#             print("Error Occured")
#             continue
        
#         if c.completed==1:
#           msg = "The task"+c.name+" is not completed yet, The deadline: "+c.deadline + " has passed already, Please complete it as soon as possible"
#           url = wurl
#           req = request.Request(url, data=bytes(parse.urlencode({'text': msg}), encoding='utf-8'), method='POST')
#           try:
#             with urlopen(req) as r:
#               body = r.read().decode('utf-8')
#               print(body)
#           except Exception as e:
#             print("Error Occured")
#             continue
         



@celery.task()
def update_time(c_id,token):
  url = "http://localhost:5000/time_update/"+str(c_id)
  headers = {
    "Authorization": token  
  }
  req = request.Request(url, headers=headers)
  req.method = lambda:'PATCH'
  
  try:
    with urlopen(req) as r:
      body = r.read().decode('utf-8')
      return body
  except Exception as e:
    return "Error Occured"