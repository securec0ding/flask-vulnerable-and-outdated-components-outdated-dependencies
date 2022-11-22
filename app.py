from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

from admin import AdminUserModelView

app = Flask(__name__)

app.secret_key = 'z2G3Nba1JQ0dwZJ421Ij9LoZRVe5Y8j6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

admin = Admin(app, name='site', template_mode='bootstrap3')

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True)
  username = Column(String(255), unique=True)
  password = Column(String(255))

admin.add_view(AdminUserModelView(User, db.session))

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.filter_by(id=user_id).first()

from views import *

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)