from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

def auth_login(request):
  username = request.form['username']
  password = request.form['password']
  db = get_db()
  error = None
  user = db.execute(
    'SELECT * FROM user WHERE username = ?', (username,)
  ).fetchone()

  if user is None:
    error = 'Incorrect username.'
  elif not check_password_hash(generate_password_hash(user['password']), password):
    error = 'Incorrect password.'

  if error is None:
    session.clear()
    session['user_id'] = user['id']
    return None
  return error