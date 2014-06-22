from app.models.matrix import Matrix
from app import db
from app.constants import Constants
import os.path
import time


class InvalidMatrixException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class MatrixController:
    @staticmethod
    def createFromFile(filename):
        mFile = open(filename, "r")
        file_contents = mFile.readlines()
        mFile.close()
        result_matrix = []

        rowCnt = len(file_contents)
        colCnt = 0

        for line in file_contents:
            columns = line.split()
            if colCnt is 0:
                colCnt = len(columns)
            elif colCnt != len(columns):
                raise InvalidMatrixException("Different column lengths found")

            result_matrix.append(columns)

        matrix = Matrix(filename, rowCnt, colCnt, 'data')
        db.session.add(matrix)
        db.session.commit()
        return matrix

    @staticmethod
    def createFromArray(array, mType):
        rowCnt = len(array)
        colCnt = len(array[0])

        matrix = Matrix("", rowCnt, colCnt, mType)
        db.session.add(matrix)
        db.session.commit()

        return matrix

    @staticmethod
    def createEmptyMatrix(rows, cols, symbol, mType):
        matrix_array = [[symbol for i in range(cols)] for j in range(rows)]

        return MatrixController.createFromArray(matrix_array, mType)

    @staticmethod
    def loadInMemory(matrix, job_id):
        mFile = open(matrix.filename, "r")
        file_contents = mFile.readlines()
        mFile.close()
        result_matrix = []

        for line in file_contents:
            columns = line.split()
            result_matrix.append(columns)

        Matrix.matrices[job_id][matrix.mType] = result_matrix

    @staticmethod
    def delete(matrix):
        db.session.delete(matrix)
        db.session.commit()

    @staticmethod
    def get(matrix_id):
        return Matrix.query.get(matrix_id)

    @staticmethod
    def get_all():
        """Get all matrixes."""
        return Matrix.query.all()

    @staticmethod
    def get_all_data():
        """Get all matrixes."""
        return Matrix.query.filter_by(mType='data').all()

    @staticmethod
    def writeToFile(matrix, fname="", overwrite=False):
        if fname != "":
            filename = fname

        if not overwrite and os.path.isfile(filename):
            i = 1
            tmpFilename = filename + "-" + str(i)
            while not overwrite and os.path.isfile(tmpFilename):
                tmpFilename = filename + "-" + str(i)
                i += 1
            filename = tmpFilename

        output = map(lambda r: ' '.join(str(x) for x in r), matrix)
        output = '\n'.join(output)

        mFile = open(filename, "w+")
        mFile.write(output)
        mFile.close()

    # @staticmethod
    # def writeArrayToFile(array, filename):

    #     output = map(lambda r: ' '.join(str(x) for x in r), array)
    #     output = '\n'.join(output)

    #     mFile = open(filename, "w+")
    #     mFile.write(output)
    #     mFile.close()

    @staticmethod
    def getRow(matrix, n):
        if n >= matrix.nRows:
            return 0

        matrix_array = Matrix.matrices[matrix.id]

        result = [float(i) for i in matrix_array[n]]

        return result

    @staticmethod
    def getColumn(matrix, n):
        result = []

        if n >= matrix.nCols:
            return 0

        matrix_array = Matrix.matrices[matrix.id]

        for i in range(matrix.nRows):
            result.append(float(matrix_array[i][n]))

        return result

    @staticmethod
    def setCell(matrix, row, col, value):
        matrix[row][col] = value

    @staticmethod
    def transpose(matrix):
        matrix_T = [[]]
        for i in range(len(matrix[0])):
            for j in range(len(matrix)):
                matrix_T[j][i] = matrix[i][j]

        return matrix_T
