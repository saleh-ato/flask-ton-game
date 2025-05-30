from flask import Flask, render_template, request, make_response, session, url_for, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)
import secrets
import os

app=Flask(__name__)
app.config['SECRET_KEY'] = '[Your Secret Key]'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Generate a CSRF token per session
@app.before_request
def set_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)

filedir=os.path.dirname(os.path.abspath(__file__))
goalroute=os.path.join(filedir,"app.db")
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+goalroute

UPLOAD_FOLDER = os.path.join(filedir,"uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/uploads/<path:path>")
@app.route("/images/<path:path>")
def static_dir(path):
    path=path.lower()
    return send_from_directory("uploads", path)

db= SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

import models
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
import views
#import flskcrpt.userviews

# import time
# import atexit
# from SchedulE import check_all
# from apscheduler.schedulers.background import BackgroundScheduler

'''
def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
'''

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=check_all, trigger="interval", minutes=15)
# #scheduler.add_job(func=check_all, trigger="interval", minutes=1)
# scheduler.start()
