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

        JobController.getTask(job, 1)
        task = JobController.getTask(job, 1)
        assert task
        job2 = JobController.getJobWithFreeTask()
        assert job2

    def testTaskManager(self):
        matrixA = MatrixController.create("sample_matrices/A20")
        matrixB = MatrixController.create("sample_matrices/B20")
        result = Matrix.query.all()
        print (len(result))
        job = JobController.create(matrixA, matrixB)
        assert job
        job2 = JobController.getJobWithFreeTask()
        assert job2
        task = TaskManager.getTask(1)
        assert task
        TaskController.setResult(task, 5, 19, 69)

    def testTaskAPI(self):
        matrixA = MatrixController.create("sample_matrices/A20")
        matrixB = MatrixController.create("sample_matrices/B20")
        job = JobController.create(matrixA, matrixB)

        with app.test_client() as c, app.app_context():
            resp = c.get('/api/task/request_task/%d' % (1))
            data = json.loads(resp.data)
            assert 'rows' in data
            assert 'id' in data
            print (data)

        return





if __name__ == '__main__':
    unittest.main()