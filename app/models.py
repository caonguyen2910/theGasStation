from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from geoalchemy2 import Geometry


class USER(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    full_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Integer, default=0)

    def set_password(self, password_input):
        self.password = generate_password_hash(password_input)

    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)


@login.user_loader
def load_user(id):
    return USER.query.get(int(id))


class CAYXANGPOINT(db.Model):
    __tablename__ = "cayxangpoint"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=False)
    geom = db.Column(Geometry('POINT'))
