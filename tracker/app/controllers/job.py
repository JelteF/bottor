from app import db
from app.models.job import Job
from app.models.task import Task
from app.controllers.matrix import MatrixController


class JobController:
    class IllegalSizeException(Exception):
        def __init__(self, arg):
            self.args = arg

    @staticmethod
    def create(matrixA, matrixB):
        if matrixA.nCols is not matrixB.nRows:
            raise IllegalSizeException("Columns A is not rows B")

        return Job(matrixA, matrixB)

    @staticmethod
    def delete(job):
        db.session.delete(job)
        db.session.commit()

    @staticmethod
    def get(job_id):
        return Job.query.get(job_id)

    @staticmethod
    def getTaskMatrixArray(job):
        matrix = MatrixController.get(job.taskMatrix)
        return MatrixController.loadAsArray(matrix)

    @staticmethod
    def getTask(job):
        taskMatrix = JobController.getTaskMatrixArray(job)

        startRow = 0
        startCol = 0

        TASK_SIZE = 3
        STATE_WORKING = "1"
        STATE_NONE = "0"

        # Find first 0 in taskMatrix
        while (taskMatrix[startRow][startCol] is not STATE_NONE):
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
                and taskMatrix[startRow + nRows][startCol + nCols] is STATE_NONE
                and nCols < TASK_SIZE):
            nCols += 1

        # Take some rows
        while (startRow + nRows < job.resultRows
                and taskMatrix[startRow + nRows][startCol + nCols - 1] is STATE_NONE
                and nRows < TASK_SIZE):
            nRows += 1

        # Set on working
        for i in range(nRows):
            for j in range(nCols):
                taskMatrix[startRow + i][startCol + j] = STATE_WORKING
                #changeState(taskMatrix, STATE_WORKING, startRow + i, startCol + j)

        filename = MatrixController.get(job.taskMatrix).filename
        MatrixController.writeArrayToFile(taskMatrix, filename)

        return Task(job, startRow, startCol, nRows, nCols)

    def changeState(matrix, state, row, col):
         matrix[row][col] = state

    # def setResult(self, result, row, col):
    #     self.resultMatrix[row][col] = result
    #     changeState(STATE_DONE, row, col)
    #     self.completed += 1

    # def isFinished(self):
    #     return self.completed is self.toComplete
