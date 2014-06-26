from app.utils.base_model import BaseEntity
from app import db
from datetime import datetime


class Task(db.Model, BaseEntity):
    __tablename__ = 'task'

    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    startRow = db.Column(db.Integer)
    startCol = db.Column(db.Integer)
    nRows = db.Column(db.Integer)
    nCols = db.Column(db.Integer)
    startTime = db.Column(db.DateTime)
    toComplete = db.Column(db.Integer)
    completed = db.Column(db.Integer)
    peer_id = db.Column(db.Integer, db.ForeignKey('peer.id'))
    peer = db.relationship('Peer', backref=db.backref('task', uselist=False))

    def __init__(self, job_id, peer_id, startRow, startCol, nRows, nCols):
        self.job_id = job_id
        self.startRow = startRow
        self.startCol = startCol
        self.nRows = nRows
        self.nCols = nCols
        self.startTime = datetime.now()
        self.toComplete = nRows * nCols
        self.completed = 0
        self.peer_id = peer_id
