import unittest
import os
import json

from glob import glob
from app import app, db
from app.models.matrix import Matrix
from app.controllers.matrix import MatrixController
from app.controllers.job import JobController
from app.controllers.taskmanager import TaskManager
from app.controllers.task import TaskController

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
        matrix = MatrixController.createFromFile("sample_matrices/A50")
        assert matrix
        matrix3 = MatrixController.createFromArray(Matrix.matrices[matrix.id])
        assert matrix3
        MatrixController.setCell(matrix3, 0, 0, 0)
        MatrixController.writeToFile(matrix3, "")

        row = MatrixController.getRow(matrix3, 0)
        column = MatrixController.getColumn(matrix3, 0)  

        matrix2 = MatrixController.createEmptyMatrix(20, 20, 0)
        assert matrix2
        MatrixController.writeToFile(matrix2)
        MatrixController.writeToFile(matrix2, "result_matrices/BLABLA")

    def testJobController(self):
        matrixA = "sample_matrices/A20"
        matrixB = "sample_matrices/B20"
        job = JobController.create(matrixA, matrixB)
        assert job

        array = Matrix.matrices[job.getResultMatrix()]
        MatrixController.writeArrayToFile(array, "result_matrices/test3")

        JobController.getTask(job, 1)
        task = JobController.getTask(job, 1)
        assert task
        job2 = JobController.getJobWithFreeTask()
        assert job2

    def testTaskManager(self):
        matrixA = "sample_matrices/A20"
        matrixB = "sample_matrices/B20"
        job = JobController.create(matrixA, matrixB)
        assert job
        job2 = JobController.getJobWithFreeTask()
        assert job2
        task = TaskManager.getTask(1)
        assert task
        TaskController.setResult(task, 5, 19, 69)
        matrix = MatrixController.get(job.resultMatrix)
        MatrixController.writeToFile(matrix, "result_matrices/TestManager", True)

    def testShit(self):
        matrixA = "sample_matrices/A20"
        matrixB = "sample_matrices/B20"
        job = JobController.create(matrixA, matrixB)
        job = JobController.create(matrixA, matrixB)
        job = JobController.create(matrixA, matrixB)




if __name__ == '__main__':
    unittest.main()