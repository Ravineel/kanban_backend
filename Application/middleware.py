import jwt
from functools import wraps
from flask import current_app as app
from flask import request,jsonify,make_response
from Application.model import User



def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    if 'x-access-token' in request.headers:
      token = request.headers['x-access-token']
    if not token:
      return ##return error message
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'])
      current_user = User.query.filter_by(u_id=data['u_id']).first()
      if not current_user:
        return ##return error message
    except:
      return ##raise error
    return f(current_user, *args, **kwargs)
  return decorated