from flask import Blueprint, jsonify, request
from app.controllers import JobController
from app.views import login
from app.models import Matrix

job_api = Blueprint('job_api', __name__, url_prefix='/api/job/')


@job_api.route('', methods=['POST'])
@login.login_redirect
def create():
    """ Create new job """
    matrixA = Matrix.by_id(request.json['A'])
    matrixB = Matrix.by_id(request.json['B'])
    JobController.create(matrixA, matrixB)

    return jsonify()
