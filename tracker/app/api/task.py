from flask import Blueprint, request
from app.controllers.taskmanager import TaskManager
from app.controllers.task import TaskController

import json

task_api = Blueprint('task_api', __name__, url_prefix='/api/task')


@task_api.route('/request_task/<int:peer_id>', methods=['GET'])
def get(peer_id):
    task = TaskManager.getTask(peer_id)

    return TaskController.getAsJson(task)


@task_api.route('/send_result', methods=['POST'])
def result():
    result = request.json

    task_id = result['id']
    row = result['results']['row']
    col = result['results']['col']
    value = result['results']['value']

    TaskManager.setResult(task_id, row, col, value)

