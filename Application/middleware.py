import jwt
from functools import wraps
from flask import current_app as app
from flask import request,jsonify,make_response
from Application.model import User
from .Validation import *
import moment



class TokenExpiredError(Exception):
  def __init__(self, message):
    super().__init__(message)
    self.message = message
  pass
class TokenInvalidError(Exception):
  def __init__(self, message):
    super().__init__(message)
    self.message = message
  pass
class TokenRequiredError(Exception):
  def __init__(self, message):
    super().__init__(message)
    self.message = message
  

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    auth_header = request.headers.get('Authorization')
    if auth_header:
      try:
          token = auth_header.split(" ")[1]
      except IndexError:
          raise ValidationError(401, "TK001", "malformed") 
         
    else:
      token = ''
    if not token:
      raise TokenRequiredError()
    
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

      if moment.unix(data["exp"]) < moment.now():
        raise TokenExpiredError("error")

      current_user = User.query.filter_by(public_id=data['public_id']).first()
      
      if current_user.jwt_token != token:
        raise TokenInvalidError()
    
    except TokenExpiredError as te:
      raise ValidationError(401, "TK003", "Token is Expired!")
    except TokenInvalidError as ti:
      raise ValidationError(401, "TK004", "Token is Invalid!")
    except TokenRequiredError as tr:
      raise ValidationError(401, "TK002", "Token is Required!")
    except Exception as e:
      raise ValidationError(401, "TK005", "Token is Invalid!")

    return f(current_user, *args, **kwargs)

  return decorated

  