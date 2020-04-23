from flask import Flask, Blueprint, redirect, render_template, request, flash, jsonify, url_for, abort
from flask_login import LoginManager, login_required, current_user
from app.models import User, Favourites
from app import db
import requests
import json


main = Blueprint('main', __name__)

@main.route("/", methods=['POST','GET'])
def home():

  '''favqs random qoute of the day'''
  res = requests.get("https://favqs.com/api/qotd")
  #parse json to dict
  a = res.json()
  author = a["quote"]["author"]
  q_day = a["quote"]["body"]

  return(render_template("home.html", author=author, q_day=q_day))



#favqs api key
api_key = "1f8a41cae02a612c161aea7a57be1702"

@main.route("/search", methods=['POST'])
def search():
  get_q = request.form.get("word")
  api_endpoint = "https://favqs.com/api/quotes/?filter="+get_q
  res = requests.get(api_endpoint, headers={'Authorization': "Token token="+api_key})
  parse = res.json()
  quotes=parse['quotes']
  return(render_template("quotespage.html", quotes=quotes))
  
#bookmark quotes 
@main.route("/bookmark/<idd>")
@login_required
def bookmark(idd):
  get_q = "https://favqs.com/api/quotes/:quote_id/{idd}".format(idd=str(idd))
  res = requests.get(get_q, headers={'Authorization': "Token token="+api_key, "Content-Type": "application/json"})
  parse = res.json()
  info = parse["body"]+" -"+parse["author"]
  save_bookmark = Favourites(qoute=info, fav=current_user)
  db.session.add(save_bookmark)
  db.session.commit()
  return(redirect(url_for('main.profile', username=current_user.username)))

#delete bookmarks
@main.route("/delete/<id>", methods=["POST"])
@login_required
def delete(id):
  pass

@main.route("/<username>")
@login_required
def profile(username):
  get_user = User.query.filter_by(username=username).first()

  if not get_user or username != current_user.username:
    abort(404)
  
  user_favourites= Favourites.query.all()
  user_fav=[]
  for info in user_favourites:
    if info.fav.username == current_user.username:
      user_fav.append(info)

  return(render_template("profile.html", info=user_fav))
