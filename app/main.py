from flask import Flask, Blueprint, redirect, render_template, request, flash, jsonify, url_for, abort
from flask_login import LoginManager, login_required, current_user
from app.models import User, Favourites
from app import db
import requests
import json


main = Blueprint('main', __name__)

@main.route("/", methods=['POST','GET'])
def home():

  '''favqs qoute of the day'''
  res = requests.get("https://favqs.com/api/qotd")
  #parse json to dict
  a = res.json()
  author = a["quote"]["author"]
  q_day = a["quote"]["body"]

  return(render_template("home.html", author=author, q_day=q_day))


#get qoutes for user and integrate api
#favqs.com/api
api_key = "1f8a41cae02a612c161aea7a57be1702"
@main.route("/search", methods=['POST'])
def search():
  get_q = request.form.get("word").title()
  


@main.route("/profile", methods=['POST', 'GET'])
def profile():
  pass
