from Task import Task

class IllegalSizeException(Exception):
    def __init__(self, arg):
        self.args = arg

class Job:
    TASK_SIZE = 3
    STATE_WORKING = 1
    STATE_DONE = 2

    def __init__(self, matrixA, matrixB):
        if matrixA.cols is not matrixB.rows:
            raise IllegalSizeException("Columns A is not Rows B")

        self.matrixA = matrixA
        self.matrixB = matrixB
        self.resultCols = self.matrixA.rows
        self.resultRows = self.matrixB.cols
        self.resultMatrix = [[0 for i in range(self.resultCols)] for j in \
            range(self.resultRows)]
        self.taskMatrix = [[0 for i in range(self.resultCols)] for j in \
            range(self.resultRows)]
        self.completed = 0
        self.toComplete = self.resultCols * self.resultRows

    ''' Find an empty square to calculate '''
    def getTask(self):
        startRow = 0
        startCol = 0

        # Find first 0 in taskMatrix
        while (self.taskMatrix[startRow][startCol] is not 0):
            startCol += 1
            if startCol >= self.resultRows:
                startCol = 0
                startRow += 1
                if startRow >= self.resultRows:
                    return 0 # NO TASKS TO DO, COMPLETED OR EVERYTHING RUNNING

        nCols = 0
        nRows = 0

        # Take a few more columns
        while (startCol + nCols < self.resultCols
                and self.taskMatrix[startRow + nRows][startCol + nCols] is 0
                and nCols < TASK_SIZE):
            nCols += 1

        # Take some rows
        while (startRow + nRows < self.resultRows
                and self.taskMatrix[startRow + nRows][startCol + nCols] is 0
                and nRows < TASK_SIZE):
            nRows += 1

        # Set on working
        for i in range(nRows):
            for j in range(nCols):
                changeState(STATE_WORKING, startRow + i, startCol + j)

        return Task(self, startRow, startCol, nRows, nCols)

    def changeState(self, state, row, col):
        self.taskMatrix[row, col] = state

    def setResult(self, result, row, col):
        self.resultMatrix[row][col] = result
        changeState(STATE_DONE, row, col)
        self.completed += 1
