from flask import Blueprint, jsonify, request
from app.controllers.job import Job

task_api = Blueprint('task_api', __name__, url_prefix='/api/task')


@task_api.route('/request_task/<int:peer_id>', methods=['GET'])
def get(peer_id):
    return



@task_api.route('/send_result', methods=['POST'])
def result():
    result = request.json

    task_id = result['id']
    row = result['results']['row']
    col = result['results']['col']
    value = result['results']['value']

    TaskManager.setResult(task_id, row, col, value)

