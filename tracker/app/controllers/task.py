from datetime import datetime
from app import db
from flask import jsonify
from app.controllers.matrix import MatrixController


from app.models.task import Task
from app.models.job import Job


class TaskController:

    def create(job, peer, startRow, startCol, nRows, nCols):
        task = Task(job.id, peer, startRow, startCol, nRows, nCols)
        db.session.add(task)
        db.session.commit()
        return task

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
        from app.controllers.job import JobController
        task.completed += 1
        job = JobController.get(task.job)
        JobController.setResult(job, row, col, value)

    def getRunningTime(task):
        return datetime.now() - task.startTime

    def isCompleted(task):
        return task.toComplete == task.completed

    def getAsJson(task):
        from app.controllers.job import JobController
        json = {}
        rows = []
        cols = []

        job = JobController.get(task.job)
        matrixA = MatrixController.get(job.matrixA)
        matrixB = MatrixController.get(job.matrixB)

        for i in range(task.nRows):
            row = MatrixController.getRow(matrixA, task.startRow + i)
            rows.append({ task.startRow + i : row })

        for i in range(task.nCols):
            col = MatrixController.getRow(matrixB, task.startCol + i)
            cols.append({ task.startCol + i : col })

        return jsonify(id=task.id, rows=rows, columns=cols)