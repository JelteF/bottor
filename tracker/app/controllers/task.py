from datetime import datetime, timedelta
from app import db
from flask import jsonify
from app.constants import Constants
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

    def delete(task):
        db.session.delete(task)
        db.session.commit()

    def cancelTask(task_id):
        from app.controllers.job import JobController
        task = TaskController.get(task_id)
        job = JobController.get(task.job)

        cancelCnt = 0

        for i in range(task.nRows):
            for j in range(task.nCols):
                if JobController.getState(job, task.startRow + i,
                        task.startCol +j) != Constants.STATE_DONE:
                    JobController.changeState(job, Constants.STATE_NONE,
                        task.startRow + i, task.startCol + j)
                    cancelCnt += 1

        job.running -= cancelCnt
        job.free += cancelCnt
        TaskController.delete(task)

    # Get time in seconds
    def getLongRunningTasks(time):
        tasks = Task.query.filter(Task.startTime < datetime.now() - timedelta(seconds=time))

        return tasks

    def getRunningTime(task):
        return datetime.now() - task.startTime

    def isCompleted(task):
        return task.toComplete == task.completed

    def getAsJson(task):
        from app.controllers.job import JobController

        job = JobController.get(task.job)

        matrixA = Matrix.matrices[job.matrixA]
        matrixB = Matrix.matrices[job.matrixB]

        partA = matrixA[task.startRow:task.nRows + task.startRow]
        partB = matrixB[task.startCol:task.nCols + task.startCol]

        response = jsonify(id=task.id, start_row=task.startRow,
                           start_col=task.startCol,
                           matrixA=partA, matrixB=partB)
        return response
