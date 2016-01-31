from passlib.apps import custom_app_context as pwd_context

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.Integer, default=999)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.role = 999

    def __repr__(self):
        return '<User %r>' % (self.username)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
