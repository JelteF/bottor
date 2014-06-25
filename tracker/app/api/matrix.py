"""matrix.py - Controller for Matrix."""
from flask import Blueprint, jsonify, request
from app.controllers import MatrixController
from app.utils import serialize_sqla
from app.views import login

matrix_api = Blueprint('matrix_api', __name__, url_prefix='/api/matrix')


@matrix_api.route('', methods=['POST'])
@login.login_redirect
def create():
    """ Create new matrix """
    matrix_dict = request.json

    matrix = MatrixController.createFromFile(matrix_dict['filename'])

    return jsonify(id=matrix.id)


@matrix_api.route('/<int:matrix_id>', methods=['DELETE'])
@login.login_redirect
def delete(matrix_id):
    """ Delete matrix """
    matrix = MatrixController.get(matrix_id)

    if not matrix:
        return jsonify(error='Matrix not found'), 500

    MatrixController.delete(matrix)

    return jsonify()


@matrix_api.route('/<int:matrix_id>', methods=['GET'])
@login.login_redirect
def get(matrix_id):
    """ Get matrix """
    matrix = MatrixController.get(matrix_id)

    if not matrix:
        return jsonify(error='Matrix not found'), 500

    return jsonify(matrix=serialize_sqla(matrix))


@matrix_api.route('/all', methods=['GET'])
@login.login_redirect
def get_all():
    """ Get all data matrices """
    matrices = MatrixController.get_all_data()

    if not matrices:
        return jsonify(error='No matrices were found'), 500

    return jsonify(matrices=serialize_sqla(matrices))
