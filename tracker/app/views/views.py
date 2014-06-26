"""views.py - View for administration."""
from flask import render_template, Blueprint, redirect
from app.views import login
from app.controllers import PeerController, MatrixController, JobController

views_blueprint = Blueprint('views', __name__, url_prefix='')


@views_blueprint.route('/home/', methods=['GET'])
@views_blueprint.route('/', methods=['GET'])
@login.login_redirect
def home():
    return render_template('home.htm', data={})


@views_blueprint.route('/matrix/', methods=['GET'])
@login.login_redirect
def matrix():
    return render_template('matrix.htm', data={
        'matrixes': MatrixController.get_all()
    })


@views_blueprint.route('/status/', methods=['GET'])
@login.login_redirect
def status():
    return render_template('status.htm', data={
        'peers': PeerController.get_all()
    })


@views_blueprint.route('/job/', methods=['GET'])
@login.login_redirect
def job():
    jobs = JobController.get_all()
    for job in jobs:
        print(job.matrixA)
        print(job.matrixB)
    return render_template('job.htm', data={'jobs': jobs, })


@views_blueprint.route('/multiply/', methods=['GET'])
@login.login_redirect
def multiply():
    return render_template('multiply.htm', data={
        'matrices': MatrixController.get_all_data(),

    })


@views_blueprint.route('/uploads/<path:filename>')
@login.login_redirect
def uploaded_file(filename):
    print(filename)
    return redirect('static/matrix/' + filename, code=301)
