from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .models import db, User
from . import login_manager
import sqlite3
import random
import string

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
DATABASE = "instance/Users.db"

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', msg='')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(name=username).first()
        if user:
            if not user.check_password('483578515166259'):
                if user.check_password(password):
                    login_user(user)
                    return redirect('/')
                else:
                    return render_template('login.html',msg='Incorrect login')
            else:
                return redirect('/first-login')
        else:
            return render_template('login.html',msg='Incorrect login')




@auth_bp.route('/admin-panel/invite-user', methods=['POST'])
@login_required
def invite():
    email = request.form.get('email')
    role = request.form.get('role')
    existing_user = User.query.filter_by(email=email).first()
    if existing_user is None:
        characters = string.ascii_letters + string.digits
        activation = ''.join(random.choice(characters) for i in range(24))
        #generate random api key
        api_key = ''.join(random.choice(characters) for i in range(24))
        user = User(
                email=email,
                role=role,
                validated=activation,
                api_key=api_key,
            )
        if role=="Admin":
            user.level = 1
            user.is_admin = 1
        if role=="Beta":
            user.level = 2
        if role == "User":
            user.level = 3
        user.set_password("483578515166259")
        db.session.add(user)
        db.session.commit()
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO 'api_access' (key,last_gen) VALUES (?,?)",(api_key,""))
        conn.commit()
        conn.close()
    return redirect('/admin-panel')

@auth_bp.route('/first-login/<code>', methods=['GET','POST'])
def first_login(code=""):
    if request.method == "GET":
        return render_template('first_login.html',code=code,msg="")
    else:
        username= request.form.get('username')
        password = request.form.get('password')
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("SELECT name FROM 'flasklogin-users' WHERE name = ?",(username,))
        user = cur.fetchall()
        if len(user)>0:
            return render_template('first_login.html',code=code,msg="Username already taken")
        else:
            user = User.query.filter_by(validated=code).first()
            if user:
                user.set_password(password)
                user.validated = ""
                user.is_pending = 0
                user.pfp = "/static/images/default-avatar.png"
                user.name = username
                db.session.commit()
                login_user(user)
                return redirect('/')
            else:
                return render_template('first_login.html',code=code,msg="Cette invitation n'est plus valide")

@auth_bp.route('/admin-panel/delete-user/<code>', methods=['GET'])
@login_required
def delete_user(code):
    user = User.query.filter_by(id=code).first()
    if user and current_user.level<=1 and user.name != current_user.name and user.level<current_user.level:
        db.session.delete(user)
        db.session.commit()
    return redirect('/admin-panel')

@auth_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect("/login")


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")
