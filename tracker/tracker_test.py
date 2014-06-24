import unittest
import os
import json
import time

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


    # def testMatrixController(self):
    #     matrix = MatrixController.createFromFile("sample_matrices/A50")
    #     assert matrix
    #     matrix3 = MatrixController.createFromArray(Matrix.matrices[matrix.id])
    #     assert matrix3
    #     MatrixController.setCell(matrix3, 0, 0, 0)
    #     MatrixController.writeToFile(matrix3, "")

    #     row = MatrixController.getRow(matrix3, 0)
    #     column = MatrixController.getColumn(matrix3, 0)  

    #     matrix2 = MatrixController.createEmptyMatrix(20, 20, 0)
    #     assert matrix2
    #     MatrixController.writeToFile(matrix2)
    #     MatrixController.writeToFile(matrix2, "result_matrices/BLABLA")

    # def testJobController(self):
    #     matrixA = "sample_matrices/A20"
    #     matrixB = "sample_matrices/B20"
    #     job = JobController.create(matrixA, matrixB)
    #     assert job

    #     array = Matrix.matrices[job.getTaskMatrix()]
    #     MatrixController.writeArrayToFile(array, "result_matrices/test3a")

    #     task1 = JobController.getTask(job, 1)
    #     assert task1
    #     print (job.running)
    #     task2 = JobController.getTask(job, 1)
    #     assert task2
    #     job2 = JobController.getJobWithFreeTask()
    #     assert job2
    #     task3 = JobController.getTask(job, 1)
    #     assert task3

    #     resArray = Matrix.matrices[job2.getTaskMatrix()]
    #     MatrixController.writeArrayToFile(array, "result_matrices/test3b")

    # def testTaskManager(self):
    #     matrixA = "sample_matrices/A20"
    #     matrixB = "sample_matrices/B20"
    #     job6 = JobController.create(matrixA, matrixB)
    #     assert job6
    #     job2 = JobController.create(matrixA, matrixB)

    #     task1 = TaskManager.getTask(1)
    #     while task1:
    #         job = JobController.get(task1.job)
    #         array = Matrix.matrices[job.getTaskMatrix()]
    #         MatrixController.writeArrayToFile(array, "result_matrices/testTaskManager" + str(job.id))
    #         task1 = TaskManager.getTask(1)

    #     TaskController.cancelTask(2)
    #     array = Matrix.matrices[job6.getTaskMatrix()]
    #     MatrixController.writeArrayToFile(array, "result_matrices/testTaskManager" + str(job6.id) + "b")
    #     print (job6.running)
    #     print (job6.free)

    def testShizzle(self):
        matrixA = "sample_matrices/A20"
        matrixB = "sample_matrices/B20"
        job = JobController.create(matrixA, matrixB)
        job2 = JobController.create(matrixA, matrixB)

        task1 = TaskManager.getTask(1)
        assert task1

        task2 = TaskManager.getTask(1)
        assert task2

        array = Matrix.matrices[job.getTaskMatrix()]
        MatrixController.writeArrayToFile(array, "result_matrices/test_job_cancelling_1")
        time.sleep(2)
        task3 = TaskManager.getTask(1)
        assert task3
        task4 = TaskManager.getTask(1)
        MatrixController.writeArrayToFile(array, "result_matrices/test_job_cancelling_2")
        TaskManager.cancelLongRunningTasks()
        MatrixController.writeArrayToFile(array, "result_matrices/test_job_cancelling_3")






    # def testShit(self):
    #     matrixB = MatrixController.createFromFile("sample_matrices/B20")
    #     transposed = MatrixController.transpose(matrixB)




if __name__ == '__main__':
    unittest.main()