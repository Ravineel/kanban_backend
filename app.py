import os
from re import template
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from Application.config import LocalDevelopmentConfig
from Application.database import db


app=None
api-None

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
  return app,api

app,api = create_app()

from Application.API import *

api.add_resource(Signup,'/signup')


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)
