import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from Application.config import LocalDevelopmentConfig
from Application.database import db
from Application.middleware import *
# from flask_jwt import JWT, jwt_required, current_identity

app=None
api=None
jwt=None

def create_app():
  app=Flask(__name__,template_folder='templates',static_folder='assets')
  if os.getenv('ENV',"development")=='Production':
    raise Exception("Not available")

  else:
    print("Running in development mode")
    app.config.from_object(LocalDevelopmentConfig)
  
  db.init_app(app)
  api=Api(app)
  # jwt=JWT(app,authenticate,identity)
  app.app_context().push()
  return app,api,jwt

app,api,jwt = create_app()


from Application.API.Login_Signup.log_sign import Login,Signup,Logout
from Application.API.User.user import UserApi
from Application.API.List.list import ListAPI


api.add_resource(Signup,'/signup')
api.add_resource(Login,'/login')
api.add_resource(Logout,'/logout')
api.add_resource(UserApi,'/user','/update_user','/del_user')
api.add_resource(ListAPI,'/get_list','/del_list','/update_list/<int:l_id>','/create_list')
if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)
