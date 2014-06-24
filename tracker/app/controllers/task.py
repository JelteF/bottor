from datetime import datetime
from app import db
from flask import jsonify
from app.models import Matrix
from app.models import Task


class TaskController:
    def create(job, peer, startRow, startCol, nRows, nCols):
        task = Task(job.id, peer, startRow, startCol, nRows, nCols)
        db.session.add(task)
        db.session.commit()
        return task

    def get(task_id):
        return Task.query.get(task_id)

    def getRunningTime(task):
        return datetime.now() - task.startTime

    def isCompleted(task):
        return task.toComplete == task.completed

    def getAsJson(task):
        from app.controllers.job import JobController

        job = JobController.get(task.job)

        matrixA = Matrix.matrices[job.id]['dataA']
        matrixB = Matrix.matrices[job.id]['dataB']

        partA = matrixA[task.startRow:task.nRows + task.startRow]
        partB = matrixB[task.startCol:task.nCols + task.startCol]

        response = jsonify(id=task.id, start_row=task.startRow,
                           start_col=task.startCol,
                           matrixA=partA, matrixB=partB)
        return response
