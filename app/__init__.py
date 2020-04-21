from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


db = SQLAlchemy()


def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  app.config['SECRET_KEY'] = 'ASpire2begreat'
  app.config['SQLALCHEMY_DATABASE_URI'] = "#"

  db.init_app(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  from app.models import User
  @login_manager.user_loader
  def load_user(user_id):
    return(User.query.get(int(user_id)))

  # blueprint for non-auth parts of app
  from app.main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  from app.forms import forms as forms_blueprint
  app.register_blueprint(forms_blueprint)


  return(app)
