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
            else:
                if colCnt is not len(columns):
                    raise InvalidMatrixException(
                        "Different column lengthsfound")
            result_matrix.append(columns)

        matrix = Matrix(filename, rowCnt, colCnt, 'data')
        db.session.add(matrix)
        db.session.commit()
        Matrix.matrices[matrix.id] = result_matrix

        return matrix

    @staticmethod
    def createFromArray(array, mType):
        rowCnt = len(array)
        colCnt = len(array[0])

        matrix = Matrix("", rowCnt, colCnt, mType)
        db.session.add(matrix)
        db.session.commit()

        Matrix.matrices[matrix.id] = array

        return matrix

    @staticmethod
    def createEmptyMatrix(rows, cols, symbol, mType):
        matrix_array = [[symbol for i in range(cols)] for j in range(rows)]

        return MatrixController.createFromArray(matrix_array, mType)

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
        elif matrix.filename == "":
            filename = (Constants.WRITEDIR + time.strftime("%Y%m%d-%H%M%S") +
                        ".botmatrix")
        else:
            filename = matrix.filename

        i = 1
        while not overwrite and os.path.isfile(filename):
            filename = filename + "-" + str(i)
            i += 1

        MatrixController.writeArrayToFile(Matrix.matrices[matrix.id], filename)

    @staticmethod
    def writeArrayToFile(array, filename):
        nRows = len(array)
        nCols = len(array[0])
        output = ""

        for i in range(nRows):
            for j in range(nCols):
                if j == 0:
                    output = output + str(array[i][j])
                else:
                    output = output + " " + str(array[i][j])
            output = output + "\n"

        mFile = open(filename, "w+")
        mFile.write(output)
        mFile.close()

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
        Matrix.matrices[matrix.id][row][col] = value
