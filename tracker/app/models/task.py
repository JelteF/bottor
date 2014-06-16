from tracker.utils.base_model import BaseEntity
from tracker import db
from sqlalchemy import Integer, ForeignKey
from datetime import datetime

class Task(db.Model, BaseEntity):
    __tablename__ = 'task'

    job = db.Column(Integer, ForeignKey('job.id'))
    startRow = db.Column(Integer)
    startCol = db.Column(Integer)
    nRows = db.Column(Integer)
    nCols = db.Column(Integer)
    startTime = db.Column(default=datetime.now)
    toComplete = db.Column(Integer)
    completed = db.Column(Integer)

    def __init__(self, job, startRow, startCol, nRows, nCols):
        self.job = job
        self.startRow = startRow
        self.startCol = startCol
        self.nRows = nRows
        self.nCols = nCols
        self.startTime = datetime.now()
        self.toComplete = nRows * nCols
        self.completed = 0