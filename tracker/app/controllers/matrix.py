from app.models.matrix import Matrix
from app import db
import os.path


class MatrixController:
    class InvalidMatrixError(RuntimeError):
        def __init__(self, arg):
            self.args = arg

    @staticmethod
    def create(filename):
        mFile = open(filename, "r")
        file_contents = mFile.readlines()


        rowCnt = len(file_contents)
        colCnt = 0

        for line in file_contents:
            columns = line.split()
            if colCnt is 0:
                colCnt = len(columns)
            else:
                if colCnt is not len(columns):
                    raise InvalidMatrixError("Different column lengths found")

        mFile.close()

        matrix = Matrix(filename, rowCnt, colCnt)

        db.session.add(matrix)
        db.session.commit()

        return matrix

    @staticmethod
    def delete(matrix):
        db.session.delete(matrix)
        db.session.commit()

    @staticmethod
    def get(matrix_id):
        return Matrix.query.get(matrix_id)

    @staticmethod
    def loadAsArray(matrix):
        mFile = open(matrix.filename, "r")
        file_contents = mFile.readlines()

        result_matrix = []

        for line in file_contents:
            columns = line.split()
            result_matrix.append(columns)

        mFile.close()
        return result_matrix


    @staticmethod
    def writeArrayToFile(matrix, filename, new=False):
        if new and os.path.isfile(filename):
            raise MatrixFileExists("Filename for new file already exists")

        nRows = len(matrix)
        nCols = len(matrix[0])
        output = ""

        for i in range(nRows):
            for j in range(nCols):
                if j == 0:
                    output = output + matrix[i][j]
                else:
                    output = output + " " + matrix[i][j]
            output = output + "\n"
            
        mFile = open(filename, "w+")
        mFile.write(output)
        mFile.close()


    @staticmethod
    def generateEmptyMatrixArray(rows, cols, symbol):
        matrix_array = [[symbol for i in range(cols)] for j in range(rows)]
        return matrix_array

    @staticmethod
    def createEmptyMatrix(rows, cols, symbol, filename):
        matrix_array = MatrixController.generateEmptyMatrixArray(rows, cols, symbol)
        MatrixController.writeArrayToFile(matrix_array, filename, True)

        return MatrixController.create(filename)

    @staticmethod
    def getRow(matrix, n):
        if n >= matrix.nRows:
            return 0

        matrix_array = MatrixController.loadAsArray(matrix)

        return matrix_array[n]

    @staticmethod
    def getColumn(matrix, n):
        result = []

        if n >= matrix.nCols:
            return 0

        matrix_array = MatrixController.loadAsArray(matrix)

        for i in range(matrix.nRows):
            result.append(matrix_array[i][n])

        return result

    @staticmethod
    def setCell(matrix, row, col, value):
        array = MatrixController.loadAsArray(matrix)
        array[row][col] = value

        MatrixController.writeArrayToFile(array, matrix.filename)
        