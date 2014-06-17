from datetime import datetime
import app.models
from app import db

class TaskController:

    def get(task_id):
        return Task.query.get(task_id)

    # def getRows(task):
    #     result = []
    #     for i in range(nRows):
    #         result.append(self.job.matrixA.getRow(startRow + i))

    #     return result

    # def getColumns(task):
    #     result = []
    #     for i in range(nCols):
    #         result.append(self.job.matrixB.getColumn(startCol + i))

    #     return result

    def setResult(task, row, col, value):
        task.completed += 1
        JobController.setResult(task.job, row, col, value)

    def getRunningTime(task):
        return datetime.now() - task.startTime

    def isCompleted(task):
        return task.toComplete == task.completed

