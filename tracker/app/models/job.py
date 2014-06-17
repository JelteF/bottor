from app.utils.base_model import BaseEntity
from app import db
from app.controllers.matrix import MatrixController
from sqlalchemy import Integer, ForeignKey
import time

class Job(db.Model, BaseEntity):
    __tablename__ = 'job'

    matrixA = db.Column(db.Integer, ForeignKey('matrix.id'))
    matrixB = db.Column(db.Integer, ForeignKey('matrix.id'))
    resultCols = db.Column(Integer)
    resultRows = db.Column(Integer)
    completed = db.Column(Integer)
    toComplete = db.Column(Integer)
    resultMatrix = db.Column(Integer, ForeignKey('matrix.id'))
    taskMatrix = db.Column(Integer, ForeignKey('matrix.id'))
    running = db.Column(Integer)
    free = db.Column(Integer)



    def __init__(self, matrixA, matrixB):
        self.resultCols = matrixA.nRows
        self.resultRows = matrixB.nCols
        fname = time.strftime("%Y%m%d-%H%M%S")
        resMatrix = MatrixController.createEmptyMatrix( \
            self.resultRows, self.resultCols, "#", 'result_matrices/' + fname + '.botmatrix')
        taskMatrix = MatrixController.createEmptyMatrix( \
            self.resultRows, self.resultCols, "0", 'task_matrices/' + fname + '.botmatrix')
        self.matrixA = matrixA.id
        self.matrixB = matrixB.id
        self.completed = 0
        self.running = 0
        self.toComplete = self.resultCols * self.resultRows
        self.free = self.toComplete
        self.resultMatrix = resMatrix.id
        self.taskMatrix = taskMatrix.id

