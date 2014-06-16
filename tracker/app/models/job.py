from app.utils.base_model import BaseEntity
from app import db
from app.controllers.matrix import MatrixController
from sqlalchemy import Integer, ForeignKey
import time

class Job(db.Model, BaseEntity):
    __tablename__ = 'job'

    matrixA = db.Column(Integer, ForeignKey('matrix.id'))
    matrixB = db.Column(Integer, ForeignKey('matrix.id'))
    resultCols = db.Column(db.Integer)
    resultRows = db.Column(db.Integer)
    completed = db.Column(db.Integer)
    toComplete = db.Column(db.Integer)
    resultMatrix = db.Column(Integer, ForeignKey('matrix.id'))
    taskMatrix = db.Column(Integer, ForeignKey('matrix.id'))



    def __init__(self, matrixA, matrixB):
        self.resultCols = matrixA.nRows
        self.resultRows = matrixB.nCols
        fname = time.strftime("%Y%m%d-%H%M%S")
        resMatrix = MatrixController.createEmptyMatrix( \
            self.resultRows, self.resultCols, "#", 'result_matrices/' + fname)
        taskMatrix = MatrixController.createEmptyMatrix( \
            self.resultRows, self.resultCols, "0", 'task_matrices/' + fname)
        self.matrixA = matrixA.id
        self.matrixB = matrixB.id
        self.completed = 0
        self.toComplete = self.resultCols * self.resultRows
        self.resultMatrix = resMatrix.id
        self.taskMatrix = taskMatrix.id

