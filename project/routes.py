from asyncio import sleep
import json
import sqlite3
import requests
from flask import Flask,render_template,request, redirect, Blueprint,Response
from flask_login import login_required, logout_user, current_user, login_user
import werkzeug
from werkzeug.utils import secure_filename
from .models import db, User
from . import login_manager, mail
from . import db
from dateutil.relativedelta import *
import urllib.request
from bs4 import BeautifulSoup as bs
import os
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
import pickle
import sys
from datetime import datetime, timedelta
from flask import send_file

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
DATABASE = "instance/Users.db"

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    
    return response

@app.route('/')
def home():
    return render_template('home.html')
