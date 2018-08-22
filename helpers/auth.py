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
  elif not check_password_hash(user['password'], password):
    error = 'Incorrect password.'

  if error is None:
    session.clear()
    session['user_id'] = user['id']
    session['username'] = user['username']
    return None
  return error

def auth_logout():
  username = session['username']
  session.clear()
  return username + " successfully logged out"

def auth_register(request):
  username = request.form['username']
  password = request.form['password']
  s3_bucket = request.form['s3_bucket']
  s3_key = request.form['s3_key']
  s3_secret = request.form['s3_secret']
  db = get_db()
  error = None

  if not username:
      error = 'Username is required.'
  elif not password:
      error = 'Password is required.'
  elif not s3_bucket:
      error = 's3_bucket is required.'
  elif not s3_key:
      error = 's3_key is required.'
  elif not s3_secret:
      error = 's3_secret is required.'
  elif db.execute(
      'SELECT id FROM user WHERE username = ?', (username,)
  ).fetchone() is not None:
      error = 'User {} is already registered.'.format(username)

  if error is None:
      db.execute(
          'INSERT INTO user (username, password, s3_bucket, s3_key, s3_secret) VALUES (?, ?, ?, ?, ?)',
          (username, generate_password_hash(password), s3_bucket, s3_key, generate_password_hash(s3_secret))
      )
      db.commit()
      return None

  return error
