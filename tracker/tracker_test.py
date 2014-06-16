import unittest
import os
from glob import glob

from app import app, db

from app.controllers.matrix import MatrixController
from app.controllers.job import JobController

class TrackerTestCase(unittest.TestCase):
    def create_app(self):
        return app

    def setUp(self):
        filelist = glob("app/*.sqlite")
        filelist += (glob("app/*.db"))
        for f in filelist:
            os.remove(f)

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def testMatrixController(self):
        matrix = MatrixController.create("sample_matrices/A50")
        assert matrix
        matrix_id = matrix.id
        matrix2 = MatrixController.get(matrix_id)
        assert matrix2
        array = MatrixController.loadAsArray(matrix2)
        assert array
        MatrixController.writeArrayToFile(array, "sample_matrices/test")


        row = MatrixController.getRow(matrix, 0)
        assert(row)
        #print(row)
        col = MatrixController.getColumn(matrix, 0)
        assert col
        #print(col)
        MatrixController.delete(matrix)
        matrix3 = MatrixController.get(matrix_id)
        assert not matrix3

        array2 = MatrixController.generateEmptyMatrixArray(20, 20, "#")
        MatrixController.writeArrayToFile(array2, "sample_matrices/test2")
        matrix4 = MatrixController.create("sample_matrices/test2")
        assert matrix4

    def testJobController(self):
        matrixA = MatrixController.create("sample_matrices/A20")
        matrixB = MatrixController.create("sample_matrices/B20")
        job = JobController.create(matrixA, matrixB)
        assert job

        resMatrix = MatrixController.get(job.matrixA)
        array = MatrixController.loadAsArray(resMatrix)
        MatrixController.writeArrayToFile(array, "sample_matrices/test3")

        JobController.getTask(job)
        JobController.getTask(job)



if __name__ == '__main__':
    unittest.main()