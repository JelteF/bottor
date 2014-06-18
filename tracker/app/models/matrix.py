from app.utils.base_model import BaseEntity
from app import db


class Matrix(db.Model, BaseEntity):
    __tablename__ = 'matrix'

    nRows = db.Column(db.Integer)
    nCols = db.Column(db.Integer)
    mType = db.Column(db.Enum('data', 'task', 'result'))
    filename = db.Column(db.String(256))

    matrices = {}

    def __init__(self, filename, nRows, nCols, mType):
        self.nRows = nRows
        self.nCols = nCols
        self.mType = mType
        self.filename = filename
