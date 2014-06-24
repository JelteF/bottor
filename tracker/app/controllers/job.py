from app import db
from app.models import Job
from app.models import Matrix
from app.constants import Constants


class JobController:
    @staticmethod
    def create(matrixA, matrixB):
        job = Job(matrixA, matrixB)
        db.session.add(job)
        db.session.commit()
        job.loadMatrices(matrixA, matrixB)
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
        from app.controllers import TaskController
        from app.controllers import MatrixController
        try:
            taskMatrix = Matrix.matrices[job.id]['task']
        except KeyError:
            job.loadMatrices(MatrixController.get(job.matrixA),
                             MatrixController.get(job.matrixB))
            taskMatrix = Matrix.matrices[job.id]['task']

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
                JobController.changeState(taskMatrix, Constants.STATE_WORKING,
                                          startRow + i, startCol + j)

        job.running += nCols * nRows
        job.free -= nCols * nRows

        return TaskController.create(job, peer_id, startRow, startCol, nRows,
                                     nCols)

    @staticmethod
    def changeState(matrix, state, row, col):
        matrix[row][col] = state

    @staticmethod
    def isFinished(job):
        return job.completed == job.toComplete
