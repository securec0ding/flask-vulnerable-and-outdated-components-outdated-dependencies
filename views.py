from app import app, db, User
from flask import request, render_template
from flask_login import login_user, logout_user

from hashlib import pbkdf2_hmac
import binascii

SALT = b'\x80\x8b\xc7t\xb7,**\t(\xbe\xe5\nq\x9b\xa0'

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
  result = None
  username = request.form.get('username')
  password = request.form.get('password')
  if username:
    user = User.query.filter_by(username=username.encode('utf-8')).first()
    if user:
      key = pbkdf2_hmac('sha256', password.encode('utf-8'), SALT, 100000)
      if binascii.hexlify(key) == user.password:
        login_user(user)
      else:
        result = 'Invalid password'
    else:
      result = 'User does not exist, please register first.'
  return render_template('index.html', result=result)

@app.route('/logout')
def logout():
  logout_user()
  return render_template('index.html', result='Logged out successfully.')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('index.html')
  username = request.form.get('username').encode('utf-8')
  password = request.form.get('password').encode('utf-8')
  confirm_password = request.form.get('confirm_password').encode('utf-8')
  if password != confirm_password:
    result = 'Passwords do not match!'
  else:
    user = User.query.filter_by(username=username).first()
    if user:
      result = 'User already exists!'
    else:
      key = pbkdf2_hmac('sha256', password, SALT, 100000)
      new_user = User(username=username, password=binascii.hexlify(key))
      db.session.add(new_user)
      db.session.commit()
      result = 'Registration successful; you may log in now.'
  return render_template('index.html', result=result)