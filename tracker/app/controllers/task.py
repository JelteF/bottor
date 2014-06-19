from datetime import datetime
from app import db
from flask import jsonify
from app.models.matrix import Matrix


from app.models.task import Task


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

        print('a1')
        job = JobController.get(task.job)
        print('a2')

        matrixA = Matrix.matrices[job.matrixA]
        matrixB = Matrix.matrices[job.matrixB]

        partA = matrixA[task.startRow:task.nRows + task.startRow]
        partB = matrixB[task.startCol:task.nCols + task.startCol]

        print('a5')

        response = jsonify(id=task.id, start_row=task.startRow,
                           start_col=task.startCol,
                           matrixA=partA, matrixB=partB)
        print('a6')
        return response
