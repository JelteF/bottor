from app.utils.base_model import BaseEntity
from app import db
from sqlalchemy import Integer, ForeignKey

class Matrix(db.Model, BaseEntity):
    __tablename__ = 'matrix'

    nRows = db.Column(db.Integer)
    nCols = db.Column(db.Integer)
    filename = db.Column(db.String(256))

    # job = db.relationship('Job', foreign_keys=[Job.matrixA, Job.matrixB,
    #     Job.resultMatrix, Job.taskMatrix])

    def __init__(self, filename, nRows, nCols):
        self.nRows = nRows
        self.nCols = nCols
        self.filename = filename
