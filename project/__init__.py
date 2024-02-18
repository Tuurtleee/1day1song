from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail


db_musics = SQLAlchemy()
db_users = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('config.Config')

    # Initialize Plugins
    db_musics.init_app(app)
    db_users.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from . import routes
        from . import auth

        # Register Blueprints
        app.register_blueprint(routes.app)
        app.register_blueprint(auth.auth_bp)


        # Create Database Models
        db_musics.create_all()
        db_users.create_all()

        return app