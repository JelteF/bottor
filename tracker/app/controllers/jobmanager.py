class JobManager:
    def __init__(self):
        self.matrices = {}

    def getMatrix(self, mId):
        return self.matrices[mId]

    def addResultMatrix(self, mId, matrix):
        self.resultMatrices[mId] = matrix

    def countMatrices(self):
        return len(self.matrices)