from flask import Blueprint, request, jsonify
from app.models.matrix import Matrix
from app import db
from app.controllers.taskmanager import TaskManager
from app.controllers import TaskController
from app.controllers import JobController
from app.constants import Constants
from app.controllers import MatrixController


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
    resultMatrix = Matrix.matrices[job.id]['result']
    taskMatrix = Matrix.matrices[job.id]['task']

    for res in result['results']:
        row = res['row']
        col = res['col']
        value = res['value']

        resultMatrix[row][col] = value
        taskMatrix[row][col] = Constants.STATE_DONE

    print ("Job " + str(job.id) + ": " + str(job.completed) + "/" + str(job.toComplete) + " completed")

    if job.isFinished():
        filename = "result_matrices/result_job_" + str(job.id)
        print ("Job " + str(job.id) + " completed. Writing result to file " + filename)
        MatrixController.writeToFile(Matrix.matrices[job.id]['result'],
                                     filename, True)
        # REMOVE JOB + MATRICES
    db.session.commit()

    return jsonify()
