"""views.py - View for administration."""
from flask import render_template, Blueprint
from app.views import login
from app.controllers import PeerController

views_blueprint = Blueprint('views', __name__, url_prefix='')


@views_blueprint.route('/home', methods=['GET'])
@views_blueprint.route('/', methods=['GET'])
@login.login_redirect
def home():
    return render_template('home.htm', data={})


@views_blueprint.route('/status', methods=['GET'])
@login.login_redirect
def status():
    return render_template('status.htm', data={
        'peers': PeerController.get_all()
    })
