from app import db
from app.models.job import Job
from app.models.matrix import Matrix
from app.controllers.task import TaskController
from app.constants import Constants


class JobController:
    @staticmethod
    def create(matrixA, matrixB):
        job = Job(matrixA, matrixB)
        db.session.add(job)
        db.session.commit()
        return job

    @staticmethod
    def delete(job):
        db.session.delete(job)
        db.session.commit()

    @staticmethod
    def get(job_id):
        return Job.query.get(job_id)

    @staticmethod
    def getJobWithFreeTask():
        return Job.query.filter(Job.free > 0).first()

    @staticmethod
    def getTask(job, peer_id):
        taskMatrix = Matrix.matrices[job.getTaskMatrix()]
        startRow = 0
        startCol = 0

        # Find first 0 in taskMatrix
        while taskMatrix[startRow][startCol] != Constants.STATE_NONE:
            startCol += 1
            if startCol >= job.resultRows:
                startCol = 0
                startRow += 1
                if startRow >= job.resultRows:
                    # NO TASKS TO DO, COMPLETED OR EVERYTHING RUNNING
                    return 0

        nCols = 0
        nRows = 0

        # Take a few more columns
        while startCol + nCols < job.resultCols and \
                taskMatrix[startRow + nRows][startCol + nCols] == \
                Constants.STATE_NONE and \
                nCols < Constants.TASK_SIZE:
            nCols += 1

        # Take some rows
        while startRow + nRows < job.resultRows and \
                taskMatrix[startRow + nRows][startCol + nCols - 1] == \
                Constants.STATE_NONE and \
                nRows < Constants.TASK_SIZE:
            nRows += 1

        # Set on working
        for i in range(nRows):
            for j in range(nCols):
                JobController.changeState(job, Constants.STATE_WORKING,
                                          startRow + i, startCol + j)

        job.running += nCols * nRows
        job.free -= nCols * nRows

        return TaskController.create(job, peer_id, startRow, startCol, nRows,
                                     nCols)

    @staticmethod
    def changeState(job, state, row, col):
        taskMatrix = Matrix.matrices[job.getTaskMatrix()]
        taskMatrix[row][col] = state

    @staticmethod
    def getState(job, row, col):
        taskMatrix = Matrix.matrices[job.getTaskMatrix()]
        return taskMatrix[row][col]
    
    @staticmethod
    def isFinished(job):
        return job.completed == job.toComplete
