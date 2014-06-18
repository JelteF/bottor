"""peer.py - Peer model."""
from app import db, app
from app.utils.base_model import BaseEntity
from sqlalchemy import event
from datetime import datetime


class Peer(db.Model, BaseEntity):
    """Piece model."""
    __tablename__ = 'peer'

    prints = ['id', 'location']

    active = db.Column(db.Boolean)
    last_active = db.Column(db.DateTime)
    location = db.Column(db.String(256))
    CPU = db.Column(db.Integer)

    def __init__(self, location=''):
        self.last_active = datetime.now()
        self.active = False
        self.location = location
        self.CPU = 0


@event.listens_for(Peer, 'load')
def check_active(peer, context):
    """Check active"""
    if ((datetime.now() - peer.last_active).total_seconds() >
            app.config['active_time']):
        peer.active = False
    db.session.add(peer)
    db.session.commit()
