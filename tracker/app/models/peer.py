"""peer.py - Peer model."""
from app import db
from app.utils.base_model import BaseEntity


class Peer(db.Model, BaseEntity):
    """Piece model."""
    __tablename__ = 'peer'

    prints = ['id', 'location']

    active = db.Column(db.Boolean)
    location = db.Column(db.String(256))
    CPU = db.Column(db.Integer)

    def __init__(self, location=''):
        self.active = False
        self.location = location
        self.CPU = 0
