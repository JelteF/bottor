from app.utils.base_model import BaseEntity
from app import db
from app.constants import Constants
from app.models.matrix import Matrix
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
        mA = MatrixController.createFromFile(matrixA)
        mB = MatrixController.createFromFile(matrixB)
        bTransp = MatrixController.transpose(mB)
        self.matrixA = mA.id
        self.matrixB = bTransp.id
        self.completed = 0
        self.running = 0
        self.resultCols = mA.nRows
        self.resultRows = mB.nCols
        self.toComplete = self.resultCols * self.resultRows
        self.free = self.toComplete

    def getMatrixA(self):
        if not self.matrixA in Matrix.matrices:
            self.initMatrices()
        return self.matrixA

    def getMatrixB(self):
        if not self.matrixB in Matrix.matrices:
            self.initMatrices()
        return self.matrixB

    def getTaskMatrix(self):
        if not self.taskMatrix in Matrix.matrices:
            self.initMatrices()
        return self.taskMatrix

    def getResultMatrix(self):
        if not self.resultMatrix in Matrix.matrices:
            self.initMatrices()
        return self.resultMatrix

    def initMatrices(self):
        if not self.matrixA in Matrix.matrices:
            MatrixController.loadInMemory(MatrixController.get(self.matrixA))
        if not self.matrixB in Matrix.matrices:
            MatrixController.loadInMemory(MatrixController.get(self.matrixB))
        # if not self.resultMatrix in Matrix.matrices:
        #     MatrixController.delete(MatrixController.get(self.resultMatrix))
        # if not self.taskMatrix in Matrix.matrices:
        #     MatrixController.delete(MatrixController.get(self.taskMatrix))

        resMatrix = MatrixController.createEmptyMatrix(
            self.resultRows, self.resultCols, "#", 'result')
        taskMatrix = MatrixController.createEmptyMatrix(
            self.resultRows, self.resultCols, Constants.STATE_NONE, 'task')
        self.resultMatrix = resMatrix.id
        self.taskMatrix = taskMatrix.id
