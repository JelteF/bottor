from app.utils.base_model import BaseEntity
from app import db
from app.models import Matrix
from app.constants import Constants


class Job(db.Model, BaseEntity):
    __tablename__ = 'job'

    resultCols = db.Column(db.Integer)
    resultRows = db.Column(db.Integer)

    toComplete = db.Column(db.Integer)
    free = db.Column(db.Integer)

    started = db.Column(db.Boolean)
    running = db.Column(db.Integer)
    completed = db.Column(db.Integer)

    # matrices
    matrixA_id = db.Column(db.Integer, db.ForeignKey('matrix.id'))
    matrixB_id = db.Column(db.Integer, db.ForeignKey('matrix.id'))

    matrixA = db.relationship('Matrix', foreign_keys=[matrixA_id])
    matrixB = db.relationship('Matrix', foreign_keys=[matrixB_id])

    resultMatrix = db.Column(db.Integer, db.ForeignKey('matrix.id'))

    tasks = db.relationship('Task', backref='job')

    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)

    def __init__(self, matrixA, matrixB):
        from app.controllers import MatrixController
        self.resultCols = matrixA.nRows
        self.resultRows = matrixB.nCols

        self.toComplete = self.resultCols * self.resultRows
        self.free = self.toComplete

        self.running = 0
        self.completed = 0

        self.matrixA = matrixA
        self.matrixB = matrixB

        self.matrixA_id = matrixA.id
        self.matrixB_id = matrixB.id

        resMatrix = MatrixController.createEmptyMatrix(
            self.resultRows, self.resultCols, "#", 'result')
        self.resultMatrix = resMatrix.id

    def getMatrixA(self):
        return Matrix.matrices[self.id]['dataA']

    def getMatrixB(self):
        return Matrix.matrices[self.id]['dataB']

    def getTaskMatrix(self):
        return Matrix.matrices[self.id]['task']

    def getResultMatrix(self):
        return Matrix.matrices[self.id]['result']

    def isFinished(self):
        return self.completed == self.toComplete

    def loadMatrices(self, matrixA, matrixB):
        from app.controllers import MatrixController
        print(self.id)

        Matrix.matrices[self.id] = {}

        MatrixController.loadInMemory(
            MatrixController.loadFromFile(matrixA.filename), self.id, 'dataA')

        bTransp = MatrixController.transpose(MatrixController.loadFromFile(
            matrixB.filename))
        MatrixController.loadInMemory(bTransp, self.id, 'dataB')

        task = [[Constants.STATE_NONE for i in range(self.resultCols)] for j in range(self.resultRows)]
        MatrixController.loadInMemory(task, self.id, 'task')

        result = [['#' for i in range(self.resultCols)] for j in range(self.resultRows)]
        MatrixController.loadInMemory(result, self.id, 'result')

        print(Matrix.matrices[self.id].keys())

        # taskMatrix = MatrixController.createEmptyMatrix(
        #     self.resultRows, self.resultCols, Constants.STATE_NONE, 'task')
        # self.taskMatrix = taskMatrix.id
