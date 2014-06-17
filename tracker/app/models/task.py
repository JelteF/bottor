from app.utils.base_model import BaseEntity
from app import db
from sqlalchemy import Integer, ForeignKey, DateTime
from datetime import datetime

class Task(db.Model, BaseEntity):
    __tablename__ = 'task'

    job = db.Column(Integer, ForeignKey('job.id'))
    startRow = db.Column(Integer)
    startCol = db.Column(Integer)
    nRows = db.Column(Integer)
    nCols = db.Column(Integer)
    startTime = db.Column(DateTime, default=datetime.now)
    toComplete = db.Column(Integer)
    completed = db.Column(Integer)
    peer = db.Column(Integer, Foreignkey('peer.id'))

    def __init__(self, job, peer, startRow, startCol, nRows, nCols):
        self.job = job
        self.startRow = startRow
        self.startCol = startCol
        self.nRows = nRows
        self.nCols = nCols
        self.startTime = datetime.now()
        self.toComplete = nRows * nCols
        self.completed = 0
        self.peer = peer