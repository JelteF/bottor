"""peer.py - Peer model."""
from app import db
from app.utils.base_model import BaseEntity


class Peer(db.Model, BaseEntity):
    """Piece model."""
    __tablename__ = 'peer'

    prints = ['id', 'location']

    location = db.Column(db.String(256))

    def __init__(self, location=''):
        self.location = location
