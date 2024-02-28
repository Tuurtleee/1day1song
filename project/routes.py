from asyncio import sleep
import json
import sqlite3
import requests
from flask import Flask,render_template,request, redirect, Blueprint,Response
from flask_login import login_required, logout_user, current_user, login_user
import werkzeug
from werkzeug.utils import secure_filename
from .models import Music, User
from . import login_manager, mail
from . import db_musics, db_users
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
from flask import jsonify

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
DATABASE = "musics.db"

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    
    return response

@app.route('/')
def home():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Exécuter une requête pour récupérer les noms de tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # Récupérer les résultats de la requête
    tables = c.fetchall()
    # Fermer la connexion à la base de données
    conn.close()
    # Afficher les noms de tables dans la console pour le débogage
    print("Tables in the database:", tables)

    # Choix de la musique the hills de the weeknd dans la base de données
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT artist_name, track_name, release_date, genre, topic FROM musics WHERE track_name = 'the hills'")
    music = c.fetchone()
    conn.close()
    music = {'artist': music[0], 'title': music[1], 'year': music[2], 'genre': music[3], 'topic': music[4]}
    print("Music choose:", music)

    return render_template('home.html', selected_music=music)

@app.route('/rechercher', methods=['GET'])
def rechercher():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    debut = request.args.get('q', default='')
    #print("Debut:", debut)
    if (debut != ""):
        c.execute("SELECT artist_name, track_name, release_date, genre, topic FROM musics WHERE track_name LIKE ? LIMIT 10", (debut + "%",))
        results = c.fetchall()
        conn.close()
        print("Results:", results)
        # Convertissez les résultats en une liste de dictionnaires
        results_list = [{'artist': row[0], 'title': row[1], 'year': row[2], 'genre': row[3], 'topic': row[4]} for row in results]

        # Renvoyez les résultats au format JSON
        return jsonify(results_list)
    else:
        return jsonify([])