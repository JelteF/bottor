from app.utils.base_model import BaseEntity
from app import db
from app.constants import Constants
from app.controllers.matrix import MatrixController


class Job(db.Model, BaseEntity):
    __tablename__ = 'job'

    matrixA = db.Column(db.Integer, db.ForeignKey('matrix.id'))
    matrixB = db.Column(db.Integer, db.ForeignKey('matrix.id'))
    filenameA = db.Column(db.String(256))
    filenameB = db.Column(db.String(256))
    resultCols = db.Column(db.Integer)
    resultRows = db.Column(db.Integer)
    completed = db.Column(db.Integer)
    toComplete = db.Column(db.Integer)
    resultMatrix = db.Column(db.Integer, db.ForeignKey('matrix.id'))
    taskMatrix = db.Column(db.Integer, db.ForeignKey('matrix.id'))
    running = db.Column(db.Integer)
    free = db.Column(db.Integer)
    started = db.Column(db.Boolean)

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
        print('blaaaaaaa iniiiiiittttt')
        matrixA = MatrixController.createFromFile(self.filenameA)
        matrixB = MatrixController.createFromFile(self.filenameB)
        self.resultCols = matrixA.nRows
        self.resultRows = matrixB.nCols
        self.toComplete = self.resultCols * self.resultRows
        self.free = self.toComplete
        resMatrix = MatrixController.createEmptyMatrix(
            self.resultRows, self.resultCols, "#", 'result')
        taskMatrix = MatrixController.createEmptyMatrix(
            self.resultRows, self.resultCols, Constants.STATE_NONE, 'task')
        self.matrixA = matrixA.id
        self.matrixB = matrixB.id
        self.resultMatrix = resMatrix.id
        self.taskMatrix = taskMatrix.id
        self.started = True
