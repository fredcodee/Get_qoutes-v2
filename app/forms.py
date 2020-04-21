from flask import Blueprint, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from flask_login import login_user, login_required, logout_user

forms = Blueprint('forms', __name__)

class LoginForm(FlaskForm):
  username = StringField('username', validators=[InputRequired()])
  password = PasswordField('password', validators=[InputRequired()])
  remember = BooleanField('remember me')
  submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])

#login
@forms.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user:
       if check_password_hash(user.password, form.password.data):
         login_user(user, remember=form.remember.data)
         return(redirect(url_for('main.home')))
    else:
      flash('username or password incorrect')
      return(redirect(url_for("main.login")))

  return(render_template("login.html", form=form))


@forms.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data,email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return(redirect(url_for('forms.login')))

    return render_template('signup.html', form=form)


@forms.route('/logout')
@login_required
def logout():
  logout_user()
  return(redirect(url_for('index')))
