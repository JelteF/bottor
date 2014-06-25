from flask import Blueprint, request, jsonify
from app.models.matrix import Matrix
from app.controllers.taskmanager import TaskManager
from app.controllers.task import TaskController
from app.controllers.job import JobController
from app.constants import Constants
from app.controllers.matrix import MatrixController


task_api = Blueprint('task_api', __name__, url_prefix='/api/task')


@task_api.route('/request_task/<int:peer_id>', methods=['GET'])
def get(peer_id):

    task = TaskManager.getTask(peer_id)
    if task == 0:
        return jsonify(), 500

    print('started json')
    json = TaskController.getAsJson(task)
    print('finished json')
    return json


@task_api.route('/send_result', methods=['POST'])
def result():
    # peer_id = 0
    result = request.json

    task_id = result['id']
    task = TaskController.get(task_id)
    task.completed += len(result['results'])
    job = JobController.get(task.job)
    job.completed += len(result['results'])
    job.running -= len(result['results'])
    resultMatrix = Matrix.matrices[job.getResultMatrix()]
    taskMatrix = Matrix.matrices[job.getTaskMatrix()]

    for res in result['results']:
        row = res['row']
        col = res['col']
        value = res['value']

        resultMatrix[row][col] = value
        taskMatrix[row][col] = Constants.STATE_DONE

    if JobController.isFinished(job):
        MatrixController.writeToFile(Matrix.matrices[job.getResultMatrix()],
                                     "result_matrices/result_job" + job.id,
                                     True)
        # REMOVE JOB + MATRICES

    return jsonify()
