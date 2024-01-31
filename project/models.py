from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'flasklogin-users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=True,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)
    role = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False,
        default="user"
    )
    level = db.Column(
        db.Integer,
        default=3,
        nullable=False
    )
    pfp = db.Column(
        db.String(200),
        default="/static/images/default-avatar.png",
        nullable=False
    )
    simulation_count = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )
    api_key = db.Column(
        db.String(200),
        nullable=True
    )
    validated = db.Column(db.String(200))
    is_pending = db.Column(db.Boolean,default=True)
    is_admin = db.Column(db.Boolean,default=False)

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
    