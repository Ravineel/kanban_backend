from datetime import timedelta
from distutils.debug import DEBUG
import os
from pickle import FALSE

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
    DEBUG=FALSE
    SQLITE_DB_DIR=None
    SQLALCHEMY_DATABASE_URI = None

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db/db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
    