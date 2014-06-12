from datetime import datetime
from Job import Job

class Task:
    def __init__(self, job, startRow, startCol, nRows, nCols):
        self.job = job
        self.startRow = startRow
        self.startCol = startCol
        self.nRows = nRows
        self.nCols = nCols
        self.startTime = datetime.now()
        self.toComplete = nRows * nCols
        self.completed = 0

    def getRows(self):
        result = []
        for i in range(nRows):
            result.append(self.job.matrixA.getRow(startRow + i))

        return result

    def getColumns(self):
        result = []
        for i in range(nCols):
            result.append(self.job.matrixB.getColumn(startCol + i))

        return result

    def setResult(self, result, row, col):
        self.job.setResult(result, row, col)
        self.completed += 1

    def getRunningTime(self):
        return datetime.now() - self.startTime
