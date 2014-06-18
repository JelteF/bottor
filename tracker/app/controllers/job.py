from app import db
from app.models.job import Job
from app.models.matrix import Matrix
from app.controllers.matrix import MatrixController
from app.controllers.task import TaskController
from app.constants import Constants


class JobController:
    class IllegalSizeException(Exception):
        def __init__(self, arg):
            self.args = arg

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
        while (taskMatrix[startRow][startCol] is not Constants.STATE_NONE):
            startCol += 1
            if startCol >= job.resultRows:
                startCol = 0
                startRow += 1
                if startRow >= job.resultRows:
                    return 0 # NO TASKS TO DO, COMPLETED OR EVERYTHING RUNNING

        nCols = 0
        nRows = 0

        # Take a few more columns
        while (startCol + nCols < job.resultCols
                and taskMatrix[startRow + nRows][startCol + nCols] is Constants.STATE_NONE
                and nCols < Constants.TASK_SIZE):
            nCols += 1

        # Take some rows
        while (startRow + nRows < job.resultRows
                and taskMatrix[startRow + nRows][startCol + nCols - 1] is Constants.STATE_NONE
                and nRows < Constants.TASK_SIZE):
            nRows += 1

        # Set on working
        for i in range(nRows):
            for j in range(nCols):
                JobController.changeState(taskMatrix, Constants.STATE_WORKING, startRow + i, startCol + j)

        #MatrixController.writeArrayToFile(taskMatrix, "test")
        job.running += nCols * nRows
        job.free -= nCols * nRows

        return TaskController.create(job, peer_id, startRow, startCol, nRows, nCols)

    def changeState(matrix, state, row, col):
        matrix[row][col] = state

    def setResult(job, row, col, result):
        resultMatrix = Matrix.matrices[job.getResultMatrix()]
        taskMatrix = Matrix.matrices[job.getTaskMatrix()]

        resultMatrix[row][col] = result
        taskMatrix[row][col] = Constants.STATE_DONE
        job.completed += 1
        job.running -= 1
        if JobController.isFinished(job):
            MatrixController.writeToFile(Matrix.matrices[job.resultMatrix],
                "result_matrices/result_job" + job.id, True)
            # REMOVE JOB + MATRICES


    def isFinished(job):
        return job.completed is job.toComplete
