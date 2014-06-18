from app.utils.base_model import BaseEntity
from app import db
from app.constants import Constants
from app.controllers.matrix import MatrixController
from sqlalchemy import Integer, ForeignKey, Boolean, String
from app.models.matrix import Matrix

class Job(db.Model, BaseEntity):
    __tablename__ = 'job'

    matrixA = db.Column(db.Integer, ForeignKey('matrix.id'))
    matrixB = db.Column(db.Integer, ForeignKey('matrix.id'))
    filenameA = db.Column(String(256))
    filenameB = db.Column(String(256))
    resultCols = db.Column(Integer)
    resultRows = db.Column(Integer)
    completed = db.Column(Integer)
    toComplete = db.Column(Integer)
    resultMatrix = db.Column(Integer, ForeignKey('matrix.id'))
    taskMatrix = db.Column(Integer, ForeignKey('matrix.id'))
    running = db.Column(Integer)
    free = db.Column(Integer)
    started = db.Column(Boolean)

    def __init__(self, matrixA, matrixB):
        self.completed = 0
        self.running = 0
        self.free = 1
        self.filenameA = matrixA
        self.filenameB = matrixB
        self.started = False

    def getMatrixA(self):
        if not self.started:
            self.initMatrices()
        return self.matrixA

    def getMatrixB(self):
        if not self.started:
            self.initMatrices()
        return self.matrixB

    def getTaskMatrix(self):
        if not self.started:
            self.initMatrices()
        return self.taskMatrix

    def getResultMatrix(self):
        if not self.started:
            self.initMatrices()
        return self.resultMatrix

    def initMatrices(self):
        matrixA = MatrixController.createFromFile(self.filenameA)
        matrixB = MatrixController.createFromFile(self.filenameB)
        self.resultCols = matrixA.nRows
        self.resultRows = matrixB.nCols
        self.toComplete = self.resultCols * self.resultRows
        self.free = self.toComplete
        resMatrix = MatrixController.createEmptyMatrix(self.resultRows,
            self.resultCols, "#")
        taskMatrix = MatrixController.createEmptyMatrix(self.resultRows,
            self.resultCols, Constants.STATE_NONE)
        self.matrixA = matrixA.id
        self.matrixB = matrixB.id
        self.resultMatrix = resMatrix.id
        self.taskMatrix = taskMatrix.id
        started = True
