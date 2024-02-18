from . import db_musics, db_users
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Music(db_musics.Model):
    """Model for the musics table"""
    __tablename__ = 'musics'
    id = db_musics.Column(
        db_musics.Integer,
        primary_key=True
    )
    artist = db_musics.Column(
        db_musics.String(100),
        nullable=False,
        unique=False
    )
    track = db_musics.Column(
        db_musics.String(100),
        nullable=False,
        unique=False
    )
    date = db_musics.Column(
        db_musics.String(100),
        nullable=False,
        unique=False
    )
    genre = db_musics.Column(
        db_musics.String(100),
        nullable=False,
        unique=False
    )
    length = db_musics.Column(
        db_musics.Integer,
        nullable=False,
        unique=False
    )
    topic = db_musics.Column(
        db_musics.String(100),
        nullable=False,
        unique=False
    )


    def __repr__(self):
        return '<Music {}>'.format(self.title)

class User(UserMixin, db_users.Model):
    """User account model."""

    __tablename__ = 'flasklogin-users'
    id = db_users.Column(
        db_users.Integer,
        primary_key=True
    )
    name = db_users.Column(
        db_users.String(100),
        nullable=True,
        unique=False
    )
    email = db_users.Column(
        db_users.String(40),
        unique=True,
        nullable=False
    )
    password = db_users.Column(
        db_users.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)
    role = db_users.Column(
        db_users.String(200),
        primary_key=False,
        unique=False,
        nullable=False,
        default="user"
    )
    level = db_users.Column(
        db_users.Integer,
        default=3,
        nullable=False
    )
    pfp = db_users.Column(
        db_users.String(200),
        default="/static/images/default-avatar.png",
        nullable=False
    )
    simulation_count = db_users.Column(
        db_users.Integer,
        default=0,
        nullable=False
    )
    api_key = db_users.Column(
        db_users.String(200),
        nullable=True
    )
    validated = db_users.Column(db_users.String(200))
    is_pending = db_users.Column(db_users.Boolean,default=True)
    is_admin = db_users.Column(db_users.Boolean,default=False)

    def account_validated(self):
        self.is_pending = False
        
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)
    