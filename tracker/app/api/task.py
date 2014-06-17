from flask import Blueprint, request, jsonify
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
    peer_id = 0
    result = request.json

    task_id = result['id']

    for res in result['results']:
        row = res['row']
        col = res['col']
        value = res['value']
        TaskManager.setResult(peer_id, task_id, row, col, value)

    return jsonify()
