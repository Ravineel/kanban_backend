import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from Application.config import LocalDevelopmentConfig
from Application.database import db
from Application import workers
from Application.middleware import *

# from flask_jwt import JWT, jwt_required, current_identity

app=None
api=None
jwt=None
celery = None

def create_app():
  app=Flask(__name__,template_folder='templates',static_folder='assets')
  if os.getenv('ENV',"development")=='Production':
    raise Exception("Not available")

  else:
    print("Running in development mode")
    app.config.from_object(LocalDevelopmentConfig)
  
  db.init_app(app)
  api=Api(app)
  app.app_context().push()
  celery = workers.celery
  celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND'],
    result_expires=3600,
    enable_utc=False,
    timezone='Asia/Kolkata',
  )
  celery.Task = workers.ContextTask
  app.app_context().push()

  return app,api,celery

app,api,celery = create_app()


from Application.API.Login_Signup.log_sign import Login,Signup,Logout
from Application.API.User.user import UserApi
from Application.API.List.list import ListAPI
from Application.API.Card.card import CardApi,CardCompleteApi
from Application.API.Summary.summary import SummaryApi

api.add_resource(Signup,'/signup')
api.add_resource(Login,'/login')
api.add_resource(Logout,'/logout')
api.add_resource(UserApi,'/user','/update_user','/del_user')
api.add_resource(ListAPI,'/get_list','/del_list','/update_list/<int:l_id>','/create_list')
api.add_resource(CardApi,'/get_card','/del_card/<int:c_id>','/update_card/<int:c_id>','/create_card','/time_update/<int:c_id>')
api.add_resource(CardCompleteApi,'/complete_card/<int:c_id>')
api.add_resource(SummaryApi,'/summary/<int:l_id>')

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)
