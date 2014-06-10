from app import db
from app.utils.base_model import BaseEntity
from werkzeug.security import generate_password_hash, check_password_hash


class Account(db.Model, BaseEntity):
    __tablename__ = 'account'

    prints = ('id', 'name', 'pw_hash')

    name = db.Column(db.String(256))
    pw_hash = db.Column(db.String(66))

    def __init__(self, name="", password=""):
        self.name = name
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
