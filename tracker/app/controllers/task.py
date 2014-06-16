from datetime import datetime
from Job import Job
from tracker.models.task import Task
from tracker import db

class TaskController:
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
